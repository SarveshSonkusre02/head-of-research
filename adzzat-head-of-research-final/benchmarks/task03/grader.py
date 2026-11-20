def grade(merge_intervals):
    cases=[([],[]),([[1,2]],[[1,2]]),([[1,4],[2,3]],[[1,4]]),([[5,7],[1,3],[2,6]],[[1,7]]),([[1,3],[3,5]],[[1,5]]),([[-5,-1],[-3,0]], [[-5,0]]),([[1,2],[4,5]],[[1,2],[4,5]])]
    checks={}
    for i,(given,expected) in enumerate(cases):
        original=[x[:] for x in given]
        try: actual=merge_intervals(given)
        except Exception: actual=None
        checks[f'case_{i+1}']=actual==expected and given==original
    invalid=[[[2,1]],[[1]],[[1,2,3]],[['1',2]],[[float('nan'),3]],[[0,float('inf')]]]
    for i,given in enumerate(invalid):
        try: merge_intervals(given); rejected=False
        except ValueError: rejected=True
        checks[f'invalid_{i+1}']=rejected
    passed=sum(checks.values()); total=len(checks)
    return {'status':'PASS' if passed==total else 'FAIL','passed':passed,'total':total,'score_percent':round(100*passed/total,1),'checks':checks}
