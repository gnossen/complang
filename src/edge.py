from alphabet import alphabet

EpsilonAlphabet = alphabet(["ε"])

class Edge:
    def __init__(self, letters, next_state):
        self.letters = set(letters)
        self.next_state = next_state

    def add_letter(self, letter):
        self.letters = self.letters | {letter}

    def is_epsilon(self):
        return len(self.letters) == 1 and list(self.letters) == ["ε"]

    @staticmethod
    def merge(edges):
        edges_ = list(edges)
        new_edges = []
        for edge in edges_:
            merged_edge = edge
            for other_edge in edges_:
                if other_edge is edge:
                    continue
                if edge.next_state is other_edge.next_state:
                    merged_edge.letters = merged_edge.letters | other_edge.letters
                    edges_.remove(other_edge)
            new_edges.append(merged_edge)
        return new_edges
