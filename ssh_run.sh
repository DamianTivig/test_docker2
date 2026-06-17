#!/bin/bash
set -e

echo "Connecting to server..."

ssh -o StrictHostKeyChecking=no uie74356@10.198.127.171 "\
cd /PROJ/db4/db/RDF/EU/2026Q1_new_server_SESP/EEU/2026R4_RDF_Europe_east_261H1/611/Scripts/ && \
./LOAD_EEU_611.CSH |& tee LOAD_EEU_611_20.LOG
"
``
