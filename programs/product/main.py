import os
import sys
sys.path.append("../automat")
from automat import Automat
from input import (
    alphabet1, states1, transitions1, initial_state1, final_states1,
    alphabet2, states2, transitions2, initial_state2, final_states2)

if __name__ == '__main__':
    a = Automat(
        alphabet=alphabet1,
        states=states1,
        transitions=transitions1,
        initial_state=initial_state1,
        final_states=final_states1,
    )

    b = Automat(
        alphabet=alphabet2,
        states=states2,
        transitions=transitions2,
        initial_state=initial_state2,
        final_states=final_states2,
    )

    if len(sys.argv) > 1:
        os.chdir(sys.argv[1])

    names = [
        'a_and_b',
        'a_or_b',
        'not_a',
        'not_b',
        'a_minus_b',
        'b_minus_a'
    ]
    ops = [
        lambda a, b: a & b,
        lambda a, b: a | b,
        lambda a, b: ~a,
        lambda a, b: ~b,
        lambda a, b: a - b,
        lambda a, b: b - a,
    ]
    for op, name in zip(ops, names):
        automat = op(a, b)
        automat.save_dot(name + '.dot')
        os.system(f'dot -Tpng {name}.dot -o {name}.png')

    with open('result.md', 'w')as f:
        for name in names:
            f.write(f'### {name} \n![]({name}.png)\n')
