#!/bin/bash
# second pass: repos without a root solution (per-project build+test) and node test suites; scratch clones only
export PATH=/root/.dotnet:$PATH DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1 DOTNET_ROLL_FORWARD=Major
S=/tmp/claude-0/-home-user/45711cf3-dc26-5c8e-a6da-4af8bd5f0946/scratchpad/aincm; B=$S/build; L=$S/dev/buildlogs
dproj() { # repo proj
  r=$1; p=$2; n=$(basename $p); cd $B/$r
  SECONDS=0; timeout 300 dotnet build $p -c Release > $L/$r.$n.build.txt 2>&1; brc=$?
  echo "CMD dotnet build $p -c Release => BUILD_RC $brc SECS $SECONDS" >> $L/$r.log
  [ $brc -ne 0 ] && { grep -m3 -E "error " $L/$r.$n.build.txt | cut -c1-250 >> $L/$r.log; return; }
  SECONDS=0
  if grep -q "Test.Sdk" $p; then
    timeout 300 dotnet test $p -c Release --no-build > $L/$r.$n.txt 2>&1; rc=$?
    echo "TEST_RC $n $rc SECS $SECONDS :: $(grep -E 'Passed!|Failed!|Aborted' $L/$r.$n.txt | tr '\n' ' ' | cut -c1-250)" >> $L/$r.log
  else
    timeout 300 dotnet run --project $p -c Release --no-build > $L/$r.$n.txt 2>&1; rc=$?
    echo "RUN_RC $n $rc SECS $SECONDS :: pass_lines=$(grep -ciE '^\s*(PASS|ok|✓)' $L/$r.$n.txt) fail_lines=$(grep -ciE '^\s*(FAIL|not ok|✗)' $L/$r.$n.txt) tail=$(tail -2 $L/$r.$n.txt | tr '\n' ' ' | cut -c1-200)" >> $L/$r.log
  fi
}
patchgj() { python3 -I -B -c "import json,sys;p=sys.argv[1]+'/global.json';d=json.load(open(p));d.setdefault('sdk',{})['rollForward']='latestMajor';json.dump(d,open(p,'w'))" $1; }
cd $B; [ -d strata ] || git clone -q /home/user/echelon-components/strata strata; patchgj $B/strata; $S/scripts/runrepo.sh strata; echo "NOTE global.json rollForward added in scratch clone (pinned SDK not installed; 10.0.404 used)" >> $L/strata.log
for r in limen ordo percepta forma forma-studio causa; do
  cd $B; [ -d $r ] || git clone -q /home/user/echelon-components/$r $r
  echo "PASS2 REV $(git -C $B/$r rev-parse --short HEAD)" >> $L/$r.log
  if [ $r = causa ]; then patchgj $B/causa; echo "NOTE global.json rollForward added in scratch clone (pinned SDK not installed; 10.0.404 used)" >> $L/$r.log; fi
  for p in $(git -C $B/$r ls-files '*.fsproj' '*.csproj' | grep -E '(^|/)tests/' | grep -v -E 'TestSupport|CompileFailure|Probe|Client.Wasm|InterpreterFrame|experiments/'); do dproj $r $p; done
  echo DONE2 >> $L/$r.log
done
for r in echelon-foundry vitium; do
  cd $B; [ -d $r ] || git clone -q /home/user/echelon-components/$r $r; cd $B/$r
  echo "PASS2 REV $(git rev-parse --short HEAD)" >> $L/$r.log
  cmd=$( [ $r = vitium ] && echo "node --test tests/*.test.mjs" || echo "node --test test/*.test.js")
  SECONDS=0; timeout 300 bash -c "$cmd" > $L/$r.node.txt 2>&1; rc=$?
  echo "CMD $cmd => NODE_RC $rc SECS $SECONDS :: $(grep -E '^# (tests|pass|fail)' $L/$r.node.txt | tr '\n' ' ')" >> $L/$r.log
  echo DONE2 >> $L/$r.log
done
for r in forma folio; do
  cd $B/$r 2>/dev/null || { cd $B; git clone -q /home/user/echelon-components/$r $r; cd $B/$r; }
  SECONDS=0; timeout 300 npm ci --ignore-scripts --no-audit --no-fund > $L/$r.npmci.txt 2>&1; echo "CMD npm ci --ignore-scripts => RC $? SECS $SECONDS" >> $L/$r.log
  if [ $r = forma ]; then cmd="node --test tests/token-compiler.test.mjs tests/token-validator.test.mjs tests/brand-compiler.test.mjs tests/external-brand-compiler.test.mjs tests/contrast-pairs.test.mjs tests/zero-runtime.test.mjs"; else cmd="npm test"; fi
  SECONDS=0; timeout 300 bash -c "$cmd" > $L/$r.node.txt 2>&1; rc=$?
  echo "CMD $cmd => NODE_RC $rc SECS $SECONDS :: $(grep -E '^# (tests|pass|fail)' $L/$r.node.txt | tr '\n' ' ') tail=$(tail -3 $L/$r.node.txt | tr '\n' ' ' | cut -c1-200)" >> $L/$r.log
  echo DONE2 >> $L/$r.log
done
for r in signal summa chrona; do
  cd $B/$r; SECONDS=0; timeout 300 npm ci --ignore-scripts --no-audit --no-fund > $L/$r.npmci.txt 2>&1; rc=$?
  echo "PASS2 CMD npm ci --ignore-scripts => RC $rc SECS $SECONDS :: $(grep -iE 'npm (error|ERR)' $L/$r.npmci.txt | head -2 | tr '\n' ' ' | cut -c1-200)" >> $L/$r.log
  if [ $rc -eq 0 ]; then for p in $(git ls-files '*.fsproj' | grep -E '^tests/' | grep -E 'Web.Tests|Signal.Tests|Chrona.Tests'); do SECONDS=0; timeout 300 dotnet test $p -c Release --no-build > $L/$r.$(basename $p).npm.txt 2>&1; echo "PASS2 TEST_RC(after npm ci) $(basename $p) $? SECS $SECONDS :: $(grep -E 'Passed!|Failed!' $L/$r.$(basename $p).npm.txt | tr '\n' ' ' | cut -c1-200)" >> $L/$r.log; done; fi
done
echo PASS2DONE
