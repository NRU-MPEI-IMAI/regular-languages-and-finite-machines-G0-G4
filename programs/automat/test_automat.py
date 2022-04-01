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
        )
        right_a_transitions = {
            '"1"': {'a': {'"10,3,6"'}, 'b': {'_'}},
            '"10,3,6"': {'b': {'"4,7"'}, 'a': {'_'}},
            '"4,7"': {'a': {'"10,3,6,8"'}, 'b': {'_'}},
            '"10,3,6,8"': {'b': {'"4,7"'}, 'a': {'"10,3,6"'}},
            '_': {'a': {'_'}, 'b': {'_'}}
        }
        right_a_final_states = {'"10,3,6"', '"10,3,6,8"'}

        right_b_transitions = {
            '"0"': {'a': {'"0,1"'}, 'b': {'"1"'}},
            '"0,1"': {'a': {'"0,1,2"'}, 'b': {'"1,2"'}},
            '"1"': {'a': {'"2"'}, 'b': {'"2"'}},
            '"0,1,2"': {'a': {'"0,1,2"'}, 'b': {'"0,1,2"'}},
            '"1,2"': {'b': {'"0,2"'}, 'a': {'"2"'}},
            '"2"': {'b': {'"0"'}, 'a': {'_'}},
            '"0,2"': {'a': {'"0,1"'}, 'b': {'"0,1"'}},
            '_': {'a': {'_'}, 'b': {'_'}}
        }
        right_b_final_states = {'"0"', '"0,2"', '"0,1,2"', '"0,1"'}

        a_transitions, a_final_states = a.to_dfa()
        b_transitions, b_final_states = b.to_dfa()

        self.assertDictEqual(right_a_transitions, a_transitions)
        self.assertEqual(right_a_final_states, a_final_states)
        self.assertDictEqual(right_b_transitions, b_transitions)
        self.assertEqual(right_b_final_states, b_final_states)

    def test_cartesian(self):
        states1 = {'A', 'B', '_'}
        transitions1 = {
            'A': {'a': {'B'}, 'b': '_'},
            'B': {'a': '_', 'b': '_'},
            '_': {'a': '_', 'b': '_'},

        }
        states2 = {'C', 'D', '!'}
        transitions2 = {
            'C': {'b': 'D', 'a': '!'},
            'D': {'b': '!', 'a': '!'},
            '!': {'b': '!', 'a': '!'},
        }
        transitions3 = {
            'C': {'a': {'D'}, 'b': 'C'},
            'D': {'a': 'D', 'b': {'C'}}
        }
        transitions4 = {
            'E': {'a': 'E', 'b': 'E'},
        }

        transitions1_2 = {
            'B!': {'a': '_!', 'b': '_!'},
            'BC': {'a': '_!', 'b': '_D'},
            'BD': {'a': '_!', 'b': '_!'},
            '_!': {'a': '_!', 'b': '_!'},
            '_C': {'a': '_!', 'b': '_D'},
            '_D': {'a': '_!', 'b': '_!'},
            'A!': {'a': 'B!', 'b': '_!'},
            'AC': {'a': 'B!', 'b': '_D'},
            'AD': {'a': 'B!', 'b': '_!'}}

        transitions3_4 = {
            'CE': {'a': 'DE', 'b': 'CE'},
            'DE': {'a': 'DE', 'b': 'CE'},
        }

        res1_2 = Automat._Automat__cartesian(
            transitions1,
            transitions2,
            states1,
            states2,
            {'a', 'b'}
        )
        res3_4 = Automat._Automat__cartesian(
            transitions3,
            transitions4,
            {'C', 'D'},
            {'E'},
            {'a', 'b'}
        )
        self.assertEqual(transitions1_2, res1_2)
        # self.assertEqual(transitions1_3, res1_3)

    def test_and(self):
        a = Automat(
            alphabet={'a', 'b'},
            states={'A', 'B', 'C'},
            transitions={
                'A': {'a': {'B'}, 'b': {'A'}},
                'B': {'a': {'C'}, 'b': {'B'}},
                'C': {'a': {'C'}, 'b': {'C'}}
            },
            initial_state='A',
            final_states={'C'},
        )
        b = Automat(
            alphabet={'a', 'b'},
            states={'D', 'E', 'F'},
            transitions={
                'D': {'a': {'D'}, 'b': {'E'}},
                'E': {'a': {'E'}, 'b': {'F'}},
                'F': {'a': {'F'}, 'b': {'F'}}
            },
            initial_state='D',
            final_states={'F'},
        )
        c = Automat(
            alphabet={'a'},
            states={'q1'},
            transitions={
                'q1': {'a': {'q1'}},
            },
            initial_state='q1',
            final_states={'q1'},
        )
        d = Automat(
            alphabet={'b'},
            states={'g1'},
            transitions={
                'g1': {'b': {'g1'}},
            },
            initial_state='g1',
            final_states={'g1'},
        )
        e = Automat(
            alphabet={'a', 'b'},
            states={'A', 'B', 'C', 'D'},
            transitions={
                'A': {'a': {'B'}, 'b': {'B'}},
                'B': {'a': {'C'}, 'b': {'C'}},
                'C': {'a': {'D'}, 'b': {'D'}},
                'D': {'a': {'D'}, 'b': {'D'}},
            },
            initial_state='A',
            final_states={'D'},
        )
        f = Automat(
            alphabet={'a', 'b'},
            states={'E', 'F'},
            transitions={
                'E': {'a': {'F'}, 'b': {'F'}},
                'F': {'a': {'E'}, 'b': {'E'}},
            },
            initial_state='E',
            final_states={'F'},
        )
        ab = a & b
        cd = c & d
        ef = e & f
        a_and_b = Automat(
            alphabet={'a', 'b'},
            states={'AD', 'AE', 'AF', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF'},
            transitions={
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
            initial_state='AD',
            final_states={'CF'},
        )
        c_and_d = Automat(
            alphabet={'a', 'b'},
            states={'q1g1'},
            transitions={
                '__': {'a': {'__'}, 'b': {'__'}},
                '_g1': {'a': {'__'}, 'b': {'_g1'}},
                'q1_': {'a': {'q1_'}, 'b': {'__'}},
                'q1g1': {'a': {'q1_'}, 'b': {'_g1'}}},
            initial_state='q1g1',
            final_states={'q1g1'},
        )
        e_and_f = Automat(
            alphabet={'a', 'b'},
            states={'AE', 'AF', 'BE', 'BF', 'CE', 'CF', 'DE', 'DF'},
            transitions={
                'AE': {'a': {'BF'}, 'b': {'BF'}},
                'BF': {'a': {'CE'}, 'b': {'CE'}},
                'CE': {'a': {'DF'}, 'b': {'DF'}},
                'DF': {'a': {'DE'}, 'b': {'DE'}},
                'DE': {'a': {'DF'}, 'b': {'DF'}},
                'AF': {'a': {'BE'}, 'b': {'BE'}},
                'BE': {'a': {'CF'}, 'b': {'CF'}},
                'CF': {'a': {'DE'}, 'b': {'DE'}}
            },
            initial_state='AE',
            final_states={'DF'},
        )
        self.assertEqual(a_and_b.alphabet, ab.alphabet)
        self.assertEqual(a_and_b.states, ab.states)
        self.assertDictEqual(a_and_b.transitions, ab.transitions)
        self.assertEqual(a_and_b.initial_state, ab.initial_state)
        self.assertEqual(a_and_b.final_states, ab.final_states)

        self.assertEqual(c_and_d.alphabet, cd.alphabet)
        self.assertEqual(c_and_d.states, cd.states)
        self.assertDictEqual(c_and_d.transitions, cd.transitions)
        self.assertEqual(c_and_d.initial_state, cd.initial_state)
        self.assertEqual(c_and_d.final_states, cd.final_states)

        self.assertEqual(e_and_f.alphabet, ef.alphabet)
        self.assertEqual(e_and_f.states, ef.states)
        self.assertDictEqual(e_and_f.transitions, ef.transitions)
        self.assertEqual(e_and_f.initial_state, ef.initial_state)
        self.assertEqual(e_and_f.final_states, ef.final_states)

    def test_or(self):
        a = Automat(
            alphabet={'a', 'b'},
            states={'A', 'B', 'C'},
            transitions={
                'A': {'a': {'B'}, 'b': {'A'}},
                'B': {'a': {'C'}, 'b': {'B'}},
                'C': {'a': {'C'}, 'b': {'C'}}
            },
            initial_state='A',
            final_states={'C'},
        )
        b = Automat(
            alphabet={'a', 'b'},
            states={'D', 'E', 'F'},
            transitions={
                'D': {'a': {'D'}, 'b': {'E'}},
                'E': {'a': {'E'}, 'b': {'F'}},
                'F': {'a': {'F'}, 'b': {'F'}}
            },
            initial_state='D',
            final_states={'F'},
        )
        c = Automat(
            alphabet={'a'},
            states={'q1'},
            transitions={
                'q1': {'a': {'q1'}},
            },
            initial_state='q1',
            final_states={'q1'},
        )
        d = Automat(
            alphabet={'b'},
            states={'g1'},
            transitions={
                'g1': {'b': {'g1'}},
            },
            initial_state='g1',
            final_states={'g1'},
        )
        ab = a | b
        cd = c | d
        a_or_b = Automat(
            alphabet={'a', 'b'},
            states={'AD', 'AE', 'AF', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF'},
            transitions={
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
            initial_state='AD',
            final_states={'CD', 'CE', 'CF', 'AF', 'BF'},
        )
        c_or_d = Automat(
            alphabet={'a', 'b'},
            states={'q1g1', '__', '_g1', 'q1_'},
            transitions={
                '__': {'a': {'__'}, 'b': {'__'}},
                '_g1': {'a': {'__'}, 'b': {'_g1'}},
                'q1_': {'a': {'q1_'}, 'b': {'__'}},
                'q1g1': {'a': {'q1_'}, 'b': {'_g1'}}},
            initial_state='q1g1',
            final_states={'q1g1', 'q1_', '_g1'},
        )
        self.assertEqual(a_or_b.alphabet, ab.alphabet)
        self.assertEqual(a_or_b.states, ab.states)
        self.assertDictEqual(a_or_b.transitions, ab.transitions)
        self.assertEqual(a_or_b.initial_state, ab.initial_state)
        self.assertEqual(a_or_b.final_states, ab.final_states)

        self.assertEqual(c_or_d.alphabet, cd.alphabet)
        self.assertEqual(c_or_d.states, cd.states)
        self.assertDictEqual(c_or_d.transitions, cd.transitions)
        self.assertEqual(c_or_d.initial_state, cd.initial_state)
        self.assertEqual(c_or_d.final_states, cd.final_states)

    def test_invert(self):
        a = Automat(
            alphabet={'a', 'b'},
            states={'A', 'B', 'C'},
            transitions={
                'A': {'a': {'B'}, 'b': {'A'}},
                'B': {'a': {'C'}, 'b': {'B'}},
                'C': {'a': {'C'}, 'b': {'C'}}
            },
            initial_state='A',
            final_states={'C'},
        )
        b = Automat(
            alphabet={'a', 'b'},
            states={'A', 'B', 'C'},
            transitions={
                'A': {'a': {'B'}, 'b': {'D'}},
                'B': {'a': {'C'}, 'b': {'B'}},
            },
            initial_state='A',
            final_states={'C'},
        )
        c = Automat(
            alphabet={'a'},
            states={'q1'},
            transitions={
                'q1': {'a': {'q1'}}},
            initial_state='q1',
            final_states={'q1'},
        )

        na = ~a
        nc = ~c
        self.assertEqual(na.alphabet, a.alphabet)
        self.assertEqual(na.states, a.states)
        self.assertDictEqual(na.transitions, {
            'A': {'a': {'B'}, 'b': {'A'}},
            'B': {'a': {'C'}, 'b': {'B'}},
            'C': {'a': {'C'}, 'b': {'C'}},
        })
        self.assertEqual(na.initial_state, a.initial_state)
        self.assertEqual(na.final_states, {'A', 'B'})

        self.assertEqual(nc.alphabet, c.alphabet)
        self.assertEqual(nc.states, c.states)
        self.assertDictEqual(nc.transitions, {'q1': {'a': {'q1'}}})
        self.assertEqual(nc.initial_state, c.initial_state)
        self.assertEqual(nc.final_states, set())

        with self.assertRaises(TypeError):
            ~b

    def test_minus(self):

        a = Automat(
            alphabet={'a'},
            states={'A'},
            transitions={
                'A': {'a': {'A'}},
            },
            initial_state='A',
            final_states={'A'},
        )

        b = Automat(
            alphabet={'a'},
            states={'A', 'B'},
            transitions={
                'A': {'a': {'B'}},
                'B': {'a': {'A'}}

            },
            initial_state='A',
            final_states={'B'},
        )

        a_minus_a = a - a
        a_minus_b = a - b
        a_minus_b.save_dot('a_b.dot')
        self.assertEqual(a_minus_a.final_states, set())
        self.assertEqual(a_minus_b.final_states, {'AA'})
        self.assertEqual(a_minus_b.transitions, {'AA': {'a': {'BA'}},
                                                 'BA': {'a': {'AA'}}})


if __name__ == '__main__':
    unittest.main()
