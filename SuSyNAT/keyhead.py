# This function is used to define the switcher dictionary
def switch_define():
    switcher = {'states': statesSwi, 'alphabet': alphabetSwi,
                'controllable': controllableSwi,
                'observable': observableSwi,
                'transitions': transitionsSwi,
                'marker-states': markerSwi,
                'initial-state': initialSwi,
                'kind': kindSwi}
    return switcher

# This function is used to determine which component current line belongs to
def HeadSwitch(switcher, head):
    func = switcher.get(head, lambda switcher: -1)
    return func(switcher)

# Below is the list for switch functions.
def statesSwi(switcher):
    del switcher['states']
    return 0

def alphabetSwi(switcher):
    del switcher['alphabet']
    return 1

def controllableSwi(switcher):
    del switcher['controllable']
    return 2

def observableSwi(switcher):
    del switcher['observable']
    return 3

def transitionsSwi(switcher):
    del switcher['transitions']
    return 4

def markerSwi(switcher):
    del switcher['marker-states']
    return 5

def initialSwi(switcher):
    del switcher['initial-state']
    return 6

def kindSwi(switcher):
    del switcher['kind']
    return 7