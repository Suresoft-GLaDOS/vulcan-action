FROM 0cherry/vulcan:0.9

RUN echo $1
COPY vulcan /vulcan
RUN chmod +x -R /vulcan
ENTRYPOINT ["python3", "/vulcan/entry.py"]
