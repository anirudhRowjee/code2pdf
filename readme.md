# Code2PDF

## This is a python program to generate a markdown file containing all the code present in the files of a directory

Steps
1. Parse directory and get paths to all files necessary, with necessary ignores (env, .pyc, etc..)
2. Open markdown file and get file contents one by one, write filepath as header and code in syntax blocks (delimited by \`\`\`)
3. Save the file as markdown or PDF and finish the process.
