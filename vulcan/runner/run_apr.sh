# vulcan/runner/run_apr.sh
#!/bin/bash

PATCH_OUTPUT_PATH=$VULCAN_OUTPUT_DIR/patch

cd $VULCAN_TARGET
echo "Find repair code"
mkdir -p $PATCH_OUTPUT_PATH
$GITHUB_ACTION_PATH/vulcan/bin/msv

# temp
DO_COPY=$(($(date +%s)%2))
if [ $DO_COPY -eq 0 ]; then
    cp -r /home/0cherry/patch $VULCAN_OUTPUT_DIR
fi