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

# =============================================
# Detect container runtime
# =============================================
if command -v docker >/dev/null 2>&1; then
  RUNTIME="docker"
elif command -v podman >/dev/null 2>&1; then
  RUNTIME="podman"
else
  RUNTIME="none"
fi

echo ""
echo "========================================="
echo "  Image          : ${IMAGE_NAME}"
echo "  Container      : ${CONTAINER_NAME}"
echo "  Container Dir  : ${CONTAINER_WORKDIR}"
echo "  Local Dir      : ${LOCAL_DIR}"
echo "  Script         : ${CSH_FILE}"
echo "  Log file       : ${LOG_FILE}"
echo "  Runtime        : ${RUNTIME}"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

# =============================================
# Common preparation function
# =============================================
prepare_scripts() {
  local work_dir="$1"

  echo "Fixing line endings and permissions..."

  # Fix line endings
  find "${work_dir}" -type f \( -name '*.CSH' -o -name '*.csh' -o -name '*.cfg' -o -name '*.pl' -o -name '*.sql' -o -name '*.sh' \) -exec dos2unix -q {} + 2>/dev/null || true

  # Make scripts executable
  find "${work_dir}" -type f \( -name '*.CSH' -o -name '*.csh' -o -name '*.pl' -o -name '*.sh' \) -exec chmod +x {} +

  # Also fix Tests directory if it exists
  local tests_dir
  tests_dir="$(dirname "${work_dir}")/Tests"
  if [ -d "${tests_dir}" ]; then
    find "${tests_dir}" -type f \( -name '*.csh' -o -name '*.CSH' -o -name '*.pl' -o -name '*.sh' -o -name '*.sql' \) -exec dos2unix -q {} + 2>/dev/null || true
    find "${tests_dir}" -type f \( -name '*.csh' -o -name '*.CSH' -o -name '*.pl' -o -name '*.sh' \) -exec chmod +x {} +
  fi
}

# =============================================
# Run based on available runtime
# =============================================
if [[ "${RUNTIME}" == "none" ]]; then
  # =========================================
  # No Docker/Podman — run directly
  # =========================================
  echo ""
  echo "========================================="
  echo "No container runtime found."
  echo "Running script directly in this environment..."
  echo "========================================="

  # Check tcsh is available
  if ! command -v tcsh >/dev/null 2>&1; then
    echo "ERROR: tcsh not found. Install it with: dnf install -y tcsh"
    exit 1
  fi

  # Check dos2unix is available
  if ! command -v dos2unix >/dev/null 2>&1; then
    echo "WARNING: dos2unix not found, skipping line-ending fixes."
  fi

  SCRIPTS_DIR="${LOCAL_DIR}"

  echo ""
  echo "--- Environment info ---"
  echo "Hostname: $(hostname)"
  echo "OS: $(cat /etc/redhat-release 2>/dev/null || echo 'unknown')"
  echo "User: $(whoami)"
  echo "Working dir: ${SCRIPTS_DIR}"
  echo ""

  # Prepare scripts
  prepare_scripts "${SCRIPTS_DIR}"

  # Check the script exists
  if [[ ! -f "${SCRIPTS_DIR}/${CSH_FILE}" ]]; then
    echo "ERROR: Script '${CSH_FILE}' not found in ${SCRIPTS_DIR}"
    echo "Available scripts:"
    ls -la "${SCRIPTS_DIR}"/*.CSH "${SCRIPTS_DIR}"/*.csh 2>/dev/null || echo "  (none found)"
    exit 1
  fi

  echo "Available scripts in ${SCRIPTS_DIR}/:"
  ls -la "${SCRIPTS_DIR}"/*.CSH "${SCRIPTS_DIR}"/*.csh "${SCRIPTS_DIR}"/*.cfg 2>/dev/null || true
  echo ""
  echo "========================================="
  echo "Running: ${CSH_FILE}"
  echo "========================================="
  echo ""

  # Run the script
  cd "${SCRIPTS_DIR}"
  tcsh "./${CSH_FILE}" 2>&1 | tee "${LOG_FILE}"

  echo ""
  echo "========================================="
  echo "Script finished."
  echo "Log file: ${SCRIPTS_DIR}/${LOG_FILE}"
  echo "========================================="

else
  # =========================================
  # Docker or Podman available
  # =========================================
  echo ""
  echo "========================================="
  echo "Using runtime: ${RUNTIME}"
  echo "========================================="

  # Check image exists, build if not
  if ! ${RUNTIME} image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Image '${IMAGE_NAME}' not found. Building..."
    ${RUNTIME} build -t "${IMAGE_NAME}" .
  else
    echo "Image '${IMAGE_NAME}' found."
  fi

  # Remove old container if present
  if ${RUNTIME} ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Removing old container '${CONTAINER_NAME}'..."
    ${RUNTIME} rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
  fi

  echo ""
  echo "Starting container and running script..."
  echo "========================================="

  ${RUNTIME} run \
    --name "${CONTAINER_NAME}" \
    --rm \
    -v "${LOCAL_DIR}:${CONTAINER_WORKDIR}" \
    -w "${CONTAINER_WORKDIR}/Scripts" \
    "${IMAGE_NAME}" \
    /bin/bash -c "
      set -e

      echo '--- Inside container ---'
      echo \"Hostname: \$(hostname)\"
      echo \"OS: \$(cat /etc/redhat-release 2>/dev/null || echo 'unknown')\"
      echo \"User: \$(whoami)\"
      echo \"Working dir: \$(pwd)\"
      echo ''

      # Fix line endings
      find . -type f \( -name '*.CSH' -o -name '*.csh' -o -name '*.cfg' -o -name '*.pl' -o -name '*.sql' -o -name '*.sh' \) -exec dos2unix -q {} + 2>/dev/null || true

      # Make scripts executable
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

      tcsh ./${CSH_FILE} 2>&1 | tee ${LOG_FILE}

      echo ''
      echo '========================================='
      echo 'Script finished.'
      echo '========================================='
    "

  echo ""
  echo "========================================="
  echo "Container execution completed."
  echo "Log file: ${LOCAL_DIR}/${LOG_FILE}"
  echo "========================================="
fi
modify this so it can find the file and run the compiler
