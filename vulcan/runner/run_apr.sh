# vulcan/runner/run_apr.sh
#!/bin/bash

PATCH_OUTPUT_PATH=$VULCAN_OUTPUT_DIR/patch

cd $VULCAN_TARGET
echo "Find repair code"
mkdir -p $PATCH_OUTPUT_PATH
$GITHUB_ACTION_PATH/vulcan/bin/msv

# temp
if [ -f $VULCAN_TARGET/patch/*-0001-*.diff ]; then
    cp -r $VULCAN_TARGET/patch $VULCAN_OUTPUT_DIR
fi