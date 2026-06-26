#!/bin/bash
# ============================================================
# update_flags_remote.sh
# Updates LOAD_CFG_NA.cfg on a remote SSH server using vars
# from a local config_vars.txt file.
#
# Usage:
#   ./update_flags_remote.sh <config_vars.txt> <remote_user> <remote_host> <remote_load_cfg_path>
#
# Example:
#   ./update_flags_remote.sh config_vars.txt uie74356 10.198.127.171 /PROJ/db4/db/RDF/NA/LOAD_CFG_NA.cfg
#
# What it does:
#   1. Sends config_vars.txt + update_flags.sh to the server.
#   2. Runs update_flags.sh remotely.
#   3. Cleanup temporary files on the server.
# ============================================================

set -e

# Argument check
if [ $# -lt 4 ]; then
    echo "Usage: $0 <config_vars.txt> <remote_user> <remote_host> <remote_path_to_load_cfg>"
    echo "Example: $0 config_vars.txt uie74356 10.198.127.171 /PROJ/db4/db/RDF/NA/LOAD_CFG_NA.cfg"
    exit 1
fi

CONFIG_VARS_FILE="$1"
REMOTE_USER="$2"
REMOTE_HOST="$3"
REMOTE_LOAD_CFG_PATH="$4"

if [ ! -f "$CONFIG_VARS_FILE" ]; then
    echo "ERROR: Config vars file not found: $CONFIG_VARS_FILE"
    exit 1
fi

# Define paths for remote temporary files
REMOTE_DIR=$(dirname "$REMOTE_LOAD_CFG_PATH")
REMOTE_CONFIG_VARS="${REMOTE_DIR}/config_vars.txt"
REMOTE_SCRIPT="${REMOTE_DIR}/update_flags.sh"

echo "========================================="
echo "Config vars file  : $CONFIG_VARS_FILE"
echo "Remote user       : $REMOTE_USER"
echo "Remote host       : $REMOTE_HOST"
echo "Remote LOAD_CFG_NA: $REMOTE_LOAD_CFG_PATH"
echo "========================================="

# Step 1: Upload config_vars.txt and update_flags.sh
echo "Uploading config_vars.txt and update_flags.sh to the remote server..."
scp -o StrictHostKeyChecking=no "$CONFIG_VARS_FILE" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_CONFIG_VARS}"
scp -o StrictHostKeyChecking=no update_flags.sh "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_SCRIPT}"

# Step 2: Run the script remotely
echo "Running the update_flags.sh script on the remote server..."
ssh -o StrictHostKeyChecking=no "${REMOTE_USER}@${REMOTE_HOST}" "
chmod +x ${REMOTE_SCRIPT} && \
${REMOTE_SCRIPT} ${REMOTE_CONFIG_VARS} ${REMOTE_LOAD_CFG_PATH}
"

# Step 3: Cleanup remote temporary files
echo "Cleaning up temporary files on the remote server..."
ssh -o StrictHostKeyChecking=no "${REMOTE_USER}@${REMOTE_HOST}" "
rm -f ${REMOTE_CONFIG_VARS} ${REMOTE_SCRIPT}
"

echo ""
echo "========================================="
echo "Done! LOAD_CFG_NA.cfg has been updated on the remote server."
echo "========================================="
