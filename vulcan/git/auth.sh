# vulcan/github_cli/auth.sh
#!/bin/bash

echo ==========gh auth login==========
echo $TOKEN > /token
gh auth login --with-token < /token
gh auth status
echo ==================================