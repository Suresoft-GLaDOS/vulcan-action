# vulcan/runner/run_validator.sh
#!/bin/bash

# temp
cd $VULCAN_TARGET_WORKDIR/src
git clean -f -d

echo [DEBUG] python3 /home/workspace/cxbuild/cxbuild.py capture make LDFLAGS="-Wl,-rpath=$MSV_REPO/src/.libs -L$MSV_REPO/src/.libs -ltest_runtime"
python3 /home/workspace/cxbuild/cxbuild.py capture make LDFLAGS="-Wl,-rpath=$MSV_REPO/src/.libs -L$MSV_REPO/src/.libs -ltest_runtime"

echo [DEBUG] python3 /home/workspace/client.py
python3 /home/workspace/client.py
