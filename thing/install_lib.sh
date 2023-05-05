
#!/bin/sh
python3.9 -m pip uninstall ../dist/hexutils-0.1.0-py3-none-any.whl --yes
echo $PWD
cd ..
echo $PWD
./create_wheel.sh
echo $PWD
cd thing/
echo $PWD
python3.9 -m pip install ../dist/hexutils-0.1.0-py3-none-any.whl


