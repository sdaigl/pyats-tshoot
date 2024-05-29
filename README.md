tshoot.py: A tool to print tree indexes, keys and values when parsing commands using Genie and pyATS 

# Important notes
## Mandatory options:
- You must set the TESTBED parameter in the script
- The -d option must be last in the command line.  It is use to specifies devices to be scan in testbed (you can append them, that is why it must be last)
- The -c option ithe command to be executed, without any other options will printout the json tree

## Other options:
- t Testbed to be use if not using default
- k to specify the k to be search will print out the required json indexes to reach the key value
- V option to match a value or and expression (using the -o option), of course, the -k option must be present
- o operator, default to ==, enables you to search for a particular value for the search key, the -V option must be present
- r  roundabout, default to false, will print out all values, keys for the level with the values was found, the -V option must be present

## In summary:
1. To print the json tree result for a command
python3 tshoot.py -c "show ip int brief" -d SWRACKB SWRACKA
this will give you the indexes to extract the value for exemple: print(p1['interface']['Vlan1']['ip_address'])

2. To show values for a particular key
python3 tshoot.py  -c "show ip int brief" -k ip_address -d SWRACKD -d SWRACKC

3. To show values that will match an expression
python3 tshoot.py  -c "show ip int brief" -k ip_address -V 192.168.2.254 -d SWRACKD -d SWRACKC

4. To show values present at the same-level key
python3 tshoot.py  -c "show mac address-table" -k mac_address -V "000c.2957.bd7f" -r -d SWRACKF -d SWRACKE -d SWRACKD -d SWRACKC -d SWRACKB -d SWRACKA

## command examples:
### Troubleshooting mac addresses
- python3 tshoot.py  -c "show mac address-table" -k mac_address -V "000c.2957.bd7f" -r -d SWRACKF -d SWRACKE -d SWRACKD -d SWRACKC -d SWRACKB -d SWRACKA
- python3 tshoot.py  -c "show arp" -k link_layer_address -V "000c.2957.bd7f" -d SWRACKF -d SWRACKE -d SWRACKD -d SWRACKC -d SWRACKB -d SWRACKA

### Troubleshooting interfaces
- python3 tshoot.py  -c "show interface trunk" -k status -d SWRACKD
- python3 tshoot.py  -c "show interfaces" -k oper_status -d SWRACKD

### Looking at various counters
- python3 tshoot.py   -c "show interfaces"  -k in_errors -V 0 -o ">" -d SWRACKD
- python3 tshoot.py -c "show interfaces" -k in_pkts -V 25011394 -o ">" -d SWRACKD
- python3 tshoot.py -c "show interfaces" -k in_pkts -V 1 -o ">" -d SWRACKA -d SWRACKB -d SWRACKC -d SWRACKD -d SWRACKE -d SWRACKF
- python3 tshoot.py -c "show interfaces" -k out_pkts -V "0" -o ">" -r  -d SWRACKB SWRACKA

### other commands
- python3 tshoot.py  -c "dir flash:" -k size -d SWRACKD
- python3 tshoot.py  -c "show ip route" -k metric -d SWRACKD
- python3 tshoot.py  -c "show running-config" -d SWRACKD
- python3 tshoot.py  -c "show configuration" -d SWRACKD

