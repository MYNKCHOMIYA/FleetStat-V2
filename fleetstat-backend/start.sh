#!/bin/bash
# ============================================================
# FleetStat Backend — Start Script
# ============================================================
# Usage:
#   ./start.sh          → Start everything in Docker (Postgres + API)
#   ./start.sh local    → Start Docker Postgres + local uvicorn (with --reload)
#   ./start.sh down     → Stop all Docker containers
#   ./start.sh logs     → View live logs from all containers
#   ./start.sh rebuild  → Force rebuild and restart
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      FleetStat Backend Launcher      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"

case "${1:-docker}" in
  local)
    echo -e "\n${YELLOW}[1/3] Starting Docker Postgres...${NC}"
    docker compose up -d postgres
    
    echo -e "${YELLOW}[2/3] Waiting for Postgres to be healthy...${NC}"
    until docker compose exec postgres pg_isready -U postgres -d fleetstat > /dev/null 2>&1; do
      echo -n "."
      sleep 1
    done
    echo -e " ${GREEN}Ready!${NC}"
    
    echo -e "${YELLOW}[3/3] Starting local uvicorn with .env.local...${NC}"
    echo -e "${GREEN}→ API will be available at http://localhost:8000${NC}"
    echo -e "${GREEN}→ Database: Docker Postgres on port 5433${NC}"
    echo ""
    
    # Use .env.local for local development
    cp .env .env.docker.bak 2>/dev/null || true
    cp .env.local .env
    
    # Run uvicorn locally with auto-reload
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    
    # Restore Docker .env when done
    cp .env.docker.bak .env 2>/dev/null || true
    ;;
    
  down)
    echo -e "\n${YELLOW}Stopping all containers...${NC}"
    docker compose down
    echo -e "${GREEN}All containers stopped.${NC}"
    ;;
    
  logs)
    echo -e "\n${YELLOW}Showing live logs (Ctrl+C to exit)...${NC}"
    docker compose logs -f
    ;;
    
  rebuild)
    echo -e "\n${YELLOW}Rebuilding and restarting...${NC}"
    docker compose down
    docker compose up -d --build
    echo -e "\n${GREEN}Rebuild complete!${NC}"
    docker compose logs -f --tail 20
    ;;
    
  docker|"")
    echo -e "\n${YELLOW}[1/2] Building and starting all containers...${NC}"
    docker compose up -d --build
    
    echo -e "${YELLOW}[2/2] Waiting for services to be healthy...${NC}"
    sleep 3
    
    # Check API health
    if curl -s http://localhost:8001/ > /dev/null 2>&1; then
      echo -e "${GREEN}✓ API is running at http://localhost:8001${NC}"
    else
      echo -e "${YELLOW}⏳ API is still starting up... check with: docker compose logs -f${NC}"
    fi
    
    echo -e "${GREEN}✓ Postgres is running on port 5433${NC}"
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║       FleetStat is running! 🚀      ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  API:      http://localhost:8001     ║${NC}"
    echo -e "${GREEN}║  Postgres: localhost:5433            ║${NC}"
    echo -e "${GREEN}║  Frontend: http://localhost:5173     ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
    ;;
    
  *)
    echo "Usage: ./start.sh [docker|local|down|logs|rebuild]"
    exit 1
    ;;
esac
