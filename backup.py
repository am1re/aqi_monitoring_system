import sys

from src import database

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2 or args[0] not in ('restore', 'backup'):
        print('Invalid arguments! Use "backup [filepath]" or "restore [filepath]"')
        exit()

    operation_type, filename = args
    if operation_type == 'backup':
        database.backup(filename)
    else:
        database.restore(filename)
