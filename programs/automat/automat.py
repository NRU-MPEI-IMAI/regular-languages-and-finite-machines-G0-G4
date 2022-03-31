from collections import defaultdict, deque

class Automat:
    '''
    class for representing final state automata.
    Automata = (
        alphabet = set of chars
        states = set of strings
        transitions = dict{state: dict{letter: {set of children} ...} ...}
        initial_state = string
        final_states = set of strings
    )
    '''

    def __init__(self, alphabet, states, transitions,
                 initial_state, final_states):
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def __lambda_connections(self, start, state, visited,
                             new_connections, new_final_states):
        '''
        searches for lambda reachable states (states that can be reached
        by any number of lambda transitions), if start state is in final_states
        adds them to the new_final_states.
        Create connections between start and children of lambda reachable states.
        Returns this connections and new_final_states
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
        returns new connections for a new state by combining connections
        of old states
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
        transforms states in transitions dictionaries to stirngs.
        Children are transformed into sets of one string.
        transforms states in "final_states" to strings
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
        function to get child of a state
        '''

        if state not in transitions or letter not in transitions[state]:
            return None
        child = transitions[state][letter]
        if isinstance(child, set):
            child = tuple(child)[0]
        return child

    @staticmethod
    def __cartesian(transitions1, transitions2, states1, states2, alphabet):
        '''
        returns cartesian product of transition tables
        '''

        transitions = defaultdict(dict)
        for letter in alphabet:
            for st1 in states1:
                for st2 in states2:
                    st1_child = Automat.__state_child(transitions1, st1, letter)
                    st2_child = Automat.__state_child(transitions2, st2, letter)
                    transitions[st1+st2][letter] = st1_child + st2_child
        return transitions

    @staticmethod
    def __new_states(states1, states2):
        '''
        function to generate new states for the new dfa generate by
        {&,|,-} operations
        '''
        new_states = set()
        for st1 in states1:
            for st2 in states2:
                new_states.add(st1+st2)
        return new_states

    @staticmethod
    def __final_state(final_states1, final_states2):
        '''
        helper function to generate final_states for dfa = dfa1 & dfa2
        '''
        final_states = set()
        for fs1 in final_states1:
            for fs2 in final_states2:
                final_states.add(fs1 + fs2)
        return final_states

    @staticmethod
    def __final_state_or(final_states1, final_states2, states1, states2):
        '''
        helper function to generate final_states for dfa = dfa1 | dfa2
        '''
        final_states = set()
        for fs1 in final_states1:
            for st2 in states2:
                final_states.add(fs1 + st2)
        for fs2 in final_states2:
            for st1 in states1:
                final_states.add(st1 + fs2)
        return final_states

    def __and__(self, other):
        '''
        dfa and operation
        '''

        if not (Automat.is_deterministic(self) and
            Automat.is_deterministic(other)):
            raise TypeError('"&" could be applied only to two dfas')
        new_alphabet = self.alphabet | other.alphabet
        ts1, full1 = Automat.__full_transitions(
            self.states,
            new_alphabet,
            self.transitions)
        ts2, full2 = Automat.__full_transitions(
            other.states,
            new_alphabet,
            other.transitions)
        states1 = self.states.copy()
        states2 = other.states.copy()
        transitions1 = self.transitions.copy()
        transitions2 = other.transitions.copy()
        if not full1:
            transitions1 = ts1
            states1.add('_')
        if not full2:
            transitions2 = ts2
            states2.add('_')
        new_transitions = self.__cartesian(
            transitions1,
            transitions2,
            states1,
            states2,
            new_alphabet)
        new_initial_state = self.initial_state + other.initial_state
        new_states = Automat.__new_states(self.states, other.states)
        new_final_states = Automat.__final_state(self.final_states,
            other.final_states)
        result = Automat(
            new_alphabet,
            new_states,
            new_transitions,
            new_initial_state,
            new_final_states,
        )
        result.__stringify()
        return result

    def __or__(self, other):
        '''
        dfa or operation
        '''
        if not (Automat.is_deterministic(self) and
            Automat.is_deterministic(other)):
            raise TypeError('"|" could be applied only to two dfas')
        new_alphabet = self.alphabet | other.alphabet
        ts1, full1 = Automat.__full_transitions(
            self.states,
            new_alphabet,
            self.transitions)
        ts2, full2 = Automat.__full_transitions(
            other.states,
            new_alphabet,
            other.transitions)
        states1 = self.states.copy()
        states2 = other.states.copy()
        transitions1 = self.transitions.copy()
        transitions2 = other.transitions.copy()
        if not full1:
            transitions1 = ts1
            states1.add('_')
        if not full2:
            transitions2 = ts2
            states2.add('_')
        new_transitions = self.__cartesian(
            transitions1,
            transitions2,
            states1,
            states2,
            new_alphabet)
        new_initial_state = self.initial_state + other.initial_state
        new_states = Automat.__new_states(states1, states2)
        new_final_states = Automat.__final_state_or(self.final_states,
            other.final_states, states1, states2)
        result = Automat(
            new_alphabet,
            new_states,
            new_transitions,
            new_initial_state,
            new_final_states,
        )
        result.__stringify()
        return result

    @staticmethod
    def __full_transitions(states, alphabet, transitions):
        '''
        returns full transition table, and True if it was already full,
        False otherwise
        '''
        new_transitions = defaultdict(dict)
        full = True
        for state in states:
            for letter in alphabet:
                if state in transitions and letter in transitions[state]:
                    if isinstance(transitions[state][letter], set):
                        new_transitions[state][letter] = tuple(transitions[state][letter])[0]
                    else:
                        new_transitions[state][letter] = transitions[state][letter]
                else:
                    full = False
                    new_transitions[state][letter] = '_'
        if not full:
            for letter in alphabet:
                new_transitions['_'][letter] = '_'
        return new_transitions, full


    def __invert__(self):
        '''
        dfa complement
        '''
        if not Automat.is_deterministic(self):
            raise TypeError('"~" could be applied only to dfa')
        ts, full = Automat.__full_transitions(
            self.states,
            self.alphabet,
            self.transitions)
        new_states = self.states.copy()
        new_transitions = self.transitions.copy()
        if not full:
            new_transitions = ts
            new_states.add('_')
        new_final_states = (new_states - self.final_states)

        result = Automat(
            alphabet=self.alphabet.copy(),
            states=new_states,
            transitions=new_transitions,
            initial_state=self.initial_state,
            final_states=new_final_states,
        )
        # result.__stringify()
        return result

    @staticmethod
    def is_deterministic(automat):
        '''
        checks if the automata is deterministic
        '''
        for state in automat.states:
            if state not in automat.transitions:
                return False
            for letter in automat.alphabet:
                if (letter not in automat.transitions[state] or
                    len(automat.transitions[state][letter]) > 1):
                    return False
        return True