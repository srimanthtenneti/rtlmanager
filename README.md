# RTLManager

A Python package to generate RTL templates based on JSON configurations.

## Installation 
git clone https://github.com/srimanthtenneti/rtlmanager
cd rtlmanager
pip install .

## Config Template - JSON

{
  "parameters" : {
    "Width" : 32, 
    "SIZE"  : 8
  },
  "module" : "test_block", 
  "global" : {
    "clock"  : ["clk", "clk1"], 
    "reset"  : ["resetn"], 
    "gating" : ["en"]  
  }, 
  "input" : {
    "a" : "Width", 
    "b" : 0
  },
    "output" : {
    "x" : "Width", 
    "y" : "SIZE"
  }
}

## Usage

```python
from rtlmanager import RTLManager

rtl_gen = RTLManager(conf='path/to/config.json')
rtl_gen.generate_rtl_template()

