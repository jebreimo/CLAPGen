# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2017 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2017-12-07.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import datetime
import os

import properties
import logger
from helpfileerror import HelpFileError
from helpfilesyntax import HelpFileSyntax


def make_default_variables():
    today = datetime.date.today()
    variables = dict(YEAR=str(today.year),
                     MONTH="%02d" % today.month,
                     DAY="%02d" % today.day)
    variables.update(dict(os.environ))
    return variables


def parse_bool(value):
    value = value.lower()
    if value in ("0", "false"):
        return False
    if value in ("1", "true"):
        return True
    raise HelpFileError("Invalid boolean value: %s" % value)


class Settings:
    def __init__(self):
        self.indentation = -1
        self.allow_abbreviations = True
        self.use_pragma_once = True
        self.class_name = "ArgumentParser"
        self.file_name = None
        self.header_extension = "h"
        self.source_extension = "cpp"
        self.namespace = ""
        self.function_name = "parse_arguments"
        self.line_width = 79
        self.add_test = False
        self.metavar_types = dict(properties.DEFAULT_METAVAR_TYPES)
        self.detect_separators = False


class Session:
    def __init__(self):
        self.settings = Settings()
        self.variables = make_default_variables()
        self.syntax = HelpFileSyntax()
        self.help_text = ""
        self.error_text = ""
        self.metavar_types = dict(properties.DEFAULT_METAVAR_TYPES)
        self.arguments = []
        self.members = []
        self.logger = logger.Logger()

    def begin_processing_file(self, file_name):
        self.logger.file_name = file_name
        self.logger.line_number = None

    def end_processing_file(self):
        self.logger.file_name = None
        self.logger.line_number = None

    def has_errors(self):
        return self.logger.counters[logger.Logger.ERROR] != 0

    def set_setting(self, name, value):
        if name == "ArgumentPrefix":
            self.syntax.argument_start = value
        elif name == "ArgumentSuffix":
            self.syntax.argument_end = value
        elif name == "ArgumentSeparator":
            self.syntax.argument_separator = value
        elif name == "IndentationWidth":
            self.settings.indentation = int(value)
        elif name == "Abbreviations":
            self.settings.allow_abbreviations = parse_bool(value)
        elif name == "PragmaOnce":
            self.settings.use_pragma_once = parse_bool(value)
        elif name == "SectionPrefix":
            self.syntax.section_prefix = value
        elif name == "VariablePrefix":
            self.syntax.variable_start = value
        elif name == "VariableSuffix":
            self.syntax.variable_end = value
        elif name == "Class_name":
            self.settings.class_name = value
        elif name == "File_name":
            self.settings.file_name = value
        elif name == "HeaderExtension":
            self.settings.header_extension = value
        elif name == "SourceExtension":
            self.settings.source_extension = value
        elif name == "Namespace":
            self.settings.namespace = value
        elif name == "FunctionName":
            self.settings.function_name = value
        elif name == "LineWidth":
            self.settings.line_width = int(value)
        elif name == "Test":
            self.settings.add_test = parse_bool(value)
        elif name == "DetectSeparators":
            self.settings.detect_separators = parse_bool(value)
        else:
            return False
        return True
