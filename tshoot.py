#!/usr/bin/env python3
"""tshoot.py: A tool to print tree indexes, keys and values when parsing commands using Genie and pyATS 

Important notes
Mandatory options:
- You must set the TESTBED parameter in the file
- The -d option must be last in the command line.  It is use to specifies devices to be scan in testbed (you can append them, that is why it must be last)
- The -c option ithe command to be executed, without any other options will printout the json tree

Other options:
-t Testbed to be use if not using default
-k to specify the k to be search will print out the required json indexes to reach the key value
-V option to match a value or and expression (using the -o option), of course, the -k option must be present
-o operator, default to ==, enables you to search for a particular value for the search key, the -V option must be present
-r  roundabout, default to false, will print out all values, keys for the level with the values was found, the -V option must be present

In summary:
1) To print the json tree result for a command
python3 tshoot.py -c "show ip int brief" -d SWRACKB SWRACKA
this will give you the indexes to extract the value for example: print(p1['interface']['Vlan1']['ip_address'])

2) To show values for a particular key (options -k)
python3 tshoot.py  -c "show ip int brief" -k ip_address -d SWRACKD -d SWRACKC

3) To show values that will match an expression. (options -k, -V, -r and maybe -o if looking at counters)
python3 tshoot.py  -c "show ip int brief" -k ip_address -V 192.168.2.254 -d SWRACKD -d SWRACKC

4) To show values present at the same-level key matching an expression (options -k, -V, -r and maybe -o if looking at counters)
python3 tshoot.py  -c "show mac address-table" -k mac_address -V "000c.2957.bd7f" -r -d SWRACKF -d SWRACKE -d SWRACKD -d SWRACKC -d SWRACKB -d SWRACKA

A good place to start with examples:
https://github.com/sdaigl/pyats-tshoot/blob/main/README.md


Command référence for pyats:
https://github.com/CiscoTestAutomation/genieparser/tree/master/src/genie/libs/parser

"""
__author__      = "Serge Daigle, sdaigl@gmail.com"
__copyright__   = "2023 - Please put my name somewhere"



#  DEFAULT VALUES TO BE CHANGED
#################################### CHANGEZ MOI ICI ####################################
TESTBED = 'yaml/f2200.yaml'
EQUIPEMENT = []
#########################################################################################

# Module import
from pkg_resources import parse_version
from genie.testbed import load
from genie.utils import Dq
from optparse import OptionParser
import operator


#  Options parser
parser = OptionParser()
parser.add_option("-t", "--testbed", dest="tb",default=TESTBED,help="test bed to analyze")
parser.add_option("-c", "--command", dest="cmd",default="show version",help="command to execute")
parser.add_option("-k", "--key", dest="key",default="",help="key to find")
parser.add_option("-V", "--Value", dest="Val",default="",help="Value to search for the specified key")
parser.add_option("-o", "--operator", dest="operator",default="==",help="operator to be used if a value specified")
parser.add_option("-r", "--roundabout", dest="roundabout",action="store_true", default=False, help="will print all keys and values at present level if value found")
parser.add_option("-d", "--devices", dest="d",action="append",default=EQUIPEMENT,help="device to be parsed option must be the last one in the cli and maybe multiple")
                  
(options, args) = parser.parse_args()

# functions
def get_truth(inp, relate, cut):
     ops = {'>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq}
     return ops[relate](inp, cut)
 
# check options                  
if options.Val != "" and options.key =="" : 
    print("You must specify -k option in order to use the -V option")
    exit(0)

# Load testbed devices according to the -d option
tb = load(options.tb)                               
devices=options.d                                  

for d in devices:
    __level=[]                                          # to find current level
    dev = tb.devices[d]                                 # choose device
    dev.connect(learn_hostname=True,log_stdout=False)   # connect using testbed creds
    p1 = dev.parse(options.cmd)                         # *** Send command specify by the -c option ***
    print("")
    print ( d+" results for: ",options.cmd)                   
    if options.Val == "" and options.key =="" : print (p1) # print json tree to screen if no other options used
    print("-"*10)                                       # use to speparate devices

                                                        
    def printlevel(level):                              # function giving required index to get the value of a key
        txt=""
        for i in range (0,len(level)):
            txt=txt+"["+"'"+str(level[i])+"'"+"]"
        return(txt)
        

    def PrintTree(dictn):                               # recursive function going thru all json data
        global __level, options
        printothkey=0
        a=""
        for key in dictn.keys():
            if options.key == "" : print(key)
            dict1=dictn[key]
            if type(dict1) is dict and printothkey==0 :            # if a dict prepare for another loop
                __level.append(key)                                # printotherkey used for the roundabout option, will print values of same level when finding a match
                a=printlevel(__level)
                if options.key == "" or options.key == key : print("dict-key:",a)                                  
                PrintTree(dict1)                                             #start recursive loop
        
            else  :                                     # analyze key if not a dict
                a=printlevel(__level)
                if options.key == key or printothkey==1:                     # analyze key
                    index=a+"["+"'"+key+"'"+"]"
                    z="print(p1"+index+")"                               # build the command to be used to obtain the result in the json tree               
                    tv="val=p1"+index                                   # create the index
                    loc={}                                                 
                    exec(tv,globals(),loc)                              # execute the command with the index to extract the value
                    extracted_value = str(loc['val'])                      # value found
                    o_text=get_truth(extracted_value, options.operator, options.Val)
                    if options.Val == ""  :
                        print("Key and level found for: "+d+": "+a+"["+"'"+key+"'"+"]")
                        print ("cmd = "+z) 
                        print ("value", extracted_value,  sep="=")
                    elif o_text or printothkey==1:
                        print("Key and level found for: "+d+": "+a+"["+"'"+key+"'"+"]")
                        print ("cmd = "+z) 
                        print ("value", extracted_value,  sep="=")
                        if options.roundabout : printothkey=1

        if len(__level) > 0 :                           # end of dict terms, remove level and process next data
            __level.pop()
            printothkey=0
            a=printlevel(__level)
            if ((options.key == "" or options.key == key) and a != "") : print("dict-key:",a)
        
    PrintTree(p1)


