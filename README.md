# Andriod-SDK-RePack
Andriod 解包接入 SDK 工具  

## 一.文件说明
	build:存放配置文件,工作目录，渠道包输出路径
	packages：渠道包输出路径
	lib：脚本文件
	tools：工具文件（不包括dx.bat,dx.bat在../adt/sdk/bulid-tools/android-xx/）
	pack_debug.bat：打包入口

## 二.工具说明
	1.dx.bat:编译，打包class成dex
		cmd = "dx --dex --output=%s %s" %(target_path,genPath)


	2.apktool:apk解包，打包
		cmd = "apktool.bat d -f %s %s" % (apkDir,target_path)
		cmd = "apktool.bat b %s" %(source_path)

	3.baksmali-1.4.2：反编译dex文件成smali文件（代码）
		cmd = "java -jar baksmali-1.4.2.jar -o %s %s" %(smaliDir,dexDir)


	4.aapt，android.jar：重新编译资源，生成R.java 
		cmd = "aapt p -f -m -J %s -S %s -I %s -M %s" %(genPath,targetResPath,"android.jar",targetManifestDir)

	5.javac -source 1.6 -target 1.6 ../R.java 编译java生成class

	6.cmd ="jarsigner -verbose -keystore %s -storepass %s -signedjar %s -digestalg SHA1 -sigalg MD5withRSA %s %s" %(keyStore,channel['keyStore_key'],packDir,apk,channel['debugkey']) apk签名

	7.zipalign.exe 资源对齐工具
		cmd ="zipalign -v 4 %s %s" %(sourceApk,alignedApk)

## 三.流程
	1.配置文件配置相关信息
	2.在工作目录创建相应sdk工作目录
	2.备份母包，解包到/upacked文件夹，复制/upacked到/decompile
	3.备份sdk
	4.反编译sdk的classes.dex文件成smali合并到/decompile/smali
	5.复制sdk资源到/decompile
	6.重新编译资源（res，manifest.xml）....
	7.封包
	8.签名
	9.对齐资源

## 四.待优化
	1.部分xml资源合并，目前需要手动合并（string.xml,AndroidManifest.xml等）
-------------------------------------------------------