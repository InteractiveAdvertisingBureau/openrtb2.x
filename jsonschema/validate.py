#!/usr/bin/env python3
"""Validate OpenRTB 2.6 JSON documents against the schema."""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from referencing import Registry, Resource
except ImportError:
    print("Required: pip install jsonschema referencing")
    sys.exit(1)


def build_registry(schema_dir):
    registry = Registry()
    for schema_file in Path(schema_dir).glob("*.json"):
        schema = json.loads(schema_file.read_text())
        if "$id" in schema:
            resource = Resource.from_contents(schema)
            registry = registry.with_resource(schema["$id"], resource)
    return registry


def validate_file(filepath, schema_name, registry, schema_dir):
    schema = json.loads((Path(schema_dir) / schema_name).read_text())
    data = json.loads(Path(filepath).read_text())
    jsonschema.validate(data, schema, registry=registry)


def main():
    schema_dir = Path(__file__).parent
    registry = build_registry(schema_dir)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        schema_name = sys.argv[2] if len(sys.argv) > 2 else "BidRequest.json"
        try:
            validate_file(filepath, schema_name, registry, schema_dir)
            print(f"PASS: {filepath}")
        except jsonschema.ValidationError as e:
            print(f"FAIL: {filepath}\n  {e.message}")
            sys.exit(1)
    else:
        failures = 0
        for example in sorted((schema_dir / "examples" / "bid-requests").glob("*.json")):
            try:
                validate_file(example, "BidRequest.json", registry, schema_dir)
                print(f"  PASS: {example.name}")
            except jsonschema.ValidationError as e:
                print(f"  FAIL: {example.name} -> {e.message}")
                failures += 1

        for example in sorted((schema_dir / "examples" / "bid-responses").glob("*.json")):
            try:
                validate_file(example, "BidResponse.json", registry, schema_dir)
                print(f"  PASS: {example.name}")
            except jsonschema.ValidationError as e:
                print(f"  FAIL: {example.name} -> {e.message}")
                failures += 1

        sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
