# -*- coding: utf-8 -*-
"""A node or step for the forcefield in a workflow"""

import molssi_workflow
import molssi_workflow.data as data
import forcefield
import logging

logger = logging.getLogger(__name__)


class Forcefield(molssi_workflow.Node):
    def __init__(self, workflow=None, gui_object=None,
                 extension=None):
        '''Initialize a forcefield step

        Keyword arguments:
        '''
        logger.debug('Creating Forcefield {}'.format(self))

        self.ff_file = \
            '/Users/psaxe/Work/Workflow/forcefield/data/pcff2018.frc'
        self.ff_name = None

        super().__init__(workflow=workflow, title='Forcefield',
                         gui_object=gui_object, extension=extension)

    def run(self):
        """Setup the forcefield
        """

        data.forcefield = forcefield.Forcefield(self.ff_file)
        data.forcefield.initialize_biosym_forcefield()

        return super().run()
