# /entry.sh
#!/bin/bash

if [ ! -f $GITHUB_WORKSPACE/vulcan_target/.vulcan.yml ]; then
  echo "Requires .vulcan.yml in your repository"
  exit 1
fi

if [ -z "$TOKEN" ]; then
  echo "Requires vulcan action input: token"
  echo "Vulcan action with: token: ${{ secrets.GITHUB_TOKEN }}"
  exit 1
fi

source $GITHUB_ACTION_PATH/vulcan/yaml/config.sh

source $GITHUB_ACTION_PATH/vulcan/git/config.sh
source $GITHUB_ACTION_PATH/vulcan/git/checkout.sh

if [ $RUN_FL ]; then
	source $GITHUB_ACTION_PATH/vulcan/runner/run_fl.sh
fi
if [ $RUN_APR ]; then
	source $GITHUB_ACTION_PATH/vulcan/runner/run_apr.sh
fi

source $GITHUB_ACTION_PATH/vulcan/git/auth.sh
# source $GITHUB_ACTION_PATH/vulcan/git/create-pull-request.sh
source $GITHUB_ACTION_PATH/vulcan/git/create-issue.sh
