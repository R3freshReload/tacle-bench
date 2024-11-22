#!/bin/bash
rm -rf ./arrayOpt/*
find ../.. -type f | grep -e "arrayOpt_[a-zA-Z0-9]*_wcet.txt$" | xargs -i cp {} arrayOpt

rm -rf ./opt/*
find ../.. -type f | grep -e "opt_[a-zA-Z0-9]*_wcet.txt$" | xargs -i cp {} opt

rm -rf ./noOpt/*
find ../.. -type f | grep -e "noOpt_[a-zA-Z0-9]*_wcet.txt$" | xargs -i cp {} noOpt
