mongo localhost:27003/admin --eval "db.shutdownServer()"
mongo localhost:27002/admin --eval "db.shutdownServer()"
mongo localhost:27001/admin --eval "db.adminCommand({ shutdown: 1, force: true })"
