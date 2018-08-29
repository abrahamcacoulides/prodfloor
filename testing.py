
def LetterToAscii(letter):
     letter_in_ascii_bin = str(bin(ord(letter))[2:])
     return(letter_in_ascii_bin)

print (LetterToAscii("C"))