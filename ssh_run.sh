#!/bin/bash

set -e # Exit immediately if a command fails

echo "Connecting to remote server..."

ssh uie74356@10.198.127.171 

echo "Connected. Starting job..."

# Go to working directory
cd /PROJ/db4/db/RDF/EU/2026Q1_new_server_SESP/EEU/2026R4_RDF_Europe_east_261H1/611/Scripts/ || {
    echo "ERROR: Directory not found"
    exit 1
}

# Run script and log output
./LOAD_EEU_611.CSH |& tee LOAD_EEU_611_20.LOG

echo "Job finished."

EOF

echo "SSH session completed."
