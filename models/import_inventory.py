#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Import inventory from xlsx file.

Uses openpyxl.
"""

import errno
import os
from contextlib import contextmanager


import openpyxl


from sqlite_engine import session_scope


__author__ = 'Brett R. Ward'

# Constants


def main():
    """Main program."""
    with session_scope() as session:
        workbook = openpyxl.load_workbook('WoF_inventory.xlsx')
        print(workbook.get_sheet_names())
        for name in workbook.get_sheet_names():
            sheet = workbook.get_sheet_by_name(name)
            for row in sheet.iter_rows():
                for cell in row:
                    print(cell.value)


if __name__ == "__main__":
    main()
