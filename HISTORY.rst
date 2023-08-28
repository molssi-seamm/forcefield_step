=======
History
=======

2023.8.27 -- Fixed issue with angle in octahedral systems
  * The SHAPES-type simple fourier potential used for octahedral complexes has a fals
    minimim at 0º. Added a LJ 1/R^12 repulsive term between the two end atoms of the
    angle to prevent small angles. This required using tabulated potentials in LAMMPS.
    
2023.5.1 -- Fixed bug in Lithium battery forcefield
  * Fixed a typo in the angle type unit line which caused a crash
    
2023.4.6 -- Added Lithium battery forcefield
  * An initial set of parameters for cathode materials, specifically LiCoO2.

2023.2.13 -- Added OPLS-AA forcefield
  * Added parameters for OPLS-AA along with some extra parameters for ionic liquids
    * PF6-
    * ethylene carbonate (EC) and fluoronated EC (FEC)
  * Added atom-typing templates for most of OPLS-AA. Still missing a few and amino
    acids and DNA not yet tested.
  * Added extensive, almost-complete testing, for OPLS-AA
    

2021.2.10 (10 February 2021)
----------------------------

* Updated the README file to give a better description.
* Updated the short description in setup.py to work with the new installer.
* Added keywords for better searchability.

2020.8.1 (1 August 2020)
------------------------

* Added support for OpenKIM potentials in LAMMPS

0.9.1 (24 May 2020)
-------------------

* Added the specialized NaCl_water forcefield for testing the MolSSI
  Driver Interface (MDI) metadynamics driver.

0.9 (15 April 2020)
-------------------

* Internal changes for compatibility
  
0.1.0 (24 December 2017)
------------------------

* First release on PyPI.
