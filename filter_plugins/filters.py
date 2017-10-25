import os
import re
import sys
import inspect


class FilterModule(object):
    def filters(self):
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        filters = {}

        for f in filter(lambda x: False if re.match("__init__.py", x) else True, os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filter_functions'))):
            m = __import__('filter_functions.{}'.format(os.path.splitext(os.path.basename(f))[0]))
            for y in [getattr(m, x) for x in dir(m)]:
                if inspect.ismodule(y):
                    for z in [getattr(y, w) for w in dir(y)]:
                        if inspect.isfunction(z):
                            filters[z.__name__] = getattr(y, z.__name__)

        return filters