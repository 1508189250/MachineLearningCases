#encoding=utf-8
# author: zuojiepeng
from decisiontree import *

def ReadData(fname):
	res = []
	i = 0
	for line in file(fname):
		item = line.split("\t")
		try:
			res += [[item[0], item[1], float(item[2].decode("utf8").encode("gbk", "ignore")), item[3], item[4], item[5], item[6]]]
		except Exception, e:
			print item[2].decode("utf8").encode("gbk", "ignore")
			continue
		if i > 100: break
		i += 1
	return res

if __name__ == "__main__":
	fname = "data/rent_house_clean.dat"
	dat = ReadData(fname)
	print GiniImpurity(dat)
	print Entropy(dat)
	dt = BuildTree(dat, ScoreF = Variance)
	#PrintTree(dt)
	DrawTree(dt, "desicion_tree.jpg")
	Prune(dt, 1.0)
	DrawTree(dt, "desicion_tree_prune.jpg")
	# 4900
	print LostFixClassify(["������", "2��1��1��", 85, "��װ��", 7, "����"], dt)
