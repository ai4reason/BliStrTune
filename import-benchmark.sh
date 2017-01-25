#!/bin/sh

if [ "$#" -ne 2 ]; then
   echo "usage: $0 DIR BID" 
   echo "use to: import benchmarks from DIR under the Benchmark ID (BID)"
   exit 1
fi

DIR=$1
BID=$2

echo -n "importing $DIR as $BID ... "

mkdir $ATP_ROOT/benchmarks/$BID
cp -r $1/* $ATP_ROOT/benchmarks/$BID
(cd $ATP_ROOT/benchmarks; ls $BID/*.p > $BID.problems)

N=`wc -l $ATP_ROOT/benchmarks/$BID.problems | cut -d" " -f1`
echo "$N problems imported"

