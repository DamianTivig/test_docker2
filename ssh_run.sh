#!/bin/bash
set -e

# Remote SSH target
USER_HOST="uie74356@10.198.127.171"

# Default remote directory
DEFAULT_DIR="/PROJ/db4/db/RDF/NA/2026Q1_SeSp/2025R4_RDF_North_America_251H0/611/Scripts"
read -r -p "Remote directory [$DEFAULT_DIR]: " REMOTE_DIR
REMOTE_DIR="${REMOTE_DIR:-$DEFAULT_DIR}"

# CSH file to run
read -r -p "Enter the .CSH script name to run (e.g. LOAD_NA_611.CSH): " CSH_FILE
if [[ -z "$CSH_FILE" ]]; then
  echo "ERROR: .CSH script name is required."
  exit 1
fi

# Log filename
read -r -p "Enter the .LOG file name (e.g. LOAD_NA_611_20.LOG): " LOG_FILE
if [[ -z "$LOG_FILE" ]]; then
  echo "ERROR: .LOG file name is required."
  exit 1
fi

# Screen session name (default: CSH base name)
DEFAULT_SESSION="${CSH_FILE%.*}"
read -r -p "Screen session name [$DEFAULT_SESSION]: " SCREEN_NAME
SCREEN_NAME="${SCREEN_NAME:-$DEFAULT_SESSION}"

echo ""
echo "========================================="
echo "  Directory : $REMOTE_DIR"
echo "  Script    : $CSH_FILE"
echo "  Log file  : $LOG_FILE"
echo "  Screen    : $SCREEN_NAME"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

echo ""
echo "Connecting to server..."
echo "The screen session will start, then you stay connected."
echo ""
echo "  Ctrl+A, D  = detach from screen (keeps it running)"
echo "  screen -r $SCREEN_NAME = reattach later"
echo "  exit       = leave the server"
echo ""

ssh -t -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=5 \
    "$USER_HOST" "
export TERM=xterm

cd '$REMOTE_DIR' || { echo 'ERROR: Cannot cd to $REMOTE_DIR'; exit 1; }

# Ensure the CSH script is executable
chmod +x '$CSH_FILE' 2>/dev/null || true

# If a session with the same name already exists, warn
if screen -list 2>/dev/null | grep -q '\\.$SCREEN_NAME[[:space:]]'; then
  echo ''
  echo 'WARNING: Screen session $SCREEN_NAME already exists!'
  screen -ls 2>/dev/null
  echo ''
  echo 'Choose:'
  echo '  1) Attach to existing session'
  echo '  2) Create new session with timestamp'
  echo '  3) Cancel'
  printf 'Choice [1/2/3]: '
  read choice
  case \"\$choice\" in
    1)
      echo 'Attaching to existing session...'
      exec screen -r '$SCREEN_NAME'
      ;;
    2)
      SCREEN_NAME='${SCREEN_NAME}_\$(date +%Y%m%d_%H%M%S)'
      echo \"Using new session name: \$SCREEN_NAME\"
      ;;
    *)
      echo 'Cancelled.'
      exit 0
      ;;
  esac
fi

# Create screen config for logging
CFG=\$(mktemp /tmp/screen_cfg.XXXXXX)
cat > \"\$CFG\" <<SCRCFG
startup_message off
deflog on
logfile $REMOTE_DIR/$LOG_FILE
logfile flush 5
SCRCFG

# Start the detached screen session
screen -dmS \"\${SCREEN_NAME:-$SCREEN_NAME}\" -c \"\$CFG\" -L tcsh -c 'cd $REMOTE_DIR && ./$CSH_FILE'

sleep 1
rm -f \"\$CFG\"

echo ''
echo '========================================='
echo '  Screen session started!'
echo '========================================='
echo '  Session : '\"\${SCREEN_NAME:-$SCREEN_NAME}\"
echo '  Log     : $REMOTE_DIR/$LOG_FILE'
echo '========================================='
echo ''
screen -ls 2>/dev/null
echo ''
echo 'Choose:'
echo '  1) Attach to screen now (Ctrl+A, D to detach later)'
echo '  2) Stay on server shell (attach later with: screen -r '\"\${SCREEN_NAME:-$SCREEN_NAME}\"')'
echo '  3) Disconnect from server'
printf 'Choice [1/2/3]: '
read choice
case \"\$choice\" in
  1)
    echo 'Attaching to screen...'
    screen -r \"\${SCREEN_NAME:-$SCREEN_NAME}\"
    echo ''
    echo 'Detached from screen. You are still on the server.'
    echo 'Type exit to disconnect, or screen -r to reattach.'
    exec bash -l
    ;;
  2)
    echo ''
    echo 'You are on the server. The script is running in screen.'
    echo 'Useful commands:'
    echo '  screen -r \"\${SCREEN_NAME:-$SCREEN_NAME}\"   # attach'
    echo '  screen -ls                          # list sessions'
    echo '  tail -f $LOG_FILE                   # watch log'
    echo '  exit                                # disconnect'
    echo ''
    exec bash -l
    ;;
  3)
    echo 'Disconnecting. Screen keeps running.'
    exit 0
    ;;
esac
"

echo ""
echo "Disconnected from server."
echo "Screen session '$SCREEN_NAME' is still running remotely."
echo "Log: $REMOTE_DIR/$LOG_FILE"
