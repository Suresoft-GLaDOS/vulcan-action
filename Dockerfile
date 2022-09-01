FROM 0cherry/vulcan:0.9

COPY vulcan $GITHUB_ACTION_PATH/vulcan
RUN chmod +x -R $GITHUB_ACTION_PATH/vulcan
ENTRYPOINT ["python3", "$GITHUB_ACTION_PATH/vulcan/entry.py"]
