# ISIS
Python bindings for ISIS

See [/bin](./bin) for examples on how to use the library

The only setup requirement is the conda environment, which installs
the ISIS binaries & Python dependencies: 

`conda env create -f environment.yml`

`conda activate isis`

[load_isis()](./isis/isis.py) uses 
[cppyy](https://cppyy.readthedocs.io/en/latest/index.html) to load
the headers and library that links the Python code to `libisis.so`


