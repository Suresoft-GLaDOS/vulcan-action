# /entry.sh
#!/bin/bash

source $GITHUB_ACTION_PATH/vulcan/git/config.sh
source $GITHUB_ACTION_PATH/vulcan/git/checkout.sh

if [ $RUN_FL ]; then
	python3 $GITHUB_ACTION_PATH/vulcan/util/testrun.py
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
