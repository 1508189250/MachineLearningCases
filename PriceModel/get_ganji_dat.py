#encoding=utf-8
# author: zuojiepeng
import urllib2, re
from bs4 import *

fname = "data/iphone5.dat"
fname_clean = "data/iphone5_clean.dat"

def Str2Unicode(val, terminal_encode = "gbk"):
	return unicode(val, terminal_encode)

def Terminal2Utf8(val, terminal_encode = "gbk"):
	return val.decode(terminal_encode).encode("utf8")

def ParsePage(soup):
	print soup.h1.text#.encoding("gbk")

def GetInfo(fname):
	'''
	url = "http://bj.ganji.com/zq_apple/o%s/"
	pat = re.compile(ur"http:\\/\\/bj.ganji.com\\/shuma\\/[a-zA-Z0-9]{1,10}x.htm")
	'''
	url = "http://www.ganji.com/shoujixinghao/iphone-iphone-5/o%s/"
	f = open(fname, "w")
	for i in range(1, 55):#54
		page = url % i 
		print page
		req = urllib2.Request(page)
		c = urllib2.urlopen(req)
		soup = BeautifulSoup(c.read(), from_encoding="utf-8")
		dls = soup.find_all("dl", attrs={"class", "list_noimg"})
		for dl in dls:
			title = dl.dt.a.text.strip()
			price = dl.dt.span.i.text.strip()
			#print title.encode("gbk", "ignore"), price
			f.write((title + "|" + price + "\n").encode("utf8"))
	f.close()

# clean rule:1,ȥ���۸�λ, �ϲ����������пո� 2������1000����6000�Ĺ��� 3�����˱����г��ַ��ֵ�
# 4����������ĸȫ��תСд����ȡ[iphone5��iphone5s��iphone5c, iphone 5, iphone 5s, iphone 5c, ƻ��5, ƻ�����, ƻ����, ƻ��5c, ƻ��5s] ��������Ϊ�������ϲ�������󣬷ֱ���1,2,3��ʾiphone5��iphone5s��iphone5c��������û��ʵ�����壬ֻ��ת������ֵ���Է����㷨���������ȡ����������Ϣ������iphone5����
# 5����ȡ��ɫ��Ϣ����ɫΪ1����ɫΪ2��û��Ĭ��3(�������Ϊ�û�1ϲ����ɫ���û�2ϲ����ɫ���û�3���ں���ɫ�����������û�����, ��Ӧ�����ֲ�ͬ�Ķ���̬��)
# 6����ȡ�����С��ֱ��������ֵ���Բ���ת�������û��������Ϣ�����ݺ��ԡ�
# 7��Ŀ����ֹ��и۰�۸��ϲ��޲����˹���/�������Ժ���
def CleanData(fin, fout):
	f = open(fout, "w")
	for line in file(fin):
		line = line.lower()
		line = line.replace(" ", "")
		if Terminal2Utf8("��") in line: continue
		if "16g" not in line and "32g" not in line and "64g" not in line: continue
		memory = "64"
		if "16g" in line: memory = "16"
		elif "32g" in line: memory = "32"
		title, price = line.split("|")
		price = price.replace(Terminal2Utf8("Ԫ"), "")
		if int(price) < 1000 or int(price) > 6000: continue
		version = "1"
		if "iphone5s" in title or Terminal2Utf8("ƻ��5s") in title: version = "2"
		elif "iphone5c" in title or Terminal2Utf8("ƻ��5c") in title: version = "3"
		color = "3"
		if Terminal2Utf8("��ɫ") in title: color = "1"
		elif Terminal2Utf8("��ɫ") in title: color = "2"
		f.write(version + "|" + color + "|" + memory + "|" + price)
		#f.write(title + "|" + price)
	f.close()

def test():
	url = ur"http:\\/\\/bj.ganji.com\\/shuma\\/[a-zA-Z0-9]{1,10}x.htm"
	pat = re.compile(url)
	txt = Str2Unicode('{"url":"http:\/\/bj.ganji.com\/shuma\/698182388x.htm","title":"\u5356\u4e00\u4e2a\u5168\u65b0\u672a\u5f00\u5c01\u7684touch 4\u9ed1\u82728G\u7684","thumb_img":"http:\/\/image.ganjistatic1.com\/gjfs06\/M04\/EF\/79\/wKhxL1JX7duzc,zeAAF532EL25Q375_216-999_8-"')
	ret = pat.findall(txt)
	print ret
	for i in ret: print "### ", i.encode("gbk")
	pass

if __name__ == "__main__":
	#test()
	#GetInfo(fname)
	CleanData(fname, fname_clean)
	#GenerateUserTagMatrix(user_tag_matrix)
