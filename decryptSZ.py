#!/usr/bin/python

# This file is free for use.

import os
import sys
import getopt
import json
import base64
import urllib2
import binascii

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
   		key = '7#J9k(b*'
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


    	headers = {'Cookie' : jsonLoad['cookie']}
    	req = urllib2.Request(jsonLoad['spt'],'',headers)
    	response = urllib2.urlopen(req)
    	page = response.read()

    	
    	subkey = 'vNnrfbrOJbY=' #response.info().getheader('Sub-Key')
    	#subkey = response.info().getheader('Sub-Key')
    	print 'Found Sub-Key: ' + subkey
    	subkey = base64.b64decode(subkey)
    	print 'Sub-Key Base64 bin: ' + binascii.hexlify(subkey)
    	outra_key = chr(ord(subkey[0:1]) ^ ord(key[0:1]))
    	outra_key = outra_key + chr(ord(subkey[1:2]) ^ ord(key[1:2]))
    	outra_key = outra_key + chr(ord(subkey[2:3]) ^ ord(key[2:3]))
    	outra_key = outra_key + chr(ord(subkey[3:4]) ^ ord(key[3:4]))
    	outra_key = outra_key + chr(ord(subkey[4:5]) ^ ord(key[4:5]))
    	outra_key = outra_key + chr(ord(subkey[5:6]) ^ ord(key[5:6]))
    	outra_key = outra_key + chr(ord(subkey[6:7]) ^ ord(key[6:7]))
    	outra_key = outra_key + chr(ord(subkey[7:8]) ^ ord(key[7:8]))
    	print binascii.hexlify(outra_key)
    	cipherPrint = DES.new(outra_key,DES.MODE_ECB)
    	print cipherPrint.decrypt(page)


if __name__ == "__main__":
   main(sys.argv[1:])