echo "running"
LOG_FILE="./validate.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
printf "\n" >> "$LOG_FILE"
if [ -d "src" ]
then
    echo "[$TIMESTAMP] src/ found" >> $LOG_FILE
else
    echo "[$TIMESTAMP] src/ not found" >> $LOG_FILE
    echo "[$TIMESTAMP] validation aborted with status code 1." >> $LOG_FILE
    exit 1
fi

if [ -e "src/config.json" ]
then
    if jq empty src/config.json >/dev/null 2>&1; then
        echo "[$TIMESTAMP] config.json is valid" >> $LOG_FILE
    else
        echo "[$TIMESTAMP] config.json is invalid" >> $LOG_FILE
        echo "[$TIMESTAMP] validation aborted with status code 1." >> $LOG_FILE
        exit 1
    fi
else
    echo "[$TIMESTAMP] config.json not found" >> $LOG_FILE
    echo "[$TIMESTAMP] validation aborted with status code 1." >> $LOG_FILE
    exit 1
fi

echo "[$TIMESTAMP] Validation completed." >> $LOG_FILE
