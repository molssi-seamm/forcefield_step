# -*- coding: utf-8 -*-

"""A node or step for the forcefield in a flowchart"""

import forcefield_step
import logging
import seamm_ff_util
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

        super().__init__(
            flowchart=flowchart, title='Forcefield', extension=extension
        )

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

        if self.ff_file[0] == '$':
            text = (
                "Reading the forcefield file given in the variable"
                " '{ff_file}'"
            )
        else:
            text = "Reading the forcefield file '{ff_file}'"

        return self.header + '\n' + __(
            text, indent=3*' ', ff_file=self.ff_file
        ).__str__()

    def run(self):
        """Setup the forcefield
        """

        next_node = super().run(printer=printer)

        ff_file = self.get_value(self.ff_file)

        printer.important(__(self.header, indent=self.indent))
        printer.important(
            __(
                "Reading the forcefield file '{ff_file}'",
                ff_file=ff_file,
                indent=self.indent + '    '
            )
        )

        if self.ff_name is None:
            data.forcefield = seamm_ff_util.Forcefield(ff_file)
        else:
            ff_name = self.get_value(self.ff_name)
            data.forcefield = seamm_ff_util.Forcefield(ff_file, ff_name)

        data.forcefield.initialize_biosym_forcefield()
        printer.important('')

        return next_node
