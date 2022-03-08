# vulcan/github_cli/create-pull-request.sh
#!/bin/bash

_create_pull_request() {
	echo ==========Creating PR==========
	echo from: $PATCH_BRANCH
	echo into: $DESTINATION_BRANCH
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
}

_create_pull_request_for_patches() {
	MAX_PR=3
	CURRENT_PR_COUNT=0
	cd $VULCAN_TARGET
	for diff_file in $(sh -c "ls $PATCH_OUTPUT_PATH/*.diff")
	do
		PATCH_BRANCH="$GITHUB_REF_NAME-auto-patch-$(date +%s%N)"
		git checkout -b $PATCH_BRANCH
		git am $diff_file
		git push origin $PATCH_BRANCH
		_create_pull_request
		
		git clean -f > /dev/null
		git checkout $DESTINATION_BRANCH
		
		CURRENT_PR_COUNT=$(( $CURRENT_PR_COUNT + 1 ))
		if [ $CURRENT_PR_COUNT -eq $MAX_PR ]; then
			break
		fi
	done
}

_create_pull_request_for_patches
