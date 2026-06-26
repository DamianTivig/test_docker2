#!/bin/bash
set -e

USER_HOST="uie74356@10.198.127.171"

# Ask for the remote directory
DEFAULT_DIR="/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts"
read -r -p "Remote directory [$DEFAULT_DIR]: " REMOTE_DIR
REMOTE_DIR="${REMOTE_DIR:-$DEFAULT_DIR}"

# Ask for the CSH script name
read -r -p "Enter the .CSH script name to run (e.g. LOAD_NA_611.CSH): " CSH_FILE
if [[ -z "$CSH_FILE" ]]; then
  echo "ERROR: .CSH script name is required."
  exit 1
fi

# Ask for the LOG file name
read -r -p "Enter the .LOG file name (e.g. LOAD_NA_611_20.LOG): " LOG_FILE
if [[ -z "$LOG_FILE" ]]; then
  echo "ERROR: .LOG file name is required."
  exit 1
fi

# Simple unique screen session name
SCREEN_NAME="run_$(date +%Y%m%d_%H%M%S)"

echo ""
echo "========================================="
echo "  Directory : $REMOTE_DIR"
echo "  Script    : $CSH_FILE"
echo "  Log file  : $LOG_FILE"
echo "  Screen    : $SCREEN_NAME (detached)"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

echo "Starting job in a detached screen session on the remote server..."
ssh -o StrictHostKeyChecking=no "$USER_HOST" "\
  export TERM=xterm; \
  source ~/.bash_profile 2>/dev/null || source ~/.profile 2>/dev/null || true; \
  cd \"$REMOTE_DIR\" && \
  screen -dmS \"$SCREEN_NAME\" bash -lc '( tcsh \"./$CSH_FILE\" ) 2>&1 | tee \"$LOG_FILE\"' \
"

echo "Launched. The job will continue running on the server even if you disconnect."
echo "Log: $REMOTE_DIR/$LOG_FILE"
