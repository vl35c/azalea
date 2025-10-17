import os
import re

from typing import Self


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


class Program:
    def __init__(self):
        self.files = {}


class PythonFile:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.classes = {}


class DocFile:
    def __init__(self, path):
        self.path = path
        self.classes = {}


class Class:
    def __init__(self, name: str, inherited_class: Self = None):
        self.name = name
        self.inherited_class = inherited_class
        self.attrs = {}
        self.methods = {}
        self.code = ""


class Method:
    def __init__(self, name: str, static_: bool = False, prop_: bool = False):
        self.name = name
        self.static = static_
        self.prop = prop_
        self.params = {}
        self.code = ""


class Attr:
    def __init__(self, name: str, type_: str = None, ignored: bool = False):
        self.name = name
        self.type_ = type_
        self.ignored = ignored


prop = False
static = False


def parse_python_file(program):
    global prop, static

    for folder in code_files:
        for file_ in code_files[folder]:
            current_class = Class("None")
            current_method = Method("None")

            path = f"{folder}/{file_}"

            with open(path, "r") as file:
                current_file = PythonFile(file_, folder)
                data = file.read()
                prop = False

                for line in data.split("\n"):
                    line = line.strip()

                    if current_method.name == "None":
                        current_class.code += line + "\n"
                    current_method.code += line + "\n"

                    if line.startswith("@property"):
                        prop = True
                    if line.startswith("@staticmethod"):
                        static = True
                    if line.startswith("class"):
                        if inherited_class := re.findall("\\(([\\w_]+)\\)", line):
                            inherited_class = inherited_class[0]
                        else:
                            inherited_class = None

                        current_class = Class(re.findall("class ([a-zA-Z0-9_]+)", line)[0], inherited_class=inherited_class)
                        current_file.classes[current_class.name] = current_class
                        current_method = Method("None")
                    if line.startswith("def"):
                        current_method_name = re.findall("def ([a-zA-Z0-9_]+)", line)[0]
                        current_method = Method(current_method_name, static_=static, prop_=prop)
                        current_class.methods[current_method.name] = current_method

                        params = re.findall(
                            "(?:[^:>] |\\()(\\w+)",
                            line.split(current_method.name)[1].split(")")[0]
                        )

                        for param in params:
                            if param in ["int", "str", "tuple", "list", "dict", "float", "char"]:
                                break
                            current_class.methods[current_method.name].params[param] = Attr(param)
                            try:
                                type_ = re.findall(f"{param}: ([\\w\\[\\]| ,]+)(?:[,)]| =)", line)[0]
                                current_class.methods[current_method.name].params[param].type_ = type_
                            except IndexError:
                                pass

                        static = False
                        prop = False
                    if "self." in line:
                        try:
                            attr = re.findall("self.([a-zA-Z0-9_]+)(?=[ =:]|$)", line)[0]
                            if "# !ignore" in line:
                                current_class.attrs[attr] = Attr(attr, ignored=True)
                            current_class.attrs[attr] = Attr(attr)
                        except IndexError:
                            pass

            program.files[current_file.name] = current_file


def parse_md_file(program):
    current_class = Class("None")
    properties = True

    for file_ in doc_files:
        path = f"{file_}/{doc_files[file_]}"

        current_file = DocFile(file_)

        with open(path, "r") as file:
            data = file.read()

            for line in data.split("\n"):
                if line.startswith("# "):
                    current_class = Class(re.findall("\\w+", line)[0])
                    current_file.classes[current_class.name] = current_class
                if "### PROPERTIES" in line:
                    properties = True
                if "### METHODS" in line:
                    properties = False
                if line.startswith("`"):
                    try:
                        name = re.findall("`([\\w_]+)[(`]", line)[0]
                        if properties:
                            current_class.attrs[name] = Attr(name)
                        else:
                            current_class.methods[name] = Method(name)
                            params = re.findall(
                                "(?:[^:>] |\\()(\\w+)",
                                line.split("-")[0]
                            )
                            if "self" in params:
                                params.remove("self")

                            for param in params:
                                type_ = re.findall(f"{param}: ([\\w\\[\\]| ,]+)(?:[,)]| =)", line)[0]
                                current_class.methods[name].params[param] = Attr(param, type_)

                    except IndexError:
                        pass

        program.files[current_file.path] = current_file


