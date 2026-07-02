#!/bin/bash
set -euo pipefail

# =============================================
# DEFAULTS
# =============================================
DEFAULT_IMAGE_NAME="rockylinux-tcsh:8"
DEFAULT_CONTAINER_NAME="rdf-runner"
DEFAULT_CONTAINER_WORKDIR="/home/devuser/env"
DEFAULT_LOCAL_DIR="./newDel"

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
    echo "ERROR: Directory '$LOCAL_DIR' does not exist."
    exit 1
fi

LOCAL_DIR="$(cd "$LOCAL_DIR" && pwd)"

read -r -p "Enter the .CSH script name: " CSH_FILE
[[ -z "$CSH_FILE" ]] && {
    echo "ERROR: Script name required."
    exit 1
}

read -r -p "Enter the .LOG file name: " LOG_FILE
[[ -z "$LOG_FILE" ]] && {
    echo "ERROR: Log file name required."
    exit 1
}

# =============================================
# FIND SCRIPT
# =============================================
SCRIPT_PATH="$(find "${LOCAL_DIR}" -type f -name "${CSH_FILE}" | head -1)"

if [[ -z "${SCRIPT_PATH}" ]]; then
    echo "ERROR: Could not locate ${CSH_FILE}"
    exit 1
fi

SCRIPT_DIR="$(dirname "${SCRIPT_PATH}")"

# =============================================
# DETERMINE PROJECT ROOT
# =============================================
PROJECT_ROOT="$(pwd)"

# =============================================
# DETECT RUNTIME
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
echo "Image          : ${IMAGE_NAME}"
echo "Container      : ${CONTAINER_NAME}"
echo "Container Dir  : ${CONTAINER_WORKDIR}"
echo "Local Dir      : ${LOCAL_DIR}"
echo "Project Root   : ${PROJECT_ROOT}"
echo "Script         : ${SCRIPT_PATH}"
echo "Log File       : ${LOG_FILE}"
echo "Runtime        : ${RUNTIME}"
echo "========================================="
echo ""

read -r -p "Proceed? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

# =============================================
# PREPARE FILES
# =============================================
prepare_scripts() {

    local work_dir="$1"

    echo "Fixing line endings..."

    find "${work_dir}" \
        -type f \
        \( \
        -name '*.CSH' -o \
        -name '*.csh' -o \
        -name '*.cfg' -o \
        -name '*.pl' -o \
        -name '*.sql' -o \
        -name '*.sh' \
        \) \
        -exec dos2unix -q {} + 2>/dev/null || true

    echo "Setting executable permissions..."

    find "${work_dir}" \
        -type f \
        \( \
        -name '*.CSH' -o \
        -name '*.csh' -o \
        -name '*.pl' -o \
        -name '*.sh' \
        \) \
        -exec chmod +x {} +

    echo "Done."
}

# =============================================
# DIRECT EXECUTION
# =============================================
if [[ "${RUNTIME}" == "none" ]]; then

    echo ""
    echo "Running without Docker/Podman..."
    echo ""

    command -v tcsh >/dev/null 2>&1 || {
        echo "ERROR: tcsh not installed."
        exit 1
    }

    prepare_scripts "${LOCAL_DIR}"

    OLD_COMPILER="$(find "${LOCAL_DIR}" -type d -name compiler 2>/dev/null | head -1 || true)"

    if [[ -n "${OLD_COMPILER}" ]]; then
        echo "Removing stale compiler directory:"
        echo "${OLD_COMPILER}"
        rm -rf "${OLD_COMPILER}"
    fi

    echo ""
    echo "--- Environment ---"
    echo "PWD       : ${PROJECT_ROOT}"
    echo "Script    : ${SCRIPT_PATH}"
    echo "User      : $(whoami)"
    echo "Hostname  : $(hostname)"
    echo ""

    cd "${PROJECT_ROOT}"

    tcsh "${SCRIPT_PATH}" 2>&1 | tee "${LOG_FILE}"

    echo ""
    echo "========================================="
    echo "Execution completed."
    echo "Log file: ${PROJECT_ROOT}/${LOG_FILE}"
    echo "========================================="

    exit 0
fi

# =============================================
# CONTAINER EXECUTION
# =============================================
echo ""
echo "Using runtime: ${RUNTIME}"
echo ""

if ! ${RUNTIME} image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Image not found. Building..."
    ${RUNTIME} build -t "${IMAGE_NAME}" .
fi

if ${RUNTIME} ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    ${RUNTIME} rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
fi

REL_SCRIPT="${SCRIPT_PATH#${LOCAL_DIR}/}"

${RUNTIME} run \
    --rm \
    --name "${CONTAINER_NAME}" \
    -v "${LOCAL_DIR}:${CONTAINER_WORKDIR}" \
    -w "${CONTAINER_WORKDIR}" \
    "${IMAGE_NAME}" \
    /bin/bash -c "
        set -e

        find . \
            -type f \
            \( \
            -name '*.CSH' -o \
            -name '*.csh' -o \
            -name '*.cfg' -o \
            -name '*.pl' -o \
            -name '*.sql' -o \
            -name '*.sh' \
            \) \
            -exec dos2unix -q {} + 2>/dev/null || true

        find . \
            -type f \
            \( \
            -name '*.CSH' -o \
            -name '*.csh' -o \
            -name '*.pl' -o \
            -name '*.sh' \
            \) \
            -exec chmod +x {} +

        OLD_COMPILER=\$(find . -type d -name compiler | head -1 || true)

        if [ -n \"\$OLD_COMPILER\" ]; then
            rm -rf \"\$OLD_COMPILER\"
        fi

        tcsh './${REL_SCRIPT}' 2>&1 | tee '${LOG_FILE}'
    "

echo ""
echo "========================================="
echo "Container execution completed."
echo "========================================="
