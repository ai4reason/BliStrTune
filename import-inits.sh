#!/bin/sh

if [ "$#" -ne 2 ]; then
   echo "usage: $0 DIR INITS" 
   echo "use to: import initial strategies from DIR under name INITS"
   exit 1
fi

DIR=$1
INITS=$2

echo -n "importing $DIR as $INITS ... "

STRATS=$ATP_ROOT/inits/$INITS/strats
PROTS=$ATP_ROOT/inits/$INITS/prots

mkdir -p $STRATS $PROTS

cp $DIR/* $STRATS

for i in `ls $STRATS`; do
   epymils_params.py $STRATS/$i > $PROTS/protocol_$i
done

N=`ls $STRATS | wc -l`
echo "$N strategies imported"

