# This is to generate test vectors for the AES program in CS361.
# Run this with:  python AEStestvectors.py

import random

def hex_number( count, padded=False ):
    # This currently generates a number of length count hex digits. 
    # Pad on the left with 0's if padded is True:
    x = random.randint( 0, 16**count )
    hexdig = "%x" % x
    if padded:
        out = hexdig.zfill( count )  # pad with 0 if necessary
        return out
    else:
        return hexdig

def AESvectors( size, num, padded ):
    # generate num vectors (one per line) of size at most count
    # hex digits
    test = (5, 6)
    test2 = test + test
    print test2
#     for i in range( num ):
#         print( hex_number( size, padded ) )

# Set the last param to True to pad all lines size hex digits.
# The padding is only needed for lines that have leading 0's.
AESvectors( size=32, num=100, padded=False )