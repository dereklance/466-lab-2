import xmltodict # install using 'pip install xmltodict'
import json

def parse(filename):
	domain = {}

	with open(filename, 'r') as xmlFile:
		xml = xmlFile.read()
		domainDict = xmltodict.parse(xml)

	for attrib in domainDict['domain']['variable']:
		domain[attrib['@name']] = []
		for val in attrib['group']:
			domain[attrib['@name']].append(val['@name'])

	return domain


def main():

	d = parse("trunk/domain.xml")

	for key, vals in d.items():
		print("{}\t-\t{}".format(key, vals))




if __name__ == '__main__':
	main()
