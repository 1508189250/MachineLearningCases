#encoding=utf-8
# author: zuojiepeng

import re, math

class classifier:
	def __init__(self, GetFeatures):
		self.fc = {}
		self.cc = {}
		self.GetFeatures = GetFeatures
		self.thresholds = {}
	def SetThreshold(self, catalogue, threshold_value):
		self.thresholds[catalogue] = threshold_value
	def GetThreshold(self, catalogue):
		if catalogue not in self.thresholds: return 1.0
		return self.thresholds[catalogue]
	def InFc(self, feature, catalogue, times = 1):
		self.fc.setdefault(feature, {})
		self.fc[feature].setdefault(catalogue, 0)
		self.fc[feature][catalogue] += times
	def InCc(self, catalogue, times = 1):
		self.cc.setdefault(catalogue, 0)
		self.cc[catalogue] += times
	def FeatureCnt(self, feature, catalogue):
		if feature in self.fc and catalogue in self.fc[feature]:
			return float(self.fc[feature][catalogue])
		return 0.0
	def CatCnt(self, catalogue):
		if catalogue in self.cc:
			return float(self.cc[catalogue])
		return 0
	def TotalCnt(self):
		return sum(self.cc.values())
	#指定分类包含指定特征的条件概率: P(feature|catalogue)
	def FProb(self, feature, catalogue): 
		if self.CatCnt(catalogue) == 0: return 0
		return self.FeatureCnt(feature, catalogue) / self.CatCnt(catalogue)
	def WeightedProb(self, feature, catalogue, FProb = FProb, weight = 1.0, assumed_prop = 0.5):
		basic_prob = FProb(feature, catalogue)
		totals = sum([self.FeatureCnt(feature, cat) for cat in self.Categories()])
		return (weight * assumed_prop + totals * basic_prob) / (weight + totals)
	def Categories(self):
		return self.cc.keys()
	def Train(self, doc, catalogue):
		features = self.GetFeatures(doc)
		for f in features:
			self.InFc(f, catalogue)
		self.InCc(catalogue)
	def Classify(self, doc, default = None):
		raise NotImplementedError, "Error: Classify hasn't been implemented!"
	#feature catalogue times
	def Save(self, fname):
		f = open(fname, "w")
		for feature, cats in self.fc.iteritems():
			for cat, cnt in cats.iteritems():
				f.write(feature.encode("utf-8")  + "\t" + cat + "\t" + str(cnt) + "\n")
		f.close()
	def InitTrainingDat(self, fname):
		for line in file(fname):
			feature, catalogue, times = line.strip().split("\t")
			feature = unicode(feature, "utf8")
			self.InFc(feature, catalogue, int(times))
			self.InCc(catalogue, int(times))

class naivebayes(classifier):
	def DocProb(self, doc, catalogue):
		features = self.GetFeatures(doc)
		p = 1
		for f in features: p *= self.WeightedProb(f, catalogue, self.FProb)
		return p
	def BayesProb(self, doc, catalogue):
		#P(catalogue)
		catalogue_prop = self.CatCnt(catalogue) / self.TotalCnt()
		#P(doc|catalogue) 
		doc_prop = self.DocProb(doc, catalogue)
		#P(catalogue|doc) = P(catalogue) * P(doc|catalogue) / P(doc), here P(doc) is omitted
		return catalogue_prop * doc_prop
	def Classify(self, doc, default = "Unkown"):
		cat_probs = {}
		second_p = 0.0
		better = default
		max_p = second_p
		best = better
		for cat in self.Categories():
			cat_probs[cat] = self.DocProb(doc, cat)
			if cat_probs[cat] > max_p:
				second_p = max_p
				better = best
				max_p = cat_probs[cat]
				best = cat
			elif cat_probs[cat] > second_p:
				second_p = cat_probs[cat]
				better = cat
		if better == default: return best
		if cat_probs[better] * self.GetThreshold(best) > cat_probs[best]: return default
		return best

class fisherclassifier(classifier):
	def __init__(self, GetFeatures):
		classifier.__init__(self, GetFeatures)
		self.critical = {}
	def SetCritical(self, catalogue, val):
		self.critical[catalogue] = val
	def GetCritical(self, catalogue):
		if catalogue not in self.critical: return 0
		return self.critical[catalogue]
	def Invchi2(self, chi, df):
		m = chi / 2.0
		sum = term = math.exp(-m)
		for i in range(1, df // 2):
			term *= m / i
			sum += term
		return min(sum, 1.0)
	def CProp(self, feature, catalogue):
		clf = self.FProb(feature, catalogue)
		if clf == 0: return 0
		freq_sum = sum([self.FProb(feature, cat) for cat in self.Categories()])
		return clf / freq_sum
	def FisherProb(self, doc, catalogue):
		p = 1
		features = self.GetFeatures(doc)
		for f in features: p = self.WeightedProb(f, catalogue, self.CProp)
		f_score = -2 * math.log(p)
		return self.Invchi2(f_score, len(features) * 2)
	def Classify(self, doc, default = "Unkonwn"):
		best = default
		max_p = 0.0
		for cat in self.Categories():
			p = self.FisherProb(doc, cat)
			if p > self.GetCritical(cat) and p > max_p:
				best = cat
				max_p = p
		return best
