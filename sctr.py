
import os
import subprocess as sp
from prettytable import PrettyTable
import sys
from cryptography.fernet import Fernet
import hashlib
from sys import exit

extt=[".pdf",".mp3",".wav",".mp4",".mkv",".png",".jpg",".jpeg",".zip",".rar",".docx"]
emb="xasdx"
start="adding200suc07@1999"
end="complete200suc07@1999"
gaps="guessit01071999"
gape="guessit07071999"
default=""
fno=1


def initialize():
	if not os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache")):
		f=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"wb")
		f.close()
	

initialize()


def scattenc(name,path,kv):
	global fno
	if not os.path.isfile(name):
		print("\n[INFO] File not found!!!")
		return
		# exit(0)
	if kv!="":
		kv = hashlib.sha256(kv.encode()) 
		kv=kv.hexdigest() 
	key = Fernet.generate_key()
	cipher_suite = Fernet(key)
	sflag=0
	dest=""
	if path=="":
		dest=input("\n[INPUT] Enter Destination - :")
		if dest=="":
			dest=default
		else:
			if ":" not in dest:
				dest=os.path.join(os.getcwd(),dest)
				dest=dest.lower()
	else:
		dest=path
		if ":" not in dest:
			dest=os.path.join(os.getcwd(),dest)
			dest=dest.lower()
	name=name.strip()
	name=name.lower()
	pname=""

	try:
		indx=[n for n,x in enumerate(name) if x=="\\"][::-1][0]
	except:
		name=os.path.join(os.getcwd(),name)
		indx=[n for n,x in enumerate(name) if x=="\\"][::-1][0]
	pname=name[:indx]
	name=name[indx+1:]
	file=open(os.path.join(pname,name),"rb")
	siz=len(file.readlines())
	file=open(os.path.join(pname,name),"rb")
	# dflag=1
	frag=[]
	for i in file.readlines():
		frag.append(i)
	n=0
	m=0
	if os.path.isdir(dest):
		f=[]
		for r,d,fi in os.walk(dest):
			for i in fi:
				f.append(os.path.join(r,i))
		if len(f)==0:
			for i in range(0,10):
				fl=open(f"{dest}/{i}","wb")

			print("\n[INFO] Empty folder!!!, Creating dumming files...")
			for r,d,fi in os.walk(dest):
				for i in fi:
					f.append(os.path.join(r,i))

		if len(f)>0:
			flag=0
			if len(frag)<len(f):
				file=open(os.path.join(r,f[0]),"rb")
				flag=1
				
				for i in file.readlines():
					if bytes(emb,"utf-8") in i:
						if str(kv)!="":
							key=str(i).split(emb)[1].split(str(kv))[1].encode()
						else:
							key=str(i).split(emb)[1].encode()
						cipher_suite = Fernet(key)
						decoded_text = cipher_suite.decrypt(str(i).split(emb)[2][:len(str(i).split(emb)[2])-3].encode())
						if bytes(name+start,"utf-8") in decoded_text:
							flag=0
							print(name+start)
							print("\n[INFO] {} already exist!!!".format(name))
							break
				if flag==1:
					print("\n[INFO] Scattering...")
					file=open(f[0],"ab")
					encoded_text = cipher_suite.encrypt(bytes(name+start,"utf-8"))
					file.write(b"\n"+bytes(emb,"utf-8")+bytes(kv,"utf-8")+key+bytes(emb,"utf-8")+encoded_text+b"\n")
					for j in frag:
						encoded_text = cipher_suite.encrypt(j)
						file.write(b"\n"+encoded_text+b"\n")
					encoded_text=cipher_suite.encrypt(bytes(name+end,"utf-8"))
					file.write(b"\n"+bytes(emb,"utf-8")+bytes(kv,"utf-8")+key+bytes(emb,"utf-8")+encoded_text+b"\n")
				f=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"ab")
				f.write(bytes(os.getcwd().lower()+"\\"+name+" -d "+dest+"\n","utf-8"))
				print("\n[INFO] Completed")
				os.remove("{}".format(os.path.join(pname,name)))
				flag=0	
			else:
				showf=0
				nl=len(frag)
				nl=int(nl/len(f))
				flag=1
				eflag=0
				for l,i in enumerate(f):
					file=open(i,"rb")
					for j in file.readlines():
						try:
							if bytes(emb,"utf-8") in j:
								if str(kv)!="":
									key=str(j).split(emb)[1].split(str(kv))[1].encode()
								else:
									key=str(j).split(emb)[1].encode()
								cipher_suite = Fernet(key)
								decoded_text = cipher_suite.decrypt(str(j).split(emb)[2][:len(str(j).split(emb)[2])-3].encode())
								if bytes(name+start,"utf-8") in decoded_text:
									flag=0
									break
						except:
							flag=0
					if flag==1:
						if showf==0:
							# if rflag==1:
							# 	print("\n[{}] - {}".format(fno,name))
							# 	fno+=1
							# else:
							print("\n[INFO] Scattering...")
							showf=1
						file=open(i,"ab")
						encoded_text = cipher_suite.encrypt(bytes(name+start,"utf-8"))
						e_nu = cipher_suite.encrypt(bytes(str(l+1)+"-"+str(len(f))+"|"+str(f),"utf-8"))
						file.write(b"\n"+bytes(emb,"utf-8")+bytes(kv,"utf-8")+key+bytes(emb,"utf-8")+encoded_text+b"\n"+e_nu+b"\n")	
						if int(n)<=len(frag):
							for j in frag[n:n+nl]:
								encoded_text = cipher_suite.encrypt(j)
								file.write(b"\n"+encoded_text+b"\n")
							n+=nl
						if l!=len(f)-1:
							encoded_text=cipher_suite.encrypt(bytes(name+end,"utf-8"))
							file.write(b"\n"+bytes(emb,"utf-8")+bytes(kv,"utf-8")+key+bytes(emb,"utf-8")+encoded_text+b"\n")
						
				if flag==1:
					file=open(f[len(f)-1],"ab")
					for l,j in enumerate(frag[n:]):
						encoded_text = cipher_suite.encrypt(j)
						file.write(b"\n"+encoded_text+b"\n")
					encoded_text=cipher_suite.encrypt(bytes(name+end,"utf-8"))
					file.write(b"\n"+bytes(emb,"utf-8")+bytes(kv,"utf-8")+key+bytes(emb,"utf-8")+encoded_text+b"\n")
					f=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"ab")
					f.write(bytes(os.getcwd().lower()+"\\"+name+" -d "+dest+"\n","utf-8"))
					print("\n[INFO] Completed")
					os.remove("{}".format(os.path.join(pname,name)))
				elif flag==0:
					print("\n[INFO] {} already exist!!!".format(name))
	else:
		print("\n[INFO] Path doesn't exist!!!")



