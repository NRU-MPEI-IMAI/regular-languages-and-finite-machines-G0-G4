import unittest
from automat import Automat


def to_dict(dfd):
    d = {}
    for key1 in dfd:
        d[key1] = dict(dfd[key1])
    return d


class TestAutomat(unittest.TestCase):

    def test_remove_lamda_connections(self):
        '''
        lambda = l
        a:
        1<-l->2!

        b:
             a
             v
        l--->2--b-->4--l
        |              |
        |              v
        1<------l------6!
        |              ^
        |              |
        l--->3--a-->5--l
             ^
             b

        c:
        a
        v
        1--b,l->2-b,l->3
        ^       |
        |       |
        l--4!<--a

        '''
        a = Automat(
            alphabet={'a', 'b'},
            states={'1', '2'},
            transitions={
                '1': {'': {'2'}},
                '2': {'': {'1'}}
            },
            initial_state='1',
            final_states={'2'}
        )

        b = Automat(
            alphabet={'a', 'b'},
            states={'1', '2', '3', '4', '5', '6'},
            transitions={
                '1': {'': {'2', '3'}},
                '2': {'a': {'2'}, 'b': {'4'}},
                '3': {'a': {'5'}, 'b': {'3'}},
                '4': {'': {'6'}},
                '5': {'': {'6'}},
                '6': {'': {'1'}}
            },
            initial_state='1',
            final_states={'6'}
        )

        c = Automat(
            alphabet={'a', 'b'},
            states={'1', '2', '3', '4'},
            transitions={
                '1': {'': {'2'}, 'a': {'1'}, 'b': {'2'}},
                '2': {'': {'3'}, 'a': {'4'}, 'b': {'3'}},
                '4': {'': {'1'}}
            },
            initial_state='1',
            final_states={'4'}
        )

        a_transitions, a_finals = a.remove_lambda_connections()
        b_transitions, b_finals = b.remove_lambda_connections()
        c_transitions, c_finals = c.remove_lambda_connections()

        right_b_transitions = {
            '1': {'a': {'2', '5'}, 'b': {'3', '4'}},
            '4': {'a': {'2', '5'}, 'b': {'3', '4'}},
            '5': {'a': {'2', '5'}, 'b': {'3', '4'}},
            '6': {'a': {'2', '5'}, 'b': {'3', '4'}},
            '2': {'a': {'2'}, 'b': {'4'}},
            '3': {'b': {'3'}, 'a': {'5'}},
        }

        right_c_transitions = {
            '1': {'a': {'1', '4'}, 'b': {'2', '3'}},
            '2': {'a': {'4'}, 'b': {'3'}},
            '4': {'a': {'1', '4'}, 'b': {'2', '3'}}
        }

        self.assertEqual(({'1': {}, '2': {}}, {'1', '2'}),
                         (to_dict(a_transitions), a_finals))
        self.assertEqual(
            (right_b_transitions, {'1', '2', '3', '6'}),
            (to_dict(b_transitions), b_finals))
        self.assertEqual(
            (right_c_transitions, {'1', '2', '3', '4'}),
            (to_dict(c_transitions), c_finals))


if __name__ == '__main__':
    unittest.main()
