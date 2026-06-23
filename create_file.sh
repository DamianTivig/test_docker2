#!/bin/bash

set -e

# Ask user for input
read -p "Enter BASE path: " BASE
read -p "Enter DELIVERY name: " DELIVERY
read -p "Enter VERSION: " VERSION

echo "Connecting to server..."

ssh -tt -o StrictHostKeyChecking=no uie74356@10.198.127.171 "\
export TERM=xterm && \
BASE='$BASE' && \
DELIVERY='$DELIVERY' && \
VERSION='$VERSION' && \

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

echo '✅ Directory structure created successfully'
"
