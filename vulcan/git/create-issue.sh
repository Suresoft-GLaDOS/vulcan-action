# /vulcan/github_cli/create-issue.sh
#!/bin/bash

_create_issue() {
	echo ==========Creating Issue==========
	VULCAN_ISSUE_CREATE_RESULT=$(\
		gh issue create \
		-t "$VULCAN_TITLE" \
		-a "$GITHUB_ACTOR" \
		-b "$(cat $VULCAN_OUTPUT_DIR/issue_body)" \
	)
	printf "$VULCAN_ISSUE_CREATE_RESULT\n"
	echo ==================================
}

python3 $GITHUB_ACTION_PATH/vulcan/git/issue_body_generator.py
_create_issue
