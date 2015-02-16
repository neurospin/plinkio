# -*- coding: utf-8 -*-
#  Genotype.py
#
#  Copyright 2013 Vincent FROUIN <vf140245@is207857>
"""
Created on Mon Oct 25 2013

@author: Vincent Frouin

Utility classes for Genotype and assayDescription data
Code according to binary plink format descritpion - S Purcell
http://pngu.mgh.harvard.edu/~purcell/plink/
"""
import re
from os import path
import numpy as np
import io.bplinkread
import annot.chip
import annot.assay
import Annotation


class GenotypeAnnotation(object):
    """ Provides object/method to support annotation on genoptype data.
    """
    autosomeHuman = range(1, 23)

    def __init__(self, source, format):
        """ ToDo
        """
        self._format = format
        self._encode = annot.assay.encodeMinAllCount
        self._filename = dict(bed=source + '.bed',
                              bim=source + '.bim',
                              fam=source + '.fam')
        for x in ('.bed$', '.bim$', '.fam$'):
            tmp = re.split(x, source)
            if tmp[-1] == '':
                self._filename = dict(bed=tmp[0] + '.bed',
                                      bim=tmp[0] + '.bim',
                                      fam=tmp[0] + '.fam')
                break
        self._snp = np.recfromtxt(self._filename['bim'])
        self._assay = np.recfromtxt(self._filename['fam'])
        self._snp_major = io.bplinkread.bedHeader(self._filename['bed'])
        self._snpListDict = dict(zip(self.snpList(), range(self.snpDim())))

    #def __del__(self):
        #"""Do  cleanups.
        #"""
        #if self._filename:

    def snpDim(self):
        """ ToDo

        Returns
        -------
        int
            number of SNP in the genotype data.
        """
        return len(self._snp)

    def snpChromDim(self):
        """ ToDo

        Returns
        -------
        list
            number of SNP per chromosome in the genotype data.
        """
        chrList = {}
        for x in GenotypeAnnotation.autosomeHuman:
            chrList["Chr%02d" % x] = sum(self._snp['f0'] == x)
        return chrList

    def snpList(self):
        """ ToDo

        Returns
        -------
        list
            SNP names available in the genotype data.
        """
        return self._snp['f1']

    def assayDim(self):
        """ ToDo
        """
        return len(self._assay)

    def assayFID(self):
        """ return the list of family enrolled in the assay

        Returns
        -------
        list
            Family id's available in the genotype data.
        """
        #TOFIX : test typed vs non-typed recarray
        if isinstance(self._assay[1], np.ndarray):
            subs = "%d" % annot.assay.plinkAssayDict['FID']
            ret_list = [annot.assay.plinkAssayFormatDict['FID'] % x
                        for x in self._assay[:, subs]]
        else:
            subs = "f%d" % annot.assay.plinkAssayDict['FID']
            ret_list = [annot.assay.plinkAssayFormatDict['FID'] % x
                        for x in self._assay[subs]]
        return ret_list

    def assayIID(self):
        """ return the list of subject enrolled in the assay

        Returns
        -------
        list
            Individual id's available in the genotype data.
        """
        #TOFIX : test typed vs non-typed recarray
        if isinstance(self._assay[1], np.ndarray):
            subs = "%d" % annot.assay.plinkAssayDict['IID']
            ret_list = [annot.assay.plinkAssayFormatDict['IID'] % x
                        for x in self._assay[:, subs]]
        else:
            subs = "f%d" % annot.assay.plinkAssayDict['IID']
            ret_list = [annot.assay.plinkAssayFormatDict['IID'] % x
                        for x in self._assay[subs]]
        return ret_list


