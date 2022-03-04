# vulcan/runner/run_apr.sh
#!/bin/bash

cd $VULCAN_TARGET

echo "Run VULCAN_YML_TEST_BUILD_COMMAND"
# sh -c "$VULCAN_YML_TEST_BUILD_COMMAND"

echo "Run VULCAN_YML_TEST_COMMAND"
# sh -c "$VULCAN_YML_TEST_COMMAND"

$GITHUB_ACTION_PATH/vulcan/bin/msv
