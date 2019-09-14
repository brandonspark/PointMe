import numpy as np

functionTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'void', 'long']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', 'I'), ('string', 'S'), ('bool', 'B'), ('float', 'F'), ('double', 'D'), ('void', 'V'), ('long', 'L')]

class Program():
	def __init__(self, cfile):
		totalText = self.cleanText(self.readText(cfile)) 
		self.lines = self.splitLines(totalText)
		self.funcDict = {}
		for i, line in enumerate(self.lines):
			flag, header = self.isFunctionHeader(line)
			if flag:
				self.funcDict[header] = i
		for i, line in enumerate(self.lines):
			for type, ID in typeMap:
				line = line.replace(type, ID)
				self.lines[i] = line.replace(type, ID)
		print("hello", self.lines)
		print(self.funcDict)
	
	def readText(self, cfile):
		f = open(cfile, 'r')
		lines = f.readlines()
		totalText = ''
		for line in lines:
			totalText += line
		return totalText

	def cleanText(self, totalText):
		totalText = totalText.replace('\n', '')
		totalText = totalText.replace('\t', '')
		totalText = totalText.replace('\\n', '\n')
		return totalText

	def splitLines(self, totalText):
		progLines = []
		currentStr = ''
		for char in totalText:
			if char == '{' or char == '}':
				if len(progLines) == 0:
					progLines.append(currentStr)
				elif len(currentStr) != 0:
					progLines.append(currentStr)
				currentStr = char
				progLines.append(currentStr)
				currentStr = ''
			elif char == ';':
				currentStr += char
				progLines.append(currentStr)
				currentStr = ''
			else:
				currentStr += char
		return progLines

	def isFunctionHeader(self, string):
		for type in functionTypes:
			if type == string[:len(type)] and string[-1] == ')':
				leftIndex = string.find('(')
				return True, string[len(type) + 1: leftIndex]
		return False, None



p = Program('cfile.txt')