#!/bin/bash
# usage: runrepo.sh <repo>   -- clones read-only repo into scratch and builds/tests it, time-boxed
export PATH=/root/.dotnet:$PATH DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 DOTNET_ROLL_FORWARD=Major
r=$1
S=/tmp/claude-0/-home-user/45711cf3-dc26-5c8e-a6da-4af8bd5f0946/scratchpad/aincm
B=$S/build; L=$S/dev/buildlogs; mkdir -p $B $L
log=$L/$r.log; : > $log
cd $B; [ -d $r ] || git clone -q /home/user/echelon-components/$r $r
cd $B/$r
echo "REV $(git rev-parse --short HEAD)" >> $log
sln=$(ls *.sln *.slnx 2>/dev/null | grep -iv '^App\.' | head -1)
if [ -n "$sln" ]; then
  echo "CMD dotnet build $sln -c Release" >> $log
  SECONDS=0
  timeout 420 dotnet build $sln -c Release > $L/$r.build.txt 2>&1; rc=$?
  echo "BUILD_RC $rc SECS $SECONDS" >> $log
  grep -E "Build succeeded|error [A-Z]+[0-9]+|Warn|Error\(s\)" $L/$r.build.txt | sort | uniq | tail -8 >> $log
  for p in $(git ls-files '*.fsproj' '*.csproj' | grep -E '^tests/|/tests/' | grep -v -E 'TestSupport|CompileFailure|Probe|Client.Wasm|Examples'); do
    SECONDS=0
    if grep -q "Test.Sdk" $p; then
      echo "CMD dotnet test $p -c Release --no-build" >> $log
      timeout 300 dotnet test $p -c Release --no-build > $L/$r.$(basename $p).txt 2>&1; rc=$?
      echo "TEST_RC $(basename $p) $rc SECS $SECONDS :: $(grep -E 'Passed!|Failed!|Total tests|Test Run Aborted' $L/$r.$(basename $p).txt | tr '\n' ' ' | cut -c1-300)" >> $log
    else
      echo "CMD dotnet run --project $p -c Release --no-build" >> $log
      timeout 300 dotnet run --project $p -c Release --no-build > $L/$r.$(basename $p).txt 2>&1; rc=$?
      echo "RUN_RC $(basename $p) $rc SECS $SECONDS :: $(tail -3 $L/$r.$(basename $p).txt | tr '\n' ' ' | cut -c1-300)" >> $log
    fi
  done
fi
echo DONE >> $log
