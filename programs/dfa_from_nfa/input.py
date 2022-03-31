'''
use this file as an input form
'''
alphabet={'a', 'b'}
states={'1', '2'}
transitions={
    '1': {'a':{'1'}, '':{'2'}},
    '2': {'':{'1'}}
}
initial_state='1'
final_states={'2'}
