# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2018 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2018-07-09.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import templateprocessor
from generate_argument_iterator import generate_argument_iterator
import generate_get_console_width
from generate_option_list import generate_options
from generate_test_code import generate_test_code
from generate_write_help_text import generate_write_help_text
from generate_parse_arguments import generate_parse_arguments
from generate_option_functions import generate_option_functions


class SourceFileGenerator(templateprocessor.Expander):
    def __init__(self, session):
        super().__init__()
        self._session = session
        self.has_namespace = session.code_properties.namespace_start
        self.namespace_start = session.code_properties.namespace_start
        self.namespace_end = session.code_properties.namespace_end

    def source_includes(self, *args):
        result = ["#include " + s for s in
                  self._session.code_properties.source_includes]
        result.extend(generate_get_console_width.generate_include_files())
        return result

    def source_code(self, *args):
        return templateprocessor.make_lines(SOURCE_NAMESPACE_TEMPLATE, self)

    def code(self, *args):
        return templateprocessor.make_lines(SOURCE_CONTENTS_TEMPLATE, self)

    def argument_iterator(self, *args):
        return generate_argument_iterator(self._session)

    def get_console_width(self, *args):
        return generate_get_console_width.generate_get_console_width()

    def help_text(self, *args):
        return templateprocessor.make_lines(
            "const char helpText[] =\n    [[[help_text_string]]];", self)

    def write_help_text_function(self, *args):
        return generate_write_help_text(self._session)

    def option_functions(self, *args):
        return generate_option_functions(self._session)

    def options(self, *args):
        return generate_options(self._session)

    def has_options(self, *args):
        return self._session.code_properties.options

    def parse_arguments(self, *args):
        return generate_parse_arguments(self._session)


def generate_source(session):
    code = templateprocessor.make_lines(session.code_properties.source_template,
                                        SourceFileGenerator(session))
    if session.settings.add_test:
        code.extend(generate_test_code(session))
    return "\n".join(code)


SOURCE_NAMESPACE_TEMPLATE = """\
[[[IF has_namespace]]]
[[[namespace_start]]]
    [[[code]]]
[[[namespace_end]]]
[[[ELSE]]]
[[[code]]]
[[[ENDIF]]]\
"""


SOURCE_CONTENTS_TEMPLATE = """\

std::string to_string(const std::string_view& wrapper)
{
    return std::string(wrapper.data(), wrapper.size());
}
[[[IF has_options]]]
[[[argument_iterator]]]
[[[ENDIF]]]
[[[get_console_width]]]
[[[write_help_text_function]]]
[[[options]]]
[[[option_functions]]]
[[[parse_arguments]]]
"""

SOURCE_CONTENTS = """\
[[[IF namespace]]]
[[[endNamespace]]]
[[[ENDIF]]]
[[[IF includeTest]]]

#include <iomanip>

template <typename It>
void printAllValues(It begin, It end)
{
    if (begin == end)
        return;
    std::cout << *begin;
    for (++begin; begin != end; ++begin)
        std::cout << ", " << *begin;
}

#define PRINT_VALUE(member) \
    std::cout << std::setw([[[memberWidth]]]) << #member ":" << " "<< args.member << "\n"
#define PRINT_STRING(member) \
    std::cout << std::setw([[[memberWidth]]]) << #member ":" << " \"" << args.member << "\"\n"
#define PRINT_LIST(member) \
    std::cout << std::setw([[[memberWidth]]]) << #member ":" << " {"; \
    printAllValues(begin(args.member), end(args.member)); \
    std::cout << "}\n"

int main(int argc, char* argv[])
{
    std::cout << "\n============================= Input Arguments "
                    "============================\n";
    for (int i = 0; i < argc; ++i)
        std::cout << "argv[" << i << "] = \"" << argv[i] << "\"\n";

    std::cout << "\n============================== Parser output "
                    "=============================\n";
    auto args = [[[qualifiedFunctionName]]](argc, argv, false);

    std::cout << "\n================================= Values "
                    "=================================\n";
    std::cout.setf(std::ios_base::boolalpha);
    std::cout.setf(std::ios_base::left, std::ios_base::adjustfield);
    [[[printMembers]]]
    return 0;
}

[[[ENDIF]]]\
"""
