# my_states.py

from state_machine.state import State

# Start of our states
class HappyState(State):

    def on_event(self, event):
        
        if event == 'sad':
            return SadState()
        elif event == 'beingfed':
            return FoodState()
        elif event == 'dirty':
            return DirtState()
        elif event == 'sick':
            return SickState()
        elif event == 'work':
            return WorkState()
        return self

class UwuState(State):

    def on_event(self, event):
        if event == 'fed':
            return HappyState()
        elif event == 'beingfed':
            return FoodState()
        elif event == 'sick':
            return SickState()
        elif event == 'work':
            return WorkState()
        return self
    
class SadState(State):

    def on_event(self, event):
        if event == 'fed':
            return HappyState()
        elif event == 'beingfed':
            return FoodState()
        elif event == 'sick':
            return SickState()
        elif event == 'work':
            return WorkState()
        return self

    
class DirtState(State):

    def on_event(self, event):
        if event == 'clean':
            print("clean")
            return HappyState()
        elif event == 'sick':
            return SickState()
        return self
    
class SickState(State):

    def on_event(self, event):
        if event == 'cured':
            return HappyState()

        return self
    
class FoodState(State):

    def on_event(self, event):
        if event == 'fed':
            return HappyState()

        return self

class WorkState(State):

    def on_event(self, event):
        if event == 'done_work':
            return HappyState()

        return self
    


# End of our states.
