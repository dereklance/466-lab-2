import xmltodict # install using 'pip install xmltodict'
import json

def parse(filename):
	with open(filename, 'r') as xmlFile:
		xml = xmlFile.read()
		domainDict = xmltodict.parse(xml)
		return domainDict