"""Regressions for the instructor's research-summary correction."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from style_rules import framing_problems

class TeachingStyleTests(unittest.TestCase):
    def test_rejected_generic_study_conclusions(self):
        sentences=[
            'The study brings drug action back to a complete causal sequence.',
            'This experiment highlights the importance of cellular machinery.',
            'The finding provides a framework for a larger neural system.',
            'The result demonstrates a general principle of drug action.',
        ]
        for text in sentences:
            with self.subTest(text=text):self.assertTrue(framing_problems(text))

    def test_concrete_mechanisms_and_instructor_example_remain_allowed(self):
        sentences=[
            'CB1 activation reorganized actin as nearby microtubules bent.',
            'The researchers blocked ROCK, an enzyme that promotes contraction.',
            'The images follow the same neuron over several minutes, allowing us to compare its appearance before and after receptor activation and see how its structure changes over time.',
            'This study shows how a chemical acting on a receptor can produce a physical change in a neuron by triggering signals that reorganize its internal framework and alter the shape of its cell body and dendrites.',
        ]
        for text in sentences:
            with self.subTest(text=text):self.assertEqual(framing_problems(text),[])

if __name__=='__main__':unittest.main()
