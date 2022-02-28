# vulcan/runner/run_fl.sh
#!/bin/bash

cd $GITHUB_WORKSPACE/vulcan_target

echo "Run VULCAN_YML_COVERAGE_BUILD_COMMAND"
sh -c "$VULCAN_YML_COVERAGE_BUILD_COMMAND"

if [ ! $? -eq 0 ]; then
  echo "Build failed"
  exit 1
fi

echo "Run VULCAN_YML_TEST_COVERAGE_COMMAND"
sh -c "$VULCAN_YML_TEST_COVERAGE_COMMAND"

$GITHUB_ACTION_PATH/vulcan/bin/sbfl
