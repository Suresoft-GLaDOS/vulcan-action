# vulcan/runner/run_apr.sh
#!/bin/bash

$GITHUB_ACTION_PATH/vulcan/bin/msv
echo "Find repair code"

# temp
cd $VULCAN_OUTPUT_DIR

set -a
MSV_REPO=/home/workspace/msv
MSV_SEARCH_REPO=/home/workspace/msv-search
MSV_WORKSPACE=$VULCAN_OUTPUT_DIR/msv-workspace
VULCAN_TARGET_WORKDIR=$MSV_WORKSPACE/$VULCAN_TARGET_NAME-workdir
MSV_JSON=$VULCAN_OUTPUT_DIR/msv-output/msv-result.json
MSV_PATCH_DIFF_PATH=$VULCAN_OUTPUT_DIR/patch
set +a

mkdir -p $MSV_WORKSPACE

echo [DEBUG] python3 $MSV_REPO/msv-runner.py -r $VULCAN_TARGET $MSV_WORKSPACE $MSV_REPO
python3 $MSV_REPO/msv-runner.py -r $VULCAN_TARGET $MSV_WORKSPACE $MSV_REPO

echo [DEBUG] python3 $MSV_SEARCH_REPO/msv-search.py -o $VULCAN_OUTPUT_DIR/msv-output -w $VULCAN_TARGET_WORKDIR -T $VULCAN_YML_TIME_OUT -m prophet -p $MSV_REPO --use-pass-test -- $MSV_REPO/tools/msv-test.py $VULCAN_TARGET_WORKDIR/src $VULCAN_TARGET_WORKDIR/tests $VULCAN_TARGET_WORKDIR
python3 $MSV_SEARCH_REPO/msv-search.py -o $VULCAN_OUTPUT_DIR/msv-output -w $VULCAN_TARGET_WORKDIR -T $VULCAN_YML_TIME_OUT -m prophet -p $MSV_REPO --use-pass-test -- $MSV_REPO/tools/msv-test.py $VULCAN_TARGET_WORKDIR/src $VULCAN_TARGET_WORKDIR/tests $VULCAN_TARGET_WORKDIR

echo [DEBUG] python3 $MSV_SEARCH_REPO/diff_gen.py -g -i $VULCAN_OUTPUT_DIR/msv-output -o $VULCAN_OUTPUT_DIR/patch $VULCAN_TARGET_WORKDIR
python3 $MSV_SEARCH_REPO/diff_gen.py -g -i $VULCAN_OUTPUT_DIR/msv-output -o $VULCAN_OUTPUT_DIR/patch $VULCAN_TARGET_WORKDIR
