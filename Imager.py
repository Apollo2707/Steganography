import click
from bitstring import BitArray
from PIL import Image
import struct


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
@click.option("--image",'-i', required=True)
@click.option('--data','-d', required=True)
def datatophoto(image, data):
	# get image
	oldimg = Image.open(image)

	#getDAta

	newimg = oldimg.resize((oldimg.size[0]*2,oldimg.size[1]*2))
	newimg.save("newimage.png")

	

def CreateFile():
	pass

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
	c = int(chra,2)
	c = str(chr(c)).encode('ascii')
	return c



if __name__ == '__main__':
	cli()