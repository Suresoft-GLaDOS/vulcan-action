FROM ubuntu:20.04

RUN echo $1
COPY vulcan /vulcan
RUN chmod +x -R /vulcan
CMD ["export"]
# ENTRYPOINT ["python3", "/vulcan/entry.py"]
