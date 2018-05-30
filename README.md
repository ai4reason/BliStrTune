# BliStrTune
Hierarchical invention of targeted  E prover strategies

This is a pre-BETA release.  It is usable with some effort.

## Requirements

This distribution contains other software packages:

* GNU Parallel (https://www.gnu.org/software/parallel)
* ParamILS (http://www.cs.ubc.ca/labs/beta/Projects/ParamILS)
* E Prover (http://www.eprover.org) 
   
   You need E "hacked" version 1.9.1 with 6 new clause evaluation functions.
   A binary for x86 is provided in `atp/bin/eprover`.  Source codes can be
   obtained at:
   
      http://people.ciirc.cvut.cz/~jakubja5/src/E-1.9.1-PARG-CPP17.tar.gz

To run this software you need to have Python, Perl, and Ruby installed.

## Quickstart

### Prepare experiments

0. Setup environment before running import scripts:
   
   ```
   $ . ./setenv.sh
   ```
   Always run the scripts from the BliStrTune directory.

1. Import benchmark problems:

   ```
   $ ./import-benchmark.sh examples/bechmarks/test test  
   importing examples/bechmarks/test as test ... 10 problems imported
   ```

2. Import initial protocols:

   ```
   $ ./import-inits.sh examples/inits/tptp tptp
   importing examples/inits/tptp as tptp ... 10 strategies imported
   ```

### Setup experiments

   ```
   $ vi BliStrTune-RUN.sh
   ```

### Run experiments

   ```
   $ ./BliStrTune-RUN.sh
   ```

### Get results (optional)
   
   ```
   $ BliStr-import-results.py BliStrTune-test-* test 1
   $ expres-greedy.py test 1
   ```

