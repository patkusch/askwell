#!/bin/sh
# Run every check on one example set:  examples/run_all.sh refund-approval/good
# Exit code is the number of checks that found something.
cd "$(dirname "$0")/.." || exit 2
D="examples/$1"; S=skills; fails=0
run() { echo "== $1"; shift; "$@"; rc=$?; [ $rc -ne 0 ] && fails=$((fails+1)); echo; }
run "stakeholder-mapping"          python3 $S/stakeholder-mapping/scripts/check.py $D/stakeholders.csv
run "requirements-writing"        python3 $S/requirements-writing/scripts/lint.py $D/requirements.txt
run "user-stories"                python3 $S/user-stories/scripts/check.py $D/stories.txt
run "acceptance-criteria"         python3 $S/acceptance-criteria/scripts/check.py $D/criteria.txt
run "requirements-traceability"   python3 $S/requirements-traceability/scripts/check.py $D/matrix.csv --tests $D/tests.csv
run "raid-log"                    python3 $S/raid-log/scripts/raid.py $D/raid.csv --today 2026-10-16
run "kpi-definition"              python3 $S/kpi-definition/scripts/check.py $D/kpis.json
run "nonfunctional-requirements" python3 $S/nonfunctional-requirements/scripts/check.py $D/nfr.csv
run "data-dictionary"             python3 $S/data-dictionary/scripts/check.py $D/dictionary.csv
run "use-cases"                   python3 $S/use-cases/scripts/check.py $D/usecase.txt
run "process-mapping"             python3 $S/process-mapping/scripts/check.py $D/process.mmd
run "vendor-selection"            python3 $S/vendor-selection/scripts/score.py $D/scorecard.json
run "backlog moscow"              python3 $S/backlog-prioritisation/scripts/score.py moscow $D/moscow.csv
run "decision-log"                python3 $S/decision-log/scripts/check.py $D/decisions.csv --today 2026-10-16
run "meeting-minutes"             python3 $S/meeting-minutes/scripts/actions.py $D/notes.txt
[ -f $D/conflict.csv ] && run "conflict-check" python3 $S/requirements-conflict-check/scripts/conflicts.py $D/conflict.csv --terms $D/terms.json
echo "== business-case"; python3 $S/business-case/scripts/case.py $D/case.json --sensitivity
exit $fails
