def _string_derp(stringy):
    r_string = ""
    for i, letter in enumerate(stringy):
        if(letter == ' '):
            i = i-1
        elif (i % 2 != 0):
            letter += letter.upper()
        else:
            letter = letter.lower()

        r_string += letter

    return r_string

print(_string_derp("asdasd asdasd asdasd"))


