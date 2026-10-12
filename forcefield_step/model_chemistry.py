# -*- coding: utf-8 -*-

"""The forcefields as model chemistries.

Every forcefield defined in a ``.frc`` file the step can find -- the package's,
the SEAMM installation's (``local:``) and the user's (``personal:``) -- is offered
as a model chemistry: ``FF@<name>`` for a classical forcefield and
``ReaxFF@<parameter set>`` for a ReaxFF one. The steps that use a forcefield
(LAMMPS, Packmol) build it from the model chemistry with :func:`forcefield`.

See lammps_step's campaign of 2026-10-11 (forcefields as model chemistries).
"""

import importlib.resources
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

#: Characters the model-chemistry grammar reserves
RESERVED = ":@/|"

#: The methods the bundled classical forcefields are offered as
METHOD_NAMES = {
    "oplsaa": "OPLS-AA",
    "oplsaa+": "OPLS-AA+",
    "pcff": "PCFF",
    "dreiding": "DREIDING",
    "dreiding/X6": "DREIDING-X6",
}

#: The model-chemistry types this package offers
TYPES = ("FF", "ReaxFF")

# Where SEAMM keeps user data, as the Forcefield step's personal:/local: files
_PERSONAL = Path("~/.seamm.d/data/Forcefields")
_LOCAL = Path("~/SEAMM/data/Forcefields")


def package_directory():
    """The directory of the forcefields shipped with this package."""
    return Path(str(importlib.resources.files("forcefield_step") / "data"))


def source_directories(root=None, data_path=None):
    """``[(source, directory)]`` searched for ``.frc`` files, in order.

    ``personal`` is ``~/.seamm.d/data/Forcefields``; ``local`` the installation's
    ``<root>/data/Forcefields`` and then the default installation's
    ``~/SEAMM/data/Forcefields``. Given a flowchart's ``data_path``, the
    ``Forcefields`` directory in each of its directories instead -- in a job
    this starts with the job's own copies of the files sent with it.
    """
    if data_path is not None:
        personal = (_PERSONAL.expanduser() / "..").resolve()
        return [
            (
                "personal" if Path(d).expanduser().resolve() == personal else "local",
                Path(d).expanduser() / "Forcefields",
            )
            for d in data_path
        ]
    if root is None:
        from seamm_util import current_root

        root = current_root()
    result = [("personal", _PERSONAL.expanduser())]
    own = Path(root).expanduser() / "data" / "Forcefields"
    base = _LOCAL.expanduser()
    result.append(("local", own))
    if own.resolve() != base.resolve():
        result.append(("local", base))
    return result


def forcefield_files(root=None, data_path=None):
    """``[(spec, path)]`` of the ``.frc`` files, the user's first.

    ``spec`` is what the Forcefield step calls the file: ``personal:<path>`` or
    ``local:<path>`` relative to its directory, or the path within the package's
    data directory.
    """
    result = []
    for source, directory in source_directories(root, data_path):
        if directory.is_dir():
            for path in sorted(directory.glob("**/*.frc")):
                result.append((f"{source}:{path.relative_to(directory)}", path))
    directory = package_directory()
    for path in sorted(directory.glob("**/*.frc")):
        result.append((str(path.relative_to(directory)), path))
    return result


def defined_forcefields(path):
    """The names of the forcefields a ``.frc`` file defines (``#define``), in
    order; the first is the file's default."""
    names = []
    try:
        with open(path, errors="replace") as fd:
            for line in fd:
                if line.startswith("#define"):
                    words = line.split()
                    if len(words) > 1:
                        names.append(words[1])
    except OSError as e:
        logger.warning(f"Could not read the forcefield file {path}: {e}")
    return names


def type_and_method(name):
    """The model-chemistry type and method for a forcefield's name.

    ``reaxff/<set>`` is ``ReaxFF@<set>``; the bundled classical forcefields have
    the names in :data:`METHOD_NAMES` (``oplsaa`` is ``FF@OPLS-AA``); any other
    name is used as it is, with the grammar's reserved characters replaced by
    ``-``.
    """
    if name.startswith("reaxff/"):
        type_, method = "ReaxFF", name[len("reaxff/") :]
    else:
        type_, method = "FF", METHOD_NAMES.get(name, name)
    for character in RESERVED:
        method = method.replace(character, "-")
    return type_, method


