#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests of the rigid water variants of oplsaa+: oplsaa+-spc_e and oplsaa+-tip3p."""

import pytest

from seamm_ff_util import Forcefield
from seamm_ff_util import FFAssigner

OPLSAA = "../forcefield_step/forcefield_step/data/oplsaa.frc"


def setup(name, configuration):
    """Methanol and water typed with the forcefield `name`."""
    ff = Forcefield(OPLSAA)
    ff.initialize_biosym_forcefield(name)
    configuration.from_smiles("CO.O")
    types = FFAssigner(ff).assign(configuration)
    return ff, types


def water(types):
    return types[2], types[-1]


def test_oplsaa_plus_water_is_flexible(configuration):
    ff, types = setup("oplsaa+", configuration)
    o, h = water(types)
    assert (o, h) == ("opls_76", "opls_77")
    assert ff.bond_parameters(o, h)[2] == "quadratic_bond"
    assert ff.angle_parameters(h, o, h)[2] == "quadratic_angle"


def test_spc_e(configuration):
    ff, types = setup("oplsaa+-spc_e", configuration)
    o, h = water(types)
    assert (o, h) == ("opls_76", "opls_77")
    _, _, form, values = ff.bond_parameters(o, h)
    assert form == "rigid_bond"
    assert float(values["R0"]) == pytest.approx(1.0)
    _, _, form, values = ff.angle_parameters(h, o, h)
    assert form == "rigid_angle"
    assert float(values["Theta0"]) == pytest.approx(109.47)
    assert float(ff.charges(o)[3]["Q"]) == pytest.approx(-0.8476)
    assert float(ff.charges(h)[3]["Q"]) == pytest.approx(0.4238)


def test_tip3p(configuration):
    ff, types = setup("oplsaa+-tip3p", configuration)
    o, h = water(types)
    assert (o, h) == ("opls_63", "opls_64")
    _, _, form, values = ff.bond_parameters(o, h)
    assert form == "rigid_bond"
    assert float(values["R0"]) == pytest.approx(0.9572)
    _, _, form, values = ff.angle_parameters(h, o, h)
    assert form == "rigid_angle"
    assert float(values["Theta0"]) == pytest.approx(104.52)
    assert float(ff.charges(o)[3]["Q"]) == pytest.approx(-0.834)


@pytest.mark.parametrize("name", ["oplsaa+", "oplsaa+-spc_e", "oplsaa+-tip3p"])
def test_methanol_unchanged(name, configuration):
    """Only the water changes: methanol keeps the oplsaa+ types and terms."""
    ff, types = setup(name, configuration)
    assert types[:2] == ["opls_99", "opls_96"]
    assert ff.bond_parameters(types[0], types[1])[2] == "quadratic_bond"


def test_nacl_water_is_rigid():
    ff = Forcefield("../forcefield_step/forcefield_step/data/nacl_water.frc")
    ff.initialize_biosym_forcefield()
    assert ff.bond_parameters("o_spc/e", "h_spc/e")[2] == "rigid_bond"
    assert ff.angle_parameters("h_spc/e", "o_spc/e", "h_spc/e")[2] == "rigid_angle"


def test_forcefield_names():
    from forcefield_step import Forcefield as Step

    step = Step()
    names = step.forcefield_names("oplsaa.frc")
    assert names[:3] == ["oplsaa+", "oplsaa+-spc_e", "oplsaa+-tip3p"]
    assert "oplsaa" in names and "CL&P" in names
    assert step.forcefield_names("nacl_water.frc") == ["nacl_water"]
    assert step.forcefield_names("OpenKIM") == []
    assert step.forcefield_names("no_such_file.frc") == []
