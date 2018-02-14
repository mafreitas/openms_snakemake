import os.path
import collections
from fficfg import *
import glob
import sys

USER_DATA = os.getcwd()
DOCKER_CMD =  "singularity exec ~/singularity/mfreitas_openms_2.2.0-2017-12-14-8115a223bb29.img"

DOCKER_DATA = os.getcwd()
OPENMS_DOCKER_IMAGE = ""
RAWFILES = glob.glob("mzml/*")

tmpdirs = ['work','dbsearch',"csv","logs"]
for dir in tmpdirs:
    make_dir(dir)

SAMPLES = []
allowed_exts = [".mzml",".mzML","MZML"]
for rawfile in RAWFILES:
    rbase = os.path.basename(rawfile)
    rbase,rext = os.path.splitext(rbase)
    if rext in allowed_exts:
        SAMPLES.append(rbase)

DBFILES = glob.glob("fasta/*")
DATABASES = []
allowed_exts = [".fasta",".FASTA"]
for dbfile in DBFILES:
    dbase = os.path.basename(dbfile)
    dbase,dext = os.path.splitext(dbase)
    if dext in allowed_exts:
        DATABASES.append(dbase)


################################################################
# Setup Targets for Pipeline
################################################################

rule targets:
    input:
        'work/combined_database_rev.fasta',
        expand("dbsearch/{sample}_myrm.idXML",sample=SAMPLES),
        expand("csv/{sample}_myrm.csv",sample=SAMPLES),
        expand('work/{sample}_myrm_idpep.idXML',sample=SAMPLES),
        expand('work/{sample}_myrm_idpep.idXML',sample=SAMPLES),
        expand('work/{sample}_myrm_idpep_pepidx.idXML',sample=SAMPLES),
        expand('csv/{sample}_myrm_idpep_pepidx.csv',sample=SAMPLES),
        'work/myrm_idpep_pepidx_merge.idXML',
        'work/myrm_idpep_pepidx_merge_filt.idXML',
        "work/fido.idXML",
        "work/fido_fdr.idXML",
        "csv/fido_fdr.csv",
        "work/fido_fdr_filt.idXML",
        "csv/fido_fdr_filt.csv",   
        "csv/protein_counts.csv"

        
################################################################
# Create Database with decoys and contaminants
################################################################

rule DecoyDatabaseRule:
    input:
        fasta = expand('fasta/{database}.fasta', database=DATABASES)
    output:
        fasta = 'work/combined_database_rev.fasta'
    params:
        log = 'log/combined_database_rev.log'
    threads: 1
    run:
        DecoyDatabaseParams['in'] = " ".join([DOCKER_DATA+"/" + s for s in input.fasta])
        DecoyDatabaseParams['decoy_string'] = "rev_"
        cmd_str = cmd(DecoyDatabaseParams)

        shell(cmd_str)


rule MyriMatchAdapterRule:
    input:
        mzml = "mzml/{datafile}.mzML",
        fasta = 'work/combined_database_rev.fasta'
    output:
        idxml = "dbsearch/{datafile}_myrm.idXML"
    params:
        log = "logs/{datafile}_myrm.log"
    threads: 12
    priority: 10
    run:
         MyriMatchAdapterParams['precursor_mass_tolerance'] = "20"
         MyriMatchAdapterParams['precursor_mass_tolerance_unit'] = "ppm"
         MyriMatchAdapterParams['fragment_mass_tolerance'] = "0.8"
         MyriMatchAdapterParams['fragment_mass_tolerance_unit'] = "Da"
         MyriMatchAdapterParams['CleavageRules'] = "Trypsin/P"
         MyriMatchAdapterParams['fixed_modifications'] = '\"Carbamidomethyl (C)\"'
         MyriMatchAdapterParams['threads'] = str(threads)
         cmd_str = cmd(MyriMatchAdapterParams)
         shell(cmd_str)

rule TextExporterSearchRule:
    input:
        xml = "dbsearch/{datafile}_myrm.idXML"
    output:
        csv = "csv/{datafile}_myrm.csv"
    params:
        log = 'false'
    threads: 1
    priority: 90
    run:
         cmd_str = cmd(TextExporterParams)
         shell(cmd_str)        

