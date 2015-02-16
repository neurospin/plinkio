# -*- coding: utf-8 -*-
#  genodata.py
#
#  Copyright 2013 Vincent FROUIN <vf140245@is207857>
"""
Created on Mon Oct 25 2013

@author: Vincent Frouin

Utility classes for genotype data and their context
"""

import numpy as np
from Genotype import Genotype
from os import path


class GenoData(object):
    """GenoData - Provides object/methods to build/access matrix of geno data
                  for numerical use
       Available methods cover two/three kinds of use:
           get_xxx: to get data
           meta_get_xxx: to get meta information
           select_xxx: to select columns
           filter_xxx: unclear if ti really has to (should include subset_maf, etc...)
    """

    def __init__(self, confobj):
        """
        """
        self._genotype = None
        self._column_descr = None
        self._subjects = None
        self._expanded_data = None
        self._gene_descr = dict()
        #
        my_source = confobj['genetics']['genofile']
        my_annot = confobj['genetics']['platform']
        my_resources = confobj['genetics']['resources']
        if path.exists(path.dirname(my_source)):
            self._genotype = Genotype(my_source,
                                      annot=my_annot, resources=my_resources)
        else:
            raise ValueError('incorrect path name: ' + path.dirname(my_source))
        #
        # Now re-concile potential diffs bw
        # list subjects info bw cfg and genotype data
        my_subject = set(confobj['genetics']['subjects'])
        my_subject = my_subject.intersection(
            set(self._genotype.getOrderedSubsetIndiv()))
        self._subjects = list(my_subject)
        self._genotype.setOrderedSubsetIndiv(self._subjects)

    def _get_genotype(self):
        """
        """
        return self._genotype

    def select_extract_snp(self, rs):
        """select_extract_snp : select function
                                 to select this speccif list of SNPs
            return :
                 np.array_uint8 of snp data (0,1,2,128 for na)
        """
        self._expanded_data = self._genotype.snpGenotypeByName(rs)
        self._column_descr = list(rs)

    def select_genelist_snp(self, gl):
        """select_genelist_snp : select function
                                 to select snp corresponding to the list of gene

           return : np.array_uint8 of snp data (0,1,2,128 for na)
        """
        rslist = []
        for i in gl:
            index_in_expand_data = 0
            tmplist = self._genotype.getChipAnnot().getRsByGene(i)
            self._gene_descr[i] = list(index_in_expand_data + np.arange(len(tmplist)))
            index_in_expand_data += len(tmplist)
            rslist.extend(tmplist)
        self._expanded_data = self._genotype.snpGenotypeByName(rslist)
        self._column_descr = list(rslist)

    def select_all_snp(self):
        """select_all_snp : select function
                                 to select all available snps
            return :
                 np.array_uint8 of snp data (0,1,2,128 for na)
        """
        self._expanded_data = self._genotype.snpGenotypeAll()
        self._column_descr = self._genotype.snpList()

    def get_data(self):
        """get_data : return genotype data (0,1,2,128 for na)
        """
        return self._expanded_data

    def get_col_idx_by_gene(self):
        """get_col_idx_by_gene: return dict keys are genes and val are
                                lsit of index in the colname data
        """
        return self._gene_descr

    def get_gene_names(self):
        """get_gene_names: returnlist of gene name currently selected
        """
        return self._gene_descr.keys()

    def get_colnames(self):
        """get_colnames: return list of snp names
        """
        return self._column_descr

    def get_subjects(self):
        """get_subjects : return the ordered subject list
        """
        return self._genotype.getOrderedSubsetIndiv()

    def meta_get_rs_by_gene(self, gene):
        """meta_get_rs_by_genlist : return rsname list
        """
        return self._genotype.getChipAnnot().getRsByGene(gene)

    def meta_get_rs_chrom(self, chrom):
        """meta_get_rs_by_genlist : return rsname list
        """
        print 'to be implemented'
