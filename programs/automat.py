from collections import defaultdict


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
