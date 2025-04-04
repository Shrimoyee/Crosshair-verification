class Customer:
    '''Represents a customer in a transaction network.'''

    def __init__(self, customer_id: int, name: str, is_fraudster: bool = False):
        assert isinstance(customer_id, int) and customer_id > 0, "Precondition: Customer ID must be a positive integer."
        assert isinstance(name, str) and name.strip(), "Precondition: Name must be a non-empty string."
        assert isinstance(is_fraudster, bool), "Precondition: is_fraudster must be a boolean."

        self.customer_id = customer_id
        self.name = name
        self.is_fraudster = is_fraudster


class TransactionNetwork:
    '''Represents a financial transaction network as a graph.'''

    def __init__(self):
        self.graph = {}  
    def add_transaction(self, sender: Customer, receiver: Customer):
        '''
        Adds a transaction link between two customers.
        Preconditions:
        - sender and receiver must be valid Customer objects.
        - sender and receiver must be different customers.
        Postconditions:
        - Both sender and receiver should exist in the graph after the function.
        '''
        assert isinstance(sender, Customer) and isinstance(receiver, Customer), "Precondition: Both sender and receiver must be valid Customer objects."
        assert sender.customer_id != receiver.customer_id, "Precondition: Sender and receiver must be different."

        if sender.customer_id not in self.graph:
            self.graph[sender.customer_id] = set()
        if receiver.customer_id not in self.graph:
            self.graph[receiver.customer_id] = set()

        self.graph[sender.customer_id].add(receiver.customer_id)
        self.graph[receiver.customer_id].add(sender.customer_id)

        assert sender.customer_id in self.graph and receiver.customer_id in self.graph, "Postcondition: Both customers must exist in the graph."
    
    def is_fraudulent_connection(self, customer_id: int, visited=None, depth: int = 3) -> bool:
        '''
        Recursively checks if a customer is within a certain connection depth to a known fraudster.
        Preconditions:
        - customer_id must be in the graph.
        - depth must be a non-negative integer.
        Postconditions:
        - Returns True if a fraudster is found within the given depth, False otherwise.
        Invariants:
        - `visited` set should not grow beyond total number of customers in the graph.
        '''
        assert isinstance(customer_id, int) and customer_id in self.graph, "Precondition: customer_id must exist in the graph."
        assert isinstance(depth, int) and depth >= 0, "Precondition: depth must be a non-negative integer."
        
        if visited is None:
            visited = set()
        
        visited.add(customer_id)
        
        # Base case: If this customer is a fraudster, return True
        for neighbor_id in self.graph.get(customer_id, []):
            assert neighbor_id in self.graph, "Invariant: Every neighbor must exist in the graph."
            if neighbor_id not in visited:
                if depth > 0:
                    if self.is_fraudulent_connection(neighbor_id, visited, depth - 1):
                        return True
        
        return False
