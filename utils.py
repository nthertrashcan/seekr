import downloader
import finder
import random
import asyncio
import websockets
import os
import shutil
import sctr


if not os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles")):
	os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles"))


dest=os.path.join(os.path.dirname(os.path.realpath(__file__)),"received")


async def getconf(websocket,ret,filename):
	pflag=0
	left=""
	if os.path.isfile(ret):
		s=os.stat(ret).st_size
		await websocket.send(f"--nbytes{s}")
		await websocket.send(filename)
		ccon=await websocket.recv()
		# print("Confirmation:",ccon)
		if ccon=="--111":
			pflag=1
		elif ccon=="--222":
			pflag=2
			left=await websocket.recv()
		elif ccon=="--000":
			print("\n[INFO] File Already Exist!!!")
		else:
			await websocket.send("--*")
	return (pflag,left)

async def send(websocket,ret):
	print("\n[INFO] Sending...")
	if(ret!=""):
		file=open(ret,'rb')
		mx=len(file.readlines())
		file.close()
		e=len(str(mx)[1:])
		if e>4:
			e=4
		nn=0
		nm=pow(10,e)
		flag=True
		while nm<mx:
			file=open(ret,"rb")
			await websocket.send(bytes(b"".join(file.readlines()[nn:nm])))
			if await websocket.recv()=="--C":
				flag=False
				break
			nn=nm
			nm+=pow(10,e)
		file.close()
		if flag:
			file=open(ret,'rb')
			await websocket.send(bytes(b"".join(file.readlines()[nn:mx])))
			await websocket.send("--received")
			print("\n[INFO] File Sent")
			file.close()
		else:
			print("\n[INFO] Stopped!!!")
	

async def resume_send(websocket,ret,left=0):
	print("\n[INFO] Resuming...")
	if ret!="":
		file=open(ret,"rb")
		mx=len(file.read())
		file.close()
		e=len(str(mx)[1:])
		if e>7:
			e=7
		left=int(left)
		nn=left
		nm=pow(10,e)
		while left>nm:
			nm+=pow(10,e)

		flag=True

		while nm<mx:
			file=open(ret,"rb")
			await websocket.send(bytes(file.read()[nn:nm]))
			if await websocket.recv()=="--C":
				flag=False
				break

			nn=nm
			nm+=pow(10,e)

		file.close()
		if flag:
			file=open(ret,'rb')
			await websocket.send(bytes(file.read()[nn:mx]))
			await websocket.send("--received")
			print("\n[INFO] File sent")
			file.close()
		else:
			print("\n[INFO] Stopped!!!")
		



async def existconf(websocket,fname):
	pflag=0
	value,file,path=scatter_existence(fname)
	if value:
		sctr.retrenc(file,path,"")
	print(dest,fname)

	if os.path.isfile(os.path.join(dest,fname)):
		s=os.stat(os.path.join(dest,fname)).st_size
		size=await websocket.recv()	
		size=int(size)
		if size>s:
			await websocket.send(f"--upnbytes{s}")
			print("\n[INFO] Resuming...")
			pflag=2
	else:
		await websocket.send(f"--upnbytes{0}")
		print("\n[INFO] Receiving...")
		pflag=1


	return (pflag,file,path)


async def receive(websocket,fname,pflag,file,path):
	f=open(os.path.join(dest,fname),"ab")
	
	flag=True
	while True:
		await websocket.send("--uploading")
		data=await websocket.recv()
		if type(data)==str:
			if data=="--X":
				break
			if data=="--C":
				flag=False
				break
		else:
			f.write(data)
	if flag:
		print("\n[INFO] Received")
		
		await websocket.send("--uploaded")
		f.close()
		if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/sctrflag.txt")):
			sf=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/sctrflag.txt"),"r")			
			if sf.read()=="1":
				path=os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/fragments")
				if file is None:
					sctr.scattenc(os.path.join(dest,fname),path,"")
				else:
					sctr.scattenc(file,path,"")

	else:
		print("\n[INFO] Stopped!!!")



def download_preprocess(message):
	ret=""
	fname=""
	path="downloaded"
	downflag=False

	temp=message[3:].lower()
	
	if temp.endswith("pdf"):
		ret=temp.replace("pdf","").strip(".").strip()+".pdf"
	elif temp.endswith("mp3"):
		ret=temp.replace("mp3","").strip(".").strip()+".mp3"
	else:
		ret=temp.strip()

	if ret.endswith(".pdf"):
		temp,fname=finder.search(ret,os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded"),[".pdf"])
		if fname=="":
			downflag=True
			path="downloaded/temp"
			ret=downloader.pdl(ret)
			fname=ret
					
		else:
			ret=temp
			
	elif ret.endswith(".mp3"):
		temp,fname=finder.search(ret,os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded"),[".mp3"])
		if fname=="":
			downflag=True
			path="downloaded/temp"
			ret=downloader.ydl(ret,mp3flag=1)
			fname=ret
		else:
			ret=temp
	else:
		if " " in ret:
			ret=ret.replace(" ","_")
		extn=[".mkv",".mp4",".webm"]
		temp,fname=finder.search(ret,os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded"),extn)
		if fname=="":
			downflag=True
			path="downloaded/temp"
			ret=downloader.ydl(ret)
			fname=ret
		else:
			if any(fname.endswith(x) for x in extn):
				ret=temp
			else:
				downflag=True
				path="downloaded/temp"
				ret=downloader.ydl(ret)
				fname=ret

	return (ret,fname,path,downflag)


def move(file):
    shutil.move(os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded/temp/{}".format(file)),os.path.join(os.path.dirname(os.path.realpath(__file__)),"downloaded/{}".format(file)))


def scatter_existence(filename):
	if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/sctrflag.txt")):
		sf=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/sctrflag.txt"),"r")
	else:
		sf=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/sctrflag.txt"),"w")
		sf.write("0")
		return (False,None,None)


	if sf.read()=="1":
		if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache")):
			files={}
			f=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"r",encoding="utf-8")
			for i in f.readlines():
				u,v=i.split("-d")
				files[u]=v

			for file in files:
				if finder.checkMatch(finder.omit(filename).lower(),finder.omit(file).lower()):
					return (True,file,files[file])
	
	return (False,None,None)





