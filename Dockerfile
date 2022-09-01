FROM 0cherry/vulcan:0.9

COPY vulcan /action
RUN chmod +x -R /action/vulcan
ENTRYPOINT ["python3", "/action/vulcan/entry.py"]
