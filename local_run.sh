#!/bin/bash
set -e

# Ask for the local directory
DEFAULT_DIR="./Scripts"
read -r -p "Local directory (default: $DEFAULT_DIR): " LOCAL_DIR
LOCAL_DIR="${LOCAL_DIR:-$DEFAULT_DIR}"

# Ask for the CSH script name
read -r -p "Enter the .CSH script name to run (e.g., LOAD_NA_611.CSH): " CSH_FILE
if [[ -z "$CSH_FILE" ]]; then
  echo "ERROR: .CSH script name is required."
  exit 1
fi

# Ask for the LOG file name
read -r -p "Enter the .LOG file name (e.g., LOAD_NA_611_20.LOG): " LOG_FILE
if [[ -z "$LOG_FILE" ]]; then
  echo "ERROR: .LOG file name is required."
  exit 1
fi

echo ""
echo "========================================="
echo "  Directory : $LOCAL_DIR"
echo "  Script    : $CSH_FILE"
echo "  Log file  : $LOG_FILE"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

# Run the .CSH script locally and capture output to the log file
echo "Running the script locally..."
(
  export TERM=xterm

  # Switch to the local directory
  cd "$LOCAL_DIR" || { echo "ERROR: Directory '$LOCAL_DIR' does not exist."; exit 1; }

  # Check if the script exists
  if [[ ! -f "$CSH_FILE" ]]; then
    echo "ERROR: Script '$CSH_FILE' not found in directory '$LOCAL_DIR'."
    exit 1
  fi
  
  # Run the script using `tcsh` and log the output
  tcsh -c "./$CSH_FILE |& tee $LOG_FILE"
)

echo ""
echo "========================================="
echo "Process completed."
echo "Log file saved to: $LOCAL_DIR/$LOG_FILE"
echo "========================================="