rule IDPosteriorErrorProbabilityRule:
    input:
        idxml = "dbsearch/{datafile}_myrm.idXML"
    output:
        idxml = "work/{datafile}_myrm_idpep.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        cmd_str = cmd(IDPosteriorErrorProbabilityParams)
        shell(cmd_str)


rule PeptideIndexerRule:
    input:
        idxml = "work/{datafile}_myrm_idpep.idXML",
        fasta = 'work/combined_database_rev.fasta'
    output:
        idxml = "work/{datafile}_myrm_idpep_pepidx.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        cmd_str = cmd(PeptideIndexerParams)
        shell(cmd_str)
        
rule TextExporterSearchIdxRule:
    input:
        xml = "work/{datafile}_myrm_idpep_pepidx.idXML"
    output:
        csv = "csv/{datafile}_myrm_idpep_pepidx.csv"
    params:
        log = 'false'
    threads: 1
    run:

         cmd_str = cmd(TextExporterParams)
         shell("echo " + cmd_str)
         shell(cmd_str)        

################################################################
# Merge Search Results and run FIDO
################################################################        

rule IDMergeFidoRule:
    input:
        idxmls = expand("work/{sample}_myrm_idpep_pepidx.idXML", sample=SAMPLES)
    output:
        idxml = "work/myrm_idpep_pepidx_merge.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        IDMergerParams['in'] = " ".join([DOCKER_DATA+"/" + s for s in input.idxmls])
        IDMergerParams['out'] = DOCKER_DATA+"/"+ output.idxml
        IDMergerParams['annotate_file_origin'] = '_true'
        cmd_str = cmd(IDMergerParams)

        shell(cmd_str)

rule IDFilterPreFidoRule:
    input:
        idxml = "work/myrm_idpep_pepidx_merge.idXML"
    output:
        idxml = "work/myrm_idpep_pepidx_merge_filt.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        IDFilterParams['score:pep'] = "1.0"
        IDFilterParams['score:prot'] = "0"        
        cmd_str = cmd(IDFilterParams)

        shell(cmd_str)

rule FidoAdapter:
    input:
        idxml = "work/myrm_idpep_pepidx_merge_filt.idXML"
    output:
        idxml = "work/fido.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        FidoAdapterParams['threads'] = str(threads)
        cmd_str = cmd(FidoAdapterParams)

        shell(cmd_str)
        
rule FalseDiscoveryRateFidoRule:
    input:
        idxml = "work/fido.idXML"
    output:
        idxml = "work/fido_fdr.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        FalseDiscoveryRateParams['PSM']=" false"
        FalseDiscoveryRateParams['protein']=" true"
        cmd_str = cmd(FalseDiscoveryRateParams)

        shell(cmd_str)
        
rule TextExporterFidoFdrRule:
    input:
        xml = "work/fido_fdr.idXML"
    output:
        csv = "csv/fido_fdr.csv"
    params:
        log = 'false'
    threads: 1
    run:

         cmd_str = cmd(TextExporterParams)
         shell("echo " + cmd_str)
         shell(cmd_str)        

rule IDFilterFidoRule:
    input:
        idxml = "work/fido_fdr.idXML"
    output:
        idxml = "work/fido_fdr_filt.idXML"
    params:
        log = 'false'
    threads: 1
    run:
        IDFilterParams['score:pep'] = "0.0"
        IDFilterParams['score:prot'] = "0.05"
        cmd_str = cmd(IDFilterParams)

        shell(cmd_str)
        
rule TextExporterFidoFdrFiltRule:
    input:
        xml = "work/fido_fdr_filt.idXML"
    output:
        csv = "csv/fido_fdr_filt.csv"
    params:
        log = 'false'
    threads: 1
    run:
         cmd_str = cmd(TextExporterParams)
         shell("echo " + cmd_str)
         shell(cmd_str)   

rule ProteinQuantifierSpecCounts:
    input:
        idxml = "work/myrm_idpep_pepidx_merge_filt.idXML",
        fido = "work/fido_fdr_filt.idXML"
    output:
        csv = "csv/protein_counts.csv"
    threads: 1
    run:
        ProteinQuantifierParams["average"] = "sum"
        ProteinQuantifierParams["top"] = "0"
        ProteinQuantifierParams["include_all"] = "_true"
        ProteinQuantifierParams["format:separator"] = ","
        cmd_str = cmd(ProteinQuantifierParams)
        print(cmd_str)
        shell(cmd_str)


        