import os
from sys import path

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
import re
import itertools
import linecache

# define the name of the file to read from
filename = "configs\\test1"


def check_desc_and_bds(line_number):
    # retrieve specific line
    #line_content = linecache.getline(filename, line_number)
    #print("Found line %i of %s:" % (line_number, filename))
    #print('Current Line Content Is :' + line_content)
    for i in range(line_number - 1, 0, -1):
        #print('I is : ' + str(i))
        line_content_tmp = linecache.getline(filename, i)
        #print('Temp Line Content Is : ' + line_content_tmp)
        line_content_tmp_lastindex = len(line_content_tmp) - 1
        if "desc" in line_content_tmp[0: 12]:
            if "desc" in line_content_tmp[0: 12] and "bds-" in line_content_tmp[0:line_content_tmp_lastindex]:
                desc = line_content_tmp[13:line_content_tmp_lastindex]
                print('Description is ' + desc)
                line_Interfac_tmp = linecache.getline(filename, i - 1)
                print('Interface is ' + line_Interfac_tmp)
                break
            # get only the nearest description
            break


def check_range_in_line(linecontent):
    b = re.findall(r"(\d\d*\d*\d*)+[-]+(\d\d*\d*\d*)", linecontent)
    if b != None:
        #print('BXX LIst is : ')
        #print(b)
        for a, b in b:
            if int(a) < 10 < int(b):
                #print('The Valid Range IS : ' + a + '-' + b)
                return True
                """ retrun true
                else return false """
        return False


def search_string_in_file(file_name, string_to_search):
    """ Search for the given string in file and return lines containing that string, along with line numbers """
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))

    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results


list1 = os.listdir("configs")
print(list1)
for files in list1:

    file2 = open("configs\\" + str(files))
    matched_lines = search_string_in_file("configs\\" + str(files), 'switchport trunk allowed')

    print('Total Matched \"switchport trunk allowed\"  in lines : ', len(matched_lines))
    for elem in matched_lines:
        #print('Line Number = ', elem[0], ' :: Line = ', elem[1])
        _is_valid_range = check_range_in_line(elem[1])
        #print(_is_valid_range)
        if _is_valid_range:
            check_desc_and_bds(elem[0])

file2.close()

