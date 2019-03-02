# -*- coding: utf-8 -*-
"""A node or step for the forcefield in a workflow"""

import molssi_workflow
import molssi_workflow.data as data
import forcefield
import logging

logger = logging.getLogger(__name__)


class Forcefield(molssi_workflow.Node):
    def __init__(self, workflow=None, extension=None):
        '''Initialize a forcefield step

        Keyword arguments:
        '''
        logger.debug('Creating Forcefield {}'.format(self))

        self.ff_file = \
            '/Users/psaxe/Work/Workflow/forcefield/data/pcff2018.frc'
        self.ff_name = None

        super().__init__(workflow=workflow, title='Forcefield',
                         extension=extension)

    def describe(self, indent='', json_dict=None):
        """Write out information about what this node will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        next_node = super().describe(indent, json_dict)

        indent += '    '
        if self.ff_file[0] == '$':
            string = indent + (
                "Reading the forcefield file given in the variable"
                " '{ff_file}'"
            )
        else:
            string = indent + (
                "Reading the forcefield file '{ff_file}'"
            )
            
        self.job_output(
            string.format(
                ff_file=self.ff_file
            )
        )
        self.job_output('')

        return next_node

    def run(self):
        """Setup the forcefield
        """

        next_node = super().run()

        ff_file = self.get_value(self.ff_file)

        indent = '    '
        string = indent + (
            "Reading the forcefield file '{ff_file}'"
        )
            
        self.job_output(
            string.format(
                ff_file=ff_file
            )
        )

        if self.ff_name is None:
            data.forcefield = forcefield.Forcefield(ff_file)
        else:
            ff_name = self.get_value(self.ff_name)
            data.forcefield = forcefield.Forcefield(ff_file, ff_name)

        data.forcefield.initialize_biosym_forcefield()

        self.job_output('')

        return next_node
