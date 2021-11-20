#coding=utf8
#负责文件操作相关
import os
import os.path
import shutil
import xml_etree
from xml.etree import ElementTree as ET

#删除文件,文件夹
def remove_files(files):
	is_file = os.path.isfile(files)	
	if is_file:
		os.remove(files)
 	else:
		shutil.rmtree(files)

#创建文件夹，文件上一级目录
def makeDirs(dirs,isfile):
	if isfile:
		fileDirs = os.path.split(dirs)
		if not os.path.exists(fileDirs[0]):
			os.makedirs(fileDirs[0])
	else:
		if not os.path.exists(dirs):
			os.makedirs(dirs)

#复制文件,文件夹
def copy_files(_from,_to):
	is_file = os.path.isfile(_from)	
	if is_file:
		print "copying file: "+_from+" to "+_to
		makeDirs(_to,is_file)
		shutil.copyfile(_from,_to)
 	else:
		print "copying dirs: "+ _from+" to "+_to
		shutil.copytree(_from,_to,True)


#返回父目录
def getParentsDir(curDir):
	parents_path = "%s" % (os.path.dirname(curDir))
	return parents_path

#返回脚本目录
def getScriptDir():
	file_path = os.path.realpath(__file__)
	return getParentsDir(file_path)

#设置并返回SDK主目录
def getCurDir():
	global base_path 
	base_path = getParentsDir(getScriptDir())	
	return base_path 

#返回工作目录路径
def getBuildDir():
	build_path = os.path.join(base_path,"build")
	return build_path

#返回工作目录
def getWorkingDir():
	work_path = os.path.join(getBuildDir(),"work")
	return work_path

#返回工具目录
def getToolsDir():
	tools_path = os.path.join(base_path,"tools")
	return tools_path#返回工具目录

#返回配置文件路径
def getSrcDir():
	src_path = os.path.join(getBuildDir(),"src")
	return src_path

#返回渠道包文件路径
def getPackagesDir():
	pack_path = os.path.join(getBuildDir(),"packages")
	return pack_path

#检测文件路径
def checkAllPath():
	print "X-SDK: checking all paths....."

#检测文件第一层目录下的文件路径
#['F:\\python\\XX_SDK\\lib', 'F:\\python\\XX_SDK\\packages', 'F:\\python\\XX_SDK\\pack_debug.bat', 'F:\\python\\XX_SDK\\script', 'F:\\python\\XX_SDK\\tools', 'F:\\python\\XX_SDK\\workspace']
def travailDir(dir_path):
	files_list = os.listdir(dir_path)
	for i in range(0,len(files_list)):
		files_list[i] = os.path.join(dir_path,files_list[i])
	return files_list

#获取需要接入SDK信息
def getCurChannel():
	src_path = getSrcDir()
	channel_list,external_list = xml_etree.getCurChannels(os.path.join(src_path,"config.xml"))
	return channel_list,external_list

#清空工作目录
def clearWorkspace():
	print "X-SDK: Workspace clearing...... "
	work_dir = getWorkingDir()
	is_exists = os.path.exists(work_dir)
	if not is_exists:
		print "X-SDK: making workspace path..."
		os.mkdir(work_dir)
	else:
		files = os.listdir(work_dir)
		if len(files)>0:
			for fname in files:
				remove_files(os.path.join(target_path,fname))

#清空工作目录某个文件
def clearWorkspace(files_name):
	print "X-SDK: workspace:",files_name,"clearing...... "
	file_dir = os.path.join(getWorkingDir(),files_name)
	is_exists = os.path.exists(file_dir)
	if is_exists:
		#print file_dir," is not exists!!"
		remove_files(file_dir)
				
def unpackApk(apkDir,target_path):
	print "X-SDK: apk package unpacking...."
	cmd = "apktool.bat d -f %s %s" % (apkDir,target_path)
	error = os.system(cmd)
	if error != 0:
		print "Error: unpack fail!!"
		os._exit(1)
	else:
		print "X-SDK: unpack apk package success!!"
		return error

#dex转smail
def dexSmali(dexDir,smaliDir):
	print "X-SDK:",dexDir,"decompiling......"
	cmd = "java -jar baksmali-1.4.2.jar -o %s %s" %(smaliDir,dexDir)
	error = os.system(cmd)
	if error != 0:
		print "Error:classes.dex decompile fail!!"
		os._exit(1)
	else:
		print "X-SDK:",dexDir,"decompiling success!!"
		return error

