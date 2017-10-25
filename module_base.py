from ansible.module_utils.basic import AnsibleModule


class BaseModule(object):
    def __init__(self, api_object, api):
        super(BaseModule, self).__init__()

        self._api_object = api_object

        input_args_list = []
        input_kwargs_list = []
        for _, method_info in self._api_object.api_spec[api]['api_methods'].iteritems():
            input_args_list.extend(method_info['args'])
            input_kwargs_list.extend(method_info['kwargs'])

        self._input_args = set(input_args_list)
        self._input_kwargs = set(input_kwargs_list)

        self._module_argument_spec = dict(
            api_domain=dict(type='str', required=True),
            auth=dict(type='dict', required=False),
            operation=dict(required=True, choices=self._api_object.api_spec[api]['api_methods'].keys())
        )

        self._module_argument_spec.update(
            {argname: dict(type='str') for argname in self._input_args}
        )

        self._module_argument_spec.update(
            {kwargname: dict(type='dict') for kwargname in self._input_kwargs}
        )

        self._required_together = (
            ['api_domain', 'operation']
        )

        self._required_if = tuple(
            [
                ['operation', method_name, method_spec['args']] for method_name, method_spec in
                self._api_object.api_spec['api_methods'].iteritems()
                ]
        )

    def get(self):
        return self._module_argument_spec, self._required_together, self._required_if
    
    def execute(self, module):
        api_domain = module.params['api_domain']
        operation = module.params['operation']
        headers = module.params['headers'] or None
        params = module.params['params'] or None
        data = module.params['data'] or None
        auth = module.params['auth'] or None
        result = None
        expected = None

        if self._api_object.api_domain is None:
            self._api_object.set_api_domain(api_domain)

        if auth:
            self._api_object.set_auth(**auth)

        if module.params['params'] is not None:
            for k in module.params['params'].keys():
                if module.params['params'][k] is None or len(str(module.params['params'][k])) == 0:
                    del module.params['params'][k]

        if module.params['data'] is not None:
            for k in module.params['data'].keys():
                if module.params['data'][k] is None or len(str(module.params['data'][k])) == 0:
                    del module.params['data'][k]


        unordered_args = {arg_name: arg_val for arg_name, arg_val in module.params.iteritems() if arg_name in self._api_object.api_spec['api_methods'][operation]['args']}
        args = [unordered_args[arg_name] for arg_name in self._api_object.api_spec['api_methods'][operation]['args']]
        kwargs = {kwarg_name: kwarg_val for kwarg_name, kwarg_val in locals().iteritems() if kwarg_name in self._api_object.api_spec['api_methods'][operation]['kwargs']}

        result = getattr(self._api_object, operation)(*args, **kwargs)

        if result.status_code in self._api_object.api_spec['api_methods'][operation]['expected_status']:
            expected = True

        else:
            expected = False

        try:
            result_json = result.json()

        except ValueError:
            result_json = {}

        return expected, result.status_code, result_json, result.url, result.request.body, result.request.headers


def run_module(api_object, api, auth=None):
    base = BaseModule(api_object, api)

    module_argument_spec, required_together, required_if = base.get()

    module = AnsibleModule(
        argument_spec=module_argument_spec,
        required_together=required_together,
        required_if=required_if
    )

    expected, status_code, result_json, result_url, result_body, result_headers = base.execute(module)

    if expected:
        try:
            module.exit_json(**result_json)

        except TypeError:
            module.exit_json(results=result_json)

        except ValueError:
            module.exit_json({'status_code': status_code})

    else:
        module.fail_json(msg='ERROR: Unexpected response!', response=result_json, url=result_url, original_request=result_body, original_headers=result_headers, status_code=status_code)







