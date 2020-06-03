from core.states import State


class ExpressionState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.state_id = "Expression"

    def on_state(self, in_data, active_phrase):
        sample = active_phrase.phrase.counter(back_vol=self.back_vol)
        return sample + in_data
