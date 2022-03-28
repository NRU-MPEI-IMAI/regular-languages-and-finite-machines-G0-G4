import os
import sys
from automat import Automat
from input import transitions, initial_state, final_states

if __name__ == '__main__':
    a = Automat(
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])
    a.save_dot('1.dot')
    a.remove_lambda_connections()
    a.save_dot('2.dot')
    a.to_dfa()
    a.save_dot('3.dot')
    os.system('dot -Tpng 1.dot -o 1.png')
    os.system('dot -Tpng 2.dot -o 2.png')
    os.system('dot -Tpng 3.dot -o 3.png')
