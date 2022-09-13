FROM 0cherry/vulcan:demo

COPY vulcan /vulcan
RUN chmod +x -R /vulcan
ENTRYPOINT ["python3", "/vulcan/entry.py"]
