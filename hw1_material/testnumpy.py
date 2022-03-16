import numpy as np

# one = np.array([[1,2,3],[3,4,5],[6,7,8]])
# two = np.array([[11,22,33],[33,44,55],[66,77,88]])
# aa = np.array([[111,222,333],[333,444,555],[666,777,888]])
# three = np.array([one,two ,aa])
# test = np.array([[1,2,3],[2,4,5]])
# print(np.shape(test))

# # cropone = one[1:,1:]
# # print(cropone)
# print(three)
# print(np.max(three))

a = []
bb = []
bb2 =[]
b =[1,2]
c = [3,4]
a.append(b)
a.append(c)
a_array = np.array(a)
bb.append(a_array)
bb.append(a_array)

bb2.append(bb[0]*2)
bb2.append(bb[1]*2)
bbb = bb2+bb
bbbarray = np.array(bbb)
bbbarray.resize(8,2)
print(bbb)
print(bbbarray)
print(np.unique(bbbarray,axis=0))
