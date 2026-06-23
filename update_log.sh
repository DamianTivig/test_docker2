#!/bin/bash

SSH_TARGET="uie74356@10.198.127.171"
REMOTE_CFG="$1"        # <-- path comes from keyboard
LOCAL_FILE="config_vars.txt"

# Check if argument was provided
if [ -z "$REMOTE_CFG" ]; then
    exit 1
fi

ssh ${SSH_TARGET} bash -s <<EOF

CFG_FILE="$REMOTE_CFG"

while IFS='=' read -r key value; do
    [ -z "\$key" ] && continue
    sed -i "s|^\${key}=.*|\${key}=\${value}|" "\$CFG_FILE"
done

EOF < "$LOCAL_FILE"

echo "Variables updated in $REMOTE_CFG"
