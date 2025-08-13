update:
	$(eval TARGET := update)

delete:
	$(eval TARGET := delete)

role:
	@if [ -z "${TARGET}" ]; then \
		./scripts/manage_collection.py add role; \
	else \
		./scripts/manage_collection.py $(TARGET) role; \
	fi

module:
	@if [ -z "${TARGET}" ]; then \
		./scripts/manage_collection.py add module; \
	else \
		./scripts/manage_collection.py $(TARGET) module; \
	fi

report:
	./scripts/manage_collection.py report
