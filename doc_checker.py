import os
import re


class File:
    def __init__(self, class_: str, inherited_class: str, attrs: list[str], methods: list[str], path: str):
        self.class_ = class_
        self.inherited_class = inherited_class
        self.attrs = attrs
        self.methods = methods
        self.path = path


code_files = {}
doc_files = {}

files = {}

def check_files():
    for folder in code_files:
        for file in code_files[folder]:
            with open(os.path.join(folder, file), 'r') as f:
                data = f.read()
                
                if "#!ignore" in data:
                    continue

                data = data.split("class")[1]

                _class = re.findall("([a-zA-Z0-9_]+)", data)[0]
                inherited_class = re.findall("[A-Z][a-zA-Z0-9_]+\\(([a-zA-Z0-9_]+)\\):", data)
                properties = re.findall("self\\.([a-zA-Z0-9_]+)", data)
                at_properties = re.findall("@property[.\n\t\r]+.+def ([a-zA-Z0-9_]+)", data)
                methods = re.findall("def ([a-zA-Z0-9_]+)", data)

                for p in at_properties + ["__init__"]:  # remove @property and __init__ function from methods
                    if p in methods:
                        methods.remove(p)

                for index, method in enumerate(methods):
                    if method == "__init__":
                        methods = methods[:index]

                properties = list(set(properties)) + at_properties

                for p in methods:
                    if p in properties:
                        properties.remove(p)

                if len(inherited_class) > 0:
                    inherited_class = inherited_class[0]
                else:
                    inherited_class = None

                files.update({_class: File(_class, inherited_class, properties, methods, folder)})

def check_folder(path: str):
    for _dir in os.listdir(path):
        if _dir.startswith('.') or _dir.startswith('__'):
            continue
        if os.path.isdir(_dir):
            check_folder(f'{path}/{_dir}')

    for file in os.listdir(path):
        if file.endswith('.py'):
            if path not in code_files:
                code_files[path] = [file]
                continue
            code_files[path].append(file)
        if file.endswith('.md'):
            doc_files[path] = file

def remove_inherited_traits():
    for name, file in files.items():
        if file.inherited_class is not None:
            for attr in files[file.inherited_class].attrs:
                if attr in file.attrs:
                    file.attrs.remove(attr)

            for method in files[file.inherited_class].methods:
                if method in file.methods:
                    file.methods.remove(method)

def find_in_docs():
    for name, file in files.items():
        with open(f'{file.path}/{doc_files[file.path]}', 'r') as f:
            data = f.read()

            for attr in file.attrs:
                if attr not in data:
                    print(f"#DOCS: attr   \x1b[1;31m[{name}.{attr}]\x1b[0;39m not found!")

            for method in file.methods:
                if method not in data:
                    print(f"#DOCS: method \x1b[1;31m[{name}.{method}()]\x1b[0;39m not found!")

def validate() -> None:
    path = os.getcwd()
    check_folder(path)

    code_files.pop(path)
    doc_files.pop(path)

    check_files()
    remove_inherited_traits()

    find_in_docs()
