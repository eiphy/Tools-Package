import read_split
import stdize

def del_event(eventc, filename):
    auto_list = read_split.ReadStd(filename)[0]
    eventc = eventc.replace(' ','')
    event_list = eventc.split(',')

    for event in event_list:
        for j in range(1,4):
            try:
                auto_list[j].remove(event)
            except:
                pass

        i = 0
        while i < len(auto_list[4]):
            eventtr = auto_list[4][i].split(',')[-1]
            eventtr = eventtr.strip()
            if eventtr == event:
                del auto_list[4][i]
            else:
                i += 1

    state = read_split.trans_split(auto_list[4])[0]
    
    if len(state) != len(auto_list[0]):
        i = 0
        while i < len(auto_list[0]):
            try:
                state.index(auto_list[0][i])
            except:
                auto_list[0].remove(auto_list[0][i])
                i = i - 1
            
            i += 1

    stdize.std_write(filename, auto_list)

# del_event('a1,a2, a3', 'Test3.cfg')