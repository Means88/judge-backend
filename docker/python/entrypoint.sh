#!/bin/sh

echo 'python /judge/code.py </judge/stdin >/judge/userout 2>/judge/usererr' > /start-judge.sh
chmod 755 /start-judge.sh
chmod 666 /judge/userout
chmod 666 /judge/usererr

su judge
export START=$(adjtimex | awk 'BEGIN{a="", b=""} NR==11{a=$2} NR==12{b=$2} END{printf("%d.%d\n", a, b)}')
export MEMORY=$(command 2>&1 time -v /bin/sh /start-judge.sh | awk 'BEGIN{FS=": "} NR==10{print $2}')
export END=$(adjtimex | awk 'BEGIN{a="", b=""} NR==11{a=$2} NR==12{b=$2} END{printf("%d.%d\n", a, b)}')

echo {\"start\": $START, \"end\": $END, \"memory\": $MEMORY} > /judge/return
