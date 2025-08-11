#!/bin/bash

# Airflow Management Script
# Usage: ./airflow.sh [start|stop|restart|logs|status]

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${YELLOW}Usage: $0 [start|stop|restart|logs|status|init]${NC}"
    echo ""
    echo "Commands:"
    echo "  start     - Start Airflow services"
    echo "  stop      - Stop Airflow services"
    echo "  restart   - Restart Airflow services"
    echo "  logs      - Show Airflow logs"
    echo "  status    - Show service status"
    echo "  init      - Initialize Airflow (first time setup)"
    echo "  cleanup   - Clean up volumes and data"
    echo ""
    echo "Examples:"
    echo "  $0 init     # First time setup"
    echo "  $0 start    # Start services"
    echo "  $0 logs     # View logs"
}

# Check if Docker and Docker Compose are installed
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed${NC}"
        exit 1
    fi
}

# Initialize Airflow (first time setup)
init_airflow() {
    echo -e "${GREEN}🚀 Initializing Airflow...${NC}"
    
    # Set permissions for Airflow directories
    echo -e "${BLUE}Setting up directories...${NC}"
    mkdir -p ./dags ./logs ./plugins ./config
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo -e "${BLUE}Creating .env file...${NC}"
        echo "AIRFLOW_UID=$(id -u)" > .env
        echo "AIRFLOW_PROJ_DIR=." >> .env
        echo "DBT_PROJ_DIR=../" >> .env
        echo "_AIRFLOW_WWW_USER_USERNAME=airflow" >> .env
        echo "_AIRFLOW_WWW_USER_PASSWORD=airflow" >> .env
    fi
    
    # Initialize the database
    echo -e "${BLUE}Initializing Airflow database...${NC}"
    docker-compose up airflow-init
    
    echo -e "${GREEN}✅ Airflow initialization complete!${NC}"
    echo -e "${YELLOW}You can now run: ./airflow.sh start${NC}"
}

# Start Airflow services
start_airflow() {
    echo -e "${GREEN}🚀 Starting Airflow services...${NC}"
    docker-compose up -d
    
    echo -e "${GREEN}✅ Airflow started successfully!${NC}"
    echo -e "${YELLOW}Web UI: http://localhost:8080${NC}"
    echo -e "${YELLOW}Username: airflow${NC}"
    echo -e "${YELLOW}Password: airflow${NC}"
}

# Stop Airflow services
stop_airflow() {
    echo -e "${YELLOW}🛑 Stopping Airflow services...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Airflow stopped${NC}"
}

# Restart Airflow services
restart_airflow() {
    echo -e "${YELLOW}🔄 Restarting Airflow services...${NC}"
    docker-compose restart
    echo -e "${GREEN}✅ Airflow restarted${NC}"
}

# Show Airflow logs
show_logs() {
    echo -e "${BLUE}📋 Showing Airflow logs...${NC}"
    docker-compose logs -f
}

# Show service status
show_status() {
    echo -e "${BLUE}📊 Airflow service status:${NC}"
    docker-compose ps
}

# Clean up volumes and data
cleanup_airflow() {
    echo -e "${RED}⚠️  This will remove all Airflow data including task history!${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🧹 Cleaning up Airflow...${NC}"
        docker-compose down -v
        docker volume prune -f
        echo -e "${GREEN}✅ Cleanup complete${NC}"
    else
        echo -e "${BLUE}Cleanup cancelled${NC}"
    fi
}

# Main script logic
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

# Check dependencies
check_dependencies

# Change to airflow directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$1" in
    init)
        init_airflow
        ;;
    start)
        start_airflow
        ;;
    stop)
        stop_airflow
        ;;
    restart)
        restart_airflow
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup_airflow
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        usage
        exit 1
        ;;
esac
