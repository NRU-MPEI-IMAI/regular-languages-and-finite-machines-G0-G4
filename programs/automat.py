from collections import defaultdict, deque

from torch import ne


class Automat:
    '''
    class for representing final state automata
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
        transitions = {}
        final_states = set()
        for state in self.transitions:
            for connection in self.transitions[state]:
                new_state = ','.join(sorted(list(state)))
                child = ','.join(sorted(
                    list(self.transitions[state][connection])))
                transitions[new_state] = {}
                transitions[new_state][connection] = {child}

        for state in self.final_states:
            new_state = ','.join(sorted(list(state)))
            final_states.add(new_state)
        
        self.transitions = transitions
        self.final_states = final_states
        
    def to_dfa(self):
        '''
        makes automat deterministic
        '''

        self.remove_lambda_connections()
        queue  = deque()
        visited = set()
        self.initial_state = frozenset(self.initial_state)
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
        return new_connections, new_final_states
