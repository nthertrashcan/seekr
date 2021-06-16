import os


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


def kmp(p,t,bflag=0):
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

					if not bflag:
						if i-j==0:
							return True
						else:
							return False
					# else:
					# 	return False
					# print("Found at index from",i-j,"to",m+i-j)
					if bflag:
						return True
					j=f[0]
				else:
					i+=1
					j+=1
			elif j>0:
				j=f[j-1]
			else:
				i+=1
		if mflag:
			return False
	else:
		return False





# direc=["c:\\users\\gaurav\\desktop","c:\\users\\gaurav\\downloads","e:\\","f:\\"]
direc=["c:\\users\\gaurav\\desktop"]


extn=["py","cpp","java","pdf","docx","doc","xml","mp3","mp4","mkv","webm","zip","rar","jpeg","jpg","png"]
sec={}

from zipfile import ZipFile
import zipfile
    
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
        	ziph.write(os.path.join(root, file), 
            	os.path.relpath(os.path.join(root, file), 
            		os.path.join(path, '..')))

def search(arg,path=None,ext=None):

	if path is not None:
		files=next(os.walk(path))[2]
		for file in files:
			if "_" in file:
				arg=arg.replace(" ","_")
			if any(file.endswith(x) for x in ext):
				if kmp(arg.lower(),file.lower()):
					return os.path.join(path,file),file

		return "",""



	else:
		for dr in direc:
			if any(arg.endswith(x) for x in extn):
				for root,directories,files in os.walk(dr):
					for file in files:
						if kmp(arg.lower(),omit(file).lower()):
							return os.path.join(root,file),file

				for root,directories,files in os.walk(dr):
					for file in files:
						if kmp(arg.lower(),omit(file).lower(),1):
							return os.path.join(root,file),file
							# exit()
			else:
				for root,directories,_ in os.walk(dr):
					for directory in directories:
						
						if kmp(arg.lower(),omit(directory).lower()):
							
							out=os.path.join(root,directory)

							zipf = zipfile.ZipFile(f'{os.path.join(root,directory)}.zip', 'w', zipfile.ZIP_DEFLATED)
							zipdir(out,zipf)
							zipf.close()
							return f"{os.path.join(root,directory)}.zip",f"{directory}.zip"

				for root,directories,_ in os.walk(dr):

					for directory in directories:
						if kmp(arg.lower(),omit(directory).lower(),1):
							out=os.path.join(root,directory)

							zipf = zipfile.ZipFile(f'{os.path.join(root,directory)}.zip', 'w', zipfile.ZIP_DEFLATED)
							print(out)
							zipdir(out,zipf)
							zipf.close()
							return f"{os.path.join(root,directory)}.zip",f"{directory}.zip"


def lof(arg):
	direcfile=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"directories.txt"),"r")


	direc=direcfile.readlines()
	print(direc)

	global extn
	flag=True

	if any(arg.endswith(x) for x in extn):
		indx=[arg.endswith(x) for x in extn].index(True)
		arg=arg.strip(extn[indx])
		extn=[extn[indx]]
		flag=False

	sen=[]
	lofiles={}

	for dr in direc:
		for root,directories,files in os.walk(dr):
			for file in files:
				if any(file.endswith(x) for x in extn):
					if arg!="":
						if kmp(omit(arg).lower(),omit(file).lower()):
							if file not in sen:
								sen.append(file)
								lofiles[file.lower()]=os.path.join(root,file)
								print("f",file)
			
					else:
						if any(file.endswith(x) for x in extn):
							if kmp(omit(arg).lower(),omit(file).lower()):
								if file not in sen:
									sen.append(file)
									lofiles[file.lower()]=os.path.join(root,file)
									print("x",file)
			
			if flag:
				for directory in directories:
					if kmp(omit(arg,0).lower(),omit(directory,0).lower()):
						if directory not in sen:
							lofiles[directory.lower()]=os.path.join(root,directory)
							sen.append(directory)
							print("d",directory)
			
	print("Sending list...")
	print(lofiles)
	return lofiles
	

def tozip(directory):
	print("Zippin...")
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





def _KMP(p,t,bflag=0):
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
					# print(f"Found {p} at index from",i-j,"to",m+i-j)
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


def checkMatchByChr(p,t):
	indx=0
	for c in p:
		value,indx=_KMP(c,t)
		t=t[indx:]
		if not value:
			return False
	return True

def checkMatch(p,t):
	# print(p,t)
	for c in p.split(" "):
		value,_=_KMP(c,t)
		if not value:
			return False
		return True




def pool(arg):
	direcfile=open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"directories.txt"),"r")


	direc=direcfile.readlines()
	print(direc)

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
		dr=dr.rstrip()
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
			
	print("Sending list...")
	return lofiles


