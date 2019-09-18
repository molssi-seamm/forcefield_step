# -*- coding: utf-8 -*-

"""A node or step for the forcefield in a flowchart"""

import forcefield_step
import configargparse
import logging
import os.path
import pkg_resources
import seamm_ff_util
import seamm
import seamm.data as data
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('forcefield')


def upcase(string):
    """Return an uppercase version of the string.

    Used for the type argument in argparse/
    """
    return string.upper()


class Forcefield(seamm.Node):

    def __init__(self, flowchart=None, extension=None):
        '''Initialize a forcefield step

        Keyword arguments:
        '''
        logger.debug('Creating Forcefield {}'.format(self))

        # Argument/config parsing
        self.parser = configargparse.ArgParser(
            auto_env_var_prefix='',
            default_config_files=[
                '/etc/seamm/forcefield_step.ini',
                '/etc/seamm/seamm.ini',
                '~/.seamm/forcefield_step.ini',
                '~/.seamm/seamm.ini',
            ]
        )

        self.parser.add_argument(
            '--seamm-configfile',
            is_config_file=True,
            default=None,
            help='a configuration file to override others'
        )

        # Options for this plugin
        self.parser.add_argument(
            "--from-smiles-log-level",
            default=configargparse.SUPPRESS,
            choices=[
                'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
            ],
            type=upcase,
            help="the logging level for the From SMILES step"
        )

        self.options, self.unknown = self.parser.parse_known_args()

        # Set the logging level for this module if requested
        if 'forcefield_log_level' in self.options:
            logger.setLevel(self.options.forcefield_log_level)

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

        if P['forcefield_file'][0] == '$':
            text = (
                "Read the forcefield file given in the variable"
                " '{forcefield_file}' and use the {forcefield} "
                "forcefield."
            )
        else:
            text = (
                "Read the forcefield file '{forcefield_file}' "
                "and use the {forcefield} forcefield."
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

        # The options from command line, config file ...
        o = self.options  # noqa: F841

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        printer.important(__(self.header, indent=self.indent))
        printer.important(
            __(
                "Reading the forcefield file '{forcefield_file}'",
                **P,
                indent=self.indent + '    '
            )
        )

        # Find the forcefield file
        path = pkg_resources.resource_filename(__name__, 'data/')
        ff_file = os.path.join(path, P['forcefield_file'])

        if P['forcefield'] == 'default':
            data.forcefield = seamm_ff_util.Forcefield(ff_file)
            printer.important(
                __(
                    "   Using the default forcefield '{ff}'.",
                    ff=data.forcefield.forcefields[0],
                    indent=self.indent + '    '
                )
            )
        else:
            data.forcefield = seamm_ff_util.Forcefield(
                ff_file, P['forcefield']
            )
            printer.important(
                __(
                    "   Using the forcefield '{forcefield}'",
                    **P,
                    indent=self.indent + '    '
                )
            )

        data.forcefield.initialize_biosym_forcefield()
        printer.important('')

        return next_node
