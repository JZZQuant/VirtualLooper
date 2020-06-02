from core.states import State


class ExpressionState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Expression"

    def on_state(self, in_data, active_phrase, back_vol):
        sample = active_phrase.phrase.counter(back_vol=back_vol)
        return sample + in_data
