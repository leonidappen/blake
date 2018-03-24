#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

if [ ! -d "$SCRIPT_DIR/backend" ] || [ ! -d "$SCRIPT_DIR/frontend" ]; then
    >&2 echo "Failed to find backend/frontend directories at $SCRIPT_DIR"
    exit 1
fi 

### Blake backend
# Create virtual environment
python3.6 -m virtualenv -p python3 --no-site-packages $SCRIPT_DIR/backend/venv

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install virtual environment."
    exit 1
fi

# Add environment variables to source script
read -d '' envvar << _EOF_
# Flask
export PYTHONPATH=$SCRIPT_DIR/backend
export FLASK_DEBUG=1
export FLASK_APP=$SCRIPT_DIR/backend/blake.py
_EOF_
echo "$envvar" >> $SCRIPT_DIR/backend/venv/bin/activate


# Install pip requirements
$SCRIPT_DIR/backend/venv/bin/pip install -r $SCRIPT_DIR/backend/requirements.txt

if [ $? -ne 0 ]; then
    >&2 echo "Failed to install python packages."
    exit 1
fi

# Install redis
curl -O http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd redis-stable
make

if [ $? -ne 0 ]; then
    >&2 echo "Failed to build redis."
    exit 1
fi