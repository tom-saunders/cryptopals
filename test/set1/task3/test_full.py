import unittest

import util.weighting

@unittest.skipUnless(util.get_tasks()[1][3], 'test not set to run')
@unittest.skipUnless(util.get_task_level() == util.config.TaskLevel.FULL, 'full test not set to run')
class S1_T3_full(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(S1_T3_full, self).__init__(*args, **kwargs)
        self.testcases = {
            ('', 'a'): (1, 1),
            ('', ''): (0, 0),
            ('a', 'b'): (1, 1),
            ('ab', 'ba'): (2, 1),
            ('aabc', 'aacb'): (2, 1),
            ('ca', 'abc'): (3, 2),
        }

    def test_edit_distance(self):
        dist = util.weighting.edit_dist
        for ((left, right), (exp, _)) in self.testcases.items():
            with self.subTest(
                    left = left,
                    right = right):
                self.assertEqual(exp, dist(left, right))
                self.assertEqual(exp, dist(right, left))

    def test_transposed_edit_distance(self):
        tp_dist = util.weighting.transposed_edit_dist
        for ((left, right), (_, exp)) in self.testcases.items():
            with self.subTest(
                    left = left,
                    right = right):
                self.assertEqual(exp, tp_dist(left, right))
                self.assertEqual(exp, tp_dist(right, left))

