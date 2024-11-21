#!/bin/bash
./checkBenchmark.sh

(cd res/platin
./collect.sh)

(cd res/sim
./collect.sh)

(cd res
python to_tex.py)

