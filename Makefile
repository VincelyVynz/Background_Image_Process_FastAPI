# Project name
APP_NAME=app

# Directory structure
DIRS = \
	$(APP_NAME) \
	$(APP_NAME)/api \
	$(APP_NAME)/jobs \
	$(APP_NAME)/models \
	$(APP_NAME)/storage/input \
	$(APP_NAME)/storage/output \
	$(APP_NAME)/utils

# Files to create
FILES = \
	$(APP_NAME)/main.py \
	$(APP_NAME)/api/routes.py \
	$(APP_NAME)/jobs/manager.py \
	$(APP_NAME)/jobs/worker.py \
	$(APP_NAME)/models/schemas.py \
	$(APP_NAME)/utils/image_ops.py

.PHONY: init clean tree

# Create folders and files
init:
	@echo "Creating project structure..."
	@mkdir -p $(DIRS)
	@touch $(FILES)
	@echo "Done."

# Remove generated structure
clean:
	@echo "Removing project structure..."
	@rm -rf $(APP_NAME)
	@echo "Cleaned."

# Show tree (optional, requires 'tree' installed)
tree:
	@tree $(APP_NAME)
