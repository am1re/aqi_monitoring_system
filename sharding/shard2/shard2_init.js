config = 
    {"_id" : "Shard2AQIMonitoringReplSet", 
        members : [
            {"_id" : 0, host : "localhost:27004"},
            {"_id" : 1, host : "localhost:27005"},
            {"_id" : 2, host : "localhost:27006", arbiterOnly : true}
        ]
    };

rs.initiate(config);
rs.status();