def compare_files(program, args):
    for file in program.files:
        if type(program.files[file]) is DocFile:
            return

        code = program.files[file]
        docs = program.files[code.path]

        classes_to_pop = []

        for c in code.classes:
            if c not in docs.classes:
                classes_to_pop.append(c)

        for c in classes_to_pop:
            if "-i" in args:
                print(f"#parsnip: \x1b[1;31mmissing class   \x1b[0;39m [\x1b[2;34m{c}\x1b[0;39m]")
            elif not "# !ignore" in code.classes[c].code:
                print(f"#parsnip: \x1b[1;31mmissing class   \x1b[0;39m [\x1b[2;34m{c}\x1b[0;39m]")
            code.classes.pop(c)

        for c in code.classes:
            if "# !ignore" in code.classes[c].code:
                continue

            for attr in code.classes[c].attrs:
                if code.classes[c].attrs[attr].ignored:
                    continue

                if attr not in docs.classes[c].attrs:
                    if code.classes[c].inherited_class is None:
                        print(f"#parnsip: \x1b[1;31mmissing attr    \x1b[0;39m [\x1b[33m{c}\x1b[39m.\x1b[2;32m{attr}\x1b[0;39m]")
                    elif attr not in docs.classes[code.classes[c].inherited_class].attrs:
                        print(f"#parsnip: \x1b[1;31mmissing attr    \x1b[0;39m [\x1b[33m{c}\x1b[39m.\x1b[2;32m{attr}\x1b[0;39m]")

            for method in code.classes[c].methods:
                if code.classes[c].methods[method].name == "__init__":
                    continue

                if method not in docs.classes[c].methods:
                    if not code.classes[c].methods[method].prop:
                        if "# !ignore" in code.classes[c].methods[method].code and not "-i" in args:
                            continue
                        print(f"#parsnip: \x1b[1;31mmissing method  \x1b[0;39m [\x1b[33m{c}\x1b[39m.\x1b[2;32m{method}\x1b[0;39m()]")
                else:
                    if not code.classes[c].methods[method].prop:
                        if "# !ignore" in code.classes[c].methods[method].code and not "-i" in args:
                            continue

                        for param in code.classes[c].methods[method].params:
                            p = code.classes[c].methods[method].params[param].name
                            type_ = code.classes[c].methods[method].params[param].type_
                            if p == "self":
                                continue
                            if not p in docs.classes[c].methods[method].params:
                                print(f"#parsnip: \x1b[1;31mmissing param   \x1b[0;39m [\x1b[2;35m{p}\x1b[0;39m] in [\x1b[33m{c}\x1b[39m.\x1b[32m{method}()\x1b[39m]")
                            else:
                                code_type = code.classes[c].methods[method].params[param].type_
                                docs_type = docs.classes[c].methods[method].params[param].type_
                                if code_type != docs_type:
                                    print(f"#parsnip: \x1b[1;31mwrong param type \x1b[0;39m[\x1b[35m{p}\x1b[39m: \x1b[2;36m{docs_type}\x1b[0;39m] from [\x1b[33m{c}\x1b[39m.\x1b[32m{method}()\x1b[39m] should be [\x1b[35m{p}\x1b[39m: \x1b[36m{code_type}\x1b[39m]")


def validate(*args) -> None:
    path = os.getcwd()
    check_folder(path)

    code_files.pop(path)
    doc_files.pop(path)

    program = Program()
    parse_python_file(program)
    parse_md_file(program)
    compare_files(program, *args)
