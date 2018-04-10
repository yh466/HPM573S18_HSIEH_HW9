import InputData as Settings
import scr.FormatFunctions as F


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of number of strokes a patient experienced
    num_of_STROKE_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_numOfStroke().get_mean(),
        interval=simOutput.get_sumStat_numOfStroke().get_t_CI(alpha=Settings.ALPHA),
        deci=2)


    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean number of strokes and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          num_of_STROKE_CI_text)

