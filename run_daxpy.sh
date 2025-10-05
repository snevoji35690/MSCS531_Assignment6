#!/bin/bash
# Explore combinations where opLat + issueLat = 7
declare -a oplat=(1 2 3 4 5 6)
declare -a isslat=(6 5 4 3 2 1)

for i in ${!oplat[@]}; do
  echo "=============================="
  echo "Running gem5 with opLat=${oplat[$i]} issueLat=${isslat[$i]}"
  echo "=============================="
  ./build/X86/gem5.opt --outdir=run_${oplat[$i]}_${isslat[$i]} configs/example/se.py \
  --cpu-type=MinorCPU --cmd=./daxpy_openmp --options="4"
done
