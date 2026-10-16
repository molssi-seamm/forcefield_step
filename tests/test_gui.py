# -*- coding: utf-8 -*-

"""Smoke test of the Tk dialog: create it and re-lay it out for every choice
that drives the layout. Skipped when no display is available."""

import pytest


@pytest.fixture()
def tk_node():
    import tkinter as tk

    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    root.withdraw()
    import Pmw
    import seamm

    Pmw.initialise(root)
    flowchart = seamm.Flowchart(namespace="org.molssi.seamm", directory=".")
    tk_flowchart = seamm.TkFlowchart(
        master=root, flowchart=flowchart, namespace="org.molssi.seamm.tk"
    )
    node = flowchart.create_node("Forcefield")
    flowchart.add_node(node)
    plugin = tk_flowchart.plugin_manager.get("Forcefield")
    tk_node = plugin.create_tk_node(
        tk_flowchart=tk_flowchart, node=node, canvas=tk_flowchart.canvas, x=100, y=100
    )
    yield tk_node
    root.destroy()


def test_forcefields_in_the_file(tk_node):
    tk_node.create_dialog()
    tk_node["forcefield_file"].set("oplsaa.frc")
    tk_node.reset_dialog()
    names = tk_node["forcefield"].combobox.cget("values")
    assert names[:4] == ("default", "oplsaa+", "oplsaa+-spc_e", "oplsaa+-tip3p")

    tk_node["forcefield"].set("oplsaa+-spc_e")
    tk_node.reset_dialog()
    assert tk_node["forcefield"].get() == "oplsaa+-spc_e"

    # A forcefield not in the new file goes back to the default
    tk_node["forcefield_file"].set("nacl_water.frc")
    tk_node.reset_dialog()
    assert tk_node["forcefield"].combobox.cget("values") == ("default", "nacl_water")
    assert tk_node["forcefield"].get() == "default"


def test_dialog_layouts(tk_node):
    tk_node.create_dialog()
    for task in ("assign forcefield to structure", "setup forcefield"):
        tk_node["task"].set(task)
        tk_node.reset_dialog()
