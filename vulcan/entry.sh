# /entry.sh
#!/bin/bash

echo "[DEBUG] GITHUB_ACTION_PATH: $GITHUB_ACTION_PATH"

source $GITHUB_ACTION_PATH/vulcan/git/config.sh
source $GITHUB_ACTION_PATH/vulcan/git/checkout.sh
source $GITHUB_ACTION_PATH/vulcan/git/auth.sh

python3 $GITHUB_ACTION_PATH/vulcan/runner/runner.py
