tshoot.py: A tool to print tree indexes, keys and values when parsing commands using Genie and pyATS. You can pretty much troubleshoot everything using a simple recursive script :)

# Important notes:
## Mandatory options:
- You must set the TESTBED parameter in the script
- The -d option must be last in the command line.  It is use to specifies devices to be scan in testbed (you can append them, that is why it must be last)
- The -c option ithe command to be executed, without any other options will printout the json tree

## Other options:
- -t Testbed to be use if not using default
- -k to specify the key to be search will print out the required json indexes to reach the key value
- -V option to match a value or and expression (using the -o option), of course, the -k option must be present
- -o operator, default to "==", enables you to search for a particular value for the search key, the -V option must be present and quotes
- -r  roundabout, default to false, will print out all values, keys for the level with the values was found, the -V option must be present

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

## Command examples:
### Troubleshooting mac addresses
- python3 tshoot.py  -c "show mac address-table" -k mac_address -V "000c.2957.bd7f" -r -d SWRACKF -d SWRACKE 
```
python3 tshoot.py -c "show mac address-table" -k mac_address -V "000c.2957.bd7f" -r -d SWRACKF -d SWRACKE

SWRACKF results for:  show mac address-table
----------
Key and level found for: SWRACKF: ['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['mac_address']
cmd = print(p1['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['mac_address'])
value=000c.2957.bd7f
Key and level found for: SWRACKF: ['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['interfaces']
cmd = print(p1['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['interfaces'])
value={'GigabitEthernet0/1': {'interface': 'GigabitEthernet0/1', 'entry_type': 'dynamic'}}

SWRACKE results for:  show mac address-table
----------
Key and level found for: SWRACKE: ['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['mac_address']
cmd = print(p1['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['mac_address'])
value=000c.2957.bd7f
Key and level found for: SWRACKE: ['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['interfaces']
cmd = print(p1['mac_table']['vlans']['1']['mac_addresses']['000c.2957.bd7f']['interfaces'])
value={'GigabitEthernet0/2': {'interface': 'GigabitEthernet0/2', 'entry_type': 'dynamic'}}
```

- python3 tshoot.py  -c "show arp" -k link_layer_address -V "000c.2957.bd7f" -d SWRACKF -d SWRACKE 
```
python3 tshoot.py -c "show arp" -k link_layer_address -V "000c.2957.bd7f" -d SWRACKF -d SWRACKE           

SWRACKF results for:  show arp
----------
Key and level found for: SWRACKF: ['interfaces']['Vlan1']['ipv4']['neighbors']['192.168.1.2']['link_layer_address']
cmd = print(p1['interfaces']['Vlan1']['ipv4']['neighbors']['192.168.1.2']['link_layer_address'])
value=000c.2957.bd7f

SWRACKE results for:  show arp
----------
Key and level found for: SWRACKE: ['interfaces']['Vlan1']['ipv4']['neighbors']['192.168.1.2']['link_layer_address']
cmd = print(p1['interfaces']['Vlan1']['ipv4']['neighbors']['192.168.1.2']['link_layer_address'])
value=000c.2957.bd7f
```

### Troubleshooting interfaces
- python3 tshoot.py  -c "show interface trunk" -k status -d SWRACKF
```
python3 tshoot.py  -c "show interface trunk" -k status -d SWRACKF

SWRACKF results for:  show interface trunk
----------
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['status']
cmd = print(p1['interface']['GigabitEthernet0/1']['status'])
value=trunking
```
#### Same command using the -r option with a value to get more interesting results

 python3 tshoot.py  -c "show interface trunk" -k status -V trunking -r -d SWRACKF
```
python3 tshoot.py  -c "show interface trunk" -k status -V trunking -r -d SWRACKF

SWRACKF results for:  show interface trunk
----------
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['status']
cmd = print(p1['interface']['GigabitEthernet0/1']['status'])
value=trunking
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['native_vlan']
cmd = print(p1['interface']['GigabitEthernet0/1']['native_vlan'])
value=1
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['vlans_allowed_on_trunk']
cmd = print(p1['interface']['GigabitEthernet0/1']['vlans_allowed_on_trunk'])
value=1-4094
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['vlans_allowed_active_in_mgmt_domain']
cmd = print(p1['interface']['GigabitEthernet0/1']['vlans_allowed_active_in_mgmt_domain'])
value=1-48,50,55,100-103,123,210
Key and level found for: SWRACKF: ['interface']['GigabitEthernet0/1']['vlans_in_stp_forwarding_not_pruned']
cmd = print(p1['interface']['GigabitEthernet0/1']['vlans_in_stp_forwarding_not_pruned'])
value=1-48,50,55,100-103,123,210
```
- python3 tshoot.py  -c "show interfaces" -k oper_status -d SWRACKD

```
python3 tshoot.py -c "show interfaces" -k oper_status -d SWRACKF

SWRACKF results for:  show interfaces
----------
Key and level found for: SWRACKF: ['Vlan1']['oper_status']
cmd = print(p1['Vlan1']['oper_status'])
value=up
Key and level found for: SWRACKF: ['FastEthernet0/1']['oper_status']
cmd = print(p1['FastEthernet0/1']['oper_status'])
value=down
Key and level found for: SWRACKF: ['FastEthernet0/2']['oper_status']
cmd = print(p1['FastEthernet0/2']['oper_status'])
:
:
```
#### Same command using the -V option with a value of up to see all "up" interfaces
```
python3 tshoot.py -c "show interfaces" -k oper_status -V "up" -d SWRACKF

SWRACKF results for:  show interfaces
----------
Key and level found for: SWRACKF: ['Vlan1']['oper_status']
cmd = print(p1['Vlan1']['oper_status'])
value=up
Key and level found for: SWRACKF: ['FastEthernet0/4']['oper_status']
cmd = print(p1['FastEthernet0/4']['oper_status'])
value=up
Key and level found for: SWRACKF: ['FastEthernet0/16']['oper_status']
cmd = print(p1['FastEthernet0/16']['oper_status'])
value=up
Key and level found for: SWRACKF: ['FastEthernet0/41']['oper_status']
cmd = print(p1['FastEthernet0/41']['oper_status'])
value=up
Key and level found for: SWRACKF: ['FastEthernet0/44']['oper_status']
cmd = print(p1['FastEthernet0/44']['oper_status'])
value=up
Key and level found for: SWRACKF: ['GigabitEthernet0/1']['oper_status']
cmd = print(p1['GigabitEthernet0/1']['oper_status'])
value=up

```



#### Looking at various counters
- python3 tshoot.py   -c "show interfaces"  -k in_errors -V 0 -o ">" -d SWRACKD
- python3 tshoot.py -c "show interfaces" -k in_pkts -V 25011394 -o ">" -d SWRACKD
- python3 tshoot.py -c "show interfaces" -k in_pkts -V 1 -o ">" -d SWRACKA -d SWRACKB -d SWRACKC -d SWRACKD -d SWRACKE -d SWRACKF
- python3 tshoot.py -c "show interfaces" -k out_pkts -V "0" -o ">" -r  -d SWRACKB SWRACKA

### other commands 
Of course the learn option could be used, but just for fun you can try stuff!
- python3 tshoot.py  -c "dir flash:" -k size -d SWRACKD
- python3 tshoot.py  -c "show ip route" -k metric -d SWRACKD
- python3 tshoot.py  -c "show running-config" -d SWRACKD
- python3 tshoot.py  -c "show configuration" -d SWRACKD

