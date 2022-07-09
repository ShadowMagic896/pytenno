from encodings.utf_8 import encode
import sys, os
from textwrap import dedent

target_dir = os.path.abspath("./pytenno")
path_sep = "."
print(target_dir)

def iter_py_files(targ: str):
    for root, dirs, files in os.walk(targ):
        # print(root, dirs, files)
        if root.startswith("_"):
            continue
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                yield os.path.join(root, file)


end = """
All Documentation
=================

This is a list of all the documentation for the PyTenno library.
"""
for file in iter_py_files(target_dir):
    relative = os.path.relpath(file, target_dir)[:-3]
    relative = path_sep.join(relative.split(os.path.sep))
    end += dedent(f"""
    .. automodule:: pytenno.{relative}
        :show-inheritance:
        :members:
        :undoc-members:
    """)

with open("docs/all.rst", "w") as f:
    print(end, file=f)
