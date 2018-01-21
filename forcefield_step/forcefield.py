# -*- coding: utf-8 -*-
"""A node or step for the forcefield in a workflow"""

import chemflowchart
import chemflowchart.data as data
import forcefield
import logging

logger = logging.getLogger(__name__)


class Forcefield(chemflowchart.Node):
    def __init__(self, workflow=None, gui_object=None,
                 extension=None):
        '''Initialize a forcefield step

        Keyword arguments:
        '''
        logger.debug('Creating Forcefield {}'.format(self))

        self.flowchart = None
        self.ff_file = \
            '/Users/psaxe/Work/ChemFlowchart/forcefield/data/pcff2017.frc'
        self.ff_name = None

        super().__init__(workflow=workflow, title='Forcefield',
                         gui_object=gui_object, extension=extension)

    def run(self):
        """Setup the forcefield
        """

        self.forcefield = forcefield.Forcefield(self.ff_file)
        data.forcefield = self.forcefield
        self.forcefield.initialize_biosym_forcefield()

        return super().run()
