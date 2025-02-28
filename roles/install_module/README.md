# Install Module

This ansible role is responsible for ensuring that any required EPICS software is available on the target host during deployment. Currently, this involves installing the `epics-bundle` rpm for a base set of software, and also performing intelligent compilation and dependency resolution for modules that don't ship with our standard distribution.

In the future this role will be updated to allow for using pre-built container images instead of in-place compilation.

## How it works

Because EPICS doesn't have a built in dependency solver, it is necessary that compatible versions are explicitly described.

As such, every module supported by this role has one or more configuration files that describe a specific version of said module, and it's dependencies. Unless otherwise stated, the `epics-bundle` is used for any baseline dependencies.

The role will build a dependency tree with the target module as a leaf, and build all modules from the top down - no need to explicitly set each dependency for every module, just the immediate parent.

Once a dependency list has been established, the role will clone and checkout the correct version of the module, then will find and remove any `RELEASE` and `CONFIG_SITE` files. These are then auto re-generated from jinja templates based on the given configuration.

Finally, the specified compilation command (default is just `make -sj`) is ran to compile the module.

## Adding a module

If the module already has a directory under `vars`, you may simply add an additional `.yml` file for the new version. A configuration must be structured as follows:

```Yaml
# Top level dictionary key must be {module_name}_{module_version}
# module_version here must be the same as the config file name
ADVimba_R1_5:

  # Same as the top level dictionary name (may be removed)
  name: ADVimba_R1_5

  # Public git URL from which to download module
  url: https://github.com/areaDetector/ADVimba

  # Module version. Either a tag or a commit hash. Branches will work also, but should not be used.
  version: R1-5

  # List of dependencies that should come from epics-bundle, and not be built by the role
  # In most cases, should just be set to /usr/lib/epics
  epics_deps:
    EPICS_BASE: /usr/lib/epics
    ASYN: /usr/lib/epics
    AUTOSAVE: /usr/lib/epics
    BUSY: /usr/lib/epics
    CALC: /usr/lib/epics
    DEVIOCSTATS: /usr/lib/epics
    SSCAN: /usr/lib/epics
    SNCSEQ: /usr/lib/epics

  # In the event that you need to specify a configuration value, like TIRPC=YES, WITH_XXX=YES etc.
  # You can add that to the config dictionary. The values defined here will take precedence, but
  # many default values are pre-set, especially for AD IOCs. See defaults/main.yml for a list.
  config:
    MY_CONFIG_VAR: "YES"

  # Any system packages to install with dnf. Typically epics-bundle
  pkg_deps:
  - epics-bundle

  # Should be true for any AD IOCs, otherwise can be omitted
  include_base_ad_config: true

  # List any additional modules that should be built by the role by name.
  # Only need to specify the immediate parent dependency.
  module_deps:
  - ADGenICam_R1_10

  # If the command needed to compile the module is anything but a make in the
  # top directory, override that here. If just make, then this key can be omitted.
  compilation_command: make -sj

```

If a module does not yet have a directory, simply add one with the module name, and add a version config file in the above format.

The name of the file should represent the version number. If the version has `-`es, you'll need to replace them with `_` characters instead.

After you've added your config file, run `make` in this directory to regenerate the below supported versions table.

## Currently supported modules

<!-- BEGIN_AUTOGEN -->

Module | Version | Url
--- | --- | ---
ADEiger | R3-4 | https://github.com/areadetector/ADEiger
ADSimDetector | 4b236f4 | https://github.com/areaDetector/ADSimDetector
ADSupport | R1-10 | https://github.com/areaDetector/ADSupport
motorSim | R1-2 | https://github.com/epics-motor/motorMotorSim
ADMerlin | R4-1 | https://github.com/areadetector/ADMerlin
ppmac | main | https://github.com/NSLS-II/ppmac
pmac | 2-6-2 | https://github.com/dls-controls/pmac
ADCore | R3-13 | https://github.com/areaDetector/ADCore
ADCore | R3-12-1 | https://github.com/areaDetector/ADCore
ADAravis | R2-3 | https://github.com/areaDetector/ADAravis
ADKinetix | R1-2 | https://github.com/NSLS-II/ADKinetix
ADVimba | R1-5 | https://github.com/areaDetector/ADVimba
ADGenICam | R1-10 | https://github.com/areaDetector/ADGenICam
