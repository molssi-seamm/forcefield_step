# -*- coding: utf-8 -*-

"""The forcefield survives a checkpoint (phase 5 resume)."""

import importlib.resources
import json

import seamm
import seamm_ff_util

import forcefield_step


def test_forcefield_round_trip():
    flowchart = seamm.Flowchart()
    node = forcefield_step.Forcefield(flowchart=flowchart)
    path = importlib.resources.files("forcefield_step") / "data" / "pcff2018.frc"
    ff = seamm_ff_util.Forcefield(str(path), uri_handler=node.uri_handler)
    ff.initialize_biosym_forcefield()

    data = json.loads(json.dumps(node.checkpoint_variable("_forcefield", ff)))
    restored = node.restore_variable("_forcefield", data)

    assert isinstance(restored, seamm_ff_util.Forcefield)
    assert restored.current_forcefield == ff.current_forcefield
    assert str(restored.filename) == str(ff.filename)
    assert sorted(restored.ff["atom_types"]) == sorted(ff.ff["atom_types"])


def test_other_values_are_not_its_business():
    node = forcefield_step.Forcefield(flowchart=seamm.Flowchart())
    assert node.checkpoint_variable("_forcefield", "OpenKIM") is None
    assert node.checkpoint_variable("other", object()) is None
    assert node.restore_variable("other", {}) is None
