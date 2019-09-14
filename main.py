import numpy as np
from evalexpression import *

functionTypes = ['$I', '$S', '$B', '$F', '$D', '$V', '$L']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', '$I'), ('string', '$S'), ('bool', '$B'), ('float', '$F'), ('double', '$D'), ('void', '$V'), ('long', '$L')]
typeMap2 = {'I': 'int', 'S': 'string', 'B': 'bool', 'F': 'float', 'D': 'double', 'L': 'long'}
castMap = {'$I': type(5), '$S': type(''), '$B': type(True), '$F': type(1.1), '$D': type(1.1), '$L': type(1)}

class Program():
	def __init__(self, cfile):
		"""
		Initializes all the program data.
		"""
		self.lines = self.splitLines(self.cleanText(self.readText(cfile)))
		self.shortenTypes()
		self.funcDict = self.getFunctions()
		self.scope = 0
		print("hello", self.lines)
		print("func", self.funcDict)
		self.declare('*x', 'malloc(sizeof(int) * 2)', '$I')

	def execute(self):
		index = 0
		while(index < len(self.lines)):
			self.readLine(self.lines[index])
			index += 1

	def getFuncValue(self, funcName, params):
		self.varDicts.append([])
		funcCode = funcDict[funcName]
		returnType = funcCode[0].split()[0]
		numParams = len(funcCode[0].split(','))
		if numParams != 1:
			assert(numParams == len(params))
			paramStrings = ['$' + (param.translate(str.maketrans('', '', string.punctuation)).strip()) for param in funcCode[0].split('$')[2:]]
			for i in range(0, len(params)):
				declare(paramStrings[i] + " = " + str(params[i]) + ';')
			for line in funcCode:
				try:
					readLine(line)
					if 'return' in line:
						ret(line)
				except ValueError as err:
					print("returning" + str(err))
					return err

	def ret(self, line):
		rest = line.replace('return', '')[:-1]
		print(rest)
		print(evalexpression.evalExpression(rest))
		raise ValueError((evalexpression.evalExpression(rest)))

	def readLine(self, line):
		if line[0] == '$' and line[-1] == ';': #its a declare
			line = line[:-1]
			split = line.split()
			if split[2] != '=':
				raise Exception('Not a valid assign.')
			if split[0] not in castMap.keys():
				raise Exception('Not a valid type.')
			expr = split[3:]
			curStr = ''
			for exp in expr:
				curStr += exp
			self.declare(split[1], curStr, split[0])
		elif line[0] == '$' and line[-1] == ')': #its a function!
			#do some function magic here
			None
		elif 'for' in line[:len('for')]:
			self.scope += 1
			rest = line[len('for'):]
			type = rest[1:2]
			assignString = rest[4:].split()
			if rest[1] != '$':
				raise Exception('Didn\'t have a type.')
			else:
				name = assignString[0]
				expression = assignString[2][:-1]
				self.assign(name, expressionString)
			print(rest)
		elif 'while' == line[:len('while')]:
			None
		elif '=' in line: #tentatively, this is a assign
			if line[-1] != ';':
					raise Exception('No semicolon.')
			else:
				line = line[:-1]
			split = line.split()
			if split[1] != '=':
				raise Exception('Not a valid assign.')
			expr = split[2:]
			curStr = ''
			for exp in expr:
				curStr += exp
			if split[0] not in varDicts[-1].keys():
				raise Exception('Variable doesn\'t exist')
			self.assign(split[0], curStr)
		elif line == '{':
			self.scope += 1
			return line
		elif line == '}':
			self.scope -= 1
			return line

	def mallocParser(self, name, expression, type):
		print(expression)
		expression = expression.replace('malloc', '')
		expression = expression.replace('(', '')
		expression = expression.replace(')', '')
		expression = expression.replace('sizeof', '')
		expression = expression.replace(' ', '')
		expression = expression.split('*')
		if expression[0].isdigit():
			type = expression[1]
		elif expression[1].isdigit():
			type = expression[0]

	def assign(self, name, expression):
		newValue = evalExpression(expression)
		var = varDicts[-1][name]
		var.value = newValue
		self.varDicts[-1].update({name : var})

	def declare(self, name, expression, type):
		if '*' in name:
			type = '$P'
			self.mallocParser(name, expression, type)
			return
		value = evalExpression(expression)
		scope = self.scope
		newVar = Variable(type, name, value, scope)
		self.varDicts[-1].update({name : newVar})

	def shortenTypes(self):
		"""
		Replaces all the types in the program with unique capital letters denoting the type.
		"""

		for i, line in enumerate(self.lines): #replaces all the types with shorter types
			for type, ID in typeMap:
				line = line.replace(type, ID)
				self.lines[i] = line.replace(type, ID)
			self.lines[i] = line.strip()

	def getFunctions(self):
		"""
		This function will go to all the line numbers of all the functions in the program, and store only the lines
		pertaining to that function in a list. It will then map the function's name to the list of the function's lines.
		"""

		functions = {}
		for i, line in enumerate(self.lines): #gets all the function lines
			flag, header = self.isFunctionHeader(line)
			if flag:
				functions[header] = i
		for funcName in functions.keys():
			scope = 0
			goodLines = []
			for line in self.lines[functions[funcName]:]:
				goodLines.append(line)
				if line == '{':
					scope += 1
				elif line == '}':
					scope -= 1
					if scope == 0:
						break
			functions[funcName] = goodLines
		print(self.lines)
		return functions

	def readText(self, cfile):
		"""
		Compiles all the text in the program.
		"""

		f = open(cfile, 'r')
		lines = f.readlines()
		totalText = ''
		for line in lines:
			totalText += line
		return totalText

	def cleanText(self, totalText):
		"""
		Deals with endline things.
		"""

		totalText = totalText.replace('\n', '')
		totalText = totalText.replace('\t', '')
		totalText = totalText.replace('\\n', '\n')
		return totalText

	def splitLines(self, totalText):
		"""
		Splits the program by semicolon and curly braces.
		"""

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
		"""
		Returns true and the name of the function if a string is a function header.
		"""

		for type in functionTypes:
			if type == string[:len(type)] and string[-1] == ')':
				leftIndex = string.find('(')
				return True, string[len(type) + 1: leftIndex]
		return False, None

p = Program('cfile.txt')