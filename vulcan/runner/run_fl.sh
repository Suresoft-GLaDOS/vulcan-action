# vulcan/runner/run_fl.sh
#!/bin/bash

# $GITHUB_ACTION_PATH/vulcan/bin/sbfl

# temp code
cd /home/workspace/sfbl
python3.9 -m sbfl -f Ochiai2 ../../runner/vulcan-demo/_work/output/$GITHUB_REPOSITORY/$VULCAN_SUFFIX/gcov > $VULCAN_OUTPUT_DIR/fl.output
