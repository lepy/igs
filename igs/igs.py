# -*- coding: utf-8 -*-

"""igs module."""

import pandas as pd
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

class Iges():
    """iges object"""
    line_font_pattern = {None: 'Default',
                         0: 'Default',
                         1: 'Solid',
                         2: 'Dashed',
                         3: 'Phantom',
                         4: 'Centerline',
                         5: 'Dotted'}

    def __init__(self, fh):

        self.df_raw = None
        self.de = None

        if fh:
            fh = StringIO(s)
            colspecs = [(0, 72), (72, 73), (73, 80)]
            self.df_raw = pd.read_fwf(fh, colspecs=colspecs, header=None, index_col=None,
                                      columns=["data", "section_code", "sequence_number"])
            self.df_raw.columns = ["data", "section_code", "sequence_number"]
            print(self.df_raw.head())
            self.de = self.read_data_entries()
            print(self.de.head())
            print(self.de.tail())

    def read_data_entries(self):
        """parse iges structure"""
        df = self.df_raw[self.df_raw["section_code"] == "D"]
        # print(df)
        entry_list = []
        columns = ["entity_type_number",
                   "parameter_data",
                   "structure",
                   "line_font_pattern",
                   "level",
                   "view",
                   "transfromation_matrix",
                   "label_display_assoc",
                   "status_number",
                   "line_weight_number",
                   "color_number",
                   "parameter_line_count",
                   "form_number",
                   "entry_label",
                   "entry_subscript_number",
                   "data",
                   ]
        for i in range(len(df) // 2):
            row0 = df.iloc[i * 2]
            row1 = df.iloc[i * 2 + 1]
            s1 = entity_type_number = row0["data"][:8]
            s2 = parameter_data = row0["data"][8:16]
            s3 = structure = row0["data"][16:24]
            s4 = line_font_pattern = row0["data"][24:32]
            s5 = level = row0["data"][32:40]
            s6 = view = row0["data"][40:48]
            s7 = transfromation_matrix = row0["data"][48:56]
            s8 = label_display_assoc = row0["data"][56:64]
            s9 = status_number = row0["data"][64:72]
            # s10 = sequence_number = row0["data"][72:80]
            s11 = entity_type_number_ = row1["data"][:8]
            s12 = line_weight_number = row1["data"][8:16]
            s13 = color_number = row1["data"][16:24]
            s14 = parameter_line_count = row1["data"][24:32]
            s15 = form_number = row1["data"][32:40]
            s16 = row1["data"][40:48]
            s17 = row1["data"][48:56]
            s18 = entry_label = row1["data"][56:64]
            s19 = entry_subscript_number = row1["data"][64:72]
            data = None
            # s20 = row1["data"][72:80]
            # iges_entity_type_number_ = row1["data"][:8]
            # print(iges_entity_type_number, iges_entity_type_number_)
            if entity_type_number != entity_type_number_:
                raise Exception("invalid data entries")
            # print(iges_entity_type_number, parameter_data, parameter_line_count)
            entry_list.append([entity_type_number,
                               parameter_data,
                               structure,
                               line_font_pattern,
                               level,
                               view,
                               transfromation_matrix,
                               label_display_assoc,
                               status_number,
                               line_weight_number,
                               color_number,
                               parameter_line_count,
                               form_number,
                               entry_label,
                               entry_subscript_number,
                               data,
                               ])
        de = pd.DataFrame(entry_list, columns=columns)
        # print(d)

        del df
        df = self.df_raw[self.df_raw["section_code"] == "P"]
        df.index = df.sequence_number
        print("!", df)
        print("!", df.data.values)

        # add param string
        param_str = df['data'].str[:64]
        param_str.name = "param_str"
        df = df.join(param_str)

        # add de_pointer
        de_pointer = df['data'].str[65:72]
        de_pointer.name = "de_pointer"
        df = df.join(de_pointer)

        # for i in range(len(df) // 2):
        #     row0 = df.iloc[i*2]
        #
        #
        # param_string = data[:64]
        # directory_pointer = int(data[64:72].strip())
        print("df", df)
        print(df.columns)
        return de


if __name__ == '__main__':
    s = """                                                                        S0000001
,,31HOpen CASCADE IGES processor 6.8,13HFilename.iges,                  G0000001
16HOpen CASCADE 6.8,31HOpen CASCADE IGES processor 6.8,32,308,15,308,15,G0000002
,1.,2,2HMM,1,0.01,15H20180114.122329,1E-07,11.510691,,,11,0,            G0000003
15H20180114.122329,;                                                    G0000004
     402       1       0       0       0       0       0       000000000D0000001
     402       0       0       1       1                               0D0000002
     144       2       0       0       0       0       0       000020000D0000003
     144       0       0       1       0                               0D0000004
     108       3       0       0       0       0       0       000010000D0000005
     108       0       0       1       0                               0D0000006
     142       4       0       0       0       0       0       000010500D0000007
     142       0       0       1       0                               0D0000008
     102       5       0       0       0       0       0       000010000D0000009
     102       0       0       1       0                               0D0000010
     110       6       0       0       0       0       0       000010000D0000011
     110       0       0       1       0                               0D0000012
     110       7       0       0       0       0       0       000010000D0000013
     110       0       0       1       0                               0D0000014
     110       8       0       0       0       0       0       000010000D0000015
     110       0       0       1       0                               0D0000016
     110       9       0       0       0       0       0       000010000D0000017
     110       0       0       1       0                               0D0000018
     144      10       0       0       0       0       0       000020000D0000019
     144       0       0       1       0                               0D0000020
     108      11       0       0       0       0       0       000010000D0000021
     108       0       0       1       0                               0D0000022
     142      12       0       0       0       0       0       000010500D0000023
     142       0       0       1       0                               0D0000024
     102      13       0       0       0       0       0       000010000D0000025
     102       0       0       1       0                               0D0000026
     110      14       0       0       0       0       0       000010000D0000027
     110       0       0       1       0                               0D0000028
     110      15       0       0       0       0       0       000010000D0000029
     110       0       0       1       0                               0D0000030
     110      16       0       0       0       0       0       000010000D0000031
     110       0       0       1       0                               0D0000032
402,2,3,19;                                                      0000001P0000001
144,5,1,0,7;                                                     0000003P0000002
108,0.,0.,-1.,0.,0,4.550729124,-0.744933762,0.,0.;               0000005P0000003
142,0,5,0,9,2;                                                   0000007P0000004
102,4,11,13,15,17;                                               0000009P0000005
110,4.550729124,-0.744933762,0.,7.323911066,1.835075705,1.;      0000011P0000006
110,7.323911066,1.835075705,0.,10.105619833,-2.675265688,0.;     0000013P0000007
110,10.105619833,-2.675265688,0.,5.242880018,-5.702914677,0.;    0000015P0000008
110,5.242880018,-5.702914677,0.,4.550729124,-0.744933762,0.;     0000017P0000009
144,21,1,0,23;                                                   0000019P0000010
108,0.,0.,1.,0.,0,7.323911066,1.835075705,0.,0.;                 0000021P0000011
142,0,21,0,25,2;                                                 0000023P0000012
102,3,27,29,31;                                                  0000025P0000013
110,7.323911066,1.835075705,0.,10.105619431,-2.675265789,0.;     0000027P0000014
110,10.105619431,-2.675265789,0.,11.510690799,0.854641465,0.;    0000029P0000015
110,11.510690799,0.854641465,0.,7.323911066,1.835075705,0.;      0000031P0000016
S      1G      4D     32P     16                                        T0000001
"""
    fh = StringIO(s)

    iges = Iges(fh)
    # colspecs = [(0, 72), (72, 73), (73, 80)]
    #
    # df = pd.read_fwf(fh, colspecs=colspecs, header=None, index_col=0)
    # # df = pd.read_csv(fh, sep=";")
    # print(df)
    # for i, row in df[df[1]=="D"].iterrows():
    #     print(row)
