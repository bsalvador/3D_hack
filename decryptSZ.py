#!/usr/bin/python
import os
import sys
import getopt
import json
import base64

from Crypto.Cipher import DES


def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'decryptSZ.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'decryptSZ.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	
		with open(inputfile, 'rb') as f_input:
			read_bytes = f_input.read()
   		f_input.close()
   		key = b'7#J9k(b*'
   		cipher = DES.new(key, DES.MODE_ECB)
   		output = cipher.decrypt(read_bytes)
   		output = output[16:len(output)]

   		while (output[len(output)-1] != '}'):
   			output = output[:(len(output)-1)]
   		

   		jsonLoad = json.loads(output)


   		url = cipher.decrypt(base64.b64decode(jsonLoad['parameters']['json_url_encode']))
		while (url[len(url)-1] != '}'):
   			url = url[:(len(url)-1)]
   		
   		
   		jsonLoad['parameters']['json_url_encode'] = url
   		saida = json.dumps(jsonLoad)
       	with open(outputfile, "wb") as f:
    		f.write(saida)
    	f.close()


	
   



if __name__ == "__main__":
   main(sys.argv[1:])