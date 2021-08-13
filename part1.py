#Thomas Patasnis AM: 3318


import sys
import time
import ast
import math


def createData(transactions_filename):
	transactions_file = open(transactions_filename, 'r')
	transactions = []
	for line in transactions_file:
		array = ast.literal_eval(line)
		transactions.append(array)
	transactions_file.close()
	return transactions




def createQueries(queries_filename):
	queries_file = open(queries_filename, 'r')
	queries = []
	for line in queries_file:
		array = ast.literal_eval(line)
		queries.append(array)
	queries_file.close()
	return queries





def naive(transactions,query):
	results = []
	for i in range(len(transactions)):
		flag = False
		for item in query:
			if(item not in transactions[i]):
				flag = True
		if(not flag):
			results.append(i)
	return results





def createBitMap(array):
	signature = 0
	visited = []
	for num in array:
		if(num not in visited):
			signature += 2**num
		visited.append(num)
	return signature



def createSigFile(transactions):
	output = open('sigfile.txt', 'w')
	sigFile = []
	for i in transactions:
		signature = createBitMap(i)
		sigFile.append(signature)
		output.write(str(signature)+"\n")
	return sigFile




def exactSignatureFile(sigFile,q_sig):
	results = []
	for i in range(len(sigFile)):
		t_sig = sigFile[i]
		if(t_sig & q_sig == q_sig):
			results.append(i)
	return results





def createInvertedIndex(transactions):
	inv_index = {}
	for i in range(len(transactions)):
		items = transactions[i]
		for item in items:
			if item not in inv_index:
				inv_index[item] = [i]
			else:
				if(i > inv_index[item][-1]):
					inv_index[item].append(i)
	return inv_index





def sortDict(dictionary):
    sort_tuple = sorted(dictionary.items(), key=lambda x: x[0])
    sort_dict = dict(sort_tuple)
    return sort_dict



def createBitSliceSigFile(sorted_inv_index):
	output = open('bitslice.txt', 'w')
	bitSlice = {}
	for key in sorted_inv_index:
		signature = createBitMap(sorted_inv_index[key])
		bitSlice[key] = signature
		output.write(str(key)+': '+str(signature)+"\n")
	return bitSlice







def containment_slice(query,bitSlice):
	q_bitmaps = []
	for i in query:
		q_bitmaps.append(bitSlice[i])
	q_sig = q_bitmaps[0]
	for i in range(len(q_bitmaps)):
		q_sig = q_sig & q_bitmaps[i]
	return q_sig





def exactBitSliceSignatureFile(q_sig):
	results = []
	bits = bin(q_sig)
	m = len(bits)-1
	for i in range(m):
		if(bits[i] == '1'):
			results.append(m-i)
	return sorted(results)



def writeInvertedIndex(sorted_inv_index):
	output = open('invfile.txt', 'w')
	for key in sorted_inv_index:
		output.write(str(key)+': '+str(sorted_inv_index[key])+"\n")




def merge(lst1,lst2):
	i=0
	j=0
	tomh = []
	while i<len(lst1) and j<len(lst2):
		a = lst1[i]
		b = lst2[j]
		if a < b:
			i+=1
		elif a > b:
			j+=1
		else:
			tomh.append(b)
			i+=1
			j+=1
	return tomh



def containment_Inv(query,sorted_inv_index):
	item1 = query[0]
	lst1 = sorted_inv_index[item1]
	for i in range(1,len(query)):
		item2 = query[i]
		lst2 = sorted_inv_index[item2]
		lst1 = merge(lst1,lst2)
	return lst1







def execute(transactions,method,queries,qnum):
	types = ["Naive Method","Signature File","Bitsliced Signature File","Inverted File"]
	if(method == 0):
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				query = queries[qnum]
				results = naive(transactions,query)
				break
			else:
				results = naive(transactions,query)
	elif(method==1):
		sigFile = createSigFile(transactions)
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				query = queries[qnum]
				q_sig = createBitMap(query)
				results = exactSignatureFile(sigFile,q_sig)
				break
			else:
				q_sig = createBitMap(query)
				results = exactSignatureFile(sigFile,q_sig)
	elif(method==2):
		inv_index = createInvertedIndex(transactions)
		sorted_inv_index = sortDict(inv_index)
		bitSlice = createBitSliceSigFile(sorted_inv_index)
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				query = queries[qnum]
				q_sig = containment_slice(query,bitSlice)
				results = exactBitSliceSignatureFile(q_sig)
				break
			else:
				q_sig = containment_slice(query,bitSlice)
				results = exactBitSliceSignatureFile(q_sig)
	elif(method==3):
		inv_index = createInvertedIndex(transactions)
		sorted_inv_index = sortDict(inv_index)
		writeInvertedIndex(sorted_inv_index)
		start_t = time.time()
		for query in queries:
			if(qnum!=-1):
				query = queries[qnum]
				results = containment_Inv(query,sorted_inv_index)
				break
			else:
				results = containment_Inv(query,sorted_inv_index)
	stop_t = time.time()
	total_time = stop_t - start_t
	if(qnum!=-1):
		print(types[method]+" result:\n"+str(results))
	print(types[method]+" computation time: "+str(total_time))




def main(argv):
	transactions_filename = argv[0]
	queries_filename = argv[1]
	qnum = int(argv[2])
	method = int(argv[3])
	transactions = createData(transactions_filename)
	queries = createQueries(queries_filename)
	if(qnum==-1):
		if method == -1:
			execute(transactions,0,queries,qnum)
			execute(transactions,1,queries,qnum)
			execute(transactions,2,queries,qnum)
			execute(transactions,3,queries,qnum)
		else:
			execute(transactions,method,queries,qnum)				
	else:
		query = queries[qnum]
		if method == -1:
			execute(transactions,0,queries,qnum)
			execute(transactions,1,queries,qnum)
			execute(transactions,2,queries,qnum)
			execute(transactions,3,queries,qnum)
		else:
			execute(transactions,method,queries,qnum)
		




if __name__ == '__main__':
	main(sys.argv[1:])