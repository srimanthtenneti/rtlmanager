# RTLManager

A Python package to generate RTL templates based on JSON configurations.

## Installation 
git clone https://github.com/srimanthtenneti/rtlmanager <br>
cd rtlmanager <br>
pip install . <br>


## Usage

```python
from rtlmanager import RTLManager

rtl_gen = RTLManager(conf='conf.json')
rtl_gen.generate_rtl_template()

