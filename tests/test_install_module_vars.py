import os

import pytest

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
    "config": dict,
}


INSTALL_MODULE_FILES = [
    os.path.splitext(f)[0]
    for f in os.listdir("roles/install_module/vars")
    if f.endswith(".yml")
]


pytestmark = pytest.mark.parametrize(
    "install_module_var_file", INSTALL_MODULE_FILES, indirect=True
)


def test_install_module_vars_files_valid(install_module_var_file):
    assert len(list(install_module_var_file.data.keys())) == 1
    assert list(install_module_var_file.data.keys())[0] == install_module_var_file.name

    # Make sure all required keys are present
    for key in REQUIRED_KEYS:
        assert key in install_module_var_file.data[install_module_var_file.name]
        assert isinstance(
            install_module_var_file.data[install_module_var_file.name][key],
            REQUIRED_KEYS[key],
        )

    # Check that optional keys, if present, are of correct type
    for key in OPTIONAL_KEYS:
        if key in install_module_var_file.data[install_module_var_file.name]:
            assert isinstance(
                install_module_var_file.data[install_module_var_file.name][key],
                OPTIONAL_KEYS[key],
            )

    # Ensure no additional keys present
    for key in install_module_var_file.data[install_module_var_file.name]:
        assert key in REQUIRED_KEYS or key in OPTIONAL_KEYS


def test_install_module_vars_files_all_module_deps_exist(
    install_module_var_file,
):
    if "module_deps" in install_module_var_file.data[install_module_var_file.name]:
        for module_dep in install_module_var_file.data[install_module_var_file.name][
            "module_deps"
        ]:
            assert module_dep in INSTALL_MODULE_FILES


def test_ensure_version_suffixed(install_module_var_file):
    assert install_module_var_file.name.endswith(
        install_module_var_file.data[install_module_var_file.name]["version"].replace(
            "-", "_"
        )
    ) or install_module_var_file.name.endswith(
        install_module_var_file.data[install_module_var_file.name]["version"].replace(
            ".", "_"
        )
    )


def test_ensure_no_main_or_master_branch(install_module_var_file):
    assert install_module_var_file.data[install_module_var_file.name][
        "version"
    ] not in ["main", "master"]
