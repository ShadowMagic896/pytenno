import os

source = ".\\pytenno"
output = ".\\docs"

ignored_files = [
    "constants.py",
    "conf.py",
]


def iter_py_files(source: str, relative: bool) -> list[str]:
    iterator = os.walk(source) if relative else os.walk(os.path.abspath(source))
    for root, dirs, files in iterator:
        for file in files:
            if (
                file.endswith(".py")
                and not file.startswith("_")
                and not f"{os.path.sep}_" in root
                and not "examples" in root
                and file not in ignored_files
            ):
                yield os.path.join(root, file).strip("./\\").replace("\\", ".")


module_template = """\
{title}
.. automodule:: {module}
    :inherited-members:
    :members:
    """

index_template = """\
Welcome to the documentation of PyTenno.
========================================
.. toctree::
    :maxdepth: 1

    {modules}
    """


def build_files(source: str, output: str):
    generated_files = []

    if not os.path.exists(source):
        raise FileNotFoundError(f"Source directory {source} does not exist")

    if not os.path.exists(output):
        os.mkdir(output)

    for file in iter_py_files(source, True):
        print(f"Building {file}")
        sphinx_path: str = file.removesuffix(".py")
        path_parts: str = sphinx_path.split(".")

        intermediate = os.sep.join(path_parts[1:-1])
        subpath = os.path.join(output, intermediate)
        os.makedirs(subpath, exist_ok=True)

        module: str = ".".join(path_parts)
        title = f"{module}\n{'=' * len(module)}"

        formatted_module_template = module_template.format(
            title=title,
            module=module,
        )
        ref_name = path_parts[1:]
        with open(f"{output}\\{os.sep.join(ref_name)}.rst", "w") as f:
            if "models" in path_parts:
                # tmpl = formatted_module_template + "This is a model used by the API, and it not supposed to be created by the user."
                f.write(formatted_module_template)
            else:
                f.write(formatted_module_template)
            generated_files.append(".".join(ref_name))

    print(f"Generated {len(generated_files)} files")
    print("Building index.rst")
    with open(f"{output}\\index.rst", "w") as out:
        modules = [module.replace(".", "/") for module in generated_files]

        out.write(index_template.format(modules="\n    ".join(modules)))

    print("Copying configuration file [from .\\dodoc\\config_template.py]")
    with open(f".\\dodoc\\config_template.py", "r") as template:
        with open(f"{output}\\conf.py", "w") as target:
            target.write(template.read())

if __name__ == "__main__":
    build_files(source, output)
