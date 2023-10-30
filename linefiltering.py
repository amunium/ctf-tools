import sys

otallowed = [
    "abcnyheter",
    "vg",
    "nrk",
    "dn",
    "dagbladet",
    "tv2",
    "e24",
    "nettavisen",
    "aftenposten",
    "bt",
    "worldwidebank"
    ]

notallowed = ["192.168.161.1"]

def main(filepath):
    with open(filepath) as f: # change name of file here.
        output=""
        lines = f.readlines()
        b = []
        for line in lines:        
            allowed = False
            for word in notallowed:
                if line.__contains__(word):
                    allowed=True
                    break
            if allowed:
                b.append(line)
        b = list(set(b)) # remove duplicates
        for line in b:
            print(line, end="")



if __name__ == "__main__":
    # Makes sure that 
    if sys.argv[1]:
        filepath = sys.argv[1]
        main(filepath)
    else:
        print("No filepath provided.")