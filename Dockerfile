FROM 0cherry/vulcan:demo

ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LIBRARY_PATH=/usr/local/lib

COPY vulcan /vulcan
RUN chmod +x -R /vulcan
ENTRYPOINT ["python3", "/vulcan/entry.py"]
