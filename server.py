import asyncio
import websockets
import os
import finder
import random
import utils
import sctr

ret=""

async def resp(websocket,path):
    
    if (websocket!=""):
        await websocket.send("--connsucc200")
        print("\n[CONNECTED]")
    pflag=0
    # print(websocket)
    while websocket:
        try:
            message=await websocket.recv()
        except:
            pass
        else:
            if type(message)==str:
                message=message.lower()
                if message=="1":
                    await websocket.send("1")
                    continue
                elif message.upper()=="--0":
                    continue
                elif message.upper()=="--1":
                    continue
                elif message.upper()=="--2":
                    continue
                elif message.upper()=="--000":
                    continue
                elif message.upper()=="--111":
                    continue
                elif message.upper()=="--222":
                    continue
                elif message.upper()=="--X":
                    continue
                else:
                    print(f"\n[INFO] Recieved: {message}")
                if "--0" in message[:3]:
                    zipflag=False
                    fname=""
        
                    message=message.split("--0")[1]

                    value,file,path=utils.scatter_existence(message)
                    if value:
                        sctr.retrenc(file,path,"gk")
                        ret=os.path.join(os.path.dirname(os.path.realpath(__file__)),f"{file}")
                        fname=ret.split("\\")[len(ret.split("\\"))-1].strip()
                     
                    if "--r" in message:
                        message=message.split("--r")[1].strip()
                        ret=message.split("--d")[1].strip()
                        fname=message.split("--d")[0].strip()                        

                    if fname!="":
                        pass
                        
                    else:
                        lofiles=finder.pool(message)
                        files="--lof{}".format("+".join(lofiles))
                        await websocket.send(files)
                        fname=await websocket.recv()
                        try:
                            if "--0" not in fname and "--1" not in fname and "--2" not in fname:
                                ret=lofiles[fname]
                                ret=finder.check(ret)
                                if ret.endswith(".zip"):
                                    zipflag=True
                                    if not fname.endswith(".zip"):
                                        fname+=".zip"
                            else:
                                await websocket.send("--*")
                                continue
                        except:
                            print("\n[INFO] Sending Cancelled...")
                            ret=""
                            zipflag=False
                    left=""
                    if(ret!=""):
                        await websocket.send("--ifp{}".format(ret))
                        pflag,left=await utils.getconf(websocket,ret,fname)
                        if pflag==1:
                            await utils.send(websocket,ret)
                        elif pflag==2:
                            await utils.resume_send(websocket,ret,left)

                    if zipflag:
                        os.remove(ret)

                    if value:
                        os.remove(fname)
                elif "--1" in message[:3]:
                    fname=message.split("--1")[1]
                    if fname!='':
                        pflag,file,path=await utils.existconf(websocket,fname)
                        if pflag!=0:
                            if file is not None:
                                sctr.cleanenc(file,path,"gk")
                            await utils.receive(websocket,fname,pflag,file,path)
                        else:
                            await websocket.send(f"--upnbytes{-2}")
                            print("\n[INFO] File Already Exist!!!")
                elif "--2" in message[:3].lower().strip():
                    ret,fname,path,downflag=utils.download_preprocess(message)
                    left=""
                    if(ret!=""):
                        if not os.path.isfile(ret):
                            ret="{}".format(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.path.join(path,ret)))
                        pflag,left=await utils.getconf(websocket,ret,fname)
                    if pflag==1:
                        await utils.send(websocket,ret)
                    elif pflag==2:
                        await utils.resume_send(websocket,ret,left)
                    if downflag:
                        utils.move(fname)


start_server=websockets.serve(resp,'0.0.0.0',12345)
asyncio.get_event_loop().run_until_complete(start_server)
print("[INFO] Listening...")
asyncio.get_event_loop().run_forever()