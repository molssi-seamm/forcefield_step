# -*- Coding: utf-8 -*-

"""Helper class needed for the stevedore integration. Needs to provide
a description() method that returns a dict containing a description of
this node, and a factory() method for creating the graphical and non-graphical
nodes."""

import forcefield_step


class ForcefieldStep(object):
    my_description = {
        "description": "An interface for the setup and control of the forcefield",
        "group": "Simulations",
        "name": "Forcefield",
    }

    def __init__(self, flowchart=None, gui=None):
        """Initialize this helper class, which is used by
        the application via stevedore to get information about
        and create node objects for the flowchart
        """
        pass

    def description(self):
        """Return a description of what this extension does"""
        return ForcefieldStep.my_description

    def create_node(self, flowchart=None, **kwargs):
        """Return a new node object"""
        return forcefield_step.Forcefield(flowchart=flowchart, **kwargs)

    def create_tk_node(self, canvas=None, **kwargs):
        """Return the graphical Tk node object"""
        return forcefield_step.TkForcefield(canvas=canvas, **kwargs)

    # ----------------------------------------------------------------------
    # The forcefields as model chemistries (see forcefield_step.model_chemistry):
    # FF@<name> and ReaxFF@<parameter set>, evaluated by LAMMPS itself.
    # ----------------------------------------------------------------------

    @classmethod
    def get_model_chemistry_options(
        cls, periodic_only=False, mdi_only=False, data_path=None
    ):
        """The forcefields in the .frc files the step can find, as model
        chemistries; ``data_path`` is a running flowchart's data directories.
        See :func:`forcefield_step.model_chemistry.get_model_chemistry_options`."""
        from .model_chemistry import get_model_chemistry_options

        return get_model_chemistry_options(
            periodic_only=periodic_only, mdi_only=mdi_only, data_path=data_path
        )

    @classmethod
    def forcefield(cls, model_chemistry, node=None):
        """The seamm_ff_util forcefield for a model chemistry from
        :meth:`get_model_chemistry_options`."""
        from .model_chemistry import forcefield

        return forcefield(model_chemistry, node=node)

    @classmethod
    def model_chemistry_data_files(cls, model_chemistry, node, local_only=True):
        """The local and personal files a job needs for the model chemistry."""
        from .model_chemistry import data_files

        return data_files(model_chemistry, node, local_only=local_only)
