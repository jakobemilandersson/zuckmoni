import matlab.engine
import os
import cPickle as pickle
import time
import re

list = []
list.append([])
i = 0

for subdir, dirs, files in os.walk('./lists3'):
    for file in files:
		s = open(os.path.join(subdir, file), "rb")
		try:
			list[i] = pickle.load(s)
		except:
			continue
		list.append([])
		i+=1
		print i
		s.close()
	


#test#	
eng = matlab.engine.connect_matlab()

l = list
l2 = []
name = l[0][0][0]

for n in range(0, len(list)-1):
	for i in range(0, len(list[n])):
	
		#gor om , till . waow
		for j in range(0, len(l[n][i])):
			l[n][i][1] = re.sub('[^0-9]+', '.', l[n][i][1])	
	
	l2.append(l[n])

l3 = [[]]

#for n in range(0, len(l2)):
	#l3[n] =  l2[n][:(len(l2)-101)]
	

print (l2[5])
#eng.calc(l2)

#test#