import io
import os
import sys
from typing import Literal

def upload(repo: Literal["pypi", "testpypi"] = "testpypi") -> None:
    [os.remove(f) for f in os.listdir("./dist")] # Clear distros
    os.system(f"py -m build") # Build wheels
    os.system(f"py -m twine upload -r {repo} ./dist") # Upload wheels to repo

if __name__ == "__main__":
    upload()