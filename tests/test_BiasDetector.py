from bias_detector.BiasDetector import *
from .common import *

from bias_detector.BiasMetric import BiasMetric

bias_detector = BiasDetector()


class TestBiasDetector:

    def test_get_p_groups(self):
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, last_names=last_names_mock, zip_codes=zip_codes_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.22120724490233212
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, zip_codes=zip_codes_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.37026898144716697
        p_groups = bias_detector.get_p_groups(first_names=first_names_mock, last_names=last_names_mock)
        assert p_groups.at[0, 'male'] == 0.0
        assert p_groups.at[0, 'female'] == 1.0
        assert p_groups.at[0, 'white'] == 0.5408381893515636

    def test_get_bias_report(self):
        bias_report = bias_detector.get_bias_report(first_names=first_names_mock,
                                                    last_names=last_names_mock, zip_codes=zip_codes_mock,
                                                    y_true=y_true_mock, y_pred=y_pred_mock, privileged_race='white',
                                                    country='US')
        bias_metrics_results = bias_report.bias_metrics_results
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].get_diff() == 0.053134892796120714
        assert bias_metrics_results.at[BiasMetric.predictive_equality.name, 'white'].get_diff() == 0.016030656112268837
        assert bias_metrics_results.at[BiasMetric.equal_opportunity.name, 'white'].get_diff() == -0.00666254800184618
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].bias_confidence.p_value == 1.0061059942609127e-07
        bias_report = bias_detector.get_bias_report(emails=emails_mock, y_true=y_true_mock, y_pred=y_pred_mock,
                                                    privileged_race='white', country='US')
        bias_metrics_results = bias_report.bias_metrics_results
        assert bias_metrics_results.at[BiasMetric.statistical_parity.name, 'male'].get_diff() == 0.048666861482969725

    def test_get_bias_report_edge_cases(self):
        assert bias_detector.get_bias_report(first_names=first_names_mock,
                                             last_names=last_names_mock, country='FR') is None
        assert bias_detector.get_bias_report(first_names=first_names_mock,
                                             last_names=last_names_mock, y_pred=None, country='US') is None

def test_get_first_names_p_gender_df():
    assert p_gender_given_first_name_df.at['MOSHE', 'male'] == 1.0
    assert p_gender_given_first_name_df.at['SARAH', 'female'] == 1.0
    assert p_gender_given_first_name_df.at['RAY', 'male'] == 0.9683544303797468