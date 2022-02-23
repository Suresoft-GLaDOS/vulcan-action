# vulcan/github_cli/auth.sh
#!/bin/bash

echo ==========gh auth login==========
gh auth login --with-token < $GITHUB_ACTION_PATH/token
gh auth status
echo ==================================