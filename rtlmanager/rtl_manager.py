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
import json
import re

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
        else :
            inputs = {}
        ### Output Signals Processing
        if 'output' in keys:
            outputs = self.confighash['output']
        else :
            outputs = {}
        ### Inout Signals Processing
        if 'inout' in keys:
            inouts = self.confighash['inout']
        ### Module Name Processing
        else :
            inouts = {}

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
                rtl_template += 'input   ' + clock + ',\n'

        ##### RESET #####
        for i, reset in enumerate(resets):
            if len(resets) > 0:
                if i == 0:
                    rtl_template += '\n// Global Signals - Resets\n'
                rtl_template += 'input   ' + reset + ',\n'

        ##### Gating Signals
        for i, gate in enumerate(gating):
            if len(gating) > 0:
                if i == 0:
                    rtl_template += '\n// Global Signals - Gating\n'
                rtl_template += 'input   ' + gate + ',\n'

        ##### Input Signals
        for i, input_name in enumerate(inputs):
            if i == 0:
                rtl_template += '\n// Input Signals\n'
            # Check if the input width is a parameter, integer, or 0
            if inputs[input_name] == 0:
                # Declare as a normal wire (no bus)
                rtl_template += f'input  {input_name},\n'
            elif isinstance(inputs[input_name], int):
                # Handle bus width given as an integer
                rtl_template += f'input   [{inputs[input_name]-1}:0] {input_name},\n'
            elif inputs[input_name] != 0:
                # Handle bus width given as a parameter (like Width or SIZE)
                rtl_template += f'input   [{inputs[input_name]}-1 : 0] {input_name},\n'
            else:
                rtl_template += f'input  {input_name},\n'

        ##### Output Signals
        for i, output_name in enumerate(outputs):
            if i == 0:
                rtl_template += '\n// Output Signals\n'
            # Check if the output width is a parameter, integer, or 0
            if outputs[output_name] == 0:
                # Declare as a normal wire (no bus)
                rtl_template += f'output  {output_name},\n'
            elif isinstance(outputs[output_name], int):
                # Handle bus width given as an integer
                rtl_template += f'output   [{outputs[output_name]-1}:0] {output_name},\n'
            elif outputs[output_name] != 0:
                # Handle bus width given as a parameter (like Width or SIZE)
                rtl_template += f'output   [{outputs[output_name]}-1 : 0] {output_name},\n'
            else:
                rtl_template += f'output  {output_name},\n'

        ##### Inout Signals
        for i, inout_name in enumerate(inouts):
            if i == 0:
                rtl_template += '\n// Inout Signals\n'
            # Check if the inout width is a parameter, integer, or 0
            if inouts[inout_name] == 0:
                # Declare as a normal wire (no bus)
                rtl_template += f'inout  {inout_name},\n'
            elif isinstance(inouts[inout_name], int):
                # Handle bus width given as an integer
                rtl_template += f'inout   [{inouts[inout_name]-1}:0] {inout_name},\n'
            elif inouts[inout_name] != 0:
                # Handle bus width given as a parameter (like Width or SIZE)
                rtl_template += f'inout   [{inouts[inout_name]}-1 : 0] {inout_name},\n'
            else:
                rtl_template += f'inout  {inout_name},\n'

        rtl_template += ');\n\n\nendmodule '
        ##### End Template Generation #####

        with open(module + '.v', 'w') as f:
            f.write(rtl_template)


    def parse_module(self, module_file):
        """Extract module name and ports with directions from the Verilog file."""
        with open(module_file, 'r') as f:
            lines = f.readlines()

        module_name = None
        ports = []
        inside_port_list = False

        for line in lines:
            line = line.strip()

            # Extract module name
            if line.startswith('module') and '(' in line:
                module_name = line.split()[1]
                inside_port_list = True
                continue

            # Extract ports and their directions
            if inside_port_list:
                if line.startswith(');'):
                    inside_port_list = False
                    break
                if line.startswith('input') or line.startswith('output') or line.startswith('inout'):
                    direction = line.split()[0]
                    port = line.split()[1].replace(',', '').replace(';', '')
                    ports.append((port, direction))

        return module_name, ports

    def instantiate_module(self, module_name, ports, instance_count):
        """Generate specified number of instantiations for a module with unconnected ports and comments."""
        instances = []
        for i in range(instance_count):
            port_map = ",\n".join([f"    .{port}(), // {direction}" for port, direction in ports])
            instances.append(f"{module_name} {module_name}_inst{i} (\n{port_map}\n);\n")
        return "\n".join(instances)

    def gen_top(self, top_name, module_instances):
        """Generate the top-level Verilog file with empty port connections and multiple instances."""
        top_module = f"module {top_name} (\n"

        # Collect all ports for the top-level module
        all_ports = set()
        module_instantiations = []

        for module_file, instance_count in module_instances:
            module_name, ports = self.parse_module(module_file)
            all_ports.update([port for port, _ in ports])
            module_instantiations.append(self.instantiate_module(module_name, ports, instance_count))

        # Define empty top-level ports to prevent syntax errors
        top_module += ",\n".join([f"    // Top-level port: {port}" for port in all_ports]) + "\n);\n\n"

        # Add module instantiations
        for inst in module_instantiations:
            top_module += inst + "\n"

        # End top-level module
        top_module += "endmodule"

        # Write the top-level file
        with open(f"{top_name}.v", 'w') as f:
            f.write(top_module)

        print(f"Top-level module {top_name} generated successfully.")
