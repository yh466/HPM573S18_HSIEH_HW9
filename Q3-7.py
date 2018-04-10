import ParameterClasses as P
import MarkovModelClasses as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create a cohort
cohort_no = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NO)

cohort_ac = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.AC
)

# simulate the cohort
simOutputs_no = cohort_no.simulate()
simOutputs_ac = cohort_ac.simulate()

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs_no.get_survival_curve(),
    title='Survival curve for no anti-coagulant',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs_ac.get_survival_curve(),
    title='Survival curve for anti-coagulant',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )


# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs_no.get_nums_of_stroke(),
    title='Number of strokes a patient may experience without anti-coagulant',
    x_label='Number of strokes',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs_ac.get_nums_of_stroke(),
    title='Number of strokes a patient may experience with anti-coagulant',
    x_label='Number of strokes',
    y_label='Counts',
    bin_width=1
)

# print the outcomes of this simulated cohort
print('Problems 1 and 2: please see MarkovDiagrams.pdf')
print('   ')
print('Problems 3 and 7')
SupportMarkov.print_outcomes(simOutputs_no, 'No anti-coagulant:')
print('  ')
print('Problem 4: please see ParameterClasses.py, lines 76-90.')
print('   ')
print('Problem 6: please see graphs')
print('   ')
print('Problems 5 and 7')
SupportMarkov.print_outcomes(simOutputs_ac, 'Anti-coagulant:')
