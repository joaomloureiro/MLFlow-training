# ---- Config ----
CONDA_ENV  := myenv
PYTHON_VER := 3.11         # or whatever you want
VENV_DIR   := python

# Use conda run so we don't need 'conda activate' in Makefile
CONDA_PYTHON := conda run -n $(CONDA_ENV) python

.PHONY: conda-env venv install clean

# Create the conda env if it doesn't exist
conda-env:
	@echo "Ensuring conda env '$(CONDA_ENV)' exists..."
	@conda env list | grep -q "^$(CONDA_ENV) " || \
		conda create -y -n $(CONDA_ENV) python=$(PYTHON_VER)
	@echo "Conda env '$(CONDA_ENV)' ready."

# Create a venv inside the conda env's python
venv: conda-env
	@echo "Creating virtual environment in '$(VENV_DIR)'..."
	@$(CONDA_PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created at '$(VENV_DIR)'."

# Install dependencies into the venv
install: venv
	@echo "Installing dependencies into venv..."
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

# Example run target using the venv
run:
	@$(VENV_DIR)/bin/python main.py

# Remove the venv (does NOT touch conda env)
clean:
	@echo "Removing venv..."
	@rm -rf $(VENV_DIR)
	@echo "Done."