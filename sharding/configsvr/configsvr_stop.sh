mongo localhost:27009/admin --eval "db.adminCommand({ shutdown: 1, force: true })"
mongo localhost:27008/admin --eval "db.adminCommand({ shutdown: 1, force: true })"
mongo localhost:27007/admin --eval "db.adminCommand({ shutdown: 1, force: true })"
