**********************
LigParGen utility tool
**********************
The parameters from the `LigParGen Server`_ are not in a form SEAMM can use directly,
so this plug-in provides a small tool that fetches them into a forcefield file of your
own. Run it from the command line of your SEAMM environment::

    ligpargen

It asks for a SMILES string, and for each one you give it:

#. It builds the molecule and writes ``structure.mol`` in the current directory.

#. It offers you the address of the `LigParGen Server`_ and the molecule's canonical
   SMILES, copying each to the clipboard in turn. Paste the SMILES into the website's
   SMILES box, or upload ``structure.mol``, choose the charge model and the charge, and
   click **Submit Molecule**.

#. On the results page, click the **KEY** button under **TINKER** to download the
   parameters.

#. Back in the tool, press return. It finds the file you just downloaded, confirms it
   is the right one, and adds the parameters to
   ``~/.seamm.d/data/Forcefields/OPLS-AA/ligpargen.frc``, keeping a backup of the
   previous version alongside it.

Give it an empty line when you have finished. The forcefield file it writes is picked
up automatically by the ``oplsaa+`` forcefield, so the molecules you have added are
available to any step that uses it.

The order of the atoms
======================
LigParGen does not keep the order of the atoms you give it: it perceives the molecule
afresh and orders it its own way. The tool therefore works out which of LigParGen's
atoms is which of yours from the connectivity, which the .key file describes, and not
from the order the two happen to be in.

Before it adds a molecule, it checks the result against the molecule:

* every atom is given a type of its own element;
* no type claims more bonds than its element can have;
* every bond of the molecule is one that the LigParGen file has parameters for.

If any of these fails the tool stops and says which atom or bond is wrong, rather than
writing parameters that look reasonable and are not. The most likely cause is that the
.key file is for a different molecule than the one you asked for -- it is easy to
submit one SMILES to the website and another to the tool, or to pick up an older
download.

.. note::
   Forcefield files generated before SEAMM 2026.9.20 were written on the assumption
   that the two orders agreed. Where they did not, the atoms were given each other's
   types -- a hydrogen might carry the mass and charge of an oxygen -- and nothing
   reported it, because moving the charges between the atoms leaves the total
   unchanged. If you have a ``ligpargen.frc`` from before then, regenerate the
   molecules in it.

.. _LigParGen Server: https://zarbi.chem.yale.edu/ligpargen/index.html
