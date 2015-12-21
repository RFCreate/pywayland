# Copyright 2015 Sean Vig
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xml.etree.ElementTree as ET
import os

from .element import Element, Attribute, Child
from .copyright import Copyright, copyright_default
from .description import Description
from .interface import Interface
from .printer import Printer


class Scanner(Element):
    """Main scanner object

    Main scanner object that acts on the input ``wayland.xml`` file to generate
    protocol files.

    Required attributes: `name`

    Child elements: `copyright?`, `description?`, and `interface+`

    :param input_file: Name of input XML file
    """
    attributes = [Attribute('name', True)]

    children = [
        Child('copyright', Copyright, False, False),
        Child('description', Description, False, False),
        Child('interface', Interface, True, True)
    ]

    def __init__(self, input_file):
        self._input_file = os.path.basename(input_file)
        if not os.path.exists(input_file):
            raise ValueError("Input xml file does not exist: {}".format(input_file))
        xmlroot = ET.parse(input_file).getroot()
        if xmlroot.tag != 'protocol':
            raise ValueError("Input file not a valid Wayland protocol file: {}".format(input_file))

        super(Scanner, self).__init__(xmlroot)

    def __repr__(self):
        return "Scanner({})".format(self._input_file)

    def output(self, output_dir):
        """Output the scanned files to the given directory


        :param output_dir: Path of directory to output protocol files to
        :type output_dir: string
        """
        output_dir = os.path.join(output_dir, self.name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # First, we'll create the __init__.py file
        printer = Printer()
        printer.initialize_file()

        if self.copyright:
            self.copyright.output(printer)
        else:
            printer(copyright_default)

        printer()
        for iface in self.interface:
            printer('from .{} import {}  # noqa'.format(iface.module, iface.class_name))

        init_path = os.path.join(output_dir, '__init__.py')
        with open(init_path, 'wb') as f:
            printer.write(f)

        # Now build all the modules
        for iface in self.interface:
            module_path = os.path.join(output_dir, iface.module + ".py")

            printer = Printer()
            printer.initialize_file(iface.name)
            if self.copyright:
                self.copyright.output(printer)
            else:
                printer(copyright_default)
            printer()

            iface.output(printer)

            with open(module_path, 'wb') as f:
                printer.write(f)
