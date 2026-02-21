from app.models.enums import ColdStage


class LeadStateMachine:

    allowed_transitions = {
        ColdStage.new: [ColdStage.contacted],
        ColdStage.contacted: [ColdStage.qualified],
        ColdStage.qualified: [ColdStage.lost], 
    }

    @classmethod
    def validate_transition(cls, current, new):
        if current in [ColdStage.transferred, ColdStage.lost]:
            raise ValueError("Final stages cannot be modified")

        allowed = cls.allowed_transitions.get(current, [])

        if new not in allowed:
            raise ValueError(f"Invalid transition {current} → {new}")