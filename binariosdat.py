import pickle 
import numpy as np
# x = pickle.load(open('s01.dat', 'rb'),  encoding='iso-8859-1')
# print("\n",x)
# file=open("C:/Users/duvan/Dropbox/Practica/DataSet/datasetdata.txt","w")
# for i in range(len(x)):
# 	listToStr = ' '.join([str(elem) for elem in x])
# 	file.write("\n"+listToStr)
# file.close()
# x = pickle.load(open('s01.dat', 'rb',encoding='utf-8'))
x = pickle.load(open('../s01.dat', 'rb'),encoding='iso-8859-1')
f='../s01.dat'
file=open("C:/Users/duvan/Dropbox/Tesis/Zcode/DataSetDat.txt","w")
with open(f, 'rb') as f:
	# content = pickle.load(f, encoding='utf-8')
	content = pickle.load(f, encoding='iso-8859-1')
	data = content['data']
	labels = content['labels']
# Para ver los datos
print(content)
print(len(data.shape))
print(data.shape)
print(len(labels.shape))
print(labels.shape)
file.write("\n"+"El documento cuenta con ("+str(len(content))+") listas:")

print("\n","La lista etiquetas que tiene",len(labels),"etiquetas:")
for i in range(len(labels)):
	listToStr = ' '.join([str(elem) for elem in labels[i]])
	print("\n",listToStr)

print("\n","La lista datos tiene",len(data),"listas en total y cada una de estas listas tiene",len(data[0]),"listas con datos dentro de estas:")
# print("\n",data[0],"___________________________")
print("\n","Listas de los datos totales:")
for i in range(len(data)):
	listToStr = ' '.join([str(elem) for elem in data[i]])
	print(listToStr)
print("\n","Listas de datos del primer array:")
for elem in data[0]:
	print(elem)

file.close()