# Perform the git pull command and capture the output
output=$(git pull)

# Check if the output does not contain the string "Already up to date"
if [[ $output != *"Already up to date"* ]]; then
    echo "Git pull updated the repository."
    systemctl restart callbot.service
fi