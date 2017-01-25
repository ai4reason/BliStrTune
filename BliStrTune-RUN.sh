#!/bin/sh

CORES=4

BST_TIMEOUT_GLOBAL=10
BST_TIMEOUT_FINETUNES=10
BST_CUTOFF=1
BST_EVAL_LIMIT=1
BST_MIN_CEFS=3
BST_MAX_CEFS=6
BST_VERS=1
BST_TOPS=20
BST_MIN_PROC=10
BST_MAX_PROC=30000

BST_BENCHMARK=test
BST_INITSTRATS=tptp

#
# Non-hackers do not change below this line
#

. ./setenv.sh

export CORES

DIR="BliStrTune-${BST_BENCHMARK}-${BST_INITSTRATS}"
DIR="$DIR-${BST_TIMEOUT_GLOBAL}t${BST_TIMEOUT_FINETUNES}"
DIR="$DIR-cut${BST_CUTOFF}-e${BST_EVAL_LIMIT}"
DIR="$DIR-${BST_MIN_CEFS}c${BST_MAX_CEFS}"
DIR="$DIR-${BST_MIN_PROC}p${BST_MAX_PROC}"
DIR="$DIR-top${BST_TOPS}-vers${BST_VERS}-${CORES}cores"

cp -r SKEL $DIR
mv $DIR/BliStrTune.pl.template $DIR/BliStrTune.pl
mv $DIR/epymils.py.template $DIR/epymils.py

BLISTR_ARGS="BST_EVAL_LIMIT CORES BST_TOPS BST_VERS\
   BST_MIN_PROC BST_MAX_PROC BST_BENCHMARK BST_INITSTRATS"
for ARG in $BLISTR_ARGS; do
   sed -i "s/@@@${ARG}@@@/${!ARG}/g" $DIR/BliStrTune.pl 
done

EPYMILS_ARGS="BST_TIMEOUT_GLOBAL BST_TIMEOUT_FINETUNES BST_CUTOFF\
   BST_MIN_CEFS BST_MAX_CEFS CORES"
for ARG in $EPYMILS_ARGS; do
   sed -i "s/@@@${ARG}@@@/${!ARG}/g" $DIR/epymils.py
done

chmod a+x $DIR/BliStrTune.pl
chmod a+x $DIR/epymils.py

./make-initprots.sh $BST_INITSTRATS $BST_BENCHMARK $BST_EVAL_LIMIT

cp -r $ATP_ROOT/inits/$BST_INITSTRATS/${BST_EVAL_LIMIT}s $DIR/initprots
cp -r $ATP_ROOT/benchmarks/$BST_BENCHMARK $DIR/allprobs

(cd $DIR; ./BliStrTune.pl)

