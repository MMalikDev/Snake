#!/bin/bash

set -e

icon_wall="\xF0\x9F\xA7\xB1" # Brick (U+1F40D)
icon_snake="\xF0\x9F\x90\x8D " # Snake (U+1F40D)

source ./scripts/run.sh
# ---------------------------------------------------------------------- #
# Define Docker Variables
# ---------------------------------------------------------------------- #
declare -a reloads=(
    #
)

declare -a logs=(
    #
)

# ---------------------------------------------------------------------- #
# Helper
# ---------------------------------------------------------------------- #
review_stats_logs(){
    local file=src/logs/stats.log
    [[ ! -f "$file" ]] && echo "Log file not found"
    
    local death_by_snake=$(grep -c Snake $file)
    local death_by_boundary=$(grep -c Boundary $file)
    local death_total=$((death_by_snake + death_by_boundary))
    local snake_ratio=$(awk "BEGIN {print $death_by_snake / $death_total * 100}")
    local boundary_ratio=$(awk "BEGIN {print $death_by_boundary / $death_total * 100}")
    
    printf "\nGetting game stats from log file...\n"
    printf "Death caused by Snake eating itself:\t%s%% $icon_snake\n" $snake_ratio
    printf "Death caused by Boundary being hit:\t%s%% $icon_wall\n" $boundary_ratio
    
    rm -f "$file"
}

# ---------------------------------------------------------------------- #
# OPTIONS
# ---------------------------------------------------------------------- #
run_devcontainer(){
    load_env
    run_python_dev $@
    exit 0
}
run_locally(){
    load_env
    run_python $@
    review_stats_logs
    exit 0
}
run_docker(){
    reload_services ${reloads[*]}
    handle_errors $?
    
    docker image prune -f
    follow_logs ${logs[*]}
    exit 0
}

use_env_file(){
    [[ $(get_bool DEVCONTAINER) == "true" ]] && run_devcontainer $@
    [[ $(get_bool RUN_LOCAL) == "true" ]] && run_locally $@
    run_docker
}
use_wsl(){
    set -f
    local input=$1
    local IFS=','
    local array=($OPTARG)
    
    wsl --exec bash run.sh ${array[*]}
    exit 0
}

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    while getopts "w:dlch" OPTION; do
        case $OPTION in
            w) use_wsl $OPTARG      ;;
            d) run_devcontainer $@  ;;
            l) run_locally  $@      ;;
            c) run_docker           ;;
            h) display_usage        ;;
            ?) display_usage        ;;
        esac
    done
    shift $((OPTIND -1))
    
    use_env_file $@
}

main $@
