import scr.SamplePathClasses as PathCls
import scr.StatisticalClasses as StatCls
import scr.RandomVariantGenerators as rndClasses
import ParameterClasses as P
import InputData as Data


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: parameter object
        """

        self._id = id
        # random number generator for this patient
        self._rng = None
        # parameters
        self._param = parameters
        # state monitor
        self._stateMonitor = PatientStateMonitor(parameters)
        # simulation time step
        self._delta_t = parameters.get_delta_t()

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        self._rng = rndClasses.RNG(self._id)

        k = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self._stateMonitor.get_if_alive() and k*self._delta_t < sim_length:

            # find the transition probabilities of the future states
            trans_probs = self._param.get_transition_prob(self._stateMonitor.get_current_state())
            # create an empirical distribution
            empirical_dist = rndClasses.Empirical(trans_probs)
            # sample from the empirical distribution to get a new state
            # (returns an integer from {0, 1, 2, ...})
            new_state_index = empirical_dist.sample(self._rng)

            # update health state
            self._stateMonitor.update(k, P.HealthStats(new_state_index))

            # increment time step
            k += 1

    def get_survival_time(self):
        """ returns the patient's survival time"""
        return self._stateMonitor.get_survival_time()

    def get_num_of_stroke(self):
        """ returns the patient's time to the POST_STROKE state """
        return self._stateMonitor.get_num_of_STROKE()


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):
        """
        :param parameters: patient parameters
        """
        self._currentState = parameters.get_initial_health_state() # current health state
        self._delta_t = parameters.get_delta_t()                   # simulation time step
        self._survivalTime = 0                                     # survival time
        self._numOfStroke = 0                                      # initialize counter for episodes of stroke
        self._ifExperiencedStroke = False                          # if the patient has a stroke

    def update(self, k, next_state):
        """
        :param k: current time step
        :param next_state: next state
        """

        # if the patient has died, do nothing
        if not self.get_if_alive():
            return

        # update survival time when the patient dies
        if next_state is P.HealthStats.DEAD:
            self._survivalTime = (k+0.5)*self._delta_t  # corrected for the half-cycle effect

        # update number of stroke
        #if self._currentState != P.HealthStats.STROKE and next_state == P.HealthStats.STROKE:
        #    self._ifExperiencedStroke = True
        #    self._numOfStroke = self._numOfStroke + 1

        if self._currentState == P.HealthStats.STROKE:
            self._ifExperiencedStroke = True
            self._numOfStroke += 1

        # update current health state
        self._currentState = next_state

    def get_if_alive(self):
        result = True
        if self._currentState == P.HealthStats.DEAD:
            result = False
        return result

    def get_current_state(self):
        return self._currentState

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if not self.get_if_alive():
            return self._survivalTime
        else:
            return None

    def get_num_of_STROKE(self):
        """ returns the number of strokes the patient experienced"""
        return self._numOfStroke


class Cohort:
    def __init__(self, id, therapy):
        """ create a cohort of patients
        :param id: an integer to specify the seed of the random number generator
        """
        self._initial_pop_size = Data.POP_SIZE
        self._patients = []      # list of patients

        # populate the cohort
        for i in range(self._initial_pop_size):
            # create a new patient (use id * pop_size + i as patient id)
            patient = Patient(id * self._initial_pop_size + i, P.ParametersFixed(therapy))
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self):
        """ simulate the cohort of patients over the specified number of time-steps
        :returns outputs from simulating this cohort
        """

        # simulate all patients
        for patient in self._patients:
            patient.simulate(Data.SIM_LENGTH)

        # return the cohort outputs
        return CohortOutputs(self)

    def get_initial_pop_size(self):
        return self._initial_pop_size

    def get_patients(self):
        return self._patients


class CohortOutputs:
    def __init__(self, simulated_cohort):
        """ extracts outputs from a simulated cohort
        :param simulated_cohort: a cohort after being simulated
        """

        self._survivalTimes = []        # patients' survival times
        self._nums_of_STROKE = []       # number of stroke patients experienced
        # survival curve
        self._survivalCurve = \
            PathCls.SamplePathBatchUpdate('Population size over time', id, simulated_cohort.get_initial_pop_size())

        # find patients' survival times
        for patient in simulated_cohort.get_patients():

            # get the patient survival time
            survival_time = patient.get_survival_time()
            if not (survival_time is None):
                self._survivalTimes.append(survival_time)           # store the survival time of this patient
                self._survivalCurve.record(survival_time, -1)       # update the survival curve

        for patient in simulated_cohort.get_patients():
            # get the number of stroke patients experienced
            num_of_STROKE = patient.get_num_of_stroke()
            self._nums_of_STROKE.append(num_of_STROKE)


        # summary statistics
        self._sumStat_survivalTime = StatCls.SummaryStat('Patient survival time', self._survivalTimes)
        self._sumStat_numOfStroke = StatCls.SummaryStat('Number of strokes a patient experienced', self._nums_of_STROKE)

    def get_survival_times(self):
        return self._survivalTimes

    def get_nums_of_stroke(self):
        return self._nums_of_STROKE

    def get_sumStat_survival_times(self):
        return self._sumStat_survivalTime

    def get_sumStat_numOfStroke(self):
        return self._sumStat_numOfStroke

    def get_survival_curve(self):
        return self._survivalCurve