def table(t):
	print("\n[INFO]\n")
	print("--------------------------------------")
	print("| Missing Fragment\t|\tFile |")
	print("--------------------------------------")

	for key,value in t.items():
		print(f"| {key}\t\t\t|\t{value} |")



def retrenc(name,path,kv):
	if kv!="":
		kv = hashlib.sha256(kv.encode()) 
		kv=kv.hexdigest() 

	des=path.rstrip().strip(" ")
	# if "\\" in name:
	name=name.split("\\")[len(name.split("\\"))-1].strip()
	# elif "/" in name:
		# name=name.split("/")[len(name.split("/"))-1].strip()
	print(name,des)
	# exit(0)


	exflag=0
	ext=""
	for i in extt:
		if str(des.split("\\")[len(des.split("\\"))-1]).endswith(i):
			exflag=1
			ext=i
			break
	key=b""
	flag=0
	msflag=0
	if exflag==1:
		s=0
		e=0
		# if not os.path.isfile(des):

		# 	print("\n[INFO] File doesn't exist!!!")
		# 	return
		file=open(des,"rb")
		for l,i in enumerate(file.readlines()):
			if bytes(emb,"utf-8") in i:
				try:

					if str(kv)!="":
						key=str(i).split(emb)[1].split(str(kv))[1].encode()
					else:
						key=str(i).split(emb)[1].encode()
					cipher_suite = Fernet(key)
					decoded_text = cipher_suite.decrypt(str(i).split(emb)[2][:len(str(i).split(emb)[2])-3].encode())

					if bytes(name+start,"utf-8") in decoded_text:
						s=l
					elif bytes(name+end,"utf-8") in decoded_text:
						e=l
				except:
					pass
			
		if s!=0:
			print("\n[INFO] Retrieving...",name)
			file1=open(name,"wb")
			file=open(des,"rb")
			for j in file.readlines()[s+1:e]:
				if j==b"\n":
					pass
				else:
					cipher_suite = Fernet(key)
					decoded_text = cipher_suite.decrypt(j)
					file1.write(decoded_text)
			flag=1
			file1.close()
		else:
			flag=0

	else:

		if not os.path.isdir(des):

			print("\n[INFO] Path doesn't exist!!!")
			return

		fragn={}
		f=[]
		for r,d,fi in os.walk(des):
			for i in fi:
				f.append(os.path.join(r,i))
		if len(f)==0:
			print("\n[INFO] Empty folder!!!")
			return(0)
		elif len(f)>0:
			s=0
			e=0

			for k in f:
				file=open(k,"rb")
				for l,i in enumerate(file.readlines()):
					try:
						# print(i)
						if bytes(emb,"utf-8") in i:
							if str(kv)!="":
								key=str(i).split(emb)[1].split(str(kv))[1].encode()
							else:
								key=str(i).split(emb)[1].encode()
							cipher_suite = Fernet(key)
							decoded_text = cipher_suite.decrypt(str(i).split(emb)[2][:len(str(i).split(emb)[2])-3].encode())

							
							if bytes(name+start,"utf-8") in decoded_text:
								s=l
							elif bytes(name+end,"utf-8") in decoded_text:
								e=l

					except:
						pass
				if s!=-1:
					data=[]
					try:
						file=open(k,"rb")
						v=file.readlines()[s+1]
						cipher_suite = Fernet(key)
						decoded_text = cipher_suite.decrypt(v)
						v=decoded_text.decode()
						fn=int(v.split("-")[0])
						fnt=int(v.split("-")[1].strip("\n").split("|")[0].strip("\n"))
						fl=[]
						fl=eval(v.split("|")[1])
						data.append(k)
						data.append(s)
						data.append(e)
						data.append(fnt)
						data.append(fl)

						fragn[fn]=data
					except:
						pass
				else:
					print("\n[INFO] File doesn't exist!!!")
					return(0)
			flag=1

			if len(fragn)>0:
				tmp=0
				for i in fragn:
					tmp=i
					break
				print(f"\n[INFO] Total nummber of Fragments: {fragn[tmp][3]}")
				t={}

				for i in range(1,fragn[tmp][3]+1):
					if i in fragn:
						pass
					else:
						t[i]=fragn[tmp][4][i-1]
						msflag=1
						flag=0
				if len(t)>0:
					# table(t)
					tp = PrettyTable(['Missing Fragment', 'Filename'])
					for key, val in t.items():
						tp.add_row([key+1, val])
					print("\n[INFO]")
					print(tp)
			else:
				print("\n[INFO] Empty folder!!!")
				return(0)
			if msflag==1:
				pass
			else:
				print("\n[INFO] Retrieving...",name)
				file1=open(name,"wb")
				tm=set(fragn)
				for i in tm:
					file=open(fragn[i][0],"rb")
					for j in file.readlines()[int(fragn[i][1])+2:int(fragn[i][2])]:
						if j==b"\n":
							pass
						else:
							cipher_suite = Fernet(key)
							decoded_text = cipher_suite.decrypt(j)
							file1.write(decoded_text)
				file1.close()
	if flag==1:
		print("\n[INFO] Completed")
	elif flag==0 and msflag==0:
		print("\n[INFO] File doesn't exist!!!")


