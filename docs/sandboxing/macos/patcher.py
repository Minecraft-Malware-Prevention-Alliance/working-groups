import sys
import os

args_dict = {}
for arg in sys.argv[1:]:
    if '=' in arg:
        key, value = arg.split('=')
        args_dict[key] = value
    else:
        args_dict[arg] = True

if args_dict['--dir']:
    if os.path.isfile(args_dict['--dir']) & args_dict['--dir'].endswith('.sb'):
        sandbox_file = args_dict['--dir']
    else:
        print("Invalid file!")
        exit()
else:
    raise Exception('A --dir argument must be there to use --user-patch')

if args_dict['--user-patch']:
    with open(sandbox_file, 'r') as file:
        data = file.readlines()
    for line in data:
        if "$HOME" in line:
            data[data.index(line)] = line.replace("$HOME", os.getenv("HOME"))
    with open(sandbox_file, 'w') as file:
        file.writelines( data )
