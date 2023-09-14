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


def test_C2mem(oplsaa_assigner, configuration):
    """Test of atom-type assignment for 1-ethyl-3-methylimidazolium cation"""
    correct = (
        ["CE", "C1", "NA", "CW", "CW", "NA", "CR", "C1"]
        + 3 * ["opls_85"]
        + 2 * ["H1"]
        + 3 * ["HA"]
        + 3 * ["H1"]
    )
    configuration.from_smiles("CCn1cc[n+](c1)C")
    result = oplsaa_assigner.assign(configuration)
    if result != correct:
        print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
        raise AssertionError(f"\n result: {result}\ncorrect: {correct}")


def test_C3mem(oplsaa_assigner, configuration):
    """Test of atom-type assignment for 1-propyl-3-methylimidazolium cation"""
    correct = (
        ["opls_80", "C2", "C1", "NA", "CW", "CW", "NA", "CR", "C1"]
        + 5 * ["opls_85"]
        + 2 * ["H1"]
        + 3 * ["HA"]
        + 3 * ["H1"]
    )
    configuration.from_smiles("CCCn1cc[n+](c1)C")
    result = oplsaa_assigner.assign(configuration)
    if result != correct:
        print(f"Incorrect typing. Should be:\n  {correct}\nnot\n  {result}")
        raise AssertionError(f"\n result: {result}\ncorrect: {correct}")
