# OpenRTB 2.6 JSON Schema

Machine-readable JSON Schema (Draft 2020-12) definitions for all objects in the OpenRTB 2.6 specification.

## What's Included

38 schema files covering the complete OpenRTB 2.6 object model:

**Bid Request** (35 objects): BidRequest, Imp, Banner, Video, Audio, Native, Format, Metric, Pmp, Deal, Site, App, DOOH, Publisher, Content, Producer, Network, Channel, Device, Geo, User, Data, Segment, Regs, Source, SupplyChain, SupplyChainNode, EID, UID, UserAgent, BrandVersion, Qty, Refresh, RefSettings, DurFloors

**Bid Response** (3 objects): BidResponse, SeatBid, Bid

## Usage

Validate an OpenRTB bid request against the schema:

```bash
# Python
pip install jsonschema referencing
python -c "
import json, jsonschema
from referencing import Registry, Resource
from pathlib import Path

# Build a registry of all schemas for $ref resolution
registry = Registry()
schema_dir = Path('.')
for schema_file in schema_dir.glob('*.json'):
    schema = json.loads(schema_file.read_text())
    resource = Resource.from_contents(schema)
    registry = registry.with_resource(schema['$id'], resource)

# Validate
bid_request = json.load(open('examples/bid-requests/simple-banner.json'))
schema = json.load(open('BidRequest.json'))
jsonschema.validate(bid_request, schema, registry=registry)
print('Valid!')
"
```

```bash
# Node.js (ajv)
npm install ajv ajv-formats
node -e "
const Ajv = require('ajv/dist/2020');
const fs = require('fs');
const path = require('path');

const ajv = new Ajv({allErrors: true});
const schemaDir = '.';

// Load all schemas
fs.readdirSync(schemaDir)
  .filter(f => f.endsWith('.json'))
  .forEach(f => ajv.addSchema(JSON.parse(fs.readFileSync(path.join(schemaDir, f)))));

const validate = ajv.getSchema('https://iabtechlab.com/openrtb/2.6/BidRequest.json');
const bidRequest = JSON.parse(fs.readFileSync('examples/bid-requests/simple-banner.json'));
const valid = validate(bidRequest);
console.log(valid ? 'Valid!' : validate.errors);
"
```

## Design Decisions

**Forward-compatible by default.** Schemas do not set `additionalProperties: false` at the top level, honoring OpenRTB 2.6 Section 2.6: implementations "must tolerate receiving new or unexpected fields." Unknown fields pass validation.

**Deprecated fields included.** Fields deprecated in OpenRTB 2.6 (e.g., `Device.didsha1`, `User.yob`, `Video.placement`) are present with `"deprecated": true` for backward compatibility.

**Enums reference AdCOM 1.0.** Integer fields with enumerated values reference the AdCOM 1.0 list by name in their description rather than hardcoding enum arrays, since AdCOM values (especially vendor-specific 500+ ranges) change independently.

**Extension objects are open.** All `ext` properties explicitly allow additional properties for exchange-specific extensions.

## Schema Version

OpenRTB Specification: 2.6
JSON Schema Draft: 2020-12
Namespace: `https://iabtechlab.com/openrtb/2.6/`

## References

- [OpenRTB 2.6 Specification](https://github.com/InteractiveAdvertisingBureau/openrtb2.x)
- [AdCOM 1.0 Specification](https://github.com/InteractiveAdvertisingBureau/AdCOM)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)

## License

Licensed under the same terms as the parent repository (Creative Commons Attribution 3.0).
