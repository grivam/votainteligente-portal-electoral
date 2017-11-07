from constance import config
from numpy import matrix
from .adapters import Adapter, CommitmentsAdapter

class Calculator(object):
    def __init__(self,
                election,
                selected_positions=[],
                selected_proposals=[],
                questions_adapter_class=Adapter,
                commitments_adapter_class=CommitmentsAdapter):
        self.set_questions_adapter(questions_adapter_class(election, selected_positions))
        self.set_commitments_adapter(commitments_adapter_class(election, selected_proposals))
        self.election = election
        if not self.questions_adapter.positions:
            self.questions_importance = 0
            self.proposals_importance = 1
        else:
            self.questions_importance = config.DEFAULT_12_N_QUESTIONS_IMPORTANCE
            self.proposals_importance = config.DEFAULT_12_N_PROPOSALS_IMPORTANCE

    def set_questions_importance(self, importance):
        self.questions_importance = importance

    def set_proposals_importance(self, importance):
        self.proposals_importance = importance

    def set_questions_adapter(self, adapter):
        self.questions_adapter = adapter
    
    def set_commitments_adapter(self, adapter):
        self.commitments_adapter = adapter

    def _get_questions_vector_result(self):
        P = matrix(self.questions_adapter.get_responses_matrix())
        R = matrix(self.questions_adapter.get_responses_vector()).transpose()
        _r = P * R
        return _r

    def get_questions_result(self):
        candidates_vector = matrix(self.questions_adapter.candidates).transpose().tolist()
        _result = self._get_questions_vector_result().tolist()
        concatenated = []
        for index in range(len(_result)):
            concatenated.append({'candidate': candidates_vector[index][0], 'value': _result[index][0]})
        concatenated = sorted(concatenated, key=lambda t: -t['value'])
        result = {'election': self.election, 'candidates': concatenated}
        return result

    def get_commitments_result(self):
        C = self.commitments_adapter.get_commitments_matrix()
        return C * self.commitments_adapter.ones

    def _get_result(self):
        P_x_R = self._get_questions_vector_result()
        C = self.get_commitments_result()
        result = P_x_R * self.questions_importance + C * self.proposals_importance
        return result

    def get_result(self):
        candidates_vector = matrix(self.questions_adapter.candidates).transpose().tolist()
        _result = self._get_result().tolist()
        concatenated = []
        hundred_percent = len(self.questions_adapter.user_positions) + len(self.commitments_adapter.ones)
        for index in range(len(_result)):
            concatenated.append({'candidate': candidates_vector[index][0],
                                 'value': (_result[index][0]/hundred_percent) * 100})
        concatenated = filter(lambda v: v['value'], concatenated)
        concatenated = sorted(concatenated, key=lambda t: -t['value'])
        
        concatenated = concatenated[:config.N_CANDIDATOS_RESULTADO_12_N]
        result = {'election': self.election, 'candidates': concatenated}
        return result