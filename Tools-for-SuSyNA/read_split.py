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

# remove all spaces and '\n'
    for i in range(8):
        temp[i] = temp[i].replace(' ','')
        temp[i] = temp[i].replace('-','_')
        temp[i] = temp[i].strip('\n')

# deep split the list
    temp = deep_split(temp)

    return temp, 0


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
    for i in range(8):
        if i != 4:
            list_split.append(list_ori[i].split(','))
        else:
            list_split.append(list_ori[i].split('),'))

        list_split[i] = list(filter(None, list_split[i]))

    # get rid of extra whitespaces
    for i in range(8):
        for j in range(len(list_split[i])):
            list_split[i][j] = list_split[i][j].strip()

    # remove extra ',' in transition list & add ')'
    for i in range(len(list_split[4])):
        list_split[4][i] = list_split[4][i].strip(',')

    return list_split


def trans_split(trans_list, mode=0):
    statetr = []
    eventtr = []
    temp = []

    for trans in trans_list:
        temp.append(trans.strip('(').split(','))

    if mode == 1:
        return temp

    for term in temp:
        try:
            statetr.index(term[0])
        except:
            statetr.append(term[0])

        try:
            statetr.index(term[1])
        except:
            statetr.append(term[1])

        try:
            eventtr.index(term[2])
        except:
            eventtr.append(term[2])

    return list([statetr, eventtr])



        
# For test purpose
# list, error = ReadStd('EOperation.cfg')