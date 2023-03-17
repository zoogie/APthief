import os,sys,struct

if sys.version_info[0] >= 3:
	vers=3
else:
	vers=2

with open("00000000.ctx","rb+") as f:
	ctx=f.read()
	if len(sys.argv)==2 and sys.argv[1]=="TRASH":
		f.seek(0)
		f.write(b"\x00"*0x100)
		print("ctx has been trashed as you commanded")
		sys.exit(0)
	
xorexist=os.path.exists("xorpad.bin")

ctx_len=len(ctx)
xorpad=b""
apcert=b""
backup=b""
ctxdec=b""
success=0

if not xorexist:
	print("creating xorpad from .ctx file ...")
	for i in range(ctx_len):
		if vers == 2:
			xorpad+=chr(ord(ctx[i]) ^ 0xff)
		else:
			xorpad+=struct.pack("B",ctx[i] ^ 0xff)
		
	with open("xorpad.bin","wb") as f:
		f.write(xorpad)
	with open("00000000.ctx.backup","wb") as f:
		f.write(ctx)
else:
	print("generating movable_part1.sed and apcert.bin ...")
	with open("00000000.ctx.backup","rb") as f:
		backup=f.read()	
	if ctx == backup:
		print("\nERROR: it appears the apcert hasn't been written to the ctx yet, \ntry resuming the eshop download again\n")
		sys.exit(1)
	with open("xorpad.bin","rb") as f:
		xorpad=f.read()
	for i in range(ctx_len):
		if vers == 2:
			ctxdec+=chr(ord(ctx[i]) ^ ord(xorpad[i]))
		else:
			ctxdec+=struct.pack("B",ctx[i] ^ xorpad[i])
	offset=0x2fc
	while offset < ctx_len:
		apcert=ctxdec[offset:offset+0x180]
		if b"NintendoCTR2pro" in apcert:
			with open("movable_part1.sed","wb") as f:
				f.write(b"\x00"*0x1000)
				devID=int(apcert[0xA4:0xAC],16)
				f.seek(0x100)
				f.write(struct.pack("<I",devID))
				curpath=os.getcwd()
				index=curpath.index("Nintendo 3DS")  #Nintendo 3DS/
				ID0=curpath[index+13:index+13+32]
				f.seek(0x10)
				f.write(bytes(ID0,'utf-8'))
				with open("apcert.bin","wb") as g:
					g.write(apcert)
				print("success! (offset:%08X)" % offset)
				success=1
				break
		offset+=0x400
	if not success:
		print("ERROR: it appears the apcert was lost in the heat of battle, RIP")
	
print("done")