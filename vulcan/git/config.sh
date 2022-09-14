# vulcan/github_cli/auth.sh
#!/bin/bash

git config --global --add safe.directory $VULCAN_TARGET
git config --global user.email "vulcan@action"
git config --global user.name "vulcan-action"