import pytest
from pathlib import Path
import os
import yaml
from dataclasses import dataclass


@dataclass
class VarFile:
    name: str
    path: Path
    data: dict


@pytest.fixture
def var_file_reader_factory():
    def var_file_reader(var_file_path: Path) -> dict[str, VarFile]:
        var_file_paths = [f for f in var_file_path.glob("*.yml") if f.is_file()]
        var_files = {}
        for var_file in var_file_paths:
            with open(var_file, "r") as file:
                var_files[os.path.splitext(var_file.name)[0]] = VarFile(
                    name=os.path.splitext(var_file.name)[0],
                    path=var_file,
                    data=yaml.safe_load(file),
                )
        return var_files

    return var_file_reader


@pytest.fixture
def install_module_var_file(var_file_reader_factory, request) -> VarFile:
    return var_file_reader_factory(Path("roles/install_module/vars"))[request.param]


@pytest.fixture
def deploy_ioc_var_file(var_file_reader_factory, request) -> VarFile:
    return var_file_reader_factory(Path("roles/deploy_ioc/vars"))[request.param]
