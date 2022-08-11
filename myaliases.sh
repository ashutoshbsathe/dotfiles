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

# General bash stuff 
logtofile() {
    passed_cmd="$*"
    fname="$1"
    timestamp=$(date +%F.%H-%M-%S)
    echo "Executing: $passed_cmd"
    echo "Logging to: $fname.$timestamp.log"
    echo "Is the command escaped properly? [y/N]" 
    read escape_response
    if [[ $escape_response =~ ^[Yy]$ ]]
    then
        echo "-----"
        eval "$passed_cmd" 2>&1 | tee $fname.$timestamp.log 
        echo -e "\n\n\n-----\nCommand: $passed_cmd\n-----" >> $fname.$timestamp.log
        echo "-----"
    else
        echo "Exiting"
    fi
}
