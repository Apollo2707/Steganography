import click
from bitstring import BitArray
from PIL import Image
import struct
import random

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
	if ctx.invoked_subcommand is None:
		#click.echo('I was invoked without subcommand')
		pass
	else:
		#click.echo('I am about to invoke %s' % ctx.invoked_subcommand)
		pass

@cli.command()
def sync():
	click.echo('The subcommand')

@cli.command()
def testdata():
	with open("testdata.txt", 'rb') as f:
		lines = f.read()

	z = StrToBin(lines)
	out = BinToStr(z)

	with open("testdataclone.txt", 'wb') as f:
		f.write(out)


@cli.command()
@click.option('--image','-i', required=True)
def readdeviation(image):
	img = Image.open(image)
	pixelmap = img.load()
	for y in range(img.size[1]/2):
		for x in range(img.size[0]/2):
			pass




@cli.command()
@click.option("--image", '-i', required=True)
@click.option('--data', '-d', required=True)
def datatophoto(image, data):
	# get image
	oldimg = Image.open(image)

	#getData
	with open(data, 'rb') as f:
		lines = f.read()
	print(lines)
	bina = StrToBin(lines)
	print(bina)

	newimg = oldimg.resize((oldimg.size[0]*2, oldimg.size[1]*2))
	
	buildimage(oldimg, newimg, bina)

	newimg.save("newimage.png")


def CreateFile():
	pass


def buildimage(oldimage,newimage,data):
	oldpixelmap = oldimage.load()
	newpixelmap = newimage.load()
	counter = 0 

	print("Data to add to file")
	print(data)

	for y in range(oldimage.size[1]):
		for x in range(oldimage.size[0]):
			newy = y * 2
			newx = x * 2

			out = pixelConverter(oldpixelmap[x,y], data[counter:counter+3])

			newpixelmap[newx, newy] = out.tlpixel
			newpixelmap[newx + 1, newy] = out.trpixel
			newpixelmap[newx, newy + 1] = out.blpixel
			newpixelmap[newx + 1, newy + 1] = out.brpixel

	print ()


def BinToStr(input_str):
	#c = BitArray(hex=input_str)
	#print(c.bin)
	c = [input_str[i:i+8]for i in range(0, len(input_str), 8)]

	z = b''.join([str(chr(int(x, 2))).encode("ascii") for x in c])
	return z

def StrToBin(input_str):
	c = str.join('',[str(bin(x)[2:]).zfill(8) for x in input_str])
	return c


def ChrToBin(chra):
	c = str(bin(chra))[2:].zfill(8)
	return c


def BinToChr(chra):
	c = int(chra, 2)
	c = str(chr(c)).encode('ascii')
	return c
class dataHandler:
	rawBinaryData = None
	currentIndex = 0 
	
class pixelConverter:
	data = None
	majorpixel = None
	tlpixel = None
	trpixel = None
	blpixel = None
	brpixel = None

	def deviation(self, bit):
		#pos = [[1, 1, 0, -1], [1, 1, 1, 0], [1, 1, 1, -1]]
		#neg = [[-1, -1, 0, 1], [-1, -1, -1, 0], [-1, -1, -1, 1]]
		pos = [[1,0,0,0]]
		neg = [[-1,0,0,0]]
		if bit is '1':
			ret = random.choice(pos)
			random.shuffle(ret)
			return ret
		elif bit is '0':
			ret = random.choice(neg)
			random.shuffle(ret)
			return ret
		elif bit is None:
			return 0, 0, 0, 0
		else:
			return None

	def pulldata(self):

		pass

	def adddata(self, majorPixel, data):

		r, g, b, h = self.majorpixel

		reddev = deviation(self.data[0])
		greendev = deviation(self.data[1])
		bluedev = deviation(self.data[2]) 

		self.tlpixel = (r + reddev[0], g + greendev[0], b + bluedev[0])
		self.trpixel = (r + reddev[1], g + greendev[1], b + bluedev[1])
		self.blpixel = (r + reddev[2], g + greendev[2], b + bluedev[2])
		self.brpixel = (r + reddev[3], g + greendev[3], b + bluedev[3])
		


if __name__ == '__main__':
	cli()
