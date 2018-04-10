from enum import Enum
import InputData as Data


class HealthStats(Enum):
    """ health states of patients with afib """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEAD = 3


class Therapies(Enum):
    """ no vs. anticoagulant therapy """
    NO = 0
    AC = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0
        # mortality relative risk
        self._mortalityRR = 0

        # transition probabilities between states
        self._prob_matrix = Data.PROB_MATRIX

        # update the transition probability matrix if combination therapy is being used
        if self._therapy == Therapies.AC:
            # treatment relative risk
            self._treatmentRR = Data.TREATMENT_RR
            # treatment mortality risk
            self._mortalityRR = Data.MORTALITY_RR
            # calculate transition probability matrix for the combination therapy
            self._prob_matrix = calculate_prob_matrix_ac(
                matrix_no=self._prob_matrix, ac_rr=Data.TREATMENT_RR, ac_mrr=Data.MORTALITY_RR)

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]


def calculate_prob_matrix_ac(matrix_no, ac_rr, ac_mrr):
    """
    :param matrix_no: (list of lists) transition probability matrix under mono therapy
    :param ac_rr: relative risk of anticoagulant treatment
    :param ac_mrr: relative mortality rate of anticoagulant treatment
    :returns (list of lists) transition probability matrix under combination therapy """

    # create an empty matrix and populate it with zeros
    matrix_ac = []
    for s in HealthStats:
        matrix_ac.append([0] * len(HealthStats))
    #matrix_ac = matrix_no
    # populate the ac matrix
    for s in HealthStats:
        if s != HealthStats.POST_STROKE:
            matrix_ac[s.value][s.value+1:] = matrix_no[s.value][s.value+1:]
            matrix_ac[s.value][s.value] = matrix_no[s.value][s.value]
            matrix_ac[s.value][s.value-1:] = matrix_no[s.value][s.value-1:]
    for s in HealthStats:
       if s is HealthStats.POST_STROKE:
            matrix_ac[s.value][s.value-1] = ac_rr * matrix_no[s.value][s.value-1]
            matrix_ac[s.value][s.value+1] = ac_rr * ac_mrr * matrix_no[s.value][s.value+1]
            matrix_ac[s.value][s.value] = 1 - matrix_ac[s.value][s.value-1] - matrix_ac[s.value][s.value+1]
            matrix_ac[s.value][s.value-2] = matrix_no[s.value][s.value-2]

    #for s in HealthStats:
    #    if s is HealthStats.WELL:
    #        matrix_ac[s.value][s.value+1:] = matrix_no[s.value][s.value+1:]

    #for s in HealthStats:
    #    if s is HealthStats.STROKE:
    #        matrix_ac[s.value][s.value+1] = matrix_no[s.value][s.value+1]
    return matrix_ac
