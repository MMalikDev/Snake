#!/bin/bash

# Icons
icon_log="\xF0\x9F\x93\x91" # Bookmark Tabs (U+1F4D1)
icon_start="\xF0\x9F\x9B\xA0 " # Hammer and Wrench (U+1F6E0)

display_usage() {
    cat << EOF

Usage: $0 [OPTIONS] [ARGS]

Run Project in specified environment

    OPTIONS
     -d [ARGS]      Run in Devcontainer
     -l [ARGS]      Run in Local env
     -c             Start the Docker container
     -e [ARGS]      Execute the program in the container
     -w [ARGS]      Rerun this script in WSL with provided ARGS

     -h             Display this help

    ARGS
     1. Action          human | neural show | neural train | ham
     2. UI              cli | gui | cui

Configure $0 defaults using .env file

    Environment:
        - Docker (Default)  (N/A)
        - DEVCONTAINER=True ( 1 )
        - RUN_LOCALLY=True  ( 1 )

    Keep Docker Logs:
        - KEEP_LOGS=True    ( 1 )

    Default args and their [OPTIONS]:
        Default UI
            - CUI=False                     [0 | 1]
            - GUI=False                     [0 | 1]
            - CLI=False                     [0 | 1]

        Default Player
            - HAM=False                     [0 | 1]
            - HUMAN=False                   [0 | 1]
            - NEURAL=False                  [0 | 1]

        Default Reinforcement  Learning
            - SHOW_TRAINING_GRAPHS=True     [0 | 1]
            - TRAIN_AGENT=False             [0 | 1]
            - AGENT_DEMO=False              [0 | 1]

EOF
    
    exit 1
}

# Generic
load_env(){
    set -a
    source .env
}
get_env(){
    echo $(grep -i "$@" .env | cut -d "=" -f 2)
}
get_bool(){
    local variable=$(get_env "$@" | tr '[A-Z]' '[a-z]')
    
    if [[ $variable =~ (1|true) ]]; then
        echo true
    else
        echo false
    fi
}

# Error Handlers
handle_errors(){
    if [[ $(get_bool KEEP_LOGS) == "true" ]]; then
        printf "\n$icon_log Keeping logs...\n\n"
        return
    fi
    if [[ $@ != 0 ]]; then
        printf "\n$icon_start Error encountered!\n\n"
        exit 1
    fi
    
    clear
    printf "\n$icon_log Cleared logs...\n\n"
}
log_error() {
    echo "$1" 2>&1;
    exit 1;
}

# Docker
reload_services(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_start Reloading the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_start Reloading all services\n\n"
    fi
    
    docker compose up -d
    echo "$services" | xargs docker compose kill
    echo "$services" | xargs docker compose up --force-recreate --build -d
}
follow_logs(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_log Getting logs from the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_log Getting logs from all services\n\n"
    fi
    
    echo "$services" | xargs docker compose logs -f
}
cp_docker(){
    local container=$1
    local source=$2
    local target=$3
    
    local containerID=$(docker-compose ps -qa $container)
    docker cp $containerID:$source $target
}

# Python
use_venv(){
    local os=$(uname | tr '[A-Z]' '[a-z]')
    
    case ${os} in
        linux* | darwin*) source .wsl/bin/activate ;;
        mingw* | cygwin*) source .venv/Scripts/activate ;;
        *) log_error "$icon_start Unsupported operating system: $os" ;;
    esac
}
run_python(){
    printf "\n$icon_start Running Python in local venv\n\n"
    use_venv
    cd $(get_env PYTHON_IMAGE)
    python main.py $@
    cd ..
}
run_python_dev(){
    printf "\n$icon_start Running Python in devcontainer\n\n"
    cd $(get_env PYTHON_IMAGE)
    python3 main.py $@
    cd ..
}
