#!/bin/bash

. .env

function send() {
    rsync -auv --delete \
        --exclude "__pycache__" \
        "./$1" "$SSH_USER@$SERVER_HOST:/home/$SSH_USER/$1"
}

if [[ $1 =~ u ]]; then
    send "requirements.txt"

    send "data/"
    send "storage/"
    send "app/"
    send "main.py"
    send "settings.py"
fi

if [[ $1 =~ c ]]; then
    ssh -t "$SSH_USER@$SERVER_HOST" "tmux"
fi
