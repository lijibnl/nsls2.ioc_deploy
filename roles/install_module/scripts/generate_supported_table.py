#!/usr/bin/env python3
import os

import yaml


def autogen_table():

    module_table = ""
    for module_dir in os.listdir("vars"):
        if os.path.isdir(f"vars/{module_dir}"):
            for version_file in os.listdir(f"vars/{module_dir}"):
                with open(f"vars/{module_dir}/{version_file}") as fp:
                    print(f"Found {module_dir} version file: {version_file}")
                    version = version_file.split(".")[0]
                    module = yaml.safe_load(fp)[f"{module_dir}_{version}"]
                    module_table += (
                        f"{module_dir} | {module['version']} |"
                        f" [{module_dir}_{version}]({module['url']}/tree/{version})\n"
                    )

    return f"""<!-- BEGIN_AUTOGEN -->

Module | Version | Url
--- | --- | ---
{module_table}"""


def update_table_in_readme():
    print("Generating supported module table")

    with open("README.md", "r") as fp:
        lines = fp.readlines()

    with open("README.md", "w") as fp:
        table = autogen_table()

        for line in lines:
            if line.startswith("<!-- BEGIN_AUTOGEN -->"):
                fp.write(table)
                break
            fp.write(line)


if __name__ == "__main__":
    update_table_in_readme()
