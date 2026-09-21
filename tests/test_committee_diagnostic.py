import unittest
import numpy as np
from corrlaw.committee_diagnostic import spread_summary


class CommitteeDiagnosticTests(unittest.TestCase):
    def test_added_witness_exposes_small_spread_but_does_not_change_error(self):
        original=np.zeros((3,1));augmented=np.tile([-1.,0.,1.],(3,1))
        result=spread_summary(original,augmented,.2,False)
        self.assertTrue(result['ordinary_false_consensus'])
        self.assertFalse(result['augmented_false_consensus'])
        self.assertTrue(result['high_error_low_spread_flag_removed'])
        self.assertEqual(result['off_rmse'],.2)

    def test_adding_central_members_can_reduce_spread(self):
        original=np.tile([-.06,.06],(4,1))
        augmented=np.concatenate((original,np.zeros((4,20))),axis=1)
        result=spread_summary(original,augmented,.2,False)
        self.assertTrue(result['spread_threshold_crossed_down'])
        self.assertTrue(result['high_error_low_spread_flag_added'])
        self.assertLess(result['augmented_rms_spread'],result['ordinary_rms_spread'])

    def test_low_error_does_not_become_false_consensus(self):
        result=spread_summary(np.zeros((2,1)),np.ones((2,1)),.01,True)
        self.assertFalse(result['ordinary_false_consensus'])
        self.assertTrue(result['poor_observational_fit'])


if __name__=='__main__':unittest.main()