class Genotype(GenotypeAnnotation):
    """ Provides object/method to support the data from a genotype file
    """
    def __init__(self, source,
                 format="bed",
                 annot="default",
                 resources=path.join(path.dirname(__file__),
                                     "..", "data", "template", "platform"),
                 load=False):
        """ ToDo
        """
        GenotypeAnnotation.__init__(self, source, format)
        #try:
            #self._chipAnnot = Annotation.Annotation(annot, resources)
        #except:
            #self._chipAnnot = None
        self._format = format
        self._data = None
        self._anot = None
        self._orderedSubset = range(self.assayDim())

        # Load Data
        if type(source) == np.ndarray:
            # assign data from source array
            self._data = source[:]
        elif type(source) in (str, unicode):
            # only load image data from file if requested
            if load:
                self.load()
            else:
                self.preload()
        else:
            raise ValueError("Unsupported source type. Only NumPy arrays " +
                             "and filename string are supported.")

    def __del__(self):
        """ Do all necessary cleanups.
        """
        self._data = None

    def load(self):
        """ ToDo
        not used ?
        """

    def preload(self):
        """ lazy loading of annot and binary bed
        """
        if self._snp_major:
            self._data = io.bplinkread.bedRead(self._filename['bed'])
        else:
            raise ValueError("Not snp_major format Unsupported bed type.")

    def setOrderedSubsetIndiv(self, idList=[]):
        """ set a list as ordering index for subsequent queries on snps
        """
        tmp = self.assayIID()
        retOSL = []
        retMiss = []
        self._orderedSubset = []
        for x in idList:
            if x in tmp:
                retOSL.append(x)
                self._orderedSubset.append(tmp.index(x))
            else:
                retMiss.append(x)
        return retOSL, retMiss

    def getOrderedSubsetIndiv(self):
        """ get the current list used as ordering index for subsequent
        queries on snps
        """
        return [self.assayIID()[x] for x in self._orderedSubset]

    def getOrderedSubsetFamily(self):
        """ get the current list used as ordering index for subsequent
        queries on snps
        """
        return [self.assayFID()[x] for x in self._orderedSubset]

    def getChipAnnot(self):
        """ return the instance of the ChipAnnot that describe the dataset
        """
        return self._chipAnnot

    def snpGenotypeByName(self, rsname):
        """ return genotyping data as an array. The columns are in the snp of the
        rsname list and lines are ordered along with order
        specified by the setOrderedSubsetIndiv() or in the order of the load
        otherwise

        Parameters
        ----------
        rsname : list
            rsname may be a string or a list of strings (e.g. 'rs1234')

        Returns
        -------
        gt : a numpy.array
            array with lines ordered along with previously set order
        """
        rs = (rsname if type(rsname) == list else [rsname])
        gt = []
        for irs in rs:
            if not(type(irs) in (str, np.string_)):
                raise ValueError("Unsupported type for rsname : should be string.")
            tmp = self._snpListDict[irs]
            gt.append(io.bplinkread.bedDecode(self._data,
                                              len(self._assay), len(self._snp),
                                              self._encode, tmp))
        gt = np.asarray(gt).T
        #print gt.shape
        return gt[self._orderedSubset, :]

    def estimate_maf_by_name(self, rsname):
        """ query maf  by snp name

        Parameters
        ----------
        rsname : list
            may be a string or a list of strings (e.g. 'rs1234')

        Returns
        -------
        maf : a list of float
            minor allele frequency as percentage
        """
        hom1 = hom2 = het = 0
        gt = self.snpGenotypeByName(rsname)
        hom1 = np.sum(gt == 0)
        het = np.sum(gt == 1)
        hom2 = np.sum(gt == 2)
        n = 2.0 * (gt.shape[0] - np.sum(np.isnan(gt)))
        hom1, hom2 = min(hom1, hom2), max(hom1, hom2)
        return (2.0 * hom1 + het) / n

    def estimate_maf_genotype(self, gt):
        """ query maf for some genotyped data

        Parameters
        ----------
        gt : numpy.array of uint8
            some genotype data

        Returns
        -------
        maf : a list of float
            minor allele frequency as percentage
        """
        hom1 = np.sum(gt == 0, axis=0)
        het = np.sum(gt == 1, axis=0)
        hom2 = np.sum(gt == 2, axis=0)
        n = 2.0 * (gt.shape[0] - np.sum(np.isnan(gt), axis=0))
        homozygote_min = np.min(np.vstack((hom1, hom2)), axis=0)
        homozygote_maj = np.max(np.vstack((hom1, hom2)), axis=0)
        return (2.0 * homozygote_min + het) / n

    def snpGenotypeAll(self, test=False):
        """ query to get the whole genotyping data ordered along with orderedSubset
        list if it exists or in the order of the load otherwise

        Returns
        -------
        gt : a numpy.array
            ordered along with previously set order
        """
        gt = io.bplinkread.bedDecode(self._data,
                                     len(self._assay), len(self._snp),
                                     self._encode)
        if test:
            return dict(genotype=gt[self._orderedSubset, :],
                        rsname=self.snpList().tolist())
        else:
            return gt[self._orderedSubset, :]

    #def snpGenotypeAllTest(self):
        #"""
        #Query to get the whole genotyping data ordered along with orderedSubset
        #list if it exists or in the order of the load otherwise

        #Return
        #------
            #gt : a numpy.array ordered along with previously set order

        #"""
        #gt = io.bplinkread.bedDecode(self._data,
                            #len(self._assay), len(self._snp),
                            #self._encode)
        #return dict(genotype=gt[self._orderedSubset,:], rsname=self.snpList().tolist())
