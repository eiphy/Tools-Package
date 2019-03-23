import read_split
import stdize
import copy

def secolle(filename, filew='None', mode=0):
    auto_list = read_split.ReadStd(filename)[0]
    state_list, event_list = read_split.trans_split(auto_list[4])

    if mode == 0:
        if filew == 'None':
            filew = input('Please enter the file save the state & alphabet:\t')

        state = 'states = ' + ', '.join(state_list) + '\n'
        event = 'alphabet = ' + ', '.join(event_list) + '\n'

        with open(filew, 'w') as fileobject:
            fileobject.write(state)
            fileobject.write(event)

    else:
        auto_list[0] = copy.deepcopy(state_list)
        auto_list[1] = copy.deepcopy(event_list)
        auto_list[2] = copy.deepcopy(event_list)
        auto_list[3] = copy.deepcopy(event_list)

        stdize.std_write(filew, auto_list)

# secolle('EOperation.cfg', 'Test.cfg')