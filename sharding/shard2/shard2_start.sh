mkdir -p shard2a shard2b shard2c

mongod --shardsvr --dbpath shard2a --port 27004 --replSet Shard2AQIMonitoringReplSet --fork --logpath shard2a/shard2a.log &
mongod --shardsvr --dbpath shard2b --port 27005 --replSet Shard2AQIMonitoringReplSet --fork --logpath shard2b/shard2b.log &
mongod --shardsvr --dbpath shard2c --port 27006 --replSet Shard2AQIMonitoringReplSet --fork --logpath shard2c/shard2c.log &

sleep 1s
ps -ef | grep mongo

mongo -port 27004 shard2_init.js
