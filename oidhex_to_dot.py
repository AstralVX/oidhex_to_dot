# Supports both hex notation with and without spaces
def oid_hex_to_dot(oidhex_string_orig):
    # Remove any spaces
    oidhex_string = ''
    for c in oidhex_string_orig:
        if c != ' ':
            oidhex_string += c    
        
    ''' Input is a hex string and as one byte is 2 charecters i take an 
        empty list and insert 2 characters per element of the list.
        So for a string 'DEADBEEF' it would be ['DE','AD','BE,'EF']. '''
    hex_list = [] 
    for char in range(0,len(oidhex_string),2):
        hex_list.append(oidhex_string[char]+oidhex_string[char+1])

    ''' I have deleted the first two element of the list as my hex string
        includes the standard OID tag '06' and the OID length '0D'. 
        These values are not required for the calculation as i've used 
        absolute OID and not using any ASN.1 modules. Can be removed if you
        have only the data part of the OID in hex string. '''
    del hex_list[0]
    del hex_list[0]

    # An empty string to append the value of the OID in standard notation after
    # processing each element of the list.
    OID_str = ''

    # Convert the list with hex data in str format to int format for 
    # calculations.
    for element in range(len(hex_list)):
        hex_list[element] = int(hex_list[element],16)

    # Convert the OID to its standard notation. Sourced from code in other 
    # languages and adapted for python.

    # The first two digits of the OID are calculated differently from the rest. 
    x = int(hex_list[0] / 40)
    y = int(hex_list[0] % 40)
    if x > 2:
        y += (x-2)*40
        x = 2;

    OID_str += str(x)+'.'+str(y)

    val = 0
    for byte in range(1,len(hex_list)):
        val = ((val<<7) | ((hex_list[byte] & 0x7F)))
        if (hex_list[byte] & 0x80) != 0x80:
            OID_str += "."+str(val)
            val = 0

    # print the OID in dot notation.
    print (OID_str)

# --------------------------------------------------------------------------------

def encode_variable_length_quantity(v:int) -> list:
    # Break it up in groups of 7 bits starting from the lowest significant bit
    # For all the other groups of 7 bits than lowest one, set the MSB to 1
    m = 0x00
    output = []
    while v >= 0x80:
        output.insert(0, (v & 0x7f) | m)
        v = v >> 7
        m = 0x80
    output.insert(0, v | m)
    return output

def encode_oid_string(oid_str:str) -> tuple:
    a = [int(x) for x in oid_str.split('.')]
    oid = [a[0]*40 + a[1]] # First two items are coded by a1*40+a2
    # A rest is Variable-length_quantity
    for n in a[2:]:
        oid.extend(encode_variable_length_quantity(n))
    oid.insert(0, len(oid)) # Add a Length
    oid.insert(0, 0x06) # Add a Type (0x06 for Object Identifier)
    return oid

def oid_dot_to_hex(argv):
    oid = encode_oid_string(argv)
    str = " ".join("{:02x}".format(num) for num in oid)
    print(str)

# --------------------------------------------------------------------------------

import sys
if len(sys.argv) != 3:
    print("[-] Missing args: oidhex_to_dot.py \"0a 1b etc\" [input -h or -d]")
    sys.exit()

if (sys.argv[1] == "-h"):
    # "06 09 2A 86 48 86 F7 14 01 05 09"
    # "060a2b060104018237020104"
    oid_hex_to_dot(sys.argv[2])
elif (sys.argv[1] == "-d"):
    # "1.2.840.113556.1.5.9"
    oid_dot_to_hex(sys.argv[2])