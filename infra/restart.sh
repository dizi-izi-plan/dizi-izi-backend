#!/bin/sh

# Run before script: chmod +x restart.sh

# Check if a command-line argument is passed
if [ $# -eq 0 ]; then
  echo "Need to pass the Docker Compose container name as an argument"
  echo "Allowed argument: 'all', 'frontend', 'backend', 'database', 'nginx', 'certbot'"
  exit 1
fi

# Create container name
if [ "$1" = 'all' ]; then
  container=''
else
  case "$1" in
    frontend|backend|database|nginx|certbot)
      container="$1"
      ;;
    *)
      echo "Incorrect container name: $1. "
      echo "Allowed argument: 'all', 'frontend', 'backend', 'database', 'nginx', 'certbot'"
      exit 1
      ;;
  esac
fi

echo "Download new images"
docker compose pull
echo

if [ -z "$container" ]; then
  echo "Updating all containers"
  docker compose down -v
  docker compose up --force-recreate -d

else
  echo "Updating container: $container"
  echo "Func not realized, use 'all' "
#  docker compose stop
#  docker compose down -v "$container"
#  docker compose up --force-recreate -d "$container"
#  docker compose start
fi

echo "Clean up unused volumes and images"
docker volume prune -f
docker image prune -f
echo

echo "Available containers:"
echo
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
echo
