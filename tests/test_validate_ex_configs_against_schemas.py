import os

import pytest
import yamale
import yaml
from schema import Optional, Or, Schema

COMMON_ROLES = [
    "install_module",
    "deploy_ioc",
    "deploy_common",
    "host_info",
    "manage_iocs",
]

DEVICE_ROLES = [role for role in os.listdir("roles") if role not in COMMON_ROLES]

BASE_IOC_CONFIG_SCHEMA = Schema(
    {
        "type": Or(*DEVICE_ROLES),
        "environment": {str: Or(str, int, float)},
        Optional("substitutions"): {
            str: Or(
                {
                    "templates": [
                        {
                            "filepath": str,
                            "pattern": [str],
                            "instances": [[str, int, float]],
                        }
                    ],
                    Optional("template_macros"): str,
                    Optional("load_as_template"): bool,
                },
                [{"filepath": str, "pattern": [str], "instances": [[str, int, float]]}],
            )
        },
        Optional("required_module"): str,
        Optional("executable"): str,
    },
    ignore_extra_keys=True,
)


pytestmark = pytest.mark.parametrize("device_role", DEVICE_ROLES)


def test_ensure_example_present(device_role):
    assert os.path.exists(os.path.join("roles", device_role, "example.yml")), (
        f"Example configuration file for {device_role} role is missing."
    )


def test_ensure_required_schema_present(device_role):
    schema_path = os.path.join("roles", device_role, "schema.yml")
    assert os.path.exists(schema_path), (
        f"Schema file for {device_role} role is missing at {schema_path}."
    )


def test_ensure_example_validates_with_base_schema(device_role):
    with open(os.path.join("roles", device_role, "example.yml"), "r") as fp:
        example_data = yaml.safe_load(fp)
        ioc_name = list(example_data.keys())[0]
        ioc_config = example_data[ioc_name]
        try:
            BASE_IOC_CONFIG_SCHEMA.validate(ioc_config)
        except Exception as e:
            pytest.fail(
                f"Example configuration for {ioc_name} in {device_role} role does not conform to the base IOC config schema: {e}"
            )


def test_ensure_example_validates_with_role_specific_schema(device_role):
    schema_path = os.path.join("roles", device_role, "schema.yml")
    example_path = os.path.join("roles", device_role, "example.yml")

    schema = yamale.make_schema(schema_path)

    with open(example_path, "r") as fp:
        example_data = yaml.safe_load(fp)
        ioc_name = list(example_data.keys())[0]
        ioc_config = example_data[ioc_name]

    data = yamale.make_data(content=yaml.dump(ioc_config))

    try:
        yamale.validate(schema, data, strict=False)
    except yamale.YamaleError as e:
        pytest.fail(
            f"Example configuration for {ioc_name} in {device_role} role does not conform to the role-specific schema: {e}"
        )
