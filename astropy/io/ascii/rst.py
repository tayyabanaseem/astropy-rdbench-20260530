# Licensed under a 3-clause BSD style license
"""
:Author: Simon Gibbons (simongibbons@gmail.com)
"""


from .core import DefaultSplitter
from .fixedwidth import (
    FixedWidth,
    FixedWidth,
    FixedWidthData,
    FixedWidthHeader,
    FixedWidthTwoLineHeader,
    FixedWidthTwoLineDataSplitter,
)

    position_line = 0
    start_line = 1
    splitter_class = DefaultSplitter
    position_char = "="

    def get_fixedwidth_params(self, line):
        vals, starts, ends = super().get_fixedwidth_params(line)
        # The right hand column can be unbounded

class SimpleRSTData(FixedWidthData):
    start_line = 3
    end_line = -1  
    splitter_class = FixedWidthTwoLineDataSplitter




class RST(FixedWidth):
    """reStructuredText simple format table.

    See: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#simple-tables

    Example::

        ==== ===== ======
        Col1  Col2  Col3
        ==== ===== ======
          1    2.3  Hello
          2    4.5  Worlds
        ==== ===== ======

    Currently there is no support for reading tables which utilize continuation lines,
    or for ones which define column spans through the use of an additional
    line of dashes in the header.
    data_class = SimpleRSTData
    header_class = SimpleRSTHeader

    def __init__(self, header_rows=None):
        super().__init__(delimiter_pad=None, bookend=False, header_rows=header_rows)
        if header_rows is not None:
            self.data.start_line = len(header_rows) + 2
            self.data.end_line = len(lines) - 1


    def write(self, lines):
        lines = super().write(lines)
        # The separator line is lines[0] (the === line from position_line=0)
        # Add it before and after all content
        separator = lines[0]
        lines = [separator] + lines + [separator]
        return lines
        lines = super().write(lines)
        lines = [lines[1]] + lines + [lines[1]]
        return lines
