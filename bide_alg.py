from typing import *
from collections import defaultdict
from prefixspan import PrefixSpan

T = TypeVar("T")
Entries = List[Tuple[int, int]]

def invertedindex(seqs: Iterable[Sequence[T]], entries: Entries = None) -> Mapping[T, Entries]:
    index: Mapping[T, Entries] = defaultdict(list)

    for k, seq in enumerate(seqs):
        i, lastpos = entries[k] if entries else (k, -1)

        for p, item in enumerate(seq, start=(lastpos + 1)):
            l = index[item]
            if len(l) and l[-1][0] == i:
                continue

            l.append((i, p))

    return index


def nextentries(data: Sequence[Sequence[T]], entries: Entries) -> Mapping[T, Entries]:
    return invertedindex(
        (data[i][lastpos + 1:] for i, lastpos in entries),
        entries
    )
class bide_alg:
    
    def __init__(self, db, minsup, minlen, maxlen):
        
        self._db = db
        self.minsup = minsup
        self.minlen = minlen
        self.maxlen = maxlen
        self._results = [] # type: Any
    
    def __reversescan(self, db, patt, matches, check_type):
        
        # db: complete database
        # patt: the current pattern
        # matches: a list of tuples (row_index, the index of the last element of patt within db[row_index])
        def islocalclosed(previtem):
            closeditems = set()
            
            for k, (i, endpos) in enumerate(matches):
                localitems = set()
                
                for startpos in range(endpos-1, -1, -1):
                    item = db[i][startpos]
                    
                    if item == previtem:
                        matches[k] = (i, startpos)
                        break
                    
                    localitems.add(item)
                
                # first run: add elements of localitems to closeditems
                # after first run: start intersection
                (closeditems.update if k==0 else closeditems.intersection_update)(localitems)
                
            return len(closeditems) > 0
            
        check = True if check_type == 'closed' else False
        for previtem in reversed(patt[:-1]):
            
            if islocalclosed(previtem):
                check = False if check_type == 'closed' else True
                break
                
        return check
        
    def isclosed(self, db, patt, matches):
        
        return self.__reversescan(db, [None, *patt, None], [(i, len(db[i])) for i, _ in matches], 'closed')

    
    def canclosedprune(self, db, patt, matches):
        
        return self.__reversescan(db, [None, *patt], matches[:], 'prune')
        
    
    def bide_frequent_rec(self, patt, matches):
        
        # if pattern's length is greater than minimum length, consider whether it should be recorded
        if len(patt) >= self.minlen:
            
            sup = len(matches)
            # if pattern's support < minsup, stop
            if sup < self.minsup:
                return None
            # if pattern is closed, record the pattern and its support
            if self.isclosed(self._db, patt, matches):
                self._results.append((patt, sup))
                
        # if pattern's length is greater than maximum length, stop recurssion
        if len(patt) == self.maxlen:
            return None
            
        # find the following items
        occurs = nextentries(self._db, matches)
        for newitem, newmatches in occurs.items():
            # set the new pattern
            newpatt = patt + [newitem]
                
            # can we stop pruning the new pattern
            if self.canclosedprune(self._db, newpatt, newmatches):
                continue
            self.bide_frequent_rec(newpatt, newmatches)
    
    def _mine(self):
        # type: (Callable[[Pattern, Matches], None]) -> Any
        self._results.clear()

        self.bide_frequent_rec([], [(i, -1) for i in range(len(self._db))])    
