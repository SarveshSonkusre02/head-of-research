import math

def merge_intervals(intervals):
    normalized=[]
    for item in intervals:
        if not isinstance(item,(list,tuple)) or len(item)!=2: raise ValueError('each interval must contain two endpoints')
        a,b=item
        if isinstance(a,bool) or isinstance(b,bool) or not isinstance(a,(int,float)) or not isinstance(b,(int,float)): raise ValueError('endpoints must be numeric')
        if not math.isfinite(a) or not math.isfinite(b) or a>b: raise ValueError('invalid interval endpoints')
        normalized.append([a,b])
    normalized.sort(key=lambda x:(x[0],x[1]))
    merged=[]
    for start,end in normalized:
        if not merged or start>merged[-1][1]: merged.append([start,end])
        else: merged[-1][1]=max(merged[-1][1],end)
    return merged
