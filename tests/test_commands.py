# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import unittest
import re
from saws.commands import AwsCommands


class CommandsTest(unittest.TestCase):

    def test_generate_all_commands(self):
        aws_commands = AwsCommands()
        commands, sub_commands, global_options, resource_options, \
            ec2_states = aws_commands.generate_all_commands()
        num_commands = 0
        num_sub_commands = 0
        num_global_options = 0
        num_resource_options = 0
        num_ec2_states = 0
        with open(AwsCommands.SOURCES_PATH) as f:
            for line in f:
                line = re.sub('\n', '', line)
                if AwsCommands.COMMANDS_HEADER in line:
                    num_commands = \
                        int(line.strip(AwsCommands.COMMANDS_HEADER))
                elif AwsCommands.SUB_COMMANDS_HEADER in line:
                    num_sub_commands = \
                        int(line.strip(AwsCommands.SUB_COMMANDS_HEADER))
                elif AwsCommands.GLOBAL_OPTIONS_HEADER in line:
                    num_global_options = \
                        int(line.strip(AwsCommands.GLOBAL_OPTIONS_HEADER))
                elif AwsCommands.RESOURCE_OPTIONS_HEADER in line:
                    num_resource_options = \
                        int(line.strip(AwsCommands.RESOURCE_OPTIONS_HEADER))
                elif AwsCommands.EC2_STATES_HEADER in line:
                    num_ec2_states = \
                        int(line.strip(AwsCommands.EC2_STATES_HEADER))
        assert len(commands) == num_commands
        assert len(sub_commands) == num_sub_commands
        assert len(global_options) == num_global_options
        assert len(resource_options) == num_resource_options
        assert len(ec2_states) == num_ec2_states
