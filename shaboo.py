import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
import re
import itertools
import xlsxwriter
import xlrd

list1 = os.listdir("C:\\Users\\Emara\\Downloads\\BDs Test interfaces\\")
list2 = os.listdir("C:\\Users\\Emara\\Downloads\\BDs Test Config\\")
# print (list2)
# print (list1)

MyDict = dict()
TotalPortsNumber = 0
TotalSubint = 0
TotalVI = 0
Z = 0

for files in list1:
    file1 = open("C:\\Users\\Emara\\Downloads\\BDs Test interfaces\\" + str(files))
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
            # if "up             up" in line:
            interface_Name = line[0: 12]
            # interface_Desc = line[54: 120]
            line_lastIndx = len(line) - 1
            interface_Desc = line[54: line_lastIndx]
            if "BDS" in interface_Desc or "bds" in interface_Desc:
                print(
                    ' BDS Interfaces IF Found interface with name ' + interface_Name + ' and its desc is ' + interface_Desc)

            if "BDS" in interface_Desc or "bds" in interface_Desc or "Node" in interface_Desc or "node" in interface_Desc or "lte" in interface_Desc or "LTE" in interface_Desc or "EITCHuawaiIBS" in interface_Desc or "Huawai-IBS" in interface_Desc or "MobileIBS" in interface_Desc or "HuaweiIBS" in interface_Desc or "5G" in interface_Desc or "HuawIBS" in interface_Desc:
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

                file2 = open("C:\\Users\\Emara\\Downloads\\BDs Test Config\\" + str(files))
                for i, line2 in enumerate(file2):

                    if ("," + str(o1) + ",") in line2 or ("," + str(o1) + "-") in line2 or (
                            "-" + str(o1) + ",") in line2:
                        x = int(i) - 10
                        file2.seek(0)
                        for j, line3 in enumerate(file2):
                            if x < j < i:
                                if "desc" in line3[0: 12]:
                                    line3_lastindx = len(line3) - 1
                                    desc = line3[13:line3_lastindx]
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
                        if "switchport trunk allowed vlan" in line2:
                            # print (i)
                            # print  (line2)
                            b = re.search(r"(\d\d*\d*\d*)+[-]+(\d\d*\d*\d*)", line2)
                            if b == None:
                                pass
                            if b != None:
                                if int(b.group(1)) < int(o1) < int(b.group(2)):
                                    # print (b.group(1))
                                    # print (b.group(2))
                                    q = (str(b.group(1)) + "-" + str(b.group(2)))
                                    print(q)
                                    Range.append(q)
                                    # print (i)
                                    x = int(i) - 12
                                    # print (x)
                                    file2.seek(0)
                                    for j, line3 in enumerate(file2):
                                        if x < j < i:
                                            if "desc" in line3[0: 12]:
                                                # desc = line3[13:50]
                                                desc = line3[13:50]
                                                print('Config Desc found IS ' + desc)
                                                if "BDS" or "bds" in desc:
                                                    print('BDS Desc found IS ' + desc)
                                                    Desc.append(desc)
                                                else:
                                                    continue
                                            if "interface" in line3[0:9]:
                                                # print ("True")
                                                interface = line3[9:60]
                                                print(interface)
                                                int_name.append(interface)

                print('int_name Len is :' + str(len(int_name)))
                print('desc Len is :' + str(len(Desc)))
                if len(Desc) > 0:
                    # print('desc [0] is '+desc)
                    if ("BDS" or "bds") not in desc:
                        print('Desc Not Matching BDS')
                        continue
                # else:
                # continue

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

# print("TotalPort is :  " + str(TotalPortsNumber))
# print("TotalSub is :  " + str(TotalSubint))
# print("TotalVI is :  " + str(TotalVI))
# print(VI_list)
# print(TotalVI)
