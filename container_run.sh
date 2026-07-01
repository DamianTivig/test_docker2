#!/bin/bash
set -euo pipefail

# =============================================
# DEFAULTS
# =============================================
DEFAULT_IMAGE_NAME="rockylinux-tcsh:8"
DEFAULT_CONTAINER_NAME="rdf-runner"
DEFAULT_CONTAINER_WORKDIR="/home/devuser/env"
DEFAULT_LOCAL_DIR="./local_env"

# =============================================
# USER INPUT
# =============================================
read -r -p "Docker image name (default: ${DEFAULT_IMAGE_NAME}): " IMAGE_NAME
IMAGE_NAME="${IMAGE_NAME:-${DEFAULT_IMAGE_NAME}}"

read -r -p "Container name (default: ${DEFAULT_CONTAINER_NAME}): " CONTAINER_NAME
CONTAINER_NAME="${CONTAINER_NAME:-${DEFAULT_CONTAINER_NAME}}"

read -r -p "Container working directory (default: ${DEFAULT_CONTAINER_WORKDIR}): " CONTAINER_WORKDIR
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-${DEFAULT_CONTAINER_WORKDIR}}"

read -r -p "Local directory to mount (default: ${DEFAULT_LOCAL_DIR}): " LOCAL_DIR
LOCAL_DIR="${LOCAL_DIR:-${DEFAULT_LOCAL_DIR}}"

# Resolve to absolute path
if [[ ! -d "$LOCAL_DIR" ]]; then
  echo "ERROR: Directory '${LOCAL_DIR}' does not exist."
  exit 1
fi
LOCAL_DIR="$(cd "$LOCAL_DIR" && pwd)"

read -r -p "Enter the .CSH script name to run (e.g., LOAD_NA_617.CSH): " CSH_FILE
if [[ -z "$CSH_FILE" ]]; then
  echo "ERROR: .CSH script name is required."
  exit 1
fi

read -r -p "Enter the .LOG file name (e.g., LOAD_NA_617_01.LOG): " LOG_FILE
if [[ -z "$LOG_FILE" ]]; then
  echo "ERROR: .LOG file name is required."
  exit 1
fi

echo ""
echo "========================================="
echo "  Image          : ${IMAGE_NAME}"
echo "  Container      : ${CONTAINER_NAME}"
echo "  Container Dir  : ${CONTAINER_WORKDIR}"
echo "  Local Dir      : ${LOCAL_DIR}"
echo "  Script         : ${CSH_FILE}"
echo "  Log file       : ${LOG_FILE}"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

# =============================================
# STEP 1: Check if image exists, build if not
# =============================================
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
  echo ""
  echo "Image '${IMAGE_NAME}' not found. Building..."
  docker build -t "${IMAGE_NAME}" .
fi

# =============================================
# STEP 2: Stop/remove old container if running
# =============================================
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing old container '${CONTAINER_NAME}'..."
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1
fi

# =============================================
# STEP 3: Run the script inside the container
# =============================================
echo ""
echo "Starting container and running script..."
echo "========================================="

docker run \
  --name "${CONTAINER_NAME}" \
  --rm \
  -v "${LOCAL_DIR}:${CONTAINER_WORKDIR}" \
  -w "${CONTAINER_WORKDIR}/Scripts" \
  "${IMAGE_NAME}" \
  /bin/bash -c "
    set -e

    echo '--- Inside container ---'
    echo \"Hostname: \$(hostname)\"
    echo \"OS: \$(cat /etc/redhat-release)\"
    echo \"User: \$(whoami)\"
    echo \"Working dir: \$(pwd)\"
    echo ''

    # Fix line endings on all scripts
    find . -type f \( -name '*.CSH' -o -name '*.csh' -o -name '*.cfg' -o -name '*.pl' -o -name '*.sql' -o -name '*.sh' \) -exec dos2unix -q {} + 2>/dev/null || true

    # Make all scripts executable
    find . -type f \( -name '*.CSH' -o -name '*.csh' -o -name '*.pl' -o -name '*.sh' \) -exec chmod +x {} +

    # Also fix Tests scripts
    if [ -d '../Tests' ]; then
      find ../Tests -type f \( -name '*.csh' -o -name '*.CSH' -o -name '*.pl' -o -name '*.sh' -o -name '*.sql' \) -exec dos2unix -q {} + 2>/dev/null || true
      find ../Tests -type f \( -name '*.csh' -o -name '*.CSH' -o -name '*.pl' -o -name '*.sh' \) -exec chmod +x {} +
    fi

    # Check script exists
    if [ ! -f '${CSH_FILE}' ]; then
      echo 'ERROR: Script ${CSH_FILE} not found in container.'
      echo 'Available scripts:'
      ls -la *.CSH *.csh 2>/dev/null || echo '  (none found)'
      exit 1
    fi

    echo 'Available scripts in Scripts/:'
    ls -la *.CSH *.csh *.cfg 2>/dev/null || true
    echo ''
    echo '========================================='
    echo 'Running: ${CSH_FILE}'
    echo '========================================='
    echo ''

    # Run with tcsh, log output
    tcsh ./${CSH_FILE} 2>&1 | tee ${LOG_FILE}

    echo ''
    echo '========================================='
    echo 'Script finished.'
    echo '========================================='
  "

echo ""
echo "========================================="
echo "Container execution completed."
echo "Log file: ${LOCAL_DIR}/Scripts/${LOG_FILE}"
echo "========================================="
