#!/usr/bin/python

DOCUMENTATION = '''
---
module:  cf_service_keys
short_description:  Interact with the Cloud Foundry ServiceKeys API
'''

EXAMPLES = '''

'''

from pycf.cloudfoundry import ServiceKeys
from ansible.module_utils.basic import AnsibleModule  # This must be included in order for the program structure to work
from ansible_resources.library.cf_base import run_module


if __name__ == "__main__":
    run_module(ServiceKeys())

