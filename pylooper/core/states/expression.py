from core.states import State


class ExpressionState(State):
    def __init__(self, session):
        State.__init__(self, session)
        self.name = "Expression"
