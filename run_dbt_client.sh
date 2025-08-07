#!/bin/bash

# DBT Multi-Client Runner Script
# Usage: ./run_dbt_client.sh <client> <environment> <command> [additional_args]
# Example: ./run_dbt_client.sh client_a dev run
# Example: ./run_dbt_client.sh client_b prod test --select employee_details

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${YELLOW}Usage: $0 <client> <environment> <command> [additional_args]${NC}"
    echo ""
    echo "Clients:"
    echo "  client_a  - Uses DBT_VISHAL_DATASET"
    echo "  client_b  - Uses DBT_client_b_DATASET"
    echo ""
    echo "Environments:"
    echo "  dev   - Development environment"
    echo "  prod  - Production environment"
    echo ""
    echo "Commands:"
    echo "  run     - Run models"
    echo "  test    - Run tests"
    echo "  seed    - Load seed data"
    echo "  build   - Run models and tests"
    echo "  debug   - Test connection"
    echo "  docs    - Generate and serve docs"
    echo ""
    echo "Examples:"
    echo "  $0 client_a dev run"
    echo "  $0 client_b prod test"
    echo "  $0 client_a dev seed"
    echo "  $0 client_b dev build --select employee_details"
}

# Check if at least 3 arguments are provided
if [ $# -lt 3 ]; then
    echo -e "${RED}Error: Insufficient arguments${NC}"
    usage
    exit 1
fi

CLIENT=$1
ENVIRONMENT=$2
COMMAND=$3
shift 3  # Remove first 3 arguments, leaving any additional args

# Validate client
if [[ ! "$CLIENT" =~ ^(client_a|client_b)$ ]]; then
    echo -e "${RED}Error: Invalid client '$CLIENT'. Must be 'client_a' or 'client_b'${NC}"
    usage
    exit 1
fi

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|prod)$ ]]; then
    echo -e "${RED}Error: Invalid environment '$ENVIRONMENT'. Must be 'dev' or 'prod'${NC}"
    usage
    exit 1
fi

# Set target based on client and environment
TARGET="${CLIENT}_${ENVIRONMENT}"

echo -e "${GREEN}Running DBT for:${NC}"
echo -e "  Client: ${YELLOW}$CLIENT${NC}"
echo -e "  Environment: ${YELLOW}$ENVIRONMENT${NC}"
echo -e "  Target: ${YELLOW}$TARGET${NC}"
echo -e "  Command: ${YELLOW}dbt $COMMAND${NC}"
echo ""

# Special handling for docs command
if [ "$COMMAND" = "docs" ]; then
    echo -e "${GREEN}Generating and serving documentation...${NC}"
    dbt docs generate --target $TARGET "$@"
    echo -e "${GREEN}Starting docs server...${NC}"
    dbt docs serve --target $TARGET "$@"
else
    # Run the DBT command with the specified target
    echo -e "${GREEN}Executing: dbt $COMMAND --target $TARGET $*${NC}"
    dbt $COMMAND --target $TARGET "$@"
fi

echo -e "${GREEN}✅ DBT command completed successfully!${NC}"
