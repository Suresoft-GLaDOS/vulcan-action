# vulcan/github_cli/auth.sh
#!/bin/bash

echo ==========gh auth login==========
echo $TOKEN > $GITHUB_ACTION_PATH/token
gh auth login --with-token < $GITHUB_ACTION_PATH/token
gh auth status
rm $GITHUB_ACTION_PATH/token
echo ==================================