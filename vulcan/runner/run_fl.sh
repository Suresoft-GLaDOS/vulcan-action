# vulcan/runner/run_fl.sh
#!/bin/bash

# $GITHUB_ACTION_PATH/vulcan/bin/sbfl
echo "Find fault localization"

# temp code
python3.9 -m sbfl -f Ochiai2 $GCOV_PATH/* -s $VULCAN_OUTPUT_DIR/fl.json -i $VULCAN_OUTPUT_DIR/info.json
