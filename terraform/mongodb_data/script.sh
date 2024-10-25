envdir=".venv"
rm -rf $envdir

export PATH="$PWD/$envdir:$PATH"
python3 -m venv $envdir
pip install bcrypt pymongo[srv] certifi dnspython

python3 data.py

rm -rf $envdir
