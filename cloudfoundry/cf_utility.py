DOCUMENTATION = '''
---
module:  cf_utility
short_description:  Utility module for the Cloud Foundry API
'''

EXAMPLES = '''

'''

from ansible.module_utils.basic import AnsibleModule


class CloudFoundryUtilityModule(object):
    def __init__(self, module):
        super(CloudFoundryUtilityModule, self).__init__()
        self.module = module
        self.error = {}
        self.results = {}
        self.results['applications'] = []

        getattr(self, '{}'.format(self.module.params['operation']))()

    def generate_app_manifest(self):
        required_app_params = [
            'name',
            'path'
        ]

        for i, app in enumerate(self.module.params['apps']):
            for r in required_app_params:
                if r not in app.keys():
                    self.error['msg'] = "ERROR! missing parameter '{}' in app (index: {})".format(r, i)
                    break
        
            if len(self.error) == 0:
                self.results['applications'].append(
                    {
                        (k.replace('_', '-') if k != 'disk_quota' else k): v for k, v in app.iteritems()
                    }
                )


def main():
    module = AnsibleModule(
        argument_spec = dict(
            operation = dict(required=True, choices=['generate_app_manifest']),
            apps = dict(type='list')
        ),
        required_together = (
            ['operation', 'generate_app_manifest', ['apps']]
        )
    )

    cf_utility = CloudFoundryUtilityModule(module)
    
    if len(cf_utility.error) == 0:
        module.exit_json(**cf_utility.results)

    else:
        module.fail_json(msg=cf_utility.error['msg'])

if __name__ == "__main__":
    main()
