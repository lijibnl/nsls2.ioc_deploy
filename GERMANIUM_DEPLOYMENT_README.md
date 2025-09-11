# Germanium Detector IOC Deployment Guide

This guide explains how to deploy Germanium detector IOCs using the `nsls2.ioc_deploy` Ansible collection.

## Overview

The Germanium detector IOC is based on the NSLS2EM module and provides EPICS support for Germanium detectors. The deployment process involves:

1. Installing the NSLS2EM module and its dependencies
2. Deploying IOC instances with device-specific configurations
3. Setting up systemd services for IOC management

## Prerequisites

### System Requirements
- Linux system with EPICS Base installed
- Ansible 2.14+ and Python 3.8+
- Network access to the Germanium detector hardware
- Proper network configuration for EPICS communication

### Required EPICS Modules
The following EPICS modules must be available on the target system:
- EPICS Base
- asyn
- autosave
- busy
- calc
- sncseq
- sscan
- deviocstats
- AreaDetector (ADCore)
- PSCDRV

## Files Created

### 1. Module Configuration
- `roles/install_module/vars/nsls2em_05e8a65.yml` - NSLS2EM module configuration

### 2. Device Role
- `roles/germanium/` - Complete device role for Germanium detectors
  - `example.yml` - Example IOC configuration
  - `schema.yml` - Configuration schema validation
  - `README.md` - Device-specific documentation
  - `tasks/main.yml` - Deployment tasks
  - `templates/base.cmd.j2` - EPICS startup commands
  - `templates/calibration.cmd.j2` - Calibration template

### 3. Integration Files
- `roles/deploy_ioc/vars/germanium.yml` - Integration with deploy_ioc system

### 4. Example Files
- `example-germanium-deployment.yml` - Example playbook
- `example-host-config.yml` - Example host configuration
- `example-inventory.yml` - Example inventory

## Configuration

### Host Configuration

Create a host configuration file (e.g., `host-config.yml`) with the following structure:

```yaml
# Host-specific settings
host_softioc_user: "softioc"
host_softioc_group: "n2sn-instadmin"
host_epics_intf: "192.168.1.50"

# IOC configurations
germanium-01:
  type: germanium
  environment:
    ENGINEER: "Dr. Smith"
    PREFIX: "XF:31ID1-ES{GE:01}"
    SYS: "XF:31ID1-ES"
    DEV: "GE:01"
    PORT: "GE01"
    IP: "192.168.1.100"
    RING_SIZE: "32768"
    DEVICE_IP: "192.168.1.100"
    DEVICE_SN: "GE001"
  substitutions:
    quadEM_nsls2em:
      - filepath: "quadEM_nsls2em.template"
        pattern: ["P=$(SYS)", "R={$(DEV)}", "PORT=$(PORT)", "ADDR=0", "TIMEOUT=1"]
        instances: [["XF:31ID1-ES", "GE:01", "GE01", "0", "1"]]
    # ... additional substitutions
```

### Environment Variables

Each Germanium IOC requires the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `ENGINEER` | Name of responsible engineer | "Dr. Smith" |
| `PREFIX` | EPICS PV prefix | "XF:31ID1-ES{GE:01}" |
| `SYS` | System prefix | "XF:31ID1-ES" |
| `DEV` | Device name | "GE:01" |
| `PORT` | Port name | "GE01" |
| `IP` | Device IP address | "192.168.1.100" |
| `RING_SIZE` | Ring buffer size | "32768" |
| `DEVICE_IP` | Physical device IP | "192.168.1.100" |
| `DEVICE_SN` | Device serial number | "GE001" |

## Deployment

### 1. Install the Collection

```bash
# Install required Ansible collections
ansible-galaxy collection install -r collections/requirements.yml

# Install the nsls2.ioc_deploy collection
ansible-galaxy collection install .
```

### 2. Create Inventory

Create an inventory file (e.g., `inventory.yml`):

```yaml
all:
  children:
    ioc_hosts:
      hosts:
        ioc-host-01:
          ansible_host: 192.168.1.50
          ansible_user: ansible
          ansible_become: true
```

### 3. Create Playbook

Create a playbook (e.g., `deploy-germanium.yml`):

```yaml
---
- name: Deploy Germanium Detector IOCs
  hosts: ioc_hosts
  gather_facts: true
  vars:
    host_config: "{{ lookup('file', 'host-config.yml') | from_yaml }}"
    deploy_ioc_target: "all"
  
  roles:
    - nsls2.ioc_deploy.deploy_ioc
```

### 4. Run Deployment

```bash
ansible-playbook -i inventory.yml deploy-germanium.yml
```

## Post-Deployment

### IOC Management

After deployment, IOCs can be managed using the `manage_iocs` role:

```bash
# Start an IOC
ansible-playbook -i inventory.yml manage-iocs.yml -e "manage_iocs_command=start" -e "manage_iocs_subcommand=germanium-01"

# Stop an IOC
ansible-playbook -i inventory.yml manage-iocs.yml -e "manage_iocs_command=stop" -e "manage_iocs_subcommand=germanium-01"

# Restart an IOC
ansible-playbook -i inventory.yml manage-iocs.yml -e "manage_iocs_command=restart" -e "manage_iocs_subcommand=germanium-01"
```

### Verification

1. Check IOC status:
   ```bash
   systemctl status softioc-germanium-01
   ```

2. Check IOC logs:
   ```bash
   journalctl -u softioc-germanium-01 -f
   ```

3. Test EPICS PVs:
   ```bash
   caget XF:31ID1-ES{GE:01}:Status
   ```

## Troubleshooting

### Common Issues

1. **Module not found**: Ensure all required EPICS modules are installed
2. **Network connectivity**: Verify device IP addresses and network configuration
3. **Permission issues**: Check that the softioc user has proper permissions
4. **Port conflicts**: Ensure unique port numbers for each IOC

### Logs

- IOC logs: `/var/log/softioc/<ioc-name>/`
- Systemd logs: `journalctl -u softioc-<ioc-name>`
- EPICS logs: Check IOC console output

## Customization

### Calibration

Device-specific calibration can be added by modifying the generated calibration file:
`/epics/iocs/<ioc-name>/calibration/<device-sn>.cmd`

### Database Templates

Additional database templates can be loaded by adding them to the `substitutions` section of the host configuration.

### Environment Variables

Additional environment variables can be added to the `environment` section of each IOC configuration.

## Support

For issues with the Germanium IOC deployment:

1. Check the IOC logs for error messages
2. Verify network connectivity to the detector hardware
3. Ensure all required EPICS modules are properly installed
4. Review the host configuration for syntax errors

## References

- [NSLS2EM Module Documentation](https://github.com/lijibnl/GermaniumIOC)
- [nsls2.ioc_deploy Collection Documentation](README.md)
- [EPICS AreaDetector Documentation](https://areadetector.github.io/master/index.html)


