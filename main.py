import glob, configparser, os

'''
Ignore can be a set of extensions or directories (similar to .gitignore)
'''

def ignore_config_parser(path_ignore):
    '''
    parser for .ini style ignore config file
    '''

    config = configparser.ConfigParser(allow_no_value = True)
    config.read(path_ignore)
    directories = [x[0] for x in config.items('directories')]
    extensions = [x[0] for x in config.items('extensions')]
    specifics = [x[0] for x in config.items('specifics')]

    data = {
        'directories' : directories,
        'extensions' : extensions,
        'specifics' : specifics,
    }

    return data

def can_file_be_ignored(filepath, ignore):
    '''
    Tells us if a file can be ignored per ignore configurations
    args -
        > filepath - full path of files
        > ignore - ignore config object
    '''
    # check for directory violations
    filepath_dirs = filepath.split('/')
    for level in filepath_dirs:
        if level in ignore['directories']:
            return True

    # check for extension violations
    filename = filepath_dirs[-1]
    if filename in ignore['specifics']:
        return True

    extension = os.path.split(filename)[1]
    if extension in ignore['extensions']:
        return True

    return False

def get_files_in_directory(dirname, ignore):
    '''
    check all files in a directory to see which can be ignored per ignore settings
    '''
    files = [f for f in glob.iglob(dirname + '**/**', recursive=True)]
    files = [x for x in files if not can_file_be_ignored(x, ignore)]
    files = [x for x in files if not os.path.isdir(x)]
    print(files)
    return files


template = '''
## {path}
```{language}

{code}

```

'''

def generate_markdown_file(filepaths, targetpath):
    target = open('{target}'.format(target=targetpath), 'w+')
    for file in filepaths:
        temp = open(file, 'r+')
        lines = temp.readlines()
        dump = ""
        for line in lines:
            dump += line
        dump = (dump.rstrip()).lstrip()
        present = template.format(language='python', path=file, code=dump)
        target.write(present)
    target.close()


if __name__ == '__main__':
    logo = '''
               _      ___                       _       _                     
              | |    |__ \                     | |     | |                    
  ___ ___   __| | ___   ) |_ __ ___   __ _ _ __| | ____| | _____      ___ __  
 / __/ _ \ / _` |/ _ \ / /| '_ ` _ \ / _` | '__| |/ / _` |/ _ \ \ /\ / / '_ \ 
| (_| (_) | (_| |  __// /_| | | | | | (_| | |  |   < (_| | (_) \ V  V /| | | |
 \___\___/ \__,_|\___|____|_| |_| |_|\__,_|_|  |_|\_\__,_|\___/ \_/\_/ |_| |_|

'''
    print(logo)
    print(" Welcome to code2markdown!")
    projpath = input("Please enter path of folder to capture  >>> ")
    targetname = input("Enter the path/name of the file to write to (eg - 'test.md' ) >>> ")
    ignorepath = input("Enter ignorefile path/filename >>> ")
    ignore = ignore_config_parser(ignorepath)
    print(" Processing ... ")
    files = get_files_in_directory(projpath, ignore)
    print(" Generating markdown file ... ")
    generate_markdown_file(files, targetname)
    print(" Successfully generated at {filename}".format(filename=targetname))





