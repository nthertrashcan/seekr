import os
from zipfile import ZipFile
import zipfile
    
if not os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles")):
	os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles"))


direc=["c:\\users\\gaurav\\desktop","c:\\users\\gaurav\\downloads","e:\\","f:\\"]
extn=["py","cpp","java","pdf","docx","doc","xml","mp3","mp4","mkv","webm","zip","rar","jpeg","jpg","png"]
sec={}




def prefix_func(p):
	m=len(p)
	f=[0]*m
	i=1
	j=0

	while i<m:
		if p[i]==p[j]:
			f[i]=j+1
			i+=1
			j+=1

		elif j>0:
			j=f[j-1]
		else:
			i+=1
	return f


def KMP(p,t,bflag=0):
	m=len(p)
	n=len(t)
	if m>0:
		f=prefix_func(p)
		i=0
		j=0
		mflag=True

		while i<n:
			if t[i]==p[j]:
				if j==m-1:
					mflag=False
					return (True,i-j+1)
					j=f[0]
				else:
					i+=1
					j+=1
			elif j>0:
				j=f[j-1]
			else:
				i+=1
		if mflag:
			return (False,-1)
	else:
		return (False,-1)


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
        	ziph.write(os.path.join(root, file), 
            	os.path.relpath(os.path.join(root, file), 
            		os.path.join(path, '..')))


def tozip(directory):
	print("\n[INFO] Zippin...")
	zipf = zipfile.ZipFile(f'{directory}.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir(directory,zipf)
	zipf.close()
	return


def check(arg):
	if any(arg.endswith(x) for x in extn):
		return arg
	else:
		tozip(arg)
		return arg+".zip"


def omit(arg,flag=1):
	global extn
	ext=""
	if flag:
		if any(arg.endswith(x) for x in extn):
			indx=[arg.endswith(x) for x in extn].index(True)
			arg=arg.strip(extn[indx])
			ext="."+extn[indx]

	arg=arg.replace("the","",1)
	arg=arg.replace("_"," ")
	arg=arg.replace("."," ")
	arg=arg.replace("0","")
	arg=arg.replace("1","")
	arg=arg.replace("2","")
	arg=arg.replace("3","")
	arg=arg.replace("4","")
	arg=arg.replace("5","")
	arg=arg.replace("6","")
	arg=arg.replace("7","")
	arg=arg.replace("8","")
	arg=arg.replace("9","")

	arg=arg.strip()
	return arg+ext






def checkMatchByChr(p,t):
	indx=0
	for c in p:
		value,indx=KMP(c,t)
		t=t[indx:]
		if not value:
			return False
	return True

def checkMatch(p,t):
	# print(p,t)
	for c in p.split(" "):
		value,_=KMP(c,t)
		if not value:
			return False
		return True



def search(arg,path=None,ext=None):

	if path is not None:
		files=next(os.walk(path))[2]
		for file in files:
			if "_" in file:
				arg=arg.replace(" ","_")
			if any(file.endswith(x) for x in ext):
				if checkMatch(omit(arg).lower(),omit(file).lower()):
					return os.path.join(path,file),file

	return "",""



def pool(arg):
	global direc
	if os.path.isfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/directories.txt")):
		direcfile=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"utilfiles/directories.txt"),"r")
		direc=direcfile.readlines()
		temp=[]
		for l,i in enumerate(direc):
			i=i.rstrip()
			if os.path.isdir(i):
				temp.append(i)
		direc=set(temp)

	print("\n[DIRECTORIES]",direc)

	global extn
	ext=[]
	flag=True

	if any(arg.endswith(x) for x in extn):
		indx=[arg.endswith(x) for x in extn].index(True)
		arg=arg.strip(extn[indx])
		ext=[extn[indx]]
		flag=False
	else:
		ext=extn

	sen=[]
	lofiles={}
	for dr in direc:
		for root,directories,files in os.walk(dr):
			for file in files:
				if any(file.endswith(x) for x in ext):
					if arg!="":
						if checkMatch(omit(arg).lower(),omit(file).lower()):
							if file not in sen:
								sen.append(file)
								lofiles[file.lower()]=os.path.join(root,file)
								print("f",file)
			
					else:
						if any(file.endswith(x) for x in ext):
							if checkMatch(omit(arg).lower(),omit(file).lower()):
								if file not in sen:
									sen.append(file)
									lofiles[file.lower()]=os.path.join(root,file)
									print("x",file)
			
			if flag:
				for directory in directories:
					if checkMatch(omit(arg,0).lower(),omit(directory,0).lower()):
						if directory not in sen:
							lofiles[directory.lower()]=os.path.join(root,directory)
							sen.append(directory)
							print("d",directory)
			
	print("\n[INFO] Sending list...")
	return lofiles



