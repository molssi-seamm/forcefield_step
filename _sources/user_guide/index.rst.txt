.. _user-guide:

**********
User Guide
**********
The Forcefield plug-in manages one or more forcefields or sets of interatomic potentials
for your simulations. It reads a forcefield file, selects a particular forcefield from
the file, and prepares the forcefield parameters for susbsequent simulation steps. This
step can also be used to assign the forcefield to the molecule or system that you are
working on, though that happens by default when you start the simulation, so you don't
need to handle it explicitly.

If you want to understand more about the theory and definition of forcefields, see the
`Overview of Forcefields`_ in the main SEAMM documentation.

Forcefields as model chemistries
================================
The forcefields can also be chosen with a **Model Chemistry** step instead of a
Forcefield step: this plug-in offers every forcefield it can find as a model chemistry,
and LAMMPS and Packmol then use it as they would the Forcefield step's.

* A classical forcefield is ``FF@<name>``, with the name the forcefield has in its
  file: ``FF@oplsaa+``, ``FF@oplsaa`` and ``FF@CL&P`` from ``oplsaa.frc``,
  ``FF@pcff``, ``FF@dreiding``, ``FF@dreiding-X6``, ... Only ``:``, ``@``, ``/`` and
  ``|`` are replaced, by ``-``, since the model chemistry uses them itself.
* A file that another forcefield file includes is part of that forcefield, not a
  forcefield of its own: e.g. ``OPLS-AA/ligpargen.frc``, which LigParGen's parameters
  are written to, extends ``FF@oplsaa+``.
* A ReaxFF parameter set is ``ReaxFF@<set>``, e.g. ``ReaxFF@CHO_cho_2008``.
* There is no program in front: LAMMPS evaluates the forcefield itself.

The forcefields come from the files shipped with this plug-in and from your own:
``~/.seamm.d/data/Forcefields`` (``personal:``), then the installation's
``<root>/data/Forcefields`` and ``~/SEAMM/data/Forcefields`` (``local:``), searched in
that order, so a forcefield of your own with the same name as a shipped one is used
instead of it. Your files are sent with a job submitted to a JobServer, as with the
Forcefield step.

The atoms are typed when the forcefield is needed -- by LAMMPS when it writes its
input, by Packmol for each kind of molecule -- unless they already have types for it, so
the Forcefield step's "assign forcefield to structure" is not needed.

The Forcefield step's default, the file ``oplsaa.frc`` with its default forcefield, is
``FF@oplsaa+``, the first forcefield in the file.

The following sections cover accessing and controlling forcefields.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   ligpargen/index

Index
=====

* :ref:`genindex`


.. _Overview of Forcefields:  https://molssi-seamm.github.io/background/forcefields/overview.html
