# -*- coding: utf-8 -*-

"""A node or step for the forcefield in a flowchart"""

import logging
import os.path
import pkg_resources
import pprint

import forcefield_step
import seamm
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('forcefield')


class Forcefield(seamm.Node):

    def __init__(self, flowchart=None, extension=None):
        """Initialize a forcefield step

        Keyword arguments:
        """
        logger.debug('Creating Forcefield {}'.format(self))

        super().__init__(
            flowchart=flowchart, title='Forcefield', extension=extension
        )

        self.parameters = forcefield_step.ForcefieldParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return forcefield_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return forcefield_step.__git_revision__

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

            text = (
                "Use '{atomtyping_engine}' to assign the forcefield"
                "{forcefield} to the system object."
                )

        return self.header + '\n' + __(
            text,
            indent=4 * ' ',
            **P,
        ).__str__()

    def run(self):
        """Setup the forcefield
        """

        next_node = super().run(printer=printer)

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        printer.important(__(self.header, indent=self.indent))

        atomtyping_engine = seamm.AtomTyperFactory(namespace='org.molssi.seamm.atom_typers').create(atomtyping_engine=P["atomtyping_engine"],forcefield="Amber",parameter_set="GAFF")

        self.set_variable("_atomtyping_engine", atomtyping_engine)

        system_db = self.get_variable('_system_db')

        atomtyping_engine.assign_parameters(system=system_db)

        printer.important('')

        return next_node
