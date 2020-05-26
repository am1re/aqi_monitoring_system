# aqi_monitoring_system

scrapy crawl iqair for filling database

python menu.py for visualization

python backup.py backup/restore [filepath] for saving or restoring data


cd replication
sh start_dbs.sh/stop_dbs.sh
to start/stop mongo with configured replica sets

cd sharding
sh start.sh/stop.sh/delete_data.sh
to start/stop mongo with configured local sharding
and remove all local dbs
