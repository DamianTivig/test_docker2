#!/bin/bash
set -e

echo "Connecting to server..."

ssh -tt -o StrictHostKeyChecking=no uie74356@10.198.127.171 "\
export TERM=xterm && \
source ~/.bash_profile 2>/dev/null || source ~/.profile 2>/dev/null || true && \
cd /PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts/ && \
tcsh -c './LOAD_NA_611.CSH |& tee LOAD_NA_611_20.LOG'
"
``
