#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for reading LigParGen output into a forcefield file.

LigParGen orders the atoms its own way, so the .key file's order is not the
configuration's. These tests use the real .key file for fluoroethylene carbonate
(FEC), where the two orders differ:

    .key          O C O C C H F O H H
    configuration O C O C C F O H H H
"""

import json
from pathlib import Path

import pytest

from molsystem.system_db import SystemDB
from forcefield_step.ligpargen import add_to_ff, ff_template, key_atom_types, reader

FEC = "O=C1OC[C@H](F)O1"


@pytest.fixture()
def FEC_configuration():
    """FEC, built the way the utility builds it."""
    db = SystemDB(filename="file:ligpargen_db?mode=memory&cache=shared")
    configuration = db.create_system(name="FEC").create_configuration(name="initial")
    configuration.from_smiles(FEC)
    # The utility rebuilds from the canonical SMILES, which is what is sent to
    # LigParGen, so the atom order must come from that.
    configuration.from_smiles(configuration.to_smiles(canonical=True))

    yield configuration

    db.close()


@pytest.fixture()
def FEC_key():
    """The data from the real .key file LigParGen returned for FEC."""
    return reader(Path(__file__).parent / "data" / "FEC.key")


def test_key_and_configuration_orders_differ(FEC_configuration, FEC_key):
    """The premise: the two orders are not the same."""
    from molsystem.elements import to_symbols

    key_order = [to_symbols([int(atom[4])])[0] for atom in FEC_key["atom"]]
    assert key_order == ["O", "C", "O", "C", "C", "H", "F", "O", "H", "H"]
    assert list(FEC_configuration.atoms.symbols) == [
        "O",
        "C",
        "O",
        "C",
        "C",
        "F",
        "O",
        "H",
        "H",
        "H",
    ]


def test_key_atom_types_maps_by_connectivity(FEC_configuration, FEC_key):
    """Each atom gets the type of the LigParGen atom bonded as it is."""
    types = key_atom_types(FEC_configuration, FEC_key)

    # The fluorine is the 6th atom for us and the 7th for LigParGen.
    assert types[5] == "806"
    # The ring oxygen bonded to both carbons.
    assert types[6] == "807"
    # The two hydrogens on the CH2 carbon, then the one on the CHF carbon. 805 is
    # the CHF hydrogen -- putting it on a CH2 hydrogen is the error that elements
    # alone cannot catch.
    assert set(types[7:9]) == {"808", "809"}
    assert types[9] == "805"


def test_atom_types_valences_are_possible(FEC_configuration, FEC_key):
    """The number of connections comes from the .key, so it fits the element."""
    ff = add_to_ff(ff_template, FEC_configuration, FEC_key)

    section = ff.split("#atom_types")[1].split("#charges")[0]
    valences = {}
    for line in section.splitlines():
        fields = line.split()
        if len(fields) == 7 and "_" in fields[2]:
            valences[fields[2].split("_")[1]] = (fields[4], int(fields[5]))

    assert valences["806"] == ("F", 1)
    assert valences["807"] == ("O", 2)
    assert valences["800"] == ("O", 1)
    assert valences["801"] == ("C", 3)
    for _type, (element, n_bonds) in valences.items():
        assert n_bonds <= {"H": 1, "F": 1, "O": 2, "C": 4}[element]


def test_fragment_types_match_the_smarts(FEC_configuration, FEC_key):
    """Each position of the fragment's SMARTS gets the type of that atom."""
    ff = add_to_ff(ff_template, FEC_configuration, FEC_key)

    fragments = json.loads(
        ff.split("#fragments ligpargen")[1].split("#reference")[0].strip()
    )
    entry = list(list(fragments.values())[0].values())[0]
    types = [_type.split("_", 1)[1] for _type in entry["atom types"]]

    assert entry["SMARTS"] == "O=C1OC([H])([H])[C@@](F)([H])O1"
    #                          0 1  2 3  4    5    6      7  8   9
    assert types[0] == "800"  # the carbonyl oxygen
    assert types[3] == "803"  # the CH2 carbon
    assert set(types[4:6]) == {"808", "809"}  # its two hydrogens
    assert types[6] == "804"  # the CHF carbon
    assert types[7] == "806"  # its fluorine
    assert types[8] == "805"  # its hydrogen -- the one that used to go astray
    assert types[9] == "807"  # the ring oxygen


def test_mismatched_key_is_rejected(FEC_configuration, FEC_key):
    """A .key file for a different molecule does not silently half-match."""
    del FEC_key["atom"][-1]

    with pytest.raises(ValueError, match="different molecule"):
        key_atom_types(FEC_configuration, FEC_key)
