#!/bin/bash

set -e

echo "Connecting to server..."

ssh -tt -o StrictHostKeyChecking=no uie74356@10.226.131.21 "\
export TERM=xterm && \
BASE='/db4/db/RDF/NA/2025Q1' && \
DELIVERY='2024R4_RDF_North_America_241H0' && \
VERSION='510' && \

echo 'Creating folder structure...' && \

mkdir -p \$BASE/\$DELIVERY/\$VERSION && \
cd \$BASE/\$DELIVERY/\$VERSION || exit 1 && \

mkdir -p Scripts && \
mkdir -p Tests/RDF && \
mkdir -p Tests/SIZE && \
mkdir -p Tests/SVF && \
mkdir -p Tests/UT && \
mkdir -p Tests/load && \
mkdir -p patches && \

touch Tests/RDF/AbakusRDF.csh && \
touch Tests/SIZE/drop_users.sql && \
touch Tests/SIZE/space_calculate.sql && \
touch Tests/SVF/AbakusSVF.csh && \
touch Tests/UT/runUT && \
touch Tests/load/allfiles && \
touch Tests/load/rdfdeploy && \

echo 'Structure created successfully'
"