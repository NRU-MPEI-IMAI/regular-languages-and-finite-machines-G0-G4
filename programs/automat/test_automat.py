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
            transitions={
                '1': {'': {'2'}},
                '2': {'': {'1'}}
            },
            initial_state='1',
            final_states={'2'}
        )

        b = Automat(
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

    def test_dfa_connection(self):
        '''
        a:
        +--------+--+
        b  a     |  a
        v  v     |  v
        2  3     4  5
        ^  ^     ^  ^
        a  a     a  a
        +--+--1--+--+
        '''

        a = Automat(
            transitions={
                '1': {'a': {'2', '3', '4'}, 'b': '3'},
                '4': {'a': {'3', '5'}, 'b': '2'}
            },
            initial_state='1',
            final_states={'5'}
        )

        right_a14 = {frozenset({'4', '1'}): {
            'a': {'3', '4', '2', '5'},
            'b': {'2', '3'}}}

        right_a235 = {frozenset({'2', '3', '5'}): {}}
        self.assertDictEqual(right_a14, a._Automat__dfa_connection({'1', '4'}))
        self.assertDictEqual(
            right_a235, a._Automat__dfa_connection({'2', '3', '5'}))

    def test_to_dfa(self):
        '''
        a:

        +->5--a->6--b->7--a->8-l+
        l                       v
        1<----------l---------->9-a>10!
        l                       ^
        +->2--a->3--b->4 ------l+

        b:

        +-a,b->1-a,b-+
        |            |
        |            v
        0!<----b-----2
        ^
        a
        '''

        a = Automat(
            transitions={
                '1': {'': {'2', '5', '9'}},
                '2': {'a': {'3'}},
                '3': {'b': {'4'}},
                '4': {'': {'9'}},
                '5': {'a': {'6'}},
                '6': {'b': {'7'}},
                '7': {'a': {'8'}},
                '8': {'': {'9'}},
                '9': {'': {'1'}, 'a': {'10'}},
                '10': {}
            },
            initial_state='1',
            final_states={'10'}
        )

        b = Automat(
            transitions={
                '0': {'a': {'0', '1'}, 'b': {'1'}},
                '1': {'a': {'2'}, 'b': {'2'}},
                '2': {'b': {'0'}},
            },
            initial_state='0',
            final_states={'0'}
        )
        right_a_transitions = {
            '"1"': {'a': {'"10,3,6"'}},
            '"10,3,6"': {'b': {'"4,7"'}},
            '"4,7"': {'a': {'"10,3,6,8"'}},
            '"10,3,6,8"': {'b': {'"4,7"'}, 'a': {'"10,3,6"'}}
        }
        right_a_final_states = {'"10,3,6"', '"10,3,6,8"'}

        right_b_transitions = {
            '"0"': {'a': {'"0,1"'}, 'b': {'"1"'}},
            '"0,1"': {'a': {'"0,1,2"'}, 'b': {'"1,2"'}},
            '"1"': {'a': {'"2"'}, 'b': {'"2"'}},
            '"0,1,2"': {'a': {'"0,1,2"'}, 'b': {'"0,1,2"'}},
            '"1,2"': {'b': {'"0,2"'}, 'a': {'"2"'}},
            '"2"': {'b': {'"0"'}},
            '"0,2"': {'a': {'"0,1"'},
                    'b': {'"0,1"'}}
        }
        right_b_final_states = {'"0"', '"0,2"', '"0,1,2"', '"0,1"'}

        a_transitions, a_final_states = a.to_dfa()
        b_transitions, b_final_states = b.to_dfa()

        self.assertDictEqual(right_a_transitions, a_transitions)
        self.assertEqual(right_a_final_states, a_final_states)
        self.assertDictEqual(right_b_transitions, b_transitions)
        self.assertEqual(right_b_final_states, b_final_states)


if __name__ == '__main__':
    unittest.main()
