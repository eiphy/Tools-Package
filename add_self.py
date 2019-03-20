import read_split
import stdize
import copy


def add_self(statec, eventc, filew, mode=0, filer='None'):

    statec = statec.replace(' ','')
    state_list = statec.split(',')
    eventc = eventc.replace(' ','')
    event_list = eventc.split(',')

    trans_list = []

    for i in range(len(state_list)):
        for j in range(len(event_list)):
            if mode == 0:
                temp = '(' + state_list[i] + ', ' + state_list[i] + ', ' + event_list[j] + ')'
            else:
                temp = '(' + state_list[i] + ',' + state_list[i] + ',' + event_list[j]
            trans_list.append(temp)

    trans = ', '.join(trans_list)

    if mode == 0:
        with open(filew, 'w') as fileobject:
            fileobject.write(trans)
    else:
        if filer == 'None':
            filer = input('Please enter the filename of automaton to be read:\t')
        
        auto_list, error = read_split.ReadStd(filer)
        if error != 0:
            print(error)
            return error

        auto_list[4].extend(trans_list)

        auto_list = copy.deepcopy(check_state(state_list, event_list, auto_list))

        stdize.std_write(filew, auto_list, 0)

    return 0 


def check_state(state_list, event_list, auto_list):
    stateo = ''.join(auto_list[0])
    evento = ''.join(auto_list[1])
    for i in range(len(state_list)):
        if stateo.find(state_list[i]) == -1:
            print("Warning: the selfloop state '" + state_list[i] + "' is not in the original state space.\n It is added to the original state space")
            auto_list[0].append(state_list[i])

    for i in range(len(event_list)):
        if evento.find(event_list[i]) == -1:
            print("Warning: the selfloop event '" + event_list[i] + "' is not in the original alphabet.\n It is added to the original alphabet")
            auto_list[1].append(event_list[i])

    return auto_list


add_self('du_1,de_2, de_3, df_4', 'a1,a2, a3','Test3.cfg',1,'EOperation.cfg')

        