rmdir /Q /S  "./build"
py -m sphinx.cmd.build -b "html" "." "./build"