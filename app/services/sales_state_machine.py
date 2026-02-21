from app.models.enums import SalesStage


class SalesStateMachine:

    allowed_transitions = {
        SalesStage.new: [SalesStage.kyc, SalesStage.lost],
        SalesStage.kyc: [SalesStage.agreement, SalesStage.lost],
        SalesStage.agreement: [SalesStage.paid, SalesStage.lost],
        SalesStage.paid: [],
        SalesStage.lost: [],
    }

    @classmethod
    def validate_transition(cls, current_stage: SalesStage, new_stage: SalesStage):

        if current_stage == new_stage:
            return

        if new_stage not in cls.allowed_transitions[current_stage]:
            raise ValueError(
                f"Cannot переходить from {current_stage} to {new_stage}"
            )