def cleanenc(name,path,kv):
	if kv!="":
		kv = hashlib.sha256(kv.encode()) 
		kv=kv.hexdigest() 
	des=""
	nname=""
	fil=[]
	f=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"rb")
	for i in f.readlines():
		if name.lower() in i.decode().strip("\n").split("-d")[0].strip().lower():
			fil.append(i.decode().strip("\n"))
	fil=set(fil)
	if path=="":
		flag=0
		
		if len(fil)>1:
			fdic={}
			for l,i in enumerate(fil):
				if name in i.split("-d")[0].strip():
					if "-d" in i:
						print(l+1,"-",i.split("-d")[1].strip())
						fdic[l+1]=i.split("-d")[1].strip()	
			des=default
			for i in fil:
				if name in i.split("-d")[0].strip():
					if des in i.split("-d")[1].strip():
						nname=i
						break			
		else:
			for i in fil:
				nname=i
				des=i.split("-d")[1].strip()
		# if path=="":
		# 	path=input("\n[INPUT] Enter destination -: ")
		if ":" not in path:
			des=os.getcwd()+"\\"+path
		else:
			des=path
	else:
		des=""
		if ":" not in path:
			des=os.getcwd()+"\\"+path
		else:
			des=path

		for i in fil:
			if name.lower() in i.split("-d")[0].strip().lower():
				if des.lower() in i.split("-d")[1].strip().lower():
					nname=i
					break
	exflag=0
	name=name.lower()
	if des!="":
		for i in extt:
			if str(des.split("\\")[len(des.split("\\"))-1]).endswith(i):
				exflag=1
				ext=i
				break
		flag=1
		if exflag==1:
			if not os.path.isfile(des):
				print("\n[INFO] File doesn't exist!!!")
				return(0)
			s=0
			e=0
			file=open(des,"rb")
			for l,i in enumerate(file.readlines()):
				try:
					if bytes(emb,"utf-8") in i:
						if str(kv)!="":
							key=str(i).split(emb)[1].split(str(kv))[1].encode()
						else:
							key=str(i).split(emb)[1].encode()
						cipher_suite = Fernet(key)
						decoded_text = cipher_suite.decrypt(str(i).split(emb)[2][:len(str(i).split(emb)[2])-3].encode())
						if bytes(name+start,"utf-8") in decoded_text:
							s=l
						elif bytes(name+end,"utf-8") in decoded_text:
							e=l 
				except:
					pass
			if s!=0:
				print("\n[INFO] Cleaning...",name," from ",des)
				file1=open(os.path.join(os.getcwd(),"temp"),"wb")
				file=open(des,"rb")
				for j in file.readlines()[:s]:
					file1.write(j)
				file1=open(os.path.join(os.getcwd(),"temp"),"ab")
				file=open(des,"rb")
				for j in file.readlines()[e+1:]:
					file1.write(j)
				file1=open(os.path.join(os.getcwd(),"temp"),"rb")
				file=open(des,"wb")
				for j in file1.readlines():
					file.write(j)
				file1.close()
				os.remove("{}".format(os.path.join(os.getcwd(),"temp")))
				flag=0
			else:
				flag=1
		else:
			if not os.path.isdir(des):
				print("\n[INFO] Path doesn't exist!!!")
				return(0)
			showf=0
			f=[]
			for r,d,fi in os.walk(des):
				for i in fi:
					f.append(os.path.join(r,i))
			if len(f)==0:
				print("\n[INFO] Empty folder!!!")
				return(0)
			elif len(f)>0:
				for i in f:
					s=0
					e=0
					file=open(i,"rb")
					for l,j in enumerate(file.readlines()):
						try:
							if bytes(emb,"utf-8") in j:
								if str(kv)!="":
									key=str(j).split(emb)[1].split(str(kv))[1].encode()
								else:
									key=str(j).split(emb)[1].encode()
								cipher_suite = Fernet(key)
								decoded_text = cipher_suite.decrypt(str(j).split(emb)[2][:len(str(j).split(emb)[2])-3].encode())
								if bytes(name+start,"utf-8") in decoded_text:
									s=l
								elif bytes(name+end,"utf-8") in decoded_text:
									e=l
						except:
							pass
					if s!=0:
						if showf==0:
							print("\n[INFO] Cleaning...",name," from ",des)
							showf=1
						file1=open(os.path.join(r,"temp"),"wb")
						file=open(i,"rb")
						for j in file.readlines()[:s]:
							file1.write(j)
						file1=open(os.path.join(r,"temp"),"ab")
						file=open(i,"rb")
						for j in file.readlines()[e+1:]:
							file1.write(j)
						file1=open(os.path.join(r,"temp"),"rb")
						file=open(i,"wb")
						for j in file1.readlines():
							file.write(j)
						file1.close()
						os.remove("{}".format(os.path.join(r,"temp")))
						flag=0
					else:
						flag=1
				
		if flag==0:
			print("\n[INFO] Completed")
			if nname!="":
				fil=[]
				file=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"rb")
				for i in file.readlines():
					fil.append(i.decode().strip("\n"))
				fil=set(fil)
				fil.remove(nname)
				file=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"Scatter/cache"),"wb")
				for i in fil:
					file.write(bytes(i,"utf-8")+b"\n")
		elif flag==1:
			print("\n[INFO] File doesn't exist!!!")

