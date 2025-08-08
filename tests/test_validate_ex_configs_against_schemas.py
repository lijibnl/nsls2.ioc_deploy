import os

import pytest
import yamale
import yaml

COMMON_ROLES = [
    "install_module",
    "deploy_ioc",
    "deploy_common",
    "host_info",
    "manage_iocs",
]

DEVICE_ROLES = [role for role in os.listdir("roles") if role not in COMMON_ROLES]


class IOCTypeValidator(yamale.validators.Validator):
    tag = "ioc_type"

    def _is_valid(self, value):
        return value in DEVICE_ROLES


pytestmark = pytest.mark.parametrize("device_role", DEVICE_ROLES)


def test_ensure_example_present(device_role):
    assert os.path.exists(os.path.join("roles", device_role, "example.yml")), (
        f"Example configuration file for {device_role} role is missing."
    )


def test_ensure_required_schema_present(device_role):
    schema_path = os.path.join("roles", device_role, "schema.yml")
    assert os.path.exists(schema_path), f"Schema file for {device_role} role is missing at {schema_path}."


def test_ensure_example_validates_with_base_schema(device_role):
    with open(os.path.join("roles", device_role, "example.yml")) as fp:
        example_data = yaml.safe_load(fp)
        ioc_name = list(example_data.keys())[0]
        ioc_config = example_data[ioc_name]

    validators = yamale.validators.DefaultValidators.copy()
    validators["ioc_type"] = IOCTypeValidator

    data = yamale.make_data(content=yaml.dump(ioc_config))
    base_schema = yamale.make_schema("roles/deploy_ioc/schema.yml", validators=validators)

    try:
        yamale.validate(base_schema, data, strict=False)
    except Exception as e:
        pytest.fail(
            f"Ex. config for {ioc_name} in {device_role} role doesn't conform to the base IOC config schema: {e}"
        )


def test_ensure_example_validates_with_role_specific_schema(device_role):
    schema_path = os.path.join("roles", device_role, "schema.yml")
    example_path = os.path.join("roles", device_role, "example.yml")

    schema = yamale.make_schema(schema_path)

    with open(example_path) as fp:
        example_data = yaml.safe_load(fp)
        ioc_name = list(example_data.keys())[0]
        ioc_config = example_data[ioc_name]

    data = yamale.make_data(content=yaml.dump(ioc_config))

    try:
        yamale.validate(schema, data, strict=False)
    except yamale.YamaleError as e:
        pytest.fail(f"Ex. config for {ioc_name} in {device_role} role doesn't conform to the role-specific schema: {e}")
