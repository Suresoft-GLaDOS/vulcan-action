# vulcan/runner/run_fl.sh
#!/bin/bash

# $GITHUB_ACTION_PATH/vulcan/bin/sbfl
echo "Find fault localization"

# temp code
cd /home/workspace/sbfl
python3.9 -m sbfl -f Ochiai2 ../../runner/vulcan-demo/_work/output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX/gcov/* -s $VULCAN_OUTPUT_DIR/fl.json -i $VULCAN_OUTPUT_DIR/info.json
