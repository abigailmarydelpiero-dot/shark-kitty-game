# my_states.py

from state_machine.state import State

# Start of our states
class HappyState(State):

    def on_event(self, event):
        
        if event == 'ignored':
            return SadState()

        return self


class HungryState(State):

    def on_event(self, event):
        if event == 'fed':
            return HappyState()

        return self
    
class SadState(State):

    def on_event(self, event):
        if event == 'fed':
            return HappyState()

        return self
# End of our states.
