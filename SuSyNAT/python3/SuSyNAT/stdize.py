import read_split
import copy


# This function reads the file, standardlize it and write it out.
def stdize(filer, filew):
    auto_list, error = read_split.ReadStd(filer)

    error = std_write(filew, auto_list, error)
    return error


def std_write(filew, std_list, error=0):
    if error != 0:
        print(error)
        return -1

    std_list[4] = copy.deepcopy(std_transitions(std_list[4]))
    std_list = std_join(std_list)

    with open(filew, 'w') as fileobject:
        fileobject.write('[automaton]\n')
        if std_list[-1] == '0\n':
            for i in range(7):
                fileobject.write(std_list[i])
        else:
            for i in range(8):
                fileobject.write(std_list[i])

    return 0


def std_transitions(trlist):
    trlist_deep = []
    for i in range(len(trlist)):
        trlist[i] = trlist[i].strip('(')
        temp = trlist[i].split(',')
        temp = ', '.join(temp)
        temp = '(' + temp + ')'
        trlist_deep.append(temp)

    return trlist_deep


def std_join(temp_list):
    head = ['states = ', 'alphabet = ', 'controllable = ', 'observable = ', 'transitions = ', 
        'marker-states = ', 'initial-state = ', 'kind = ']

    out_list = []

    for i in range(8):
        out_list.append(', '.join(temp_list[i]))
        out_list[i] = head[i] + out_list[i] + '\n'

    return out_list


# stdize('Test.cfg', 'Test2.cfg')
