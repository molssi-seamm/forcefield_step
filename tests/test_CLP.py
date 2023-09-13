#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for atom type assignment for CL&P forcefield forcefield."""


def test_TFSI(oplsaa_assigner, configuration):
    """Test of atom-type assignment bis(trifluoromethanesulfonyl)imide anion"""
    correct = (
        ["Cbt"]
        + 3 * ["Fbt"]
        + ["Sbt", "Obt", "Obt"]
        + ["Nbt"]
        + ["Sbt", "Obt", "Obt"]
        + ["Cbt"]
        + 3 * ["Fbt"]
    )
    configuration.from_smiles("C(F)(F)(F)S(=O)(=O)[N-]S(=O)(=O)C(F)(F)F")
    result = oplsaa_assigner.assign(configuration)
    if result != correct:
        print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
        raise AssertionError(f"\n result: {result}\ncorrect: {correct}")
