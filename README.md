# RTLManager

A Python package to generate RTL templates based on JSON configurations.

## Installation 
git clone https://github.com/srimanthtenneti/rtlmanager
cd rtlmanager
pip install .


## Usage

```python
from rtlmanager import RTLManager

rtl_gen = RTLManager(conf='conf.json')
rtl_gen.generate_rtl_template()

