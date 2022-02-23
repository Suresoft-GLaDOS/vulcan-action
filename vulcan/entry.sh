# /entry.sh
#!/bin/bash

if [ ! -f $GITHUB_WORKSPACE/vulcan_target/.vulcan.yml ]; then
  echo "Requires .vulcan.yml in your repository"
  exit 1
fi

source $GITHUB_WORKSPACE/vulcan/github_cli/config.sh
source $GITHUB_WORKSPACE/vulcan/github_cli/checkout.sh

source $GITHUB_WORKSPACE/vulcan/runner/run_fl.sh
source $GITHUB_WORKSPACE/vulcan/runner/run_apr.sh

source $GITHUB_WORKSPACE/vulcan/github_cli/auth.sh
source $GITHUB_WORKSPACE/vulcan/github_cli/create-issue.sh
