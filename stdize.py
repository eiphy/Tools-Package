import read_split
import copy


# This function reads the file, standardlize it and write it out.
def stdize():
    filer = input('Please enter the input filename:\t')
    filew = input('Please enter the output filename:\t')

    auto_list, error = read_split.ReadStd(filer)

    if error != 0:
        print(error)
        return -1

    auto_list[4] = copy.deepcopy(std_transitions(auto_list[4]))
    auto_list = std_join(auto_list)

    with open(filew, 'w') as fileobject:
        fileobject.write('[automaton]\n')
        if auto_list[-1] == '0\n':
            for i in range(7):
                fileobject.write(auto_list[i])
        else:
            for i in range(8):
                fileobject.write(auto_list[i])


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
    head = ['states = ', 'alphabet = ', 'controllable = ', 'observalble = ', 'transitions = ', 
        'marker-states = ', 'initial-state = ', 'kind = ']

    out_list = []

    for i in range(8):
        out_list.append(', '.join(temp_list[i]))
        out_list[i] = head[i] + out_list[i] + '\n'

    return out_list


stdize()
