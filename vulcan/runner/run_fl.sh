# vulcan/runner/run_fl.sh
#!/bin/bash

cd $GITHUB_WORKSPACE/vulcan_target

echo "Run VULCAN_YML_COVERAGE_BUILD_COMMAND"
sh -c "$VULCAN_YML_COVERAGE_BUILD_COMMAND" > /dev/null

if [ ! $? -eq 0 ]; then
  echo "Build failed"
  exit 1
fi

echo "Run split test by VULCAN_YML_TEST_COVERAGE_COMMAND"
source $GITHUB_ACTION_PATH/vulcan/util/test.sh

$GITHUB_ACTION_PATH/vulcan/bin/sbfl
