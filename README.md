<h1>Bide algorithm</h1>
Implement Bide algorithm for searching closed frequent sequences


Example
---------------------------
Import
```
from bide_alg import *
```
Given data as follows, each element is a sequence. 
```
db = [
    [0, 1, 2, 3, 4, 4],
    [1, 1, 1, 3, 4, 3],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2, 4, 3],
]
```
Execute bide algorithm to find closed frequent patterns with the minimum support greater than or equal to 2, minimum length >=2, and maximum length <=5 on db by:
```
bide_obj = bide_alg(db, 2 , 4, 5)
bide_obj._mine()
```
Show result:
```
bide_obj._results
```
```
[([1, 2], 3),
 ([1, 2, 3], 2),
 ([1, 2, 4], 2),
 ([1, 2, 2], 2),
 ([1, 3], 3),
 ([1, 3, 4], 2),
 ([1, 4], 3),
 ([1, 1, 1, 4, 3], 2)]
```


Reference
---------------------------
1. J. Wang and J. Han, "BIDE: efficient mining of frequent closed sequences," Proceedings. 20th International Conference on Data Engineering, Boston, MA, USA, 2004, pp. 79-90.
doi: 10.1109/ICDE.2004.1319986
keywords: {data mining;optimisation;search problems;pattern mining algorithm;BIDE;sequence closure checking;frequent closed sequence;bidirectional extension;search space;BackScan pruning method;Scan-Skip optimization technique;Data mining;Itemsets;Bidirectional control;Optimization methods;Pattern analysis;Computer science;Runtime;Databases;Proteins;XML},
URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1319986&isnumber=29235

2. Refer to package prefixspan, https://pypi.org/project/prefixspan/