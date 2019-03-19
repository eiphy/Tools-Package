import keyhead
# This function is used to read the cfg file and convert the content to list for later process & check the basic syntax.
def ReadStd(filename):
    with open(filename) as fileobject:
        temp = fileobject.readlines()
    if temp[0] != '[automaton]\n':
        error = 'Structure of the file is wrong'
        return -1, error

    temp, error = componentsSplit(temp[1:])
    if error != 0:
        return -1, error

# remove all spaces
    for i in range(7):
        temp[i] = temp[i].replace(' ','')

    temp = deep_split(temp)

    return temp, 1


# This function is used to split the automaton components into different list
# according to its head.
def componentsSplit(list):
    # The dictionary for spliting the automaton components.
    switcher = keyhead.switch_define()
    ind = list[0].find('=')
    if ind == -1:
        error = 'The syntax of first line is wrong'
        return -1, error

    temp = ['0'] * 8
    i = 0
    
    for lines in list:
        ind = lines.find('=')
        if  ind == -1:
            if temp[i].strip(' ') == '\n':
                temp[i] = lines
            else:
                temp[i] = temp[i].rstrip()
                if temp[i][-1] != ',':
                    temp[i] = temp[i] + ','
                temp[i] = temp[i] + lines
        else:
            i = keyhead.HeadSwitch(switcher, lines[0:ind].strip())
            if i == -1:
                error = 'The head is wrong'
                return -1, error

            temp[i] = lines[ind+1:]

    return temp, 0

def deep_split(list_ori):
    list_split = []
    
    # deep split the list according to ','
    for i in range(7):
        if i != 4:
            list_split.append(list_ori[i].split(','))
        else:
            list_split.append(list_ori[i].split(')'))

    # get rid of extra spaces
    for i in list_split:
        for j in i:
            j = j.strip()

    return list_split
        

list, error = ReadStd('EOperation.cfg')