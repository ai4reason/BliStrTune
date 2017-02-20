#!/bin/sh

export ATP_ROOT=$PWD/atp
export PATH=$ATP_ROOT/bin:$PATH
export PYTHONPATH=$ATP_ROOT:$PYTHONPATH
# ENIGMA_ROOT is exported elsewhere

mkdir -p $ATP_ROOT/benchmarks
mkdir -p $ATP_ROOT/results
mkdir -p $ATP_ROOT/protos

