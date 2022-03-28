# /entry.sh
#!/bin/bash

VULCAN_TARGET_NAME=$VULCAN_TARGET
VULCAN_TARGET=$GITHUB_WORKSPACE/$VULCAN_TARGET
VULCAN_YML_PATH=$VULCAN_TARGET/vulcan.yml
VULCAN_SUFFIX="$(date +%s%N)"
VULCAN_OUTPUT_DIR=$GITHUB_WORKSPACE/../../output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX

if [ ! -f $VULCAN_YML_PATH ]; then
  echo "Requires vulcan.yml in your repository"
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
	source $GITHUB_ACTION_PATH/vulcan/util/test.sh
	source $GITHUB_ACTION_PATH/vulcan/runner/run_fl.sh
fi
if [ $RUN_APR ]; then
	source $GITHUB_ACTION_PATH/vulcan/runner/run_apr.sh
fi

source $GITHUB_ACTION_PATH/vulcan/git/auth.sh

if [ -f $PATCH_OUTPUT_PATH/*-0001-*.diff ] && [ ! -f $PATCH_OUTPUT_PATH/*-0002-*.diff ];
then
	source $GITHUB_ACTION_PATH/vulcan/git/create-pull-request.sh
else
	source $GITHUB_ACTION_PATH/vulcan/git/create-issue.sh
fi
