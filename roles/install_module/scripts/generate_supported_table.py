#!/usr/bin/env python3
import os
import yaml

print("Generating supported module table")

with open("README.md", "r") as fp:
    lines = fp.readlines()

def autogen_table():

    module_table = ""
    for dir in os.listdir("vars"):
        if os.path.isdir(f"vars/{dir}"):
            for version_file in os.listdir(f"vars/{dir}"):
                with open(f"vars/{dir}/{version_file}") as fp:
                    print(f"Detected module {dir} version file:  {version_file}")
                    version = version_file.split(".")[0]
                    module = yaml.safe_load(fp)[f"{dir}_{version}"]
                    module_table += f"{dir} | {module['version']} | [{dir}_{version}]({module['url']}/tree/{version})\n"

    return f"""<!-- BEGIN_AUTOGEN -->

Module | Version | Url
--- | --- | ---
{module_table}"""

with open("README.md", "w") as fp:
    table = autogen_table()

    for line in lines:
        if line.startswith("<!-- BEGIN_AUTOGEN -->"):
            fp.write(table)
            break
        else:
           fp.write(line)
