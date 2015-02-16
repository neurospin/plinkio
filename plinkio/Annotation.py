# -*- coding: utf-8 -*-
"""
Utility class for annotations on various chip manufacturer
"""
# Author : V Frouin
#      (code according to binary plink format descritpion - S Purcell)
#import re
#import numpy as np
#import io.bplinkread
#import annot.chip
#import annot.assay

import sqlite3
from os import path
from glob import glob
from numpy import where


class Annotation(object):
    """ ToDo
    """

    def __init__(self, source=None, resources=None, MaskWithGenotype=None):
        """
        Annotation(source, Mask) return an Annotation object. really ugly.
        implicit name finding of the sql file.

        Parameters
        ----------
        source :  id of the manifacturer chip

        Mask : TO BE FIX

        Returns
        -------
        An annotation object

        """
        #self._pdb = glob(path.join(path.dirname(__file__), "data","*.sql"))
        self._pdb = glob(path.join(resources, "*.sql"))

        if source is None:
            print [(path.basename(x).split("_")[1],
                   path.basename(x))for x in self._pdb]
            return
        platform = source + '.sql'
        #print platform
        #print [path.basename(x).split("_")[1] for x in self._pdb]
        ind = where([path.basename(x).split("_")[1] ==
                     platform for x in self._pdb])
        chipAnnotDb = self._pdb[ind[0]]
        self._conn = sqlite3.connect(chipAnnotDb)
        self._sql = self._conn.cursor()
        if MaskWithGenotype is None:
            self._maskWithGenotype = None
        else:
            self._maskWithGenotype = set(MaskWithGenotype.snpList())

    def __execute__(self, cmd):
        """
        """
        self._sql.execute(cmd)
        return [row for row in self._sql]

    def getRsByGene(self, gene):
        """
        GetRsByGene(geneName) : return a list of SNP paving the transcribed
        part of the gene

        Parameters
        ----------
        geneName :  a str for one gene symbol

        part : "TR", "HTR", "HTRT" # TO BE FIX
                TR : from the transcript part (exons and introns)
                HTR : TR + header part to cover transcription factor area
                HTRT : HTR + trailer part to cover transcription factor area

        header : inerger to specify bp length in bp

        trailer : inerger to specify bp length in bp

        Returns
        -------
        list of SNP (rsname)

        """
        cmd = 'SELECT DISTINCT dbgene.gstart, dbgene.gend, dbgene.chrname \
               FROM dbgene \
               WHERE genename ="%s"' % gene
        row = self.__execute__(cmd)
        if len(row) != 1:
            raise ValueError("Number of selected gene should be exactly 1")
        start = row[0][0]
        stop = row[0][1]
        chrom = row[0][2]
        cmd = "SELECT name FROM dbsnp \
               WHERE       dbsnp.stop > %d \
                      AND  dbsnp.stop < %d \
                      AND  dbsnp.chrom = %s" % (start, stop, chrom[3:])
        if self._maskWithGenotype is None:
            return [str(x[0]) for x in self.__execute__(cmd)]
        else:
            query_set = set([str(x[0]) for x in self.__execute__(cmd)])
            return list(query_set.intersection(self._maskWithGenotype))

    def getRsByChrom(self, chrNum):
        """
        getGeneByRs(rsname) :  return a list of SNP for a chrom
        Parameters
        ----------
        chrNum : <1..22, 23(X), 24(Y)>

        Returns
        -------
        list of SNP (rsname)
        """
        cmd = "SELECT name FROM dbsnp \
               WHERE dbsnp.chrom = %s" % (chrNum)
        if self._maskWithGenotype is None:
            return [str(x[0]) for x in self.__execute__(cmd)]
        else:
            query_set = set([str(x[0]) for x in self.__execute__(cmd)])
            return list(query_set.intersection(self._maskWithGenotype))

    def getGeneByRs(self, rsname):
        """
        getGeneByRs(rsname) : return the gene containing the SNP (rsname)

        Parameters
        ----------
        rsname :  a str for one SNP symbol

        Returns
        -------
        the corresponding Gene
        """
        cmd = 'SELECT dbsnp.start, dbsnp.stop, dbsnp.chrom \
               FROM dbsnp WHERE name = "%s"' % rsname
        row = self.__execute__(cmd)
        if len(row) < 1:
            raise ValueError("This SNP is not in the chip")
        start = row[0][0]
        stop = row[0][1]
        chrom = 'chr' + row[0][2]
        cmd = 'SELECT DISTINCT dbgene.genename \
               FROM dbgene \
               WHERE dbgene.gstart <= "%s" \
               AND dbgene.gend >= "%s" \
               AND dbgene.chrname == "%s"' % \
               (start, stop, chrom)
        row = self.__execute__(cmd)
        if len(row) != 1:
            raise ValueError("This SNP is incorrectly linked to genes")
        return str(row[0][0])
