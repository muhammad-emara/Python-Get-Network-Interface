import linecache
import os
import re

import pandas as pd
from openpyxl import load_workbook

list1 = os.listdir("configs\\BDs Test interfaces\\")
list2 = os.listdir("configs\\BDs Test Config\\")
# print (list2)
# print (list1)

MyDict = dict()
TotalPortsNumber = 0
TotalSubint = 0
TotalVI = 0
Z = 0

for files in list1:
    file1 = open("configs\\BDs Test interfaces\\" + str(files))
    N = str(files)
    PortsNumber = 0
    VI = 0
    Physical = []
    subinterface1 = 0
    subinterface = []
    VI_list = []
    Desc = []
    Desc1 = []
    Desc2 = []
    int_name = []
    z = str
    Z1 = str
    Range = []
    for line in file1:
        int_name = []
        Desc = []
        Physical = []
        Desc1 = []
        if "up             up" in line and "Vl" in line[0: 2]:
            interface_Name = line[0: 12]
            interface_Desc = line[54: 120]
            # print(' Outer IF Found interface with name ' + interface_Name + ' and its desc is ' + interface_Desc)
            if "Node" in interface_Desc or "node" in interface_Desc or "lte" in interface_Desc or "LTE" in interface_Desc or "EITCHuawaiIBS" in interface_Desc or "Huawai-IBS" in interface_Desc or "MobileIBS" in interface_Desc or "HuaweiIBS" in interface_Desc or "5G" in interface_Desc or "HuawIBS" in interface_Desc:
                VI = VI + 1
                print('Found interface with name ' + interface_Name + ' and its desc is ' + interface_Desc)
                p = (str(interface_Name))
                p1 = p.strip(' ')
                o = p.strip('Vl')
                o1 = o.strip(' ')
                print(o1)
                Physical.append(p1)
                Desc1.append(interface_Desc)
                print(interface_Desc)

                # file2 = open("configs\\BDs Test Config\\" + str(files), "r+")
                # print('linecache.getline(file2, 4258) is i ' + linecache.getline("configs\\BDs Test Config\\" + str(files), 4258))

                with open("configs\\BDs Test Config\\" + str(files), "r+") as file2:
                    # x_file = "configs\\test1"
                    # print('File Name is ' + str(x_file))
                    # print('linecache.getline(file2, 4258) is i ' + linecache.getline("configs\\BDs Test Config\\" + str(files), 4258)) #4258

                    def check_desc_and_bds(line_number):
                        # retrieve specific line
                        line_content = linecache.getline("configs\\BDs Test Config\\" + str(files), line_number)
                        print("Found line %i of %s:" % (line_number, "configs\\BDs Test Config\\" + str(files)))
                        print('Current Line Content Is :' + line_content)
                        for i in range(line_number - 1, 0, -1):
                            print('I is : ' + str(i))
                            line_content_tmp = linecache.getline("configs\\BDs Test Config\\" + str(files), i)
                            print('Temp Line Content Is : ' + line_content_tmp)
                            line_content_tmp_lastindex = len(line_content_tmp) - 1
                            if "desc" in line_content_tmp[0: 12]:
                                if "desc" in line_content_tmp[0: 12] and "bds-" in line_content_tmp[
                                                                                   0:line_content_tmp_lastindex]:
                                    desc = line_content_tmp[13:line_content_tmp_lastindex]
                                    print('Description is ' + desc)
                                    line_Interfac_tmp = linecache.getline("configs\\BDs Test Config\\" + str(files),
                                                                          i - 1)
                                    print('Interface is ' + line_Interfac_tmp)
                                    break
                                # get only the nearest description
                                break


                    def check_range_in_line(linecontent):
                        b = re.findall(r"(\d\d*\d*\d*)+[-]+(\d\d*\d*\d*)", linecontent)
                        if b != None:
                            # print('BXX LIst is : ')
                            # print(b)
                            for a, b in b:
                                if int(a) < int(o1) < int(b):
                                    # print('The Valid Range IS : ' + a + '-' + b)
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


                    for i, line2 in enumerate(file2):
                        print('for i, line2 in enumerate(file2): Line2 value is ')
                        print(line2)
                        print('for i, line2 in enumerate(file2): I value is : ')
                        print(i)

                        if ("," + str(o1) + ",") in line2 or ("," + str(o1) + "-") in line2 or (
                                "-" + str(o1) + ",") in line2:
                            z = linecache.getline("configs\\BDs Test Config\\" + str(files), i)
                            print(z)
                            x = int(i) - 10
                            file2.seek(0)
                            for j, line3 in enumerate(file2):
                                if x < j < i:
                                    if "desc" in line3[0: 12]:
                                        desc = line3[13:50]
                                        print('Config Dec is ' + desc)
                                        Desc.append(desc)
                                    if "interface" in line3[0:9]:
                                        # print ("True")
                                        interface = line3[9:60]
                                        print(interface)
                                        int_name.append(interface)

                                        # print (int_name)

                        elif ("," + str(o1) + ",") not in line2 or ("," + str(o1) + "-") not in line2 or (
                                "-" + str(o1) + ",") not in line2:
                            for files in list1:
                                matched_lines = search_string_in_file(
                                    "configs\\BDs Test Config\\" + str(files), 'switchport trunk allowed')
                                print('Total Matched \"switchport trunk allowed\"  in lines : ', len(matched_lines))
                                for elem in matched_lines:
                                    print('Line Number = ', elem[0], ' :: Line = ', elem[1])
                                    _is_valid_range = check_range_in_line(elem[1])
                                    print(_is_valid_range)
                                    if _is_valid_range:
                                        check_desc_and_bds(elem[0])

                    print('int_name Len is :' + str(len(int_name)))
                    print('desc Len is :' + str(len(desc)))
                    if len(int_name) > 0 and len(desc) > 0:
                        # print('desc [0] is '+desc)
                        if 'BDS' not in desc:
                            print('Desc Not Matching BDS')
                            continue
                    else:
                        continue

                    print('int_name IS \n')

                    print(int_name)
                    print('Desc IS \n')
                    print(Desc)
                    print(N)
                    if Z == 0:
                        # df1 = pd.DataFrame({'Physical': int_name ,'Uplink_Descreption': Desc , 'Uplink' : N })
                        df1 = pd.DataFrame.from_dict(
                            {'Physical': pd.Series(int_name), 'Uplink_Descreption': pd.Series(Desc), 'Uplink': N,
                             'VLAN': pd.Series(Physical)
                                , 'Int_Desc': pd.Series(Desc1)})
                        writer = pd.ExcelWriter('Ahmed1.xlsx', engine='xlsxwriter')
                        df1.to_excel(writer, sheet_name='VI_Interfaces', index=False)
                        writer.save()
                        Z = +1
                        print(Z)

                    elif Z == 1:
                        df1 = pd.DataFrame(
                            {'Physical': pd.Series(int_name), 'Uplink_Descreption': pd.Series(Desc), 'Uplink': N,
                             'VLAN': pd.Series(Physical)
                                , 'Int_Desc': pd.Series(Desc1)})
                        writer = pd.ExcelWriter('Ahmed1.xlsx', engine='openpyxl')
                        writer.book = load_workbook('Ahmed1.xlsx')
                        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
                        reader = pd.read_excel('Ahmed1.xlsx', 'VI_Interfaces')
                        df1.to_excel(writer, sheet_name='VI_Interfaces', index=False, startrow=len(reader) + 2)
                        writer.save()
                        writer.close()

    # file1.close()
    # file2.close()

print("TotalPort is :  " + str(TotalPortsNumber))
print("TotalSub is :  " + str(TotalSubint))
print("TotalVI is :  " + str(TotalVI))
print(VI_list)
print(TotalVI)
