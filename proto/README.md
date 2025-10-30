# Protocol Buffers specification

## About

Protocol Buffers is the standard binary encoding for OpenRTB. The expectation
is that updates are made to the standard and `openrtb.proto` in lockstep.

The `openrtb.proto` definition included here is expected to be an exact
representation of the OpenRTB standard in Protocol Buffers. There are two
caveats:

1. OpenRTB contains several fields that take boolean values, though are
expressed as integers in JSON. They are expressed as booleans in Protocol
Buffers.
2. Enumerations are currently expressed as integers in both JSON and Protocol
Buffers. This is a holdover from using proto2 syntax, which did not support
the extensible enumerations used in OpenRTB. This may be changed in the future.
Meanwhile, code definitions for the standard enumerated values can be found at
https://github.com/IABTechLab/adcom-proto.

## How to get started

From the command line:

1. Install `make` and the latest version of `protoc`.
2. Open the `Makefile` and choose the language(s) for which the Protocol Buffers
object code should be generated.
3. Run `make`.
