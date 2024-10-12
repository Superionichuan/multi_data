#THIS PROGRAM IS DESIGNED TO MONITOR CONFIGURATIONS USED DURING DOING CONCURRENT MACHINE LEARNING WITH DPGEN

# ` Multi_data.py `

# python '<file_adress eg ./iter*>,<c/r/col/column/row>,<[] []--- all avaliable [0:2.3.6:9]]----- 0 2 3 6 7 8 9 [:3] ---- 0 1 2 3>,<0 ---- read from col or row subtitle 1----> read from file name 2----> read from infile.json>;<><><>;<txt=on>;<type=row>;<name=infile.dat>'    

# an Example
# python multi_data.py './iter*,c,[0:2],0'
# infile.json is needed to support multi_data.py  ; if it is absent, 1 :  python multi_data.py files='./iter*,c,[0:2],0' to generate a  standard infile.json, than run : python multi_data.py './iter*,c,[0:2],0'

# Seperate configuration group and defination can be divided by ';'   



#### multi_data.py ####
## Note:
# When input is files=''   like python ccmp.py files=''  it means “ python multi_data.py ''  ”。 When input is '' , multi_data.py  will not analysis configstr but read dirs and mode deposited in infile.json.
# When "files=" is not specified in argstr, just read ccmp.conf and use input_files tag to obatin input arg for multi_data.

# Seperately used from ccmp and other scripts. To achieve this, one should install multi_data.py seperately.

# Standard infile.json
{
    "configuration[1]": {
        "files": [
            "ccdc_iter_000000_pres_20-130_modeldevi_F"
        ],
        "type": "row",
        "ranges": [],
        "label_mode": 0,
        "skip_head": 1
    },
    "write_text": {
        "txt": "on",
        "name": "infile.dat",
        "type": "column"
    },
    "titles": {
        "title_0": "iter_000000_pres_20",
        "title_1": "iter_000000_pres_40",
        "title_2": "iter_000000_pres_80",
        "title_3": "iter_000000_pres_100",
        "title_4": "iter_000000_pres_120",
        "title_5": "iter_000000_pres_130"
    }
}

# skip_head: x  means skip x row or x column to read data in.

# mode 0 ------> read label from first row or column.
# mode 1 ------> read label from file name.
# mode 2 ------> read label from infile.json.


# you can set ;txt=on ; type=xxx ; name =xxx in the args, and  you can also modify it in the infile.json directly.
