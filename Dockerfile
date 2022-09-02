FROM ubuntu:20.04

RUN export
COPY vulcan /vulcan
RUN chmod +x -R /vulcan
ENTRYPOINT ["python3", "/vulcan/entry.py"]
