# Germanium Detector IOC

Ansible role for deploying Germanium detector IOC instances using the GERMANIUM module.

## Configuration

The Germanium IOC requires the following environment variables:

- `ENGINEER`: Name of the engineer responsible for this IOC
- `PREFIX`: EPICS PV prefix for the IOC
- `SYS`: System prefix
- `DEV`: Device name
- `PORT`: Port name for the device
- `IP`: IP address of the device
- `DEVICE_IP`: IP address of the physical device

## Substitutions

The role supports loading the following database templates:

- `germanium.template`: Germanium detector configuration
- `germanium_pscdrv.template`: PSC driver configuration

## Dependencies

This role requires the GERMANIUM module to be installed, which includes:
- AreaDetector support
- PSC driver
- Various EPICS support modules (asyn, autosave, busy, calc, etc.)

