'''
use this file as an input form
'''

# input first automat:
alphabet1={'a', 'b'}
states1={'A', 'B'}
transitions1={
    'A': {'a':{'B'}, 'b':{'A'}},
    'B': {'a':{'A'}, 'b':{'B'}}
}
initial_state1='A'
final_states1={'A'}

# input second automat:
alphabet2={'a', 'b'}
states2={'C', 'D'}
transitions2={
    'C': {'a':{'C'}, 'b':{'D'}},
    'D': {'a':{'D'}, 'b':{'C'}}
}
initial_state2='C'
final_states2={'C'}
