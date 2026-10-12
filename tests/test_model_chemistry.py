#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The forcefields as model chemistries (forcefield_step.model_chemistry)."""

import types

from forcefield_step import ForcefieldStep
from forcefield_step.model_chemistry import (
    data_files,
    forcefield,
    get_model_chemistry_options,
    type_and_method,
)


def _wrapper(key, options):
    return {"level": key, "type": options[key]["type"], "options": options[key]}


def _no_user_files(tmp_path):
    """A data path with no forcefields of the user's: only the package's."""
    return [tmp_path / "empty"]


def test_bundled_forcefields_are_offered(tmp_path):
    options = get_model_chemistry_options(data_path=_no_user_files(tmp_path))
    assert options["FF@oplsaa"]["forcefield"] == "oplsaa"
    assert options["FF@oplsaa+"]["file"] == "oplsaa.frc"
    assert options["FF@CL&P"]["file"] == "oplsaa.frc"
    assert options["FF@pcff"]["file"] == "pcff2018.frc"
    assert options["FF@dreiding-X6"]["forcefield"] == "dreiding/X6"
    reaxff = options["ReaxFF@CHO_cho_2008"]
    assert reaxff["type"] == "ReaxFF" and reaxff["file"] == "reaxff/CHO_cho_2008.frc"
    assert all(not o["mdi_capable"] and o["periodic_native"] for o in options.values())
    assert all(o["source"] == "package" for o in options.values())
    # Not MDI engines: LAMMPS evaluates them itself
    assert get_model_chemistry_options(mdi_only=True) == {}


def test_names():
    """The names the files define; only the grammar's reserved characters change."""
    assert type_and_method("oplsaa+") == ("FF", "oplsaa+")
    assert type_and_method("dreiding/X6") == ("FF", "dreiding-X6")
    assert type_and_method("reaxff/CH_2018") == ("ReaxFF", "CH_2018")
    assert type_and_method("my/ff:1") == ("FF", "my-ff-1")


def test_a_users_forcefield_shadows_a_bundled_one(tmp_path):
    """The user's files come first (as their data files do), so a forcefield of
    the same name replaces the package's; files sent with a job are found."""
    directory = tmp_path / "data" / "Forcefields" / "mine"
    directory.mkdir(parents=True)
    (directory / "special.frc").write_text("#define oplsaa\n\n#define my_ff\n")
    options = get_model_chemistry_options(data_path=[tmp_path / "data"])
    assert options["FF@oplsaa"]["file"] == "local:mine/special.frc"
    assert options["FF@my_ff"]["path"] == str(directory / "special.frc")
    assert options["FF@oplsaa+"]["source"] == "package"


def test_the_forcefield_is_built(tmp_path):
    options = get_model_chemistry_options(data_path=_no_user_files(tmp_path))
    ff = forcefield(_wrapper("ReaxFF@CHO_cho_2008", options))
    assert ff.current_forcefield == "reaxff/CHO_cho_2008"
    assert ff.ff_form == "reaxff"
    # and through the step, as LAMMPS and Packmol call it
    ff = ForcefieldStep.forcefield(_wrapper("FF@oplsaa", options))
    assert ff.current_forcefield == "oplsaa"


def test_local_files_go_with_a_job(tmp_path):
    directory = tmp_path / "data" / "Forcefields"
    directory.mkdir(parents=True)
    (directory / "mine.frc").write_text("#define my_ff\n")
    options = get_model_chemistry_options(data_path=[tmp_path / "data"])
    node = types.SimpleNamespace(
        find_data_file=lambda name: tmp_path / "data" / name, references=None
    )
    files = data_files(_wrapper("FF@my_ff", options), node)
    assert files == [("data:Forcefields/mine.frc", directory / "mine.frc")]
    # The package's own files are installed wherever the step is
    assert data_files(_wrapper("FF@oplsaa", options), node) == []


def test_included_files_are_parts_not_forcefields(tmp_path):
    """oplsaa.frc includes local:OPLS-AA/ligpargen.frc, whose parameters extend
    oplsaa+: it is not offered on its own, but one not included is."""
    directory = tmp_path / "data" / "Forcefields" / "OPLS-AA"
    directory.mkdir(parents=True)
    (directory / "ligpargen.frc").write_text("#define ligpargen\n")
    (directory / "other.frc").write_text("#define other\n")
    options = get_model_chemistry_options(data_path=[tmp_path / "data"])
    assert "FF@ligpargen" not in options
    assert options["FF@other"]["file"] == "local:OPLS-AA/other.frc"
    assert "FF@oplsaa+" in options
