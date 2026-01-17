



def beautifulBinaryString(b):
    # Write your code here
    blen = len(b)
    moves = 0
 
    
    i = 0
    while i < blen:
        if b[i:i+3] == "010":
            moves += 1
            i += 3
        else:
            i += 1
    return moves



b='0100101010'
print (beautifulBinaryString(b))

