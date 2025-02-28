# Host Information Extraction

This role is responsible for extracting some information from the host configuration and placing it in variables with standard names.

It also uses some of the given host configuration to set some additional facts automatically.

## Usage

This role should be added at the top of any dependant roles to parse the read `host_config` dictionary.

First, in your playbook, use `nsls2.general.github_vars_facts` to fetch config for the given host:

```Yaml
    - name: Load host configuration
      nsls2.general.github_vars_facts:
        path: "host_vars/{{ inventory_hostname }}"
        owner: "nsls2"
        repo: "ioc-deploy-roles"
        branch: "main"
        token: "{{ gh_read_token }}"
        varname: "host_config"
        recursive: true
```

This will load the configuration to the top level `host_config` dictionary.

Then, at the top of your role, simply include this one.

```Yaml
- name: Parse host configuration information
  ansible.builtin.include_role:
    name: nsls2.ioc_deploy.host_info
```

## Input variables

Variable name | Required | Purpose
--------------|-----------|----------
`host_config` | Yes | Contains dictionary with all host configuration as read via `nsls2.general.github_vars_facts`
`ioc_name` | No | If specified, will lookup `host_config[ioc_name]` and place it in the `ioc` variable

## Output variables

Variable name | Purpose
------------|--------------
`host_info_sci_intf_ip` | IP address of the SCI network interface
`host_info_epics_intf_ip` | IP addrees of EPICS network interface
`host_info_epics_subnet` | EPICS broadcast
`host_info_softioc_user` | Username of user under which IOC will run
`host_info_softioc_group` | Group that will be assigned to generated files
`host_info_hostname` | Hostname without the domain.
`host_info_ioc_list` | List of all IOCs configured for host.
`ioc` | Special variable containing dictionary of IOC configuration requested if `ioc_name` is defined.