#!/usr/bin/python

DOCUMENTATION = '''
---
module:  docker_secret
short_description:  Interact with the Docker Secrets API
'''

EXAMPLES = '''

'''

from ansible.module_utils.basic import AnsibleModule  # This must be included in order for the program structure to work
from ansible_modules.module_base import run_module
from pyswarm.pyswarm import DockerSwarm


if __name__ == "__main__":
    run_module(DockerSwarm(), api='secret')
