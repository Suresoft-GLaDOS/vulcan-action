# vulcan/github_cli/checkout.sh
#!/bin/bash

cd $VULCAN_TARGET

DESTINATION_BRANCH="$GITHUB_REF_NAME"
PATCH_BRANCH="$GITHUB_REF_NAME-auto-patch-$VULCAN_SUFFIX"

echo ==========Switching to $PATCH_BRANCH==========
git checkout $DESTINATION_BRANCH
git checkout -b $PATCH_BRANCH
git clean
echo ==================================
