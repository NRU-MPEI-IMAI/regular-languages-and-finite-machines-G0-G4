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
            final_states={'2'},
            deterministic=False
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
            final_states={'6'},
            deterministic=False
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
            final_states={'4'},
            deterministic=False
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
            alphabet={'a', 'b'},
            states={'1', '2', '3', '4', '5'},
            transitions={
                '1': {'a': {'2', '3', '4'}, 'b': '3'},
                '4': {'a': {'3', '5'}, 'b': '2'}
            },
            initial_state='1',
            final_states={'5'},
            deterministic=False
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
            states={'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'},
            alphabet={'a', 'b'},
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
            final_states={'10'},
            deterministic=False
        )

        b = Automat(
            states={'0', '1', '2'},
            alphabet={'a', 'b'},
            transitions={
                '0': {'a': {'0', '1'}, 'b': {'1'}},
                '1': {'a': {'2'}, 'b': {'2'}},
                '2': {'b': {'0'}},
            },
            initial_state='0',
            final_states={'0'},
            deterministic=False
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
    
    def test_cartesian(self):
        states1 = {'A', 'B'}
        transitions1 = {
            'A': {'a': {'B'}}
        }
        states2 = {'C', 'D'}
        transitions2 = {
            'C': {'b': 'D'}
        }
        transitions3 = {
            'C': {'a': {'D'}, 'b':'C'},
            'D': {'a': 'D', 'b':{'C'}}
        }

        transitions1_2 = {
            'AC': {'a': '@', 'b': '@'},
            'AD': {'a': '@', 'b': '@'},
            'BC': {'a': '@', 'b': '@'},
            'BD': {'a': '@', 'b': '@'}
        }

        transitions1_3 = {
            'AC': {'a': 'BD', 'b': '@'},
            'AD': {'a': 'BD', 'b': '@'},
            'BC': {'a': '@', 'b': '@'},
            'BD': {'a': '@', 'b': '@'}
        }

        res1_2 = Automat._Automat__cartesian(
            transitions1,
            transitions2,
            states1,
            states2,
            {'a', 'b'}
            )
        res1_3 = Automat._Automat__cartesian(
            transitions1,
            transitions3,
            states1,
            states2,
            {'a', 'b'}
            )

        self.assertEqual(transitions1_2, res1_2)
        self.assertEqual(transitions1_3, res1_3)

    def test_and(self):
        a = Automat(
            alphabet = {'a', 'b'},
            states = {'A', 'B', 'C'},
            transitions = {
                'A': {'a': 'B', 'b': 'A'},
                'B': {'a': 'C', 'b': {'B'}},
                'C': {'a': {'C'}, 'b': 'C'}
            },
            initial_state = 'A',
            final_states = {'C'},
            deterministic = True
        )
        b = Automat(
            alphabet = {'a', 'b'},
            states = {'D', 'E', 'F'},
            transitions = {
                'D': {'a': {'D'}, 'b': 'E'},
                'E': {'a': 'E', 'b': 'F'},
                'F': {'a': 'F', 'b': {'F'}}
            },
            initial_state = 'D',
            final_states = {'F'},
            deterministic = True
        )
        c = Automat(
            alphabet = {'a'},
            states = {'q1'},
            transitions = {
                'q1': {'a': 'q1'},
            },
            initial_state = 'q1',
            final_states = {'q1'},
            deterministic = True
        )
        d = Automat(
            alphabet = {'b'},
            states = {'g1'},
            transitions = {
                'g1': {'b': 'g1'},
            },
            initial_state = 'g1',
            final_states = {'g1'},
            deterministic = True
        )
        ab = a & b
        cd = c & d
        a_and_b = Automat(
            alphabet = {'a', 'b'},
            states = {'AD', 'AE', 'AF', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF'},
            transitions = {
                'AE': {'a': {'BE'}, 'b': {'AF'}},
                'AF': {'a': {'BF'}, 'b': {'AF'}},
                'AD': {'a': {'BD'}, 'b': {'AE'}},
                'CE': {'a': {'CE'}, 'b': {'CF'}},
                'CF': {'a': {'CF'}, 'b': {'CF'}},
                'CD': {'a': {'CD'}, 'b': {'CE'}},
                'BE': {'a': {'CE'}, 'b': {'BF'}},
                'BF': {'a': {'CF'}, 'b': {'BF'}},
                'BD': {'a': {'CD'}, 'b': {'BE'}}
            },
            initial_state = 'AD',
            final_states = {'CF'},
            deterministic = True
        )
        c_and_d = Automat(
            alphabet = {'a', 'b'},
            states = {'q1g1'},
            transitions = {
                'q1g1': {'a': {'@'}, 'b': {'@'}},
            },
            initial_state = 'q1g1',
            final_states = {'q1g1'},
            deterministic = True
        )

        self.assertEqual(a_and_b.alphabet, ab.alphabet)
        self.assertEqual(a_and_b.states, ab.states)
        self.assertDictEqual(a_and_b.transitions, ab.transitions)
        self.assertEqual(a_and_b.initial_state, ab.initial_state)
        self.assertEqual(a_and_b.final_states, ab.final_states)
        self.assertEqual(a_and_b.deterministic, ab.deterministic)

        self.assertEqual(c_and_d.alphabet, cd.alphabet)
        self.assertEqual(c_and_d.states, cd.states)
        self.assertDictEqual(c_and_d.transitions, cd.transitions)
        self.assertEqual(c_and_d.initial_state, cd.initial_state)
        self.assertEqual(c_and_d.final_states, cd.final_states)
        self.assertEqual(c_and_d.deterministic, cd.deterministic)

    def test_or(self):
        a = Automat(
            alphabet = {'a', 'b'},
            states = {'A', 'B', 'C'},
            transitions = {
                'A': {'a': 'B', 'b': 'A'},
                'B': {'a': 'C', 'b': {'B'}},
                'C': {'a': {'C'}, 'b': 'C'}
            },
            initial_state = 'A',
            final_states = {'C'},
            deterministic = True
        )
        b = Automat(
            alphabet = {'a', 'b'},
            states = {'D', 'E', 'F'},
            transitions = {
                'D': {'a': {'D'}, 'b': 'E'},
                'E': {'a': 'E', 'b': 'F'},
                'F': {'a': 'F', 'b': {'F'}}
            },
            initial_state = 'D',
            final_states = {'F'},
            deterministic = True
        )
        c = Automat(
            alphabet = {'a'},
            states = {'q1'},
            transitions = {
                'q1': {'a': 'q1'},
            },
            initial_state = 'q1',
            final_states = {'q1'},
            deterministic = True
        )
        d = Automat(
            alphabet = {'b'},
            states = {'g1'},
            transitions = {
                'g1': {'b': 'g1'},
            },
            initial_state = 'g1',
            final_states = {'g1'},
            deterministic = True
        )
        ab = a | b
        cd = c | d
        a_and_b = Automat(
            alphabet = {'a', 'b'},
            states = {'AD', 'AE', 'AF', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF'},
            transitions = {
                'AE': {'a': {'BE'}, 'b': {'AF'}},
                'AF': {'a': {'BF'}, 'b': {'AF'}},
                'AD': {'a': {'BD'}, 'b': {'AE'}},
                'CE': {'a': {'CE'}, 'b': {'CF'}},
                'CF': {'a': {'CF'}, 'b': {'CF'}},
                'CD': {'a': {'CD'}, 'b': {'CE'}},
                'BE': {'a': {'CE'}, 'b': {'BF'}},
                'BF': {'a': {'CF'}, 'b': {'BF'}},
                'BD': {'a': {'CD'}, 'b': {'BE'}}
            },
            initial_state = 'AD',
            final_states = {'CD', 'CE', 'CF', 'AF', 'BF'},
            deterministic = True
        )
        c_and_d = Automat(
            alphabet = {'a', 'b'},
            states = {'q1g1'},
            transitions = {
                'q1g1': {'a': {'@'}, 'b': {'@'}},
            },
            initial_state = 'q1g1',
            final_states = {'q1g1'},
            deterministic = True
        )

        self.assertEqual(a_and_b.alphabet, ab.alphabet)
        self.assertEqual(a_and_b.states, ab.states)
        self.assertDictEqual(a_and_b.transitions, ab.transitions)
        self.assertEqual(a_and_b.initial_state, ab.initial_state)
        self.assertEqual(a_and_b.final_states, ab.final_states)
        self.assertEqual(a_and_b.deterministic, ab.deterministic)

        self.assertEqual(c_and_d.alphabet, cd.alphabet)
        self.assertEqual(c_and_d.states, cd.states)
        self.assertDictEqual(c_and_d.transitions, cd.transitions)
        self.assertEqual(c_and_d.initial_state, cd.initial_state)
        self.assertEqual(c_and_d.final_states, cd.final_states)
        self.assertEqual(c_and_d.deterministic, cd.deterministic)

    def test_full_transitions(self):

        alphabet = {'a', 'b'}
        transitions = {
            '1': {'a': '1'},
            '2': {'b': '2'}
        }
        full = Automat._Automat__full_transitions({'1', '2'}, {'a', 'b'},
            transitions)
        full_right = {
            '1': {'a':'1', 'b':'@'},
            '2': {'a':'@', 'b':'2'},
            '@' : {'a':'@', 'b':'@'}
        }
        self.assertDictEqual(full, full_right)
        
    
    def test_invert(self):
        a = Automat(
            alphabet = {'a', 'b'},
            states = {'A', 'B', 'C'},
            transitions = {
                'A': {'a': 'B', 'b': 'A'},
                'B': {'a': 'C', 'b': {'B'}},
                'C': {'a': {'C'}, 'b': 'C'}
            },
            initial_state = 'A',
            final_states = {'C'},
            deterministic = True
        )
        c = Automat(
            alphabet = {'a'},
            states = {'q1'},
            transitions = {
                'q1': {'a': 'q1'},
            },
            initial_state = 'q1',
            final_states = {'q1'},
            deterministic = True
        )
        na = ~a
        nc = ~c   
        print(na.transitions)
        self.assertEqual(na.alphabet, a.alphabet)
        self.assertEqual(na.states, a.states | {'@'})
        self.assertDictEqual(na.transitions, {
                'A': {'a': {'B'}, 'b': {'A'}},
                'B': {'a': {'C'}, 'b': {'B'}},
                'C': {'a': {'C'}, 'b': {'C'}},
                '@': {'a':{'@'}, 'b':{'@'}}})
        self.assertEqual(na.initial_state, a.initial_state)
        self.assertEqual(na.final_states, {'A', 'B', '@'})
        self.assertEqual(na.deterministic, a.deterministic)

        self.assertEqual(nc.alphabet, c.alphabet)
        self.assertEqual(nc.states, c.states | {'@'})
        self.assertDictEqual(nc.transitions, {
                'q1': {'a': {'q1'}},
                '@': {'a':{'@'}}
            })
        self.assertEqual(nc.initial_state, c.initial_state)
        self.assertEqual(nc.final_states, {'@'})
        self.assertEqual(nc.deterministic, c.deterministic)






if __name__ == '__main__':
    unittest.main()
