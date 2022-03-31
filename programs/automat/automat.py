from cmath import isinf
from collections import defaultdict, deque

class Automat:
    '''
    class for representing final state automata
    '''

    def __init__(self, alphabet, states, transitions,
                 initial_state, final_states, deterministic):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.deterministic = deterministic

    def __lambda_connections(self, start, state, visited,
                             new_connections, new_final_states):
        '''
        searching for lambda reachable states (states that can be reached
        by any number of lambda transitions), if start state is in final_states
        add them to new_final_states.
        Create connectins for start and children of lambda reachable states.
        Return this connections and new_final_states
        '''
        if state in self.transitions:
            for connection in self.transitions[state]:
                for child in self.transitions[state][connection]:
                    if connection == '' and child not in visited:
                        if start in self.final_states:
                            new_final_states.add(child)
                        visited.add(state)
                        self.__lambda_connections(
                            start, child, visited,
                            new_connections, new_final_states)
                        visited.remove(state)
                    else:
                        if connection != '':
                            new_connections[start][connection].add(child)
        return new_connections, new_final_states

    def remove_lambda_connections(self):
        '''
        removes lambda connections, modifies transitions and final_states,
        returns them
        '''

        all_new_connections = defaultdict(lambda: defaultdict(set))
        for state in self.transitions:
            new_connections, new_states = self.__lambda_connections(
                state, state, set(),
                defaultdict(lambda: defaultdict(set)), set())
            self.final_states |= new_states
            all_new_connections[state].update(new_connections[state])
        self.transitions = all_new_connections
        return self.transitions, self.final_states

    def __dfa_connection(self, states):
        '''
        combines connection from set of states
        '''

        new_connections = defaultdict(lambda: defaultdict(set))
        new_state = frozenset(states)
        new_connections[new_state]
        for state in states:
            if state not in self.transitions:
                continue
            for connection in self.transitions[state]:
                new_connections[new_state][connection].update(
                    self.transitions[state][connection])
        return new_connections

    def __stringify(self):
        '''
        transforms states in transitions dict to stirngs.
        Children are transformed into sets of one string.
        transforms final states to strings
        '''
        delim = ','
        transitions = {}
        final_states = set()
        for state in self.transitions:
            for connection in self.transitions[state]:
                new_state = state
                if isinstance(state, set) or isinstance(state, frozenset):
                    new_state = '"' + delim.join(sorted(list(state))) + '"'
                child = self.transitions[state][connection]
                if isinstance(child, set) or isinstance(child, frozenset):
                    child = '"' + delim.join(sorted(
                        list(child))) + '"'
                if new_state not in transitions:
                    transitions[new_state] = {}
                transitions[new_state][connection] = {child}

        for state in self.final_states:
            new_state = state
            if isinstance(new_state, set) or isinstance(new_state, frozenset):
                new_state = '"' + delim.join(sorted(list(new_state))) + '"'
            final_states.add(new_state)

        self.transitions = transitions
        self.final_states = final_states
        if (isinstance(self.initial_state, set) or
            isinstance(self.initial_state, frozenset)):
            self.initial_state = '"' + delim.join(sorted(list(self.initial_state))) + '"'

    def to_dfa(self):
        '''
        makes automat deterministic
        '''

        self.remove_lambda_connections()
        queue = deque()
        visited = set()
        self.initial_state = frozenset({self.initial_state})
        queue.append(self.initial_state)
        new_connections = {}
        new_final_states = set()
        while queue:
            state = queue.popleft()
            connections = self.__dfa_connection(state)
            new_state = list(connections.keys())[0]
            new_connections.update(connections)
            for connection in connections[new_state]:
                state = frozenset(connections[new_state][connection])
                if state not in visited:
                    queue.append(state)
                    visited.add(state)
                    if self.final_states & state:
                        new_final_states.add(state)
        self.transitions = new_connections
        self.final_states = new_final_states
        self.__stringify()
        self.deterministic = True
        return self.transitions, self.final_states

    def save_dot(self, file):
        '''
        saves graph to a dot file
        '''

        with open(file, 'w') as f:
            f.write('digraph {\n')
            f.write('rankdir = LR\n')
            if self.initial_state:
                f.write(f'{self.initial_state} [ color = "#808080", shape = circle];\n')
            if self.final_states:
                f.write(f'{",".join(self.final_states)} [shape = doublecircle];\n')
            f.write('node [shape = circle];\n')
            for state in self.transitions:
                for connection in self.transitions[state]:
                    for child in self.transitions[state][connection]:
                        f.write(f'{state} -> {child} [label = "{connection}"];\n')
            f.write('}')

    @staticmethod
    def __state_child(transitions, state, letter):
        '''
        function to get child state with connection by letter
        '''

        if state not in transitions or letter not in transitions[state]:
            return None
        return transitions[state][letter]
    
    @staticmethod
    def __cartesian(transitions1, transitions2, states1, states2, alphabet):
        '''
        return cartesian product of transitions
        '''

        transitions = defaultdict(dict)
        for st1 in states1:
            for st2 in states2:
                for letter in alphabet:
                    st1_child = Automat.__state_child(transitions1, st1, letter)
                    st2_child = Automat.__state_child(transitions2, st2, letter)
                    if not st1_child or not st2_child:
                        child = '@'
                    else:
                        if isinstance(st1_child, set):
                            st1_child = tuple(st1_child)[0]
                        if isinstance(st2_child, set):
                            st2_child = tuple(st2_child)[0]
                        child = st1_child + st2_child
                    transitions[st1+st2][letter] = child
        return transitions

    @staticmethod
    def __final_state(final_states1, final_states2):
        '''
        helper function to generate final_states after product
        '''
        final_states = set()
        for fs1 in final_states1:
            for fs2 in final_states2:
                final_states.add(fs1 + fs2)
        return final_states


    def __and__(self, other):
        '''
        dfa cartesian product
        '''

        if not (self.deterministic and other.deterministic):
            raise TypeError('only two dfas could be multiplied')
        new_alphabet = self.alphabet | other.alphabet
        new_transitions = self.__cartesian(
            self.transitions,
            other.transitions,
            self.states,
            other.states,
            new_alphabet)
        new_initial_state = self.initial_state + other.initial_state
        new_states = new_transitions.keys()
        new_final_states = Automat.__final_state(self.final_states,
            other.final_states)
        result = Automat(
            new_alphabet,
            new_states,
            new_transitions,
            new_initial_state,
            new_final_states,
            deterministic=True
        )
        result.__stringify()
        return result