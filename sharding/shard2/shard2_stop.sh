mongo localhost:27006/admin --eval "db.shutdownServer()"
mongo localhost:27005/admin --eval "db.shutdownServer()"
mongo localhost:27004/admin --eval "db.adminCommand({ shutdown: 1, force: true })"
