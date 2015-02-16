========================
Tutorial. First examples
========================

.. currentmodule:: plinkio

Create 1st level objects
========================
Genotype data file and the annotation companion file should be available in 
plinkio/data. Those examples for low level objects instances

Read a genotype file
~~~~~~~~~~~~~~~~~~~~
To read the genotype file.

   >>> import plinkio
   >>> gfn = /home/me/plinkio/data/batch12QC_N620_autosomes_X
   >>> genotype = plinkio.Genotype(gfn)

Interrogate the genotype object for a given snp

   >>> genotype.snpGenotypeByName(['rs12705964', 'rs2894699'])
   yield an uin8 numpy.array with (0,1,2); Careful: 128 code for NA

..
    Interrogate the annotation available for this genotype; here get the snps
    corresponding to a given gene. Careful: only snp known to be part of the 
    Illumina 660Quad design will be returned.

       >>> annot = genotype.getChipAnnot()
       >>> annot.getRsByGene('FOXP2')
       yield a list of snp name (rsname)

    Create 2nd level objects
    ========================
    Creation of three objects. All of them may be queried for data and domain dependant
    metainformation (eg. SNPs genes for genodata object).

    The plinkio package is not currently connected to a database. The information
    from the db are sinked in a ConfigObj file. See data/image/build_image_db_assessor.py
    scripts to learn about the implicit ontology of this ConfigOj object. One .ini
    file is available and uptodate ImagenW1.ini (Imagen data for wave 1 genotyped
    subjects)

       >>> import plinkio
       >>> from configobj import ConfigObj
       >>> from os import path
       >>> #Acces to config files
       >>> config_path = path.join(path.dirname(ig.__file__), '..', 'data', 'imagen')
       >>> #Imagen Wave1
       >>> imagen_wave1_cfg = ConfigObj(path.join(config_path,'ImagenW1.ini'))

    Now get an instance of the GenoData class.All the hereby hard coded file are available
    from the svn repository (no need for extra downloading...)

       >>> genodata object
       >>> genodata = plinkio.GenoData(imagen_wave1_cfg)

    Now get an instance of the PhenoData class. All the hereby hard coded file are available
    from the svn repository (no need for extra downloading...). Please consider
    the way a list of contrasts is passed (selection parameter) to the constructor
    to select only a few phenotypes data ([protocol, model, constrast])

       >>> selection = [['SST', 'swea_mvtroi', 'stop_success - stop_failure'],
                 ['SST', 'swea', 'stop_success - stop_failure']
                ]
       >>> roiset =  path.join(path.dirname(plinkio.__file__), 'data', 'cort_333_LR.nii.gz')
       >>> phenodata = plinkio.RoiPhenoData(imagen_wave1_cfg, selection)
       >>> phenodata.aggregate_by_rois(roiset)

    Now get an instance of the CovarData class

       >>> covardata = plinkio.CovarData(imagen_wave1_cfg)
       >>> covardata.encode(filter='dummy')
       >>> cdata = covardata.get_covarmatrix()
