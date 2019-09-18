# -*- coding: utf-8 -*-
"""Control parameters for using forcefields
"""

import logging
import os
import pkg_resources
import seamm

logger = logging.getLogger(__name__)


# Get the list of available forcefields
path = pkg_resources.resource_filename(__name__, 'data/')
forcefields = []
with os.scandir(path) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            print(entry.name)
            ffname, ext = os.path.splitext(entry.name)
            if ext == '.frc':
                forcefields.append(entry.name)


class ForcefieldParameters(seamm.Parameters):
    """The control parameters for forcefields"""

    parameters = {
        "forcefield_file": {
            "default": forcefields[0],
            "kind": "enumeration",
            "default_units": "",
            "enumeration": tuple(forcefields),
            "format_string": "s",
            "description": "Forcefield file:",
            "help_text": "The forcefield file to use."
        },
        "forcefield": {
            "default": "default",
            "kind": "enumeration",
            "default_units": "",
            "enumeration": tuple('default',),
            "format_string": "s",
            "description": "Forcefield:",
            "help_text": "The forcefield with the file."
        },
    }

    def __init__(self, defaults={}, data=None):
        """Initialize the instance, by default from the default
        parameters given in the class"""

        super().__init__(
            defaults={**ForcefieldParameters.parameters, **defaults},
            data=data
        )
