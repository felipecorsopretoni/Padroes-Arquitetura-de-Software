import inspect
import pkgutil
from importlib import import_module
from typing import Any


def _walk_modules(package_name: str) -> None:
    package = import_module(package_name)
    package_path = getattr(package, "__path__", None)
    if package_path is None:
        return
    for module_info in pkgutil.walk_packages(package_path, package.__name__ + "."):
        import_module(module_info.name)


def _iter_subclasses(base_class: type[Any]) -> list[type[Any]]:
    subclasses: list[type[Any]] = []
    for subclass in base_class.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(_iter_subclasses(subclass))
    return subclasses


def discover_instances(package_name: str, base_class: type[Any]) -> list[Any]:
    _walk_modules(package_name)
    instances: list[Any] = []
    seen: set[str] = set()
    for subclass in _iter_subclasses(base_class):
        key = f"{subclass.__module__}.{subclass.__qualname__}"
        if key in seen or inspect.isabstract(subclass):
            continue
        seen.add(key)
        instances.append(subclass())
    instances.sort(
        key=lambda item: (
            getattr(item, "priority", 100),
            item.__class__.__name__,
        )
    )
    return instances
