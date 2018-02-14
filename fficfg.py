import collections
import os
import errno

def cmd(od,log="false",debug="0",no_progress="false",echo=True):

    cmd_string = ''
    for key, value in od.items():

        if key == 'exe':
            cmd_string = value
        elif 'false' in value:
            continue
        elif value[0] == '_':  #use _ to omit the value
            cmd_string = cmd_string + ' -%s' %(key)
        elif key[0] == '_':  #use _ to omit the key
            cmd_string = cmd_string + ' %s' %(value)
        else:
            cmd_string = cmd_string + ' -%s %s' %(key, value)
    
    
    if log != "false":
        cmd_string = cmd_string + " -log " + log
    if no_progress != "false":
        cmd_string = cmd_string + " -progress "         
    
    cmd_string = cmd_string + " -debug "

    if echo:
        cmd_string = "echo " + cmd_string + " && " + cmd_string

    return cmd_string


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            print(exception)
            raise

ConsensusIDParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} ConsensusID",
"in": "{input.idxml}",
"out": "{output.idxml}",
"threads": "1"
})
    
ConsensusMapNormalizerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} ConsensusMapNormalizer",
"in": "{input.consensusxml}",
"out": "{output.consensusxml}",
"threads": "1"
})
    
DecoyDatabaseParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} DecoyDatabase",
"in": "{input.fasta}",
"out": "{output.fasta}",
"threads": "1"
})

FalseDiscoveryRateParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FalseDiscoveryRate",
"in": "{input.idxml}",
"out": "{output.idxml}",
"threads": "1"
})
    
FeatureFinderCentroidedParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FeatureFinderCentroided",
"in": "{input.mzml}",
"out": "{output.featurexml}",
"threads": "1"
})

FeatureFinderIdentificationParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FeatureFinderIdentification",
"in": "{input.mzml}",
"id": "{input.int}",
"id_ext": "{input.ext}",
"out": "{output.featurexml}",
"threads": "1"
})

FeatureFinderMultiplexParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FeatureFinderMultiplex",
"in": "{input.mzml}",
"out": "{output.consensusxml}",
"out_features": "false",
"out_mzq": "false",
"threads": "1"
})

FeatureLinkerUnlabeledKDParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FeatureLinkerUnlabeledKD",
"in": "{input.featurexmls}",
"out": "{output.consensusxml}",
"threads": "1"
})
    
FeatureLinkerUnlabeledQTParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FeatureLinkerUnlabeledQT",
"in": "{input.featurexmls}",
"out": "{output.consensusxml}",
"threads": "1"
})

FidoAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FidoAdapter",
"in": "{input.idxml}",
"out": "{output.idxml}",
"fido_executable": "/tools/Fido",
"fidocp_executable": "/tools/FidoChooseParameters",
"threads": "1"
})

FileConverterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FileConverter",
"in": "{input.mzml}",
"out": "{output.mzxml}",
"threads": "1"
})
    
FileFilterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FileFilter",
"in": "{input.featurexml}",
"out": "{output.featurexml}",
"threads": "1"
})
    
FileMergerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} FileMerger",
"in": "{input.featurexmls}",
"out": "{output.featurexml}",
"threads": "1"
})
    
HighResPrecursorMassCorrectorParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} HighResPrecursorMassCorrector",
"in": "{input.mzml}",
"out": "{output.mzml}",
"out_csv": "false",
"feature:in": "{input.featurexml}",
"threads": "1"
})

IDConflictResolverParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} IDConflictResolver",
"in": "{input.featurexml}",
"out": "{output.featurexml}",
"threads": "1"
})
    
IDFilterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} IDFilter",
"in": "{input.idxml}",
"out": "{output.idxml}",
"threads": "1"
})
    
IDMapperParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} IDMapper",
"id": "{input.idxml}",
"in": "{input.featurexml}",
"out": "{output}",
"threads": "1"
}) 
    
IDMergerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} IDMerger",
"in": "{input.idxmls}",
"out": "{output.idxml}",
"threads": "1"
})
    
IDPosteriorErrorProbabilityParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} IDPosteriorErrorProbability",
"in": "{input.idxml}",
"out": "{output.idxml}",
"threads": "1"
})

MapAlignerIdentificationParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} MapAlignerIdentification",
"in": "_true",
"out": "_true",
"reference:file": "_true",
"threads": "1"
})
    
MapAlignerPoseClusteringParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} MapAlignerPoseClustering",
"in": "_true",
"out": "{input.featurexmls}",
"threads": "1"
})
   
MultiplexResolverParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} MultiplexResolver",
"in": "{input.consensusxml}",
"out": "{output.consensusxml}",
"threads": "1"
})
    
MyriMatchAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} MyriMatchAdapter",
"in": "{input.mzml}",
"out": "{output.idxml}",
"database": "{input.fasta}",
"myrimatch_executable": "/tools/myrimatch",
"threads": "1"
})


MSGFPlusAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} MSGFPlusAdapter",
"in": "{input.mzml}",
"out": "{output.idxml}",
"mzid_out": "false",
"database": "{input.fasta}",
"executable": "/tools/MSGFPlus.jar",
"java_executable": "java",
"threads": "1"
})
 
PeptideIndexerParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} PeptideIndexer",
"in": "{input.idxml}",
"fasta": "{input.fasta}",
"out": "{output.idxml}",
"threads": "1"
})

ProteinQuantifierParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} ProteinQuantifier",
"in": "{input.idxml}",
"protein_groups": "{input.fido}",
"out": "{output.csv}",
"threads": "1"
})

TextExporterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} TextExporter",
"in": "{input.xml}",
"out": "{output.csv}",
"threads": "1"
})

XTandemAdapterParams = collections.OrderedDict({
"exe": "{DOCKER_CMD} XTandemAdapter",
"in": "{input.mzml}",
"out": "{output.idxml}",
"database": "{input.fasta}",
"xtandem_executable": "tandem.exe",
"threads": "1"
})
    
