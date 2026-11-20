from benchmarks.task03.grader import grade
from benchmarks.task03.solution import merge_intervals

def test_grader_passes(): assert grade(merge_intervals)['status']=='PASS'
def test_touching_intervals_merge(): assert merge_intervals([[1,3],[3,4]])==[[1,4]]
def test_input_not_mutated(): x=[[3,4],[1,2]]; before=[i[:] for i in x]; merge_intervals(x); assert x==before

def test_grader_rejects_constant_candidate():
    def bad_candidate(intervals):
        return []
    report = grade(bad_candidate)
    assert report['status'] == 'FAIL'
