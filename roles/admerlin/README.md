# admerlin

Ansible role for deploying admerlin IOC instances.

## Outstanding Questions for Reviewers

- [] The old role had a required_module "ADMerlin_R4_1", I've dropped this in favor of the git hash. Is this correct?
- [] Replaced EPICS_CA_MAX_ARRAY_BYTES with NELEMENTS
- [] Ignored AutoSave.cmd, postInit.cmd, and auto_settings.req from the old role. Is this all covered in deploy_ioc_use_ad_common: true?
