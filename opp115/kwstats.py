from common import *; from pipeline import lem, clean
import collections, pickle
d=load_all(); dev,test=split(d)
# lemmatize dev segments once and cache
L=[( " "+" ".join(lem(clean(s)))+" ", g) for _,segs,gold in dev for s,g in zip(segs,gold)]
pickle.dump(L,open("dev_lem.pkl","wb"))
print(len(L),"dev segments")
