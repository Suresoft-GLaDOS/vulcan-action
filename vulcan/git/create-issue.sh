# /vulcan/github_cli/create-issue.sh
#!/bin/bash

_write_fl_info_in_issue() {
	VULCAN_ISSUE_FL_CONTENTS=""
	VULCAN_TRIGGER_URL="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/blob/$GITHUB_SHA"
	$GITHUB_ACTION_PATH/jq 'sort_by(.[2]) | reverse' $VULCAN_OUTPUT_DIR/fl.json > $VULCAN_OUTPUT_DIR/fl_sortby_score.json
	for i in {0..4}
	do
		ithFL=$(sh -c "$GITHUB_ACTION_PATH/jq '.[$i]' $VULCAN_OUTPUT_DIR/fl_sortby_score.json")
		buggy_source=$(echo $ithFL | $GITHUB_ACTION_PATH/jq -r '.[0]')
		buggy_line=$(echo $ithFL | $GITHUB_ACTION_PATH/jq '.[1]')
		buggy_score=$(echo $ithFL | $GITHUB_ACTION_PATH/jq '.[2]')
		
		VULCAN_ISSUE_FL_CONTENTS=$( \
			printf "$VULCAN_ISSUE_FL_CONTENTS\n\n----\n- [ ] Suspicious score: %.2f %s/%s#L%d" \
			$buggy_score \
			$VULCAN_TRIGGER_URL \
			$buggy_source \
			$buggy_line \
		)
	done
}

_create_issue() {
	echo ==========Creating Issue==========
	COMMAND="gh issue create \
	-t \"Vulcan\" \
	-a \"$GITHUB_ACTOR\" \
	-b \"This issue is generated by Vulcan for commit: $GITHUB_SHA
	Top 5 fault localization results
	$VULCAN_ISSUE_FL_CONTENTS\" \
	|| true"
	echo $COMMAND
	EXECUTE_ISSUE_COMMAND=$(sh -c "$COMMAND")
	echo $EXECUTE_ISSUE_COMMAND
	echo ==================================
}

# exist dependency
wget -q https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux32 -O $GITHUB_ACTION_PATH/jq && chmod +x $GITHUB_ACTION_PATH/jq

_write_fl_info_in_issue
_create_issue