#复制资源
def copyRes(_from,_to):
	print "X-SDK: Resource copying......"
	strlen = len(_from)
	for root, dirs, files in os.walk(_from):
		for res_dir in dirs:
			path = root[strlen:]
			print "copying sdk dirs: "+ os.path.join(root,res_dir)+" to "+ _to + path + "/"+ res_dir
			dir_name = os.path.join(root,res_dir)
			dir_name_to = _to+path+"/"+res_dir
			is_exists = os.path.exists(dir_name_to)
			if not is_exists:
				print "makedirs "+dir_name_to
				os.mkdir(dir_name_to)

		for res_file in files:
			if res_file != "classes.dex":
				path = root[strlen:]
				print "copying sdk file: "+os.path.join(root,res_file)+" to "+ _to + path + "/" +res_file
				shutil.copyfile(os.path.join(root,res_file),_to+path+"/"+res_file)
	return 	0	

#重新编译R文件
def reCompileRes(_from,_to,smaliDir):
	print "X-SDK: resource file copy to temp......"
	resDir = os.path.join(_from,"res")
	manifestDir =  os.path.join(_from,"AndroidManifest.xml")

	targetManifestDir= os.path.join(_to,"AndroidManifest.xml")
	targetResPath = os.path.join(_to,"res")

	dexDir = os.path.join(_to,"classes.dex")

	#复制资源
	copy_files(resDir,targetResPath)
	copy_files(manifestDir,targetManifestDir)
	print "--------------------------------------"
	print "X-SDK: resource recompiling......"
	genPath = os.path.join(_to,"gen")
	if not os.path.exists(genPath):
		os.mkdir(genPath)
	#反编译成R文件
	cmd = "aapt p -f -m -J %s -S %s -I %s -M %s" % (genPath,targetResPath,"android.jar",targetManifestDir)
	error = os.system(cmd)
	if error != 0:
		print "X-SDK: Resource recompile fail!!"
		os._exit(1)
	else:
		rPath = findFile(genPath,"R.java")
		#R.java转class
		javaToClass(rPath)
		#class转dex
		classToDex(dexDir,genPath)
		#dex转smail并合并到smali文件中去
		dexSmali(dexDir,smaliDir)
		print "X-SDK: resource recompile success!!"
		return error

#查找第一个该名字的子文件
def findFile(fileDir,file_name):
	for root, dirs, files in os.walk(fileDir):
		for fname in files:
			if fname == file_name:
				return os.path.join(root,fname)
	print "cant not find",file_name,"from",fileDir

#编译java成class
def javaToClass(rDir):
	print "X-SDK: class files craeating ......"
	cmd = "javac -source 1.6 -target 1.6 %s" %(rDir)
	error = os.system(cmd)
	if error != 0:
		print "Resource recompile(javaToClass) fail!!"
		os._exit(1)
	else:
		print "X-SDK: class files craeating success!!"
		return error

#编译class成dex
def classToDex(target_path,genPath):
	print "X-SDK: dex files craeating ......"
	cmd = "dx --dex --output=%s %s" %(target_path,genPath)
	error = os.system(cmd)
	if error != 0:
		print "Resource recompile(classToDex) fail!!"
		os._exit(1)
	else:
		print "X-SDK: dex files craeating success!!!"
		return error

#重新封包
def repackToApk(source_path):
	print "X-SDK: apk repacking ......"
	cmd = "apktool.bat b %s" %(source_path)
	error = os.system(cmd)
	if error != 0:
		print "X-SDK: apk repacking fail!!"
		os._exit(1)
	else:
		print "X-SDK: apk repacking success!!!"
		return error

#重新封包
def sign(apkDir,channel):
	print "X-SDK: apk signing ......"
	apk = os.path.join(apkDir,"dist/temp.apk")
	packDir = os.path.join(getPackagesDir(),channel['name']+"/signed/temp.apk")
	makeDirs(packDir,True)
	cmd ="jarsigner -verbose -keystore %s -storepass %s -signedjar %s -digestalg SHA1 -sigalg MD5withRSA %s %s" %(channel['keyStoreDir'],channel['keyStore_key'],packDir,apk,channel['debugkey'])
	#jarsigner -verbose -keystore F:\python\XX_SDK\lib\keyStore/mwmj-sign-key.keystore -storepass xxg5200wan -signedjar F:\python\XX_SDK\packages\pj/temp.apk -digestalg SHA1 -sigalg MD5withRSA F:\python\XX_SDK\workspace\pj\unpacked\dist/temp.apk mwmj
	error = os.system(cmd)
	if error != 0:
		print "X-SDK: apk signing fail!!"
		os._exit(1)
	else:
		print "X-SDK: apk signing success!!!"
		return error

#对齐Apk资源
def alignRes(sourceDir,alignDir):
	print "X-SDK: apk Res aligning ......"
	makeDirs(alignDir,True)
	cmd ="zipalign -f 4 %s %s" %(sourceDir,alignDir)
	error = os.system(cmd)
	if error != 0:
		print "X-SDK: Res aligning fail!!"
		os._exit(1)
	else:
		print "X-SDK: apk Res aligning success!!!"
		return error

