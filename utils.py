import downloader
import finder
import random
import asyncio
import websockets
import os
import shutil
import sctr

if os.path.isfile("destination.txt"):
	dest=open("destination.txt").readlines()
else:
	dest=os.path.join(os.path.dirname(os.path.realpath(__file__)),"recieved")



async def getconf(websocket,ret,filename):
	pflag=0
	left=""
	if os.path.isfile(ret):
		s=os.stat(ret).st_size
		await websocket.send(f"--nbytes{s}")
		await websocket.send(filename)
		ccon=await websocket.recv()
		print("confirmation:",ccon)
		if ccon=="--111":
			pflag=1
		elif ccon=="--222":
			pflag=2
			left=await websocket.recv()
		elif ccon=="--000":
			print("Already Exist!!!")
		else:
			await websocket.send("--*")
	return (pflag,left)

async def send(websocket,ret):
	print("Sending...")
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
			print("finished!!!")
			file.close()
		else:
			print("Sending Stopped!!!")
	

async def resume_send(websocket,ret,left=0):
	print("Resuming...")
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
			print("finished!!!")
			file.close()
		else:
			print("Resuming Stopped!!!")
		



async def existconf(websocket,fname):
	pflag=0
	if os.path.isfile(os.path.join(dest,fname)):
		s=os.stat(os.path.join(dest,fname)).st_size
		size=await websocket.recv()	
		size=int(size)
		if size>s:
			await websocket.send(f"--upnbytes{s}")
			print("Resuming...")
			pflag=2
	else:
		await websocket.send(f"--upnbytes{0}")
		print("Receiving...")
		pflag=1

	return pflag


async def receive(websocket,fname,pflag):
	with open(os.path.join(dest,fname),"ab") as f:
	# if pflag==1:
	# 	f=open(os.path.join(dest,fname),"wb")
	# elif pflag==2:
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
			print("finished uploading!!!")
			await websocket.send("--uploaded")
		else:
			print("stopped uploading!!!")

		# f.close()
		
	



def download_preprocess(message):
	ret=""
	fname=""
	path="downloaded"
	downflag=False

	temp=message.lower().split("--2")[1]
	if temp.endswith("pdf"):
		ret=temp.strip("pdf").strip(".").strip()+".pdf"
	elif temp.endswith("mp3"):
		ret=temp.strip("mp3").strip(".").strip()+".mp3"
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





