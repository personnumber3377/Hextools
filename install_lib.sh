
#!/bin/sh
python3.9 -m pip uninstall dist/hexutils-0.1.0-py3-none-any.whl

./create_wheel.sh

python3.9 -m pip install dist/hexutils-0.1.0-py3-none-any.whl


