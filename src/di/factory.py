from .introspect import split_module_class
from importlib import import_module
import inspect
import logging
import types

logger = logging.getLogger(__name__)

def create_object(d):
    args = {}
    module = ""
    funct = ""
    # collect constructor args (deep-first)...
    for k, v in d.items():
        if isinstance(v, dict):
            # nestes objects
            obj = get_objects(v)
            args[k] = obj
        else:
            if k == 'name':
                # defines the class to instantiate later
                module, funct = split_module_class(v)
            else:
                # leaf object
                args[k] = v

    try:
        if module + funct == "":
            logger.debug('Node is a dict: %s', args)
            return args

        logger.debug("Resolving attribute %s.%s on %s", module, funct, d)
        result = getattr(import_module(module), funct)

        if isinstance(result, types.FunctionType):
            logger.debug('%s is a function', result)
        else:
            logger.debug('Calling contructor %s with %s', result, args)
            result = result(**args)

        if isinstance(result, Factory):
            result = result.get()

    except Exception as e:
        logging.exception(e)
        raise

    return result


class Factory:
    def __init__(self, target, args):
        self.module, self.funct = split_module_class(target)
        self.args = args

    def get(self):
        return getattr(import_module(self.module), self.funct)(**self.args)


class ModuleFactory(Factory):
    def __init__(self, target):
        super(ModuleFactory, self).__init__(target, None)

    def get(self):
        return getattr(import_module(self.module), self.funct)


class ListFactory(Factory):
    def __init__(self, args):
        self.args = args

    def get(self):
        return [self.args]
