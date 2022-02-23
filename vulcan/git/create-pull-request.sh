# vulcan/github_cli/create-pull-request.sh
#!/bin/bash

date +%s%N > dummy
git add dummy
git commit -m "Auto-generated"
git push origin $PATCH_BRANCH

echo ==========Creating PR==========
echo from: $PATCH_BRANCH
echo into: $DESTINATION_BRANCH
SHORT_COMMIT=${GITHUB_SHA:0:6}
COMMAND="gh pr create \
-B $DESTINATION_BRANCH \
-H $PATCH_BRANCH \
-t \"Vulcan\" \
-b \"This PR is auto-patch by Vulcan for commit: $GITHUB_ACTOR@$GITHUB_SHA\" \
|| true"
echo "$COMMAND"
EXECUTE_PR_COMMAND=$(sh -c "$COMMAND")
echo $EXECUTE_PR_COMMAND
echo ==================================
