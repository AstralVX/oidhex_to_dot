Python3 script that can convert between OID (hex) and DOT notation.

#### Usage:
```
python oidhex_to_dot.py -h "060a2b060104018237020104"
1.3.6.1.4.1.311.2.1.4

python oidhex_to_dot.py -h "06 09 2A 86 48 86 F7 14 01 05 09"
1.2.840.113556.1.5.9

python oidhex_to_dot.py -d "1.2.840.113556.1.5.9"
06 09 2a 86 48 86 f7 14 01 05 09
```