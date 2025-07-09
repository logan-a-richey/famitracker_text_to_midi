# handler_registry.py

from collections import defaultdict
from typing import Callable, Dict, List

# Global registry used during class scanning
_registry: Dict[Callable, List[str]] = defaultdict(list)

def register(tag: str):
    def decorator(func: Callable):
        _registry[func].append(tag)
        return func
    return decorator

def collect_handlers(instance) -> Dict[str, Callable]:
    '''
    Scans instance methods for functions with tags
    registered using @register and builds a dispatch dict.
    '''
    dispatch = {}

    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)
        if not callable(attr):
            continue

        tags = _registry.get(attr)
        if not tags:
            continue

        for tag in tags:
            dispatch[tag] = attr

    return dispatch