def get_model_chemistry_options(
    periodic_only=False, mdi_only=False, root=None, data_path=None
):
    """The forcefields as model chemistries.

    Parameters
    ----------
    periodic_only : bool
        Only those that handle periodic systems -- all of them.
    mdi_only : bool
        Only those launchable as MDI engines -- none: LAMMPS evaluates the
        forcefield itself.
    root : str or Path, optional
        The SEAMM installation; the current one by default.
    data_path : [Path], optional
        A flowchart's data directories (``Node.data_path``) to search instead
        of the default ones: in a job, its own copies of the files sent with it.

    Returns
    -------
    dict
        Keyed by the model chemistry (``FF@OPLS-AA``). Each entry has
        ``model_chemistry``, ``type``, ``description``, ``file`` (the file as the
        Forcefield step names it), ``path``, ``forcefield`` (the name in the
        file), ``source`` (``personal``, ``local`` or ``package``),
        ``periodic_native``, ``periodic_mdi`` and ``mdi_capable``. A user's
        forcefield of the same name as a bundled one is offered instead of it.
    """
    if mdi_only:
        return {}
    options = {}
    for spec, path in forcefield_files(root, data_path):
        source = spec.split(":", 1)[0] if ":" in spec else "package"
        for name in defined_forcefields(path):
            type_, method = type_and_method(name)
            key = f"{type_}@{method}"
            if key in options:
                logger.debug(
                    f"The forcefield '{name}' in {path} is shadowed by "
                    f"{options[key]['path']}"
                )
                continue
            what = "ReaxFF parameter set" if type_ == "ReaxFF" else "Forcefield"
            options[key] = {
                "model_chemistry": key,
                "type": type_,
                "description": f"{what} '{name}' from {spec}",
                "file": spec,
                "path": str(path),
                "forcefield": name,
                "source": source,
                "periodic_native": True,
                "periodic_mdi": False,
                "mdi_capable": False,
            }
    return options


def _resolve(spec, node=None):
    """The path of a forcefield file given as the Forcefield step names it."""
    for source in ("personal", "local"):
        tag = f"{source}:"
        if spec.startswith(tag):
            relative = spec[len(tag) :]
            if node is not None:
                return Path(node.find_data_file("Forcefields/" + relative))
            for source_, directory in source_directories():
                if source_ == source and (directory / relative).exists():
                    return directory / relative
            raise FileNotFoundError(f"Cannot find the forcefield file '{spec}'")
    return package_directory() / spec


def uri_handler(node=None):
    """A ``uri_handler`` for seamm_ff_util: ``local:`` includes are data files."""

    def handler(path):
        filename = str(path)
        if filename.startswith("local:"):
            return _resolve(filename, node)
        return Path(path).expanduser().resolve()

    return handler


def forcefield(model_chemistry, node=None):
    """The seamm_ff_util forcefield for a model chemistry, ready to use.

    Parameters
    ----------
    model_chemistry : dict
        The ``_model_chemistry`` wrapper of an ``FF`` or ``ReaxFF`` model
        chemistry offered by this package.
    node : seamm.Node, optional
        The step using it: its data files (a job's copies of ``local:`` and
        ``personal:`` files) and its references, which get the forcefield's
        citations.

    Returns
    -------
    seamm_ff_util.Forcefield
    """
    import seamm_ff_util

    options = model_chemistry.get("options") or {}
    spec = options.get("file")
    name = options.get("forcefield")
    if spec is None or name is None:
        raise ValueError(
            f"The model chemistry {model_chemistry.get('level')} is not a forcefield "
            "offered by the Forcefield step."
        )
    path = _resolve(spec, node)
    ff = seamm_ff_util.Forcefield(
        str(path),
        uri_handler=uri_handler(node),
        references=getattr(node, "references", None),
    )
    ff.initialize_biosym_forcefield(name)
    return ff


def data_files(model_chemistry, node, local_only=True):
    """The files a job needs for a forcefield model chemistry, as the Forcefield
    step's ``list_data_files``: ``[(uri, path)]`` of the ``local:`` and
    ``personal:`` file and its includes (and the package's, unless
    ``local_only``)."""
    import seamm_util

    options = model_chemistry.get("options") or {}
    spec = options.get("file")
    if spec is None:
        return []
    result = []
    path = _resolve(spec, node)
    if ":" in spec:
        result.append(("data:Forcefields/" + spec.split(":", 1)[1], path))
    elif not local_only:
        result.append((spec, path))
    with seamm_util.Open(
        path, "r", include="#include", uri_handler=uri_handler(node)
    ) as fd:
        for _ in fd:
            pass
        visited = fd.visited
    for uri, included in visited[1:]:
        if uri.startswith("local:"):
            result.append(("data:Forcefields/" + uri[6:], included))
        elif not local_only:
            result.append((uri, included))
    return result
