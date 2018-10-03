#-*-coding: utf-8-*-
"""
Copyright [2018] [Souza Jr, B. G.]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Bismarck Gomes Souza Junior <bismarckgomes@gmail.com>
About:  Functions that read files
"""
import re, ast
import xlrd, xlwt
import numpy as np
from xlrd.sheet import ctype_text
from datetime import date


# TABLE FUNCTIONS =============================================================#

def read_table_header_top(table):
    """
    Read a table with header in first row.

    @param  table   Matrix format

    @return dict    Dictionary with header as key
    """
    # Transpose data
    transpose = [[] for key in table[0]]
    for row in table[1:]:
        for ncol, val in enumerate(row):
            transpose[ncol].append(val)

        for i in range(len(row), len(transpose)):
            transpose[i].append('')

    # Create dictionary
    data = {}
    for i, key in enumerate(table[0]):
        data[key] = transpose[i]

    return data

def read_table_header_left(table):
    """
    Read a table whit header in first column.

    @param  table   Matrix format

    @return dict    Dictionary with header as key
    """
    data = {}
    for row in table:
        data[row[0]] = row[1:]

    return data

# CSV FILE FUNCTIONS ==========================================================#

def read_csv(filename, skip_rows=0):
    """
    Read a csv file. It is possible use ',' or ';' as delimiter and use string
    delimeters too. Ex:
    "a", "b,", 'c,'
      1,    2,    3

    @param  filename   File name (*.csv)
    @param  skip_rows  Number of lines to skip at the beginning of the file

    @return csvData    List of list
    """
    data  = []
    with open(filename, 'r') as f:
        for line in f.readlines()[skip_rows:]:
            row = []
            founds1 = re.findall(r"\s*((['\"])?.*?(?(2)\2))(?:;|\n)", line)
            founds2 = re.findall(r"\s*((['\"])?.*?(?(2)\2))(?:,|\n)", line)
            founds = founds1 if len(founds1)>=len(founds2) else founds2

            for val, s in founds:
                try:
                    val = ast.literal_eval(val)
                except:
                    pass

                row.append(val)

            if row and row != ['']:
                data.append(row)

    return data

def read_csv_as_dict(filename, skip_rows=0, header="top"):
    """
    Read a csv file. It is possible use ',' or ';' as delimiter and use string
    delimeters too. Ex:
    "a", "b,", 'c,'
      1,    2,    3

    @param  filename   File name (*.csv)
    @param  skip_rows  Number of lines to skip at the beginning of the file
    @param  header     Header position. Options: "top", "left"

    @return csvData    Dictionary with header as key
    """
    table = read_csv(filename, skip_rows)

    if (header == "top"):
        return read_table_header_top(table)

    elif (header == "left"):
        return read_table_header_left(table)

    else:
        return {}

# INI FILE FUNCTIONS ==========================================================#

def read_ini(filename):

    d = {}

    with open(filename, 'r') as f:

        for sec, data in re.findall(r"\s*\[\s*(.+?)\s*\].*?\n(.*?)(?=\n\[|$)", f.read(), re.DOTALL):
            d[sec] = {}
            for key, value, s in re.findall(r"^\s*([^#]+?)\s*=\s*((['\"])?.*?(?(3)\3))\s*(?:#.*)?(?=$)", data, re.MULTILINE):
                try:
                    value = ast.literal_eval(value)
                except:
                    pass

                d[sec][key] = value

    return d

# XLS FILE FUNCTIONS ==========================================================#

def read_xls(filename, itemsize=500):
    """
    Read a xls file as list of list.

    @param  filename   File name (*.xls or *.xlsx)
    @param  itemsize   Length of strings in table

    @return table    List of list
    """
    wb = xlrd.open_workbook(filename)
    sh = wb.sheet_by_index(0)

    table = np.chararray((sh.nrows, sh.ncols), itemsize=itemsize)
    row = 0
    for i in range(sh.nrows):
        for j in range(sh.ncols):
            if (sh.cell(row, j).ctype == 1):
                table[i][j] = sh.cell(row, j).value.encode('utf-8')

            elif (sh.cell(row, j).ctype == 2): # Number, Money
                table[i][j] = str(int(sh.cell(row, j).value))

            elif (sh.cell(row, j).ctype == 3): # Date
                d = date.fromordinal(int(sh.cell(row, j).value) + 693594)
                table[i][j] = str(d)

        row += 1

    return table

def read_xls_as_dict(filename, header="top"):
    """
    Read a xls file as dictionary.

    @param  filename   File name (*.xls or *.xlsx)
    @param  header     Header position. Options: "top", "left"

    @return            Dictionary with header as key
    """
    table = read_xls(filename)

    if (header == "top"):
        return read_table_header_top(table)

    elif (header == "left"):
        return read_table_header_left(table)

    else:
        return {}

def read_file_as_dict(filename):
    """
    Read file as a dictionary.

    @param  filename   File name (ini, csv, xls or xlsx)

    @return            Dictionary with header as key
    """
    if filename.endswith('.csv'):
        return read_csv_as_dict(filename)

    elif filename.endswith('.xls') or filename.endswith('.xlsx'):
        return read_xls_as_dict(filename)

    elif filename.endswith('.ini'):
        return read_ini(filename)
