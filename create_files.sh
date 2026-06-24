#!/bin/bash

set -e

# Ask user for input
read -p "Enter BASE path: " BASE
read -p "Enter DELIVERY name: " DELIVERY
read -p "Enter VERSION: " VERSION

echo "Connecting to server..."

# Step 1: Create directory structure
ssh -o StrictHostKeyChecking=no uie74356@10.198.127.171 "
export TERM=xterm
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Scripts
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Tests/RDF
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Tests/SIZE
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Tests/SVF
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Tests/UT
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/Tests/load
mkdir -p ${BASE}/${DELIVERY}/${VERSION}/patches
echo 'Directory structure created.'
"

# Step 2: Copy generate_files.py to remote Scripts directory
scp -o StrictHostKeyChecking=no generate_files.py uie74356@10.198.127.171:${BASE}/${DELIVERY}/${VERSION}/Scripts/generate_files.py

# Step 3: Run it remotely
ssh -o StrictHostKeyChecking=no uie74356@10.198.127.171 "
export TERM=xterm
cd ${BASE}/${DELIVERY}/${VERSION}/Scripts
python3 generate_files.py
echo '========================================='
echo 'Files generated in Scripts:'
ls -la
echo '========================================='
echo 'Full tree:'
cd ${BASE}/${DELIVERY}/${VERSION}
find . -type f
echo '========================================='
echo 'DONE'
"

echo "All done!"
