# handler_registry.py

from typing import Callable, Dict

def register(tag: str):
    def decorator(func: Callable):
        if not hasattr(func, "_dispatch_tags"):
            func._dispatch_tags = []
        func._dispatch_tags.append(tag)
        return func
    return decorator

def collect_handlers(instance) -> Dict[str, Callable]:
    dispatch = {}

    for attr_name in dir(instance):
        attr = getattr(instance, attr_name)

        # Look at the underlying function object for bound methods
        func = getattr(attr, "__func__", attr)
        tags = getattr(func, "_dispatch_tags", None)
        if not tags:
            continue

        for tag in tags:
            #print("[D] Registering \'{}\' -> {}".format(tag, attr.__name__))
            dispatch[tag] = attr  # bind method to instance
    return dispatch
