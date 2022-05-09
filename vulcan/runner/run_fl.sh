# vulcan/runner/run_fl.sh
#!/bin/bash

# $GITHUB_ACTION_PATH/vulcan/bin/sbfl
echo "Find fault localization"

# temp code
cd $SBFL_REPO
# python3 -m pip install -r requirements.txt
which python3
python3 -m sbfl -f Ochiai2 $VULCAN_OUTPUT_DIR/gcov/* -s $VULCAN_OUTPUT_DIR/fl.json -i $VULCAN_OUTPUT_DIR/info.json -c $VULCAN_OUTPUT_DIR/fl_cluster.json
