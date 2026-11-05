"""Safe YAML with unique explicit keys. YAML merge overrides remain valid."""

from collections.abc import Hashable

import yaml
from yaml.constructor import ConstructorError


_MERGE_KEY = object()


class UniqueKeyLoader(yaml.SafeLoader):
    def __init__(self, stream):
        super().__init__(stream)
        self.checked_mappings = set()

    def flatten_mapping(self, node):
        # Merge processing also visits aliased mappings. Check each mapping before
        # PyYAML expands it, so a legitimate inherited key may be overridden.
        if node in self.checked_mappings:
            return
        self.checked_mappings.add(node)
        seen = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                key = _MERGE_KEY
            elif key_node.tag == "tag:yaml.org,2002:value":
                key = "="
            else:
                key = self.construct_object(key_node)
            if not isinstance(key, Hashable):
                raise ConstructorError(None, None, "Unhashable YAML key", key_node.start_mark)
            if key in seen:
                raise ConstructorError(None, None, f"Duplicate YAML key: {key_node.value}", key_node.start_mark)
            seen.add(key)
        super().flatten_mapping(node)
