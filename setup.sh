#!/bin/bash

### General
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

### Blake backend
# Create virtual environment
python3.6 -m virtualenv -p python3 --no-site-packages $SCRIPT_DIR/backend/venv

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install virtual environment."
    exit 1
fi

# Add environment variables to source script thing
echo -e "\n\n# Flask Stuffs\nexport PYTHONPATH=$SCRIPT_DIR/backend\nexport FLASK_DEBUG=1\nexport FLASK_APP=$SCRIPT_DIR/backend/blake.py" >> $SCRIPT_DIR/backend/venv/bin/activate

# Install pip requirements
$SCRIPT_DIR/backend/venv/bin/pip install -r $SCRIPT_DIR/backend/requirements.txt

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install python packages."
    exit 1
fi
