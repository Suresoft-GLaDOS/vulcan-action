# vulcan/runner/run_validator.sh
#!/bin/bash

# temp
cd $VULCAN_TARGET_WORKDIR/src
git clean -f -d
python3 /home/workspace/cxbuild/cxbuild.py capture make LDFLAGS="-Wl,-rpath=$MSV_REPO/src/.libs -L$MSV_REPO/src/.libs -ltest_runtime"
