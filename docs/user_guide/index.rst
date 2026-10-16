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

Choosing the forcefield in a file
=================================
A forcefield file can define several forcefields. The Forcefield step lists those in
the file you pick, with ``default`` meaning the first one. ``oplsaa.frc`` defines

=================  ========================================================================
``oplsaa+``        OPLS-AA with the CL&P parameters for ionic liquids and any you have
                   added with LigParGen. Water is flexible SPC.
``oplsaa+-spc_e``  ``oplsaa+`` with rigid SPC/E water.
``oplsaa+-tip3p``  ``oplsaa+`` with rigid TIP3P water.
``oplsaa``         The original OPLS-AA.
``CL&P``           The CL&P forcefield for ionic liquids.
=================  ========================================================================

and ``nacl_water.frc`` defines ``nacl_water``, rigid SPC/E water with sodium,
potassium and chloride ions.

Rigid water
===========
Water models such as SPC/E and TIP3P were fitted as rigid molecules, and give the
density, diffusion coefficient and viscosity of liquid water they were fitted to only
when they are kept rigid. A forcefield makes bonds and angles rigid in its
``rigid_bond`` and ``rigid_angle`` sections, which give only their lengths and angles,
and take precedence over the flexible terms for the same atoms. ``oplsaa+-spc_e`` and
``oplsaa+-tip3p`` are ``oplsaa+`` with such sections for water (and, for TIP3P, the
TIP3P atom types); everything else is as in ``oplsaa+``. LAMMPS keeps these bonds and
angles at their values with SHAKE during dynamics, so you can use a 2 fs timestep.

The following sections cover accessing and controlling forcefields.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   ligpargen/index

Index
=====

* :ref:`genindex`


.. _Overview of Forcefields:  https://molssi-seamm.github.io/background/forcefields/overview.html
