# Build the docs for the proto3 definition.

LANGUAGES=java # cpp go csharp objc python ruby js

bindings:
	for x in ${LANGUAGES}; do \
		mkdir -p build/$${x}; \
		protoc --proto_path src/main --$${x}_out=build/$${x} \
			src/main/com/iabtechlab/openrtb/v2/openrtb.proto \
		; \
	done

check:
	prototool lint

clean:
	for x in ${LANGUAGES}; do \
		rm -fr $${x}/*; \
	done

docs:
	mkdir -p build
	podman run --rm \
		-v ${PWD}/build:/out \
		-v ${PWD}/src/main:/proto \
		pseudomuto/protoc-gen-doc --doc_opt=html,doc.html --proto_path=/proto \
		com/iabtechlab/openrtb/v2/openrtb.proto

watch:
	fswatch  -r ./src/ | xargs -n1 make docs
