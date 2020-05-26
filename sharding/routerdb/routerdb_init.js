sh.addShard("Shard1AQIMonitoringReplSet/localhost:27001")
sh.addShard("Shard1AQIMonitoringReplSet/localhost:27002")
sh.addShard("Shard1AQIMonitoringReplSet/localhost:27003")

sh.addShard("Shard2AQIMonitoringReplSet/localhost:27004")
sh.addShard("Shard2AQIMonitoringReplSet/localhost:27005")
sh.addShard("Shard2AQIMonitoringReplSet/localhost:27006")

sh.enableSharding("air_quality_db")

db = db.getSiblingDB('air_quality_db')
db.air_quality_data.ensureIndex( { _id : "hashed" } )
sh.shardCollection( "air_quality_db.air_quality_data", { "_id" : "hashed" } )
