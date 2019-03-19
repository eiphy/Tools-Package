import read_split
# This function reads the file, standardlize it and write it out.
def stdize():
    filer = input('Please enter the input filename')
    filew = input('Please enter the output filename')

    temp = read_split.ReadStd(filer)


# This function is used to split each components.
def stdsplit(temp):
    i = 0
    while i < 8:
        temp[i] = temp[i].strip()
