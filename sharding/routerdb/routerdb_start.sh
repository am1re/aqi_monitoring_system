mkdir -p routerdb

mongos --port 27010 --configdb configserver/localhost:27007,localhost:27008,localhost:27009 --fork --logpath routerdb/routerdb.log

sleep 1s
ps -ef | grep mongo

mongo -port 27010 routerdb_init.js
