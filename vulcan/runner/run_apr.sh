# vulcan/runner/run_apr.sh
#!/bin/bash

cd $GITHUB_WORKSPACE/vulcan_target

# $(sh -c "$(printf "$VULCAN_YML_TEST_BUILD_COMMAND")")
# $(sh -c "$(printf "$VULCAN_YML_TEST_COMMAND")")

$GITHUB_ACTION_PATH/vulcan/bin/msv
