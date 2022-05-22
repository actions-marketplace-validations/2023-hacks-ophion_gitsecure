import argparse, multiprocessing, re
import requests, json
from itertools import product

regex = {}
results = {"results":[]}
global args
def sendMessage():
	slack_link = 'https://hooks.slack.com/services/{0}'.format(args.url)
	message = '*Disclosed APIs*\n_Repo name_: {repoName}\n'.format(repoName=args.name)
	if len(results['results']) > 0:
		for res in results['results']:
			file_name = list(res.keys())[0]
			message += '_File Name_: {filename}\n'.format(filename=file_name)
			message += '\n'.join(res[file_name])
		data = {"text":message, "mrkdwn":1}
		requests.post(slack_link, data = json.dumps(data))
	print('No disclosure found')

def result(fileResult):
	for res in fileResult:
		if res is not None:
			results['results'].append(res)

def getRegex():
	global regex
	regex = requests.get('https://raw.githubusercontent.com/dxa4481/truffleHogRegexes/master/truffleHogRegexes/regexes.json').json()

def matchRegex(line):
	# create an array for returning matched keys
	matchedArray = []
	# for each key value pair in the dictionary (an item is a set of key/value pairs)
	for key, values in regex.items():
		#print(regexes)
		pythonReg = re.compile(values)
		# patern match regex in python
		match = pythonReg.search(line)
		# if match is not empty (has valid regex token)
		if match is not None:
			# append the key to the matched array so we track the instance of where plaintext token was found
			matchedArray.append(key)
		# return the array
	return matchedArray

def readFile(file):
	fileReturn = {file:[]}
	f = open('{dirs}/{file}'.format(dirs = args.dirs, file = file), encoding='utf-8')
	lines = f.readlines()
	for index, line in enumerate(lines):
		matched = matchRegex(line.strip())
		if len(matched) > 0:
			found = '👉 *Found {matches} in line {lineNum}*'.format(matches = ','.join(matched), lineNum = index+1, fileName = file)
			fileReturn[file].append(found)
	if len(fileReturn[file]) > 0:
		return fileReturn
	return None

if __name__=="__main__":
	print('v2 today')
	parser = argparse.ArgumentParser()
	parser.add_argument('--files', dest='filesToCheck', nargs="+") # adds all files passed into an array. The files are retrieved from git diff
	parser.add_argument('--repoloc', dest='dirs') # gets argument from repoloc and assigns it to a string.
	parser.add_argument('--repoName', dest='name')
	parser.add_argument('--url', dest='url')
	args = parser.parse_args()
	print('Analysing {repoName}'.format(repoName=args.name))
	getRegex()
	pool = multiprocessing.Pool(10)
	x = pool.map_async(readFile, args.filesToCheck, callback=result) # this will run the scans on files and call result for each result
	x.get()
	pool.close()
	pool.join()
	sendMessage()
