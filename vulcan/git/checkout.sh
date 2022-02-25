# vulcan/github_cli/checkout.sh
#!/bin/bash

cd $GITHUB_WORKSPACE/vulcan_target

DESTINATION_BRANCH="$GITHUB_REF_NAME"
PATCH_BRANCH="$GITHUB_REF_NAME-auto-patch-$(date +%s%N)"

echo ==========Switching to $PATCH_BRANCH==========
# git remote set-url origin $REPO
# git fetch origin '+refs/heads/*:refs/heads/*' --update-head-ok
# git --no-pager branch -a -vv
git checkout $DESTINATION_BRANCH
git checkout -b $PATCH_BRANCH
git clean
echo ==================================
