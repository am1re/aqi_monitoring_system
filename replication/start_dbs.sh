mkdir -p db1 db2 db3

mongod --dbpath db1 --port 27001 --replSet AQIMonitoringReplSet --fork --logpath db1/db1.log &
mongod --dbpath db2 --port 27002 --replSet AQIMonitoringReplSet --fork --logpath db2/db2.log &
mongod --dbpath db3 --port 27003 --replSet AQIMonitoringReplSet --fork --logpath db3/db3.log &

sleep 3s
ps -ef | grep mongod

sleep 3s
mongo -port 27001 init_replicasets.js
