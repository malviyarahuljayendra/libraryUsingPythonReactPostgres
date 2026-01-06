#!/bin/bash
set -e

# Define colors and bold text using ANSI-C quoting for real escape characters
BOLD=$'\e[1m'
NC=$'\e[0m'
GREEN=$'\e[32m'
RED=$'\e[31m'

if [ "$RUN_TESTS" = "true" ]; then
    echo "------------------------------------------------"
    echo -e "${BOLD}Running Backend Tests & Coverage...${NC}"
    echo "------------------------------------------------"
    
    # Run pytest and capture output to show it and parse for the TOTAL line
    # We use --cov-report=term-missing to show which lines are missing
    pytest --cov=backend --cov-config=.coveragerc --cov-report=term-missing backend/tests > test_output.log 2>&1
    TEST_RESULT=$?
    
    # Print the log, bolding the TOTAL line
    # The shell expands ${BOLD} and ${NC} to raw escape characters
    sed "s/^TOTAL[[:space:]]\+.*/${BOLD}&${NC}/" test_output.log
    
    if [ $TEST_RESULT -ne 0 ]; then
        echo -e "${BOLD}${RED}Tests failed! System will not boot.${NC}"
        # Print the log again on failure just in case sed didn't show everything or for clarity
        # (Though sed above should have printed it all)
        exit $TEST_RESULT
    fi
    
    echo "------------------------------------------------"
    echo -e "${BOLD}${GREEN}Tests passed. Booting application...${NC}"
    echo "------------------------------------------------"
    rm test_output.log
fi

# Execute the main application
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    exec python -m backend.main
fi
