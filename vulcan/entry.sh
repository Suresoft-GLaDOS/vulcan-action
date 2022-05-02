# /entry.sh
#!/bin/bash

# exist dependency
if [ ! -f $GITHUB_ACTION_PATH/yq ]; then
	wget -q https://github.com/mikefarah/yq/releases/download/v4.20.2/yq_linux_386 -O $GITHUB_ACTION_PATH/yq && chmod +x $GITHUB_ACTION_PATH/yq
fi
if [ ! -f $GITHUB_ACTION_PATH/jq ]; then
	wget -q https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux32 -O $GITHUB_ACTION_PATH/jq && chmod +x $GITHUB_ACTION_PATH/jq
fi

if [ ! -d $GITHUB_WORKSPACE/../../output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX ]; then
	mkdir -p $GITHUB_WORKSPACE/../../output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX
fi

set -a
VULCAN_TARGET_NAME=$VULCAN_TARGET
VULCAN_TARGET=$GITHUB_WORKSPACE/$VULCAN_TARGET
VULCAN_YML_PATH=$VULCAN_TARGET/vulcan.yml
VULCAN_SUFFIX="$(date +%s%N)"
VULCAN_OUTPUT_DIR=$(realpath $GITHUB_WORKSPACE/../../output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX)
VULCAN_PLAUSIBLE_COUNT=0
set +a

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
if [ 0 -lt $VULCAN_PLAUSIBLE_COUNT ]; then
	source $GITHUB_ACTION_PATH/vulcan/runner/run_cxbuild.sh
fi

source $GITHUB_ACTION_PATH/vulcan/git/auth.sh

cd $VULCAN_TARGET
source $GITHUB_ACTION_PATH/vulcan/git/create-issue.sh
python3 $GITHUB_ACTION_PATH/vulcan/git/create-pull-request.py
