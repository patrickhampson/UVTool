import argparse
from PIL import Image
import requests
from io import BytesIO

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def imageFromUrl( url ):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	return img;

def brightness( im ):
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

parser = argparse.ArgumentParser(description='Brightness Checker')
#parser.add_argument('cameras', default=None, help='Comma separated list of IDs')
parser.add_argument('--correct', type=str2bool, nargs='?', const=False)
args = parser.parse_args()

#if(args.cameras)
