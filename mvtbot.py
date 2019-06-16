import argparse
import ogr
import osr
import subprocess
import sys
import json


def formatTilingScheme(extent): 
    return '{0},{1},{2}'.format(
        extent[0],
        extent[3],
        max([
            extent[2] - extent[0],
            extent[3] - extent[1],
        ])
    )


def boolToYesNo(v):
    if v:
        return 'YES'
    else:
        return 'NO'


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        stdout = process.stdout.read(1)
        if process.poll() is not None:
            break
        if stdout:
            sys.stdout.write(stdout.decode('utf-8'))
            sys.stdout.flush()

    exitcode = process.poll()
    return exitcode


def generateMVT(id, epsg, min_zoom, max_zoom, out_dir, input_file, compress=False, name="", attribution="", description=""):
    epsg = int(epsg)

    extent = getMaxExtent(
        input_file,
        epsg)
    print(extent)

    tiling_scheme = formatTilingScheme(extent)

    # Because I can't work out how to do this in python at the moment
    cmd = ['ogr2ogr',
        '-progress',
        '-f', 'MVT',
        '-t_srs', 'EPSG:{0}'.format(epsg), 
        '--debug', 'on',
        '-dsco', 'TILING_SCHEME=EPSG:{0},{1}'.format(epsg, tiling_scheme),
        '-dsco', 'MINZOOM={0}'.format(min_zoom),
        '-dsco', 'MAXZOOM={0}'.format(max_zoom),
        '-dsco', 'COMPRESS={0}'.format(boolToYesNo(compress)),
        out_dir,
        input_file,
    ]
    print('===========================')
    print(cmd)
    print('===========================')
    exitcode = run_command(cmd)
    return exitcode


def getMaxExtent(in_file, out_epsg):
    source_ds = ogr.Open(in_file)

    maxExtent = [];

    for featsClass_idx in range(source_ds.GetLayerCount()):
        inLayer = source_ds.GetLayerByIndex(featsClass_idx)
        print("processing {0}".format(inLayer.GetName()))

        # input SpatialReference
        inSpatialRef = inLayer.GetSpatialRef()

        # output SpatialReference
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(out_epsg)

        # create the CoordinateTransformation
        coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

        # loop through the input features
        inFeature = inLayer.GetNextFeature()
        featureCount = inLayer.GetFeatureCount()

        while inFeature:
            geom = inFeature.GetGeometryRef()
            geom.Transform(coordTrans)
            geomEnvelope = geom.GetEnvelope()
            geomExtent = [
                geomEnvelope[0],
                geomEnvelope[2],
                geomEnvelope[1],
                geomEnvelope[3],
            ]

            if len(maxExtent) < 1:
                maxExtent = geomExtent
            else:
                maxExtent = [
                    min(maxExtent[0], geomExtent[0]),
                    min(maxExtent[1], geomExtent[1]),
                    max(maxExtent[2], geomExtent[2]),
                    max(maxExtent[3], geomExtent[3]),
                ]

            inFeature = inLayer.GetNextFeature()

    return maxExtent


def run_cli(input_file):
    data = json.load(input_file)

    for task in data.get('tasks'):
        generateMVT(
            id=task.get('id'),
            epsg=task.get('epsg'),
            min_zoom=task.get('min_zoom'),
            max_zoom=task.get('max_zoom'),
            out_dir=task.get('out_dir'),
            input_file=task.get('input_file'),
            # optional
            name=task.get('name'),
            attribution=task.get('attribution'),
            description=task.get('description')
        )

parser = argparse.ArgumentParser(description='Convert sources to mapbox-vector-tiles with GDAL.')
parser.add_argument('definition_file',
    metavar='definition_file',
    type=argparse.FileType('r'), 
    help='input definition file'
)

args = parser.parse_args()
run_cli(args.definition_file)

