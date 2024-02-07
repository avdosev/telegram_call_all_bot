#!/bin/bash

# Fetch the latest changes from origin without merging them
git fetch origin

# Compare the local master branch with the remote master branch
LOCAL=$(git rev-parse master)
REMOTE=$(git rev-parse origin/master)

if [ "$LOCAL" != "$REMOTE" ]; then
    # Check if local is behind remote
    BASE=$(git merge-base master origin/master)
    if [ "$LOCAL" = "$BASE" ]; then
        echo "Local master is behind the remote master, updating and restarting callbot.service"
        # Pull the remote master into local master
        git pull origin master
        # Restart the callbot.service
        systemctl restart callbot.service
    else
        echo "Local master has diverged from remote master or is ahead. Manual intervention required."
    fi
else
    echo "Local master is up to date with the remote master."
fi
