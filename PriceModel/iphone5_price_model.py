#encoding=utf-8
# author: zuojiepeng
from numpredict import *

def GetData(fname):
	rows = []
	for line in file(fname):
		line = line.strip()
		version, color, memory, price = line.split("|")
		rows.append({"input":(float(version), float(color), float(memory)), "result":float(price)})
	return rows

if __name__ == "__main__":
	# iphone5 16g
	vec = [1, 3, 16]
	data = GetData("data/iphone5_clean.dat")
	prices = [dat["result"] for dat in data]
	min_price = min(prices)
	max_price = max(prices)
	print "Min Price: " + str(min_price) 
	print "Max Price: " + str(max_price)

	# KNN���м۸�Ԥ��
	print KnnEstimate(data, vec)
	print WeightedKnn(data, vec)

	# ������֤��knn�ͼ�Ȩknn��Ԥ������
	#print CrossValidate(KnnEstimate, data)
	#print CrossValidate(WeightedKnn, data)

	# �����ۼƸ��ʷֲ�ͼ
	#CumulativeGraph(data, vec, max_price, step = 10, k = 10)
	# ���Ƽ۸���ʷֲ�ͼ
	#ProbabilityGraph(data, vec, max_price, step = 10, k = 10)

	# ͨ���Ż��㷨Ѱ�������������
	'''
	weight_domain = [(1, 10), (1, 10), (1, 2)]
	CostF = CreateCostFunction(KnnEstimate, data)
	scale = AnnealingOptimize(weight_domain, CostF, step = 2)
	print scale
	'''
	# ģ���˻�̫����������������Ӻ�д���ڴ�����
	scale = [6, 1, 1]
	# ��һ�����ݼ������Զ���Ӱ�첻ͬ������ֵ������Ӧ����
	sdata = ReScale(data, scale)
	vec = map(lambda x,y:x*y, vec, scale)
	print data[0]
	print sdata[0]
	# KNN���м۸�Ԥ��
	print KnnEstimate(sdata, vec)
	print WeightedKnn(data, vec)
	# �����ۼƸ��ʷֲ�ͼ
	CumulativeGraph(sdata, vec, max_price, step = 10, k = 10)
	# ���Ƽ۸���ʷֲ�ͼ
	ProbabilityGraph(sdata, vec, max_price, step = 10, k = 10)

