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
About:   Functions that read and write csv files
"""
import re, ast
import numpy as np


# CSV FILE FUNCTIONS ==========================================================#

def read_csv(filename, skip_rows=0, header="top"):
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
    if (header == "top"):
        return read_csv_header_top(filename, skip_rows)

    elif (header == "left"):
        return read_csv_header_left(filename, skip_rows)
    
    else:
        return {}

def read_raw_csv(filename, skip_rows=0):
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
            for val, s in  re.findall(r"\s*((['\"])?.*?(?(2)\2))(?:[,;]|\n)", line):
                try:
                    val = ast.literal_eval(val)
                except:
                    pass

                row.append(val)

            if row and row != ['']:
                data.append(row)

    return data

def read_csv_header_top(filename, skip_rows=0):
    """
    Read a csv file with header in first row.

    @param  filename   File name (*.csv)
    @param  skip_rows  Number of lines to skip at the beginning of the file

    @return csvData    Dictionary with header as key
    """
    raw = read_raw_csv(filename, skip_rows)
    ncols = 0

    # Transpose data
    transpose = [[] for key in raw[0]]
    for row in raw[1:]:
        for ncol, val in enumerate(row):
            transpose[ncol].append(val) 

        for i in range(len(row), len(transpose)):
            transpose[i].append('')

    # Create dictionary
    data = {}
    for i, key in enumerate(raw[0]):
        data[key] = transpose[i]

    return data

def read_csv_header_left(filename, skip_rows=0):
    """
    Read a csv file whit header in first column.

    @param  filename   File name (*.csv)
    @param  skip_rows  Number of lines to skip at the beginning of the file

    @return csvData    Dictionary with header as key
    """
    raw = read_raw_csv(filename, skip_rows)

    data = {}
    for row in raw:
        data[row[0]] = row[1:]

    return data

# INI FILE FUNCTIONS ==========================================================#

def read_ini(filename):

    d = {}

    with open(filename, 'r') as f:
                                      
        for sec, data in re.findall(r"\[\s*(.+?)\s*\].*?\n(.*?)(?=\[|$)", f.read(), re.DOTALL):
            d[sec] = {}
            for key, value in re.findall(r"\s*(.+?)\s*=\s*(.+?)\s*(?=\n|$)", data):
                try:
                    value = ast.literal_eval(value)
                except:
                    pass

                d[sec][key] = value

    return d
