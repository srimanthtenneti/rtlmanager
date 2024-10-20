"""
Project : RTLManager
Author  : tsrimanth 
Date    : 20 October 2024
Version : 0.02 
Changes : Non-Param bus generation fix. 
Bugs    : - 
NextRev : Addition of RTL2JSON, Instance Gen     
"""
import os
import sys
import json

class RTLManager:
    def __init__(self, conf=''):
        ### RTL Config - JSON Format
        self.conf = conf

    def config_parser(self):
        ### Read and Load the JSON Config
        self.confighash = json.load(open(self.conf, 'r'))

    def generate_rtl_template(self):
        ### Parse the configuration
        self.config_parser()
        ##### Start Template Generation #####
        ### Parameter Processing
        keys = self.confighash.keys()
        if 'parameters' in keys:
            params = self.confighash['parameters']
        ### Global Signals Processing
        if 'global' in keys:
            global_signals = self.confighash['global']
            clocks = global_signals['clock']
            resets = global_signals['reset']
            gating = global_signals['gating']
        ### Input Signals Processing
        if 'input' in keys:
            inputs = self.confighash['input']
        ### Output Signals Processing
        if 'output' in keys:
            outputs = self.confighash['output']
        ### Inout Signals Processing
        if 'inout' in keys:
            inouts = self.confighash['inout']
        ### Module Name Processing
        module = self.confighash['module']

        ### RTL Generation
        rtl_template = ''

        #### Add Module Name
        if len(params.keys()) > 0:
            rtl_template += 'module ' + module + ' #(\n'
            for i, param in enumerate(params.keys()):
                if i != len(params.keys()) - 1:
                    rtl_template += 'parameter ' + param + ' = ' + str(params[param]) + ',\n'
                else:
                    rtl_template += 'parameter ' + param + ' = ' + str(params[param]) + '\n'
            rtl_template += ')(\n'
        else:
            rtl_template += 'module ' + module + '(\n'

        #### Global Signals Definition

        ###### CLOCKS ######
        for i, clock in enumerate(clocks):
            if len(clocks) > 0:
                if i == 0:
                    rtl_template += '\n// Global Signals - Clocks\n'
                rtl_template += 'input wire  ' + clock + ',\n'

        ##### RESET #####
        for i, reset in enumerate(resets):
            if len(resets) > 0:
                if i == 0:
                    rtl_template += '\n// Global Signals - Resets\n'
                rtl_template += 'input wire  ' + reset + ',\n'

        ##### Gating Signals
        for i, gate in enumerate(gating):
            if len(gating) > 0:
                if i == 0:
                    rtl_template += '\n// Global Signals - Gating\n'
                rtl_template += 'input wire  ' + gate + ',\n'

        ##### Input Signals
        for i, input_name in enumerate(inputs):
            if i == 0:
                rtl_template += '\n// Input Signals\n'
            # Check if the input width is a parameter, integer, or 0
            if inputs[input_name] == 0:
                # Declare as a normal wire (no bus)
                rtl_template += f'input wire {input_name},\n'
            elif isinstance(inputs[input_name], int):
                # Handle bus width given as an integer
                rtl_template += f'input wire  [{inputs[input_name]-1}:0] {input_name},\n'
            elif inputs[input_name] != 0:
                # Handle bus width given as a parameter (like Width or SIZE)
                rtl_template += f'input wire  [{inputs[input_name]}-1 : 0] {input_name},\n'
            else:
                rtl_template += f'input wire {input_name},\n'

        ##### Output Signals
        for i, output_name in enumerate(outputs):
            if i == 0:
                rtl_template += '\n// Output Signals\n'
            # Check if the output width is a parameter, integer, or 0
            if outputs[output_name] == 0:
                # Declare as a normal wire (no bus)
                rtl_template += f'output wire {output_name},\n'
            elif isinstance(outputs[output_name], int):
                # Handle bus width given as an integer
                rtl_template += f'output wire  [{outputs[output_name]-1}:0] {output_name},\n'
            elif outputs[output_name] != 0:
                # Handle bus width given as a parameter (like Width or SIZE)
                rtl_template += f'output wire  [{outputs[output_name]}-1 : 0] {output_name},\n'
            else:
                rtl_template += f'output wire {output_name},\n'

        rtl_template += ');\n\n\nendmodule '
        ##### End Template Generation #####

        with open(module + '.v', 'w') as f:
            f.write(rtl_template)