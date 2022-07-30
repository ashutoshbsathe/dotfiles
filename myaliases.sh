#!/bin/sh 

# PID helpers for working with servers
cmdline() {
    cat /proc/$1/cmdline | tr '\000' ' '
}

powner() {
    ps -o user= -p $1
}

# NVIDIA
alias nvinfnoheader="nvidia-smi --query-gpu=fan.speed,temperature.gpu,pstate --format=csv,noheader"
