# -*- coding:utf-8 -*-
from xml.etree import ElementTree as ET

def setConfigure(config_dir):
	global root
	try:  
	    tree = ET.parse(config_dir) #打开xml文档  
	    root = tree.getroot() #获得root节点  
	except Exception, e:  
	    print "Error: cannot parse file: config.xml."  
	    return -1     

def getCurChannels(config_dir):
	#如果不存在则读取配置文件
	setConfigure(config_dir)

	channels = root.find("channels").findall("channel") #找到channels节点下的所有channel节点
	channels_list = []
	for oneper in channels:
		temp_list = {}
		for child in oneper.getchildren():
			temp_list[child.get("name")] = child.text
		channels_list.append(temp_list)

	external = root.find("external") #apk
	external_list = {}
	for child in external.getchildren():
			external_list[child.get("name")] = child.text
				

	return channels_list,external_list


def getApkFlie(config_dir):
	#如果不存在则读取配置文件
	setConfigure(config_dir)

	apk = root.find("apk") #apk
	apk_name =""
	for child in apk.getchildren():
			if child.get("name") == "apk":
				apk_name = child.text
	return apk_name