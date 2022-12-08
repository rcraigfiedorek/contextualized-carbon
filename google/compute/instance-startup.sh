export EMISSIONS_DB_PASSWORD=$(gcloud secrets versions access 1 --secret="EMISSIONS_DB_PASSWORD")
sudo -E docker compose -f /home/rcraigfiedorek/EmissionsBot/docker-compose.prod.yml down --remove-orphans
sudo -E docker compose -f /home/rcraigfiedorek/EmissionsBot/docker-compose.prod.yml pull
sudo -E docker compose -f /home/rcraigfiedorek/EmissionsBot/docker-compose.prod.yml up --detach
