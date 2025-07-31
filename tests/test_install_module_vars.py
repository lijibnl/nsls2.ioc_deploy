import os
from typing import Callable

import pytest
import yaml

INSTALL_MODULE_VARS_DIR = "roles/install_module/vars"

REQUIRED_KEYS: dict[str, type] = {
    "name": str,
    "url": str,
    "version": str,
}

OPTIONAL_KEYS: dict[str, type] = {
    "include_base_ad_config": bool,
    "module_deps": list,
    "pkg_deps": list,
    "epics_deps": list,
    "compilation_command": str,
}

INSTALL_MODULE_VARS_FILES = os.listdir(INSTALL_MODULE_VARS_DIR)


@pytest.fixture
def var_file_parser() -> Callable[[str], tuple[str, dict, dict]]:
    def parse_var_file(var_file: str):
        module_name_and_ver = os.path.splitext(var_file)[0]
        file_path = os.path.join(INSTALL_MODULE_VARS_DIR, var_file)
        with open(file_path, "r") as fp:
            module_config_var = yaml.safe_load(fp)
            module_config_dict = module_config_var[module_name_and_ver]

        return module_name_and_ver, module_config_var, module_config_dict

    return parse_var_file


@pytest.mark.parametrize("var_file", INSTALL_MODULE_VARS_FILES)
def test_install_module_vars_files_valid(var_file):
    module_name_and_ver = os.path.splitext(var_file)[0]
    file_path = os.path.join(INSTALL_MODULE_VARS_DIR, var_file)
    assert os.path.isfile(file_path)
    with open(file_path, "r") as fp:
        module_config_var = yaml.safe_load(fp)

        assert len(list(module_config_var.keys())) == 1
        assert list(module_config_var.keys())[0] == module_name_and_ver

        module_config_dict = module_config_var[module_name_and_ver]

        # Make sure all required keys are present
        for key in REQUIRED_KEYS:
            assert key in module_config_dict
            assert isinstance(module_config_dict[key], REQUIRED_KEYS[key])

        # Check that optional keys, if present, are of correct type
        for key in OPTIONAL_KEYS:
            if key in module_config_dict:
                assert isinstance(module_config_dict[key], OPTIONAL_KEYS[key])

        # Ensure no additional keys present
        for key in module_config_dict:
            assert key in REQUIRED_KEYS or key in OPTIONAL_KEYS


@pytest.mark.parametrize("var_file", INSTALL_MODULE_VARS_FILES)
def test_install_module_vars_files_all_module_deps_exist(var_file, var_file_parser):
    module_name_and_ver, module_config_var, _ = var_file_parser(var_file)
    if "module_deps" in module_config_var[module_name_and_ver]:
        for module_dep in module_config_var[module_name_and_ver]["module_deps"]:
            assert f"{module_dep}.yml" in INSTALL_MODULE_VARS_FILES


@pytest.mark.parametrize("var_file", INSTALL_MODULE_VARS_FILES)
def test_ensure_version_suffixed(var_file, var_file_parser):
    module_name_and_ver, _, module_config_dict = var_file_parser(var_file)
    assert module_name_and_ver.endswith(
        module_config_dict["version"].replace("-", "_")
    ) or module_name_and_ver.endswith(module_config_dict["version"].replace(".", "_"))


@pytest.mark.parametrize("var_file", INSTALL_MODULE_VARS_FILES)
def test_ensure_no_main_or_master_branch(var_file, var_file_parser):
    _, _, module_config_dict = var_file_parser(var_file)
    assert module_config_dict["version"] not in ["main", "master"]
