# vulcan/runner/run_apr.sh
#!/bin/bash

$GITHUB_ACTION_PATH/vulcan/bin/msv
echo "Find repair code"

# temp
cd $VULCAN_OUTPUT_DIR
MSV_REPO=/home/workspace/msv
MSV_SEARCH_REPO=/home/workspace/msv-search
MSV_WORKSPACE=$VULCAN_OUTPUT_DIR/msv-workspace
VULCAN_TARGET_WORKDIR=$MSV_WORKSPACE/$VULCAN_TARGET_NAME-workdir
mkdir -p $MSV_WORKSPACE
echo python3 $MSV_REPO/msv-runner.py -r $VULCAN_TARGET $MSV_WORKSPACE $MSV_REPO
python3 $MSV_REPO/msv-runner.py -r $VULCAN_TARGET $MSV_WORKSPACE $MSV_REPO
python3 $MSV_SEARCH_REPO/msv-search.py -o $VULCAN_OUTPUT_DIR/msv-output -w $VULCAN_TARGET_WORKDIR -m prophet -t 600 -p $MSV_REPO -- $MSV_REPO/tools/msv-test.py $VULCAN_TARGET_WORKDIR/src $VULCAN_TARGET_WORKDIR/tests $VULCAN_TARGET_WORKDIR

PATCH_OUTPUT_PATH=$VULCAN_OUTPUT_DIR/patch
mkdir -p $PATCH_OUTPUT_PATH
if [ -f $VULCAN_TARGET/patch/*-0001-*.diff ]; then
    cp -r $VULCAN_TARGET/patch $VULCAN_OUTPUT_DIR
fi