#coding=utf8
import os
import shutil
import file_utils

def checkWorkingEnviron():
	#检测Java环境
	print "checking java environ..."
	error = os.system("java -version")
	if error == 0:
		print u"JAVA environ is OK!"
	else:
		print u"Error:Java version bit is not the same with Python!"
		os._exit(1)


def main():
	#环境检测和设置工作目录
	print "**************X-SDK*******************"
	checkWorkingEnviron()
	print "--------------------------------------"
	#获取打包工具根目录
	base_path = file_utils.getCurDir()

	#进入工具箱环境
	os.chdir(file_utils.getToolsDir())
	print "Workspace:",file_utils.getToolsDir()
	print "--------------------------------------"

	#检查打包文件，读取渠道信息
	channels,external_list = file_utils.getCurChannel()
	#设置
	global APK_DIR
	global SDK_DIR
	global KEY_STORE_DIR

	APK_DIR = external_list['apkDir']
	SDK_DIR = external_list['sdkDir']
	KEY_STORE_DIR = external_list['keyStoreDir']

	if channels != None and len(channels)<0:
		print "Error:not sdk files info!!"
		os._exit(1)

	sdkIndex = 1 
	for channel in channels:
		print "--------------------------------------"

		is_exsist = os.path.exists(os.path.join(APK_DIR,channel["apkName"]))
		if not is_exsist:
			print "Error:",APK_DIR,channel["apkName"],"is not exists!!!"
			os._exit(1)


		sdk_dir = os.path.join(SDK_DIR,channel["name"]) 
		is_exsist = os.path.exists(sdk_dir)
		if not is_exsist:
			print "Error:",channel["name"],"is not exists!!!"
			os._exit(1)
		else:
			print "X-SDK: doPacking NO.%d sdk....." %(sdkIndex)
			channel["apkDir"] = os.path.join(APK_DIR,channel["apkName"])
			channel["sdkDir"] = sdk_dir
			channel["keyStoreDir"] = os.path.join(KEY_STORE_DIR,channel["keyStore"])
			ret = doPack(channel)
			sdkIndex += 1

	print "X-SDK: PACKE SUCCESS:%d PACKE FAIL:%d" %(sdkIndex-1,len(channels)-sdkIndex+1)  
	print "**************PACK FINISH!*******************"

def doPack(channel):
	print "X-SDK:",channel["name"],'sdk doPacking...'
	file_utils.clearWorkspace(channel["name"])
	#创建相应的工作目录
	workDir = os.path.join(file_utils.getWorkingDir(),channel["name"])
	#备份母包
	to_path = os.path.join(workDir,"temp.apk")
	file_utils.copy_files(channel["apkDir"],to_path)
	print "--------------------------------------"
	#解包
	unpackDir = os.path.join(workDir,"unpacked")
	file_utils.unpackApk(to_path,unpackDir)
	print "--------------------------------------"
	decompile_path = os.path.join(workDir,"decompile")
	file_utils.copy_files(unpackDir,decompile_path)
	#备份sdk
	# sdk_path = os.path.join(channel["sdkDir"],"sdks")
	# sdkSourceDir = os.path.join(sdk_path,channel["name"]) 
	sdk_dir = os.path.join(workDir,channel["name"])
	file_utils.copy_files(channel["sdkDir"],sdk_dir)
	print "--------------------------------------"
	#解压classes.dex合并到解压包目录
	smaliDir = os.path.join(decompile_path,"smali")
	dexDir = os.path.join(sdk_dir,"classes.dex")
	file_utils.dexSmali(dexDir,smaliDir)
	print "--------------------------------------"
	#合并资源
	ret = file_utils.copyRes(sdk_dir,decompile_path)
	if ret == 0:
		print "X-SDK: Resource copy success!!"
	else:
		print "X-SDK: Resource copy fail!!"
		os._exit(1)
	print "--------------------------------------"
	#重新编译资源
	tempDir = os.path.join(workDir,"temp")
	ret = file_utils.reCompileRes(decompile_path,tempDir,smaliDir)
	#封包
	if ret == 0:
		file_utils.repackToApk(decompile_path)
	print "--------------------------------------"
	#重新签名
	file_utils.sign(decompile_path,channel)
	print "--------------------------------------"
	#对齐资源

	packDir = os.path.join(file_utils.getPackagesDir(),channel['name']+"/signed/temp.apk")
	aligned = os.path.join(file_utils.getPackagesDir(),channel['name']+"/aligned/temp.apk")
	file_utils.alignRes(packDir,aligned)
	print "--------------------------------------"
	print "X-SDK: %s doPack success!!!" %(channel['name'])
	print "--------------------------------------"
	return 0

