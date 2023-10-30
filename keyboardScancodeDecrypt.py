import sys

# ISO105 - keyboard layout 00000414
ISO105 = {
    "02":"1!", "03":"2\"@",
    "04":"3#£", "05":"4¤$", "06":"5%", "07":"6&", "08":"7/{", "09":"8([",
    "0a":"9)]", "0b":"0=}", "0c":"+?", "0d":"\\`'",
    "10":"qQ", "11":"wW", "12":"eE", "13":"rR", "14":"tT", "15":"yY",
    "16":"uU", "17":"iI", "18":"oO", "19":"pP", "1a":"åÅ", "1b":"\"^",
    "1e":"aA", "1f":"sS", "20":"dD", "21":"fF",
    "22":"gG", "23":"hH", "24":"jJ", "25":"kK", "26":"lL", "27":"øØ",
    "28":"æÆ", "29":"|§", "2b":"'*",
    "2c":"zZ", "2d":"xX", "2e":"cC", "2f":"vV", "30":"bB", "31":"nN", 
    "32":"mMµ", "33":",;", "34":".:", "35":"-_", "37":"**",
    "3a":"CC"
}

def main(filepath):
    f = open(filepath,"r")
    lines = f.readlines()

    buffer = "xx"
    output = []
    capslock = False
    shift = False
    altgr = False
    ctrl = False

    print("Start")
    for line in lines:
        # split into lines and pop last to get only the needed bytes 
        bytes = [(line[i:i+2]) for i in range(0, len(line), 2)]
        
        #remove newline
        bytes.pop()
        # print("DEBUG: ", bytes)

        # buffer for getting the change in keystrokes


        # check if new character
        for b in bytes:
            if True:# b != buffer or b == "0e":
                buffer = b

                try:
                    if b == "0e":
                        # Backspace 
                        # output.pop()
                        output.append(" BACK ")
                    elif b == "39":
                        # Space
                        output.append(" ")
                    elif b == "1c":
                        # Enter
                        output.append("\n")
                    elif b == "1d":
                        # Caps lock
                        output.append(" CAPSLOCK ")
                        if capslock:
                            capslock = False
                        else:
                            capslock = True
                    elif b == "2a" or b == "36":
                        output.append(" SHIFT ")
                        shift = True
                    elif b == "38":
                        output.append(" ALTGR ")
                        altgr = True
                    elif b == "1d":
                        output.append(" CTRL ")
                        ctrl = True
                    elif b == "0f":
                        output.append(" TAB ")
                    else:
                        if altgr:
                            altgr = False
                            try:
                                output.append(ISO105[b][2])
                            except:
                                output.append(ISO105[b][0]) 
                        elif capslock:
                            if shift: 
                                # Shift
                                output.append(ISO105[b][0]) 
                                shift = False
                            else:
                                output.append(ISO105[b][1])
                        elif shift: 
                            # Shift
                            output.append(ISO105[b][1]) 
                            shift = False
                        else:
                            output.append(ISO105[b][0])
                except:
                    # Det er ikke riktig norsk mapping så her er en trashy løsning.
                    print("Byte failed: ", b)
 
    # Print teksten:
    for w in output:
        print(w, end="")

    print("\n\nFerdig")

if __name__ == "__main__":
    # Makes sure that 
    if sys.argv[1]:
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("No filepath provided.")