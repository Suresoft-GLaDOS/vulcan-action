FROM ubuntu:20.04

COPY vulcan /vulcan
RUN chmod +x -R /vulcan
# ENTRYPOINT ["python3", "/vulcan/entry.py"]
