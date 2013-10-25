=======================
Reference documentation
=======================

.. currentmodule:: igutils


The file io rely on few very low-level functions (see bplink.py). There are 2 levels of objects in the design of this version of igutils:
    #. objects to support the classical concepts of genotype data in the bioinfo community (LIMS, etc.). It includes Annot (that describe the plateform - the chip-), GenoAnnot that brings APIs from the Annot to the Geno object. The Geno object knows the data (encoded and lazy-loaded) and and knows the plateform
    #. objects that offers APIs dedicated to use in a numerical framework. At this level, the objects offer methods to obtained the block of data, information on rows and columns, method to guarantee the integrity of the internal description.

From the objects of the 2nd level, a compound object should be created that would bring multiple-block dataset with information (rows, columns) and with integrity accros the blocks.

The 1st level classes
=====================
Description of the low level classes.

Contents:

.. toctree::
   :maxdepth: 2

   low_level_1.rst

The 2nd level classes (TO BE UPDATED)
=====================
Description of the mono block classes for genodata, phenodata and covariate - in my mind the data from the patient record - (so covariate may be an non-adequate name).

Contents:

.. toctree::
   :maxdepth: 2

   monoblock_level_1.rst
