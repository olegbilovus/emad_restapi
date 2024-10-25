set -e # exit on any error
set -x # print the running commands

sudo apt install python3-venv python3-pip -y

envdir=".venv"

python3 -m venv $envdir
source $envdir/bin/activate
pip install bcrypt pymongo certifi dnspython

sleep 10
python3 "$1"

