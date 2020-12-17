class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, nodelist):
        if type(nodelist)==Node:
            self.frontier.append(nodelist)
        else:
            for node in nodelist:
                if not self.contains_state(node.state):
                    self.add(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def get_node_with_state(self, state):
        if not self.contains_state(state):
            raise Exception("Dont have state {}".format(state))
        for node in self.frontier:
            if node.state == state:
                return node
    
    def state_list(self):
        states = []
        for node in self.frontier:
            states.append(node.state)
        return states
            

    def empty(self):
        return len(self.frontier) == 0
    
    def length(self):
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node



class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
