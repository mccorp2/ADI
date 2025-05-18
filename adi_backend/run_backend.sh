cd "$(dirname "$0")"

# Create new venv if one does not yet exist
if [ ! -d "adi_venv" ]; then
    python3 -m venv adi_venv
fi

# Alias to use adi_venv's python executable
alias python=adi_venv/bin/python3

# Install requirements to venv
python -m pip install -r ./requirements.txt

# Run run the server
python server.py