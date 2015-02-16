# -*- coding: utf-8 -*-
#
# __init__.py
# Created march 2011
# Author : V Frouin, B Thirion
#
"""
plinkio was a Python module offering utilities for basic Imaging Genetics.
It has been shrinked down to a PLINK file I/O module.
In the current state of development it offers:

   #. io on genotype data in bed plink format [#f1]_,
   #. preliminary version to get phenotype and covariates,
   #. wrappers around basic univariate statistics
      ##. univariate snp level
      ##. univariate gene level (aggregating statistics) *WIP*
      ##. correction for multiple testing (minP) *WIP*


   .. rubric:: Footnotes
   .. [#f1] Purcell S, Neale B, Todd-Brown K, Thomas L, Ferreira MAR, Bender D, Maller J, Sklar P, de Bakker PIW, Daly MJ & Sham PC (2007). PLINK: a toolset for whole-genome association and population-based linkage analysis. American Journal of Human Genetics, 81.


"""
from info import __version__


#import assoc
#import tests             #TODO : no depends on rpy2 and plink commandline
#import pheno
#import covar
from Genotype import Genotype, GenotypeAnnotation
from Annotation import Annotation
#from Pheno import PhenoRead, PhenoRead2, imputePhenoAndFix
from genodata import GenoData
#from phenodata import RoiPhenoData
#from covardata import CovarData
#from minP  import minP   #TODO : reused code and license pb
