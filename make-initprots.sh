#!/bin/sh

CORES=${CORES:-4}

if [ "$#" -ne 3 ]; then
   echo "usage: $0 INITS BID LIMIT"
   echo "use to: evaluate initial protocol set INITS on benchmark BID with time LIMIT"
   exit 1
fi

INITS=$1
BID=$2
LIMIT=$3

PROTS=$ATP_ROOT/inits/$INITS/prots

OUT=$ATP_ROOT/inits/$INITS/${LIMIT}s

echo "initial evaluation of strategies $INITS on bechmark $BID @ ${LIMIT}s"
if [ -d "$OUT" ]; then
   echo "allready done"
   exit 0;
fi

mkdir -p $OUT
for init in `ls $PROTS`; do
   echo "-> $init"
   cat $ATP_ROOT/benchmarks/${BID}.problems | parallel -j$CORES "(time eprover -s -R --memory-limit=1024 --print-statistics --tstp-format `cat $PROTS/${init}` --cpu-limit=$LIMIT $ATP_ROOT/benchmarks/{}) >$OUT/{/}.$init 2>&1"
done

