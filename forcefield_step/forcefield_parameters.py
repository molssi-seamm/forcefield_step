# -*- coding: utf-8 -*-
"""Control parameters for using forcefields
"""

import importlib
import logging
import os
import pkg_resources
import seamm

logger = logging.getLogger(__name__)

# Check if we can use OpenKIM
if importlib.util.find_spec('kim_query') is None:
    forcefields = []
else:
    forcefields = ['OpenKIM']

plugin_manager = seamm.PluginManager("org.molssi.seamm.atom_typers")
available_atomtyping_engines= []

logger.debug('Looking for installed forcefield plugins')

for group in plugin_manager.groups():
    for plugin in plugin_manager.plugins(group):
        available_atomtyping_engines.append(plugin)

available_atomtyping_engines = tuple(available_atomtyping_engines)

class ForcefieldParameters(seamm.Parameters):
    """The control parameters for forcefields"""

    parameters = {
        "atomtyping_engine": {
            "default": available_atomtyping_engines[0],
            "kind": "enumeration",
            "default_units": "",
            "enumeration": available_atomtyping_engines,
            "format_string": "s",
            "description": "The atomtyping tool to be used:",
            "help_text": "The atomtyping tool to use."
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**ForcefieldParameters.parameters, **defaults},
            data=data
        )
