# -*- coding: utf-8 -*-
"""A node or step for the forcefield in a flowchart"""

import forcefield
import logging
import seamm
import seamm.data as data
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('forcefield')


class Forcefield(seamm.Node):
    def __init__(self, flowchart=None, extension=None):
        '''Initialize a forcefield step

        Keyword arguments:
        '''
        logger.debug('Creating Forcefield {}'.format(self))

        self.ff_file = \
            '/Users/psaxe/Work/Flowchart/forcefield/data/pcff2018.frc'
        self.ff_name = None

        super().__init__(flowchart=flowchart, title='Forcefield',
                         extension=extension)

    def describe(self, indent='', json_dict=None):
        """Write out information about what this node will do
        If json_dict is passed in, add information to that dictionary
        so that it can be written out by the controller as appropriate.
        """

        next_node = super().describe(indent, json_dict)

        if self.ff_file[0] == '$':
            string = (
                "Reading the forcefield file given in the variable"
                " '{ff_file}'"
            )
        else:
            string = (
                "Reading the forcefield file '{ff_file}'"
            )
            
        job.job(
            __(string, ff_file=self.ff_file, indent=self.indent+'    ')
        )

        return next_node

    def run(self):
        """Setup the forcefield
        """

        next_node = super().run(printer=printer)

        ff_file = self.get_value(self.ff_file)

        printer.important(
            __("Reading the forcefield file '{ff_file}'",
               ff_file=ff_file, indent=self.indent+'    ')
        )

        if self.ff_name is None:
            data.forcefield = forcefield.Forcefield(ff_file)
        else:
            ff_name = self.get_value(self.ff_name)
            data.forcefield = forcefield.Forcefield(ff_file, ff_name)

        data.forcefield.initialize_biosym_forcefield()

        return next_node
