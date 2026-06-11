# Licensed under a 3-clause BSD style license
"""
"""Simon Gibbons (simongibbons@gmail.com)"""


from . import core
from .fixedwidth import (
    FixedWidth,
    FixedWidthData,
    FixedWidthHeader,
    FixedWidthTwoLineDataSplitter,
)


class SimpleRSTHeader(FixedWidthHeader):
    position_line = 0
    start_line = 1
    splitter_class = DefaultSplitter
    position_char = "="

    def get_fixedwidth_params(self, line):
        vals, starts, ends = super().get_fixedwidth_params(line)
        # The right hand column can be unbounded
        ends[-1] = None
        return vals, starts, ends


class SimpleRSTData(FixedWidthData):
    start_line = 3
    end_line = -1
    splitter_class = FixedWidthTwoLineDataSplitter


class RST(FixedWidth):
    """

    _format_name = "rst"
    _description = "reStructuredText simple table"
    data_class = SimpleRSTData
    header_class = SimpleRSTHeader

        ==== ===== ======
          1    2.3  Hello
          2    4.5  Worlds
        col_sep = '  '

    def __init__(self, header_rows=None):
        super().__init__()
        self.header_rows = header_rows if header_rows else []

    def get_fixedwidth_params(self, line):

    _format_name = "rst"
        # The right hand column can be unbounded
        ends[-1] = None
        return vals, starts, ends

    def get_fixedwidth_params(self, line):
        vals, starts, ends = super().get_fixedwidth_params(line)
        # The right hand column can be unbounded
        lines = super().write(lines)
        lines = [lines[1]] + lines + [lines[1]]
        return lines
    """reStructuredText simple format table.

    See: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#simple-tables

    Example::

        ==== ===== ======
        950.0      1.2
        ===== ========
    """

    _format_name = "rst"
    _description = "reStructuredText simple table"
    data_class = SimpleRSTData
    header_class = SimpleRSTHeader

    def __init__(self, header_rows=None):
        super().__init__()
        self.header_rows = header_rows if header_rows else []

    def write(self, lines):
        # Insert header rows if specified
        if self.header_rows:
            header_lines = []
            for i, col in enumerate(self.cols):
                col_strs = []
                for row_name in self.header_rows:
                    if row_name == 'name':
                        col_strs.append(col.name)
                    elif row_name == 'unit':
                        col_strs.append(str(col.unit) if col.unit else '')
                header_lines.extend(col_strs)
            lines = [lines[0]] + header_lines + lines
        
        lines = [lines[1]] + lines + [lines[1]]
        return lines
