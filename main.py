import numpy as np
#from evalexpression import *
import Variable
import string

functionTypes = ['$I', '$S', '$B', '$F', '$D', '$V', '$L']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', '$I'), ('string', '$S'), ('bool', '$B'), ('float', '$F'), ('double', '$D'), ('void', '$V'), ('long', '$L')]
typeMap2 = {'$I': 'int', '$S': 'string', '$B': 'bool', '$F': 'float', '$D': 'double', '$L': 'long'}
castMap = {'$I': type(5), '$S': type(''), '$B': type(True), '$F': type(1.1), '$D': type(1.1), '$L': type(1)}
operators = ["+","-","*","/","(",")","=="]
precedence = {"*":5, "/":5, "+":3, "-":3,"==":1,"(":-1}


def stringIsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def applyOperator(op, v1, v2):
	return Variable.Variable(None, None, int(eval(str(v2.value)+op+str(v1.value))), None)

class Program():
	def __init__(self, cfile):
		"""
		Initializes all the program data.
		"""
		self.lines = self.splitLines(self.cleanText(self.readText(cfile)))
		self.shortenTypes()
		self.funcDict = self.getFunctions()
		self.varDicts = [{"nope":"hi"}]
		self.scope = 0
		self.heapDict = {}
		self.heapNum = 0
		self.mallocParser('*x', 0, 'malloc(sizeof($I) * 8)', '$I')
	#	print(self.lines)
	#	print(self.heapDict)
	#	print(self.heapNum)
	#	print("woah")
		#print("hello", self.lines)
		#print("func", self.funcDict)
		#self.readLine('for($I i = 0;')

	def execute(self):
		index = 0
		while(i < len(self.lines)):
			self.readLine(self.lines[i])
			i += 1

	def getFuncValue(self, funcName, params):
		self.varDicts.append({})
		funcCode = self.funcDict[funcName]
		returnType = funcCode[0].split()[0]
		numParams = len(funcCode[0].split(','))
#		print("num params", numParams)
		if numParams != 0:
#			print("declaring params")
			paramStrings = ['$' + (param.translate(str.maketrans('', '', string.punctuation)).strip()) for param in funcCode[0].split('$')[2:]]
			for i in range(0, len(params)):
				self.readLine(paramStrings[i] + " = " + str(params[i]) + ';')
		for line in funcCode:
			self.readLine(line)
			if 'return' in line:
				rest = line.replace('return', '')[:-1]
				return Variable.Variable(None, None, self.evalExpression(rest).value, None)

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

		elif 'for' in line or 'while' in line:
			self.loop(line)
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
			if split[0] not in self.varDicts[-1].keys():
				raise Exception('Variable doesn\'t exist')
			self.assign(split[0], curStr)
		elif line == '{':
			self.scope += 1
			return line
		elif line == '}':
			self.scope -= 1
			return line

	def assign(self, name, expression):
#		print("expression is", expression)
		if '*' in name:
			self.mallocParser(1, name, expression, mtype)
			return
		newValue = self.evalExpression(expression)
#		print("new value: ", newValue)
		var = self.varDicts[-1][name]
		var.value = newValue.value
		self.varDicts[-1].update({name : var})

	def declare(self, name, expression, mtype):
#		print('!!', name)
		if '*' in name:
			self.mallocParser(0, name, expression, mtype)
			return
		value = self.evalExpression(expression)
		scope = self.scope
		newVar = Variable.Variable(mtype, name, value.value, scope)
		self.varDicts[-1].update({name : newVar})

	def mallocParser(self, flag, name, expression, type):
#		print("expr", expression)
		hasDigit = False
		for char in expression:
			if char.isdigit():
#				print("found digit")
				hasDigit = True
				break
		expression = expression.replace('malloc', '')
		expression = expression.replace('(', '')
		expression = expression.replace(')', '')
		expression = expression.replace('sizeof', '')
		expression = expression.replace(' ', '')
		expression = expression.split('*')
		if not hasDigit: #not found digit
			size = 1
			type = expression[0]
		else:
			if expression[0].isdigit():
				type = expression[1]
				if '*' in type:
					type = '$P'
				size = expression[0]
			elif expression[1].isdigit():
				type = expression[0]
				if '*' in type:
					type = '$P'
				size = expression[1]
		self.heapDict[self.heapNum] = [Variable.Variable('-', type, None, self.scope) for i in range(int(size))]
		self.heapNum += 1
		if flag == 1: #assign
			obj = self.varDicts[-1][name]
			obj.value = self.heapNum - 1
			obj.type = '$P'
			obj.scope = self.scope
		else: #declare
			obj = Variable.Variable(name, '$P', self.heapNum - 1, self.scope)
			self.varDicts[-1][name] = obj
		return self.heapNum - 1

	def isValidAssign(self, line):
		hasType = False
#		print("line is: ", line)
		if line[0] == '$':
			hasType = True
		
		if line[-1] != ';':
			pass
		#	raise Exception('No semicolon.')
		else:
			if expression[0].isdigit():
				type = expression[1]
				if '*' in type:
					type = '$P'
				size = expression[0]
			elif expression[1].isdigit():
				type = expression[0]
				if '*' in type:
					type = '$P'
				size = expression[1]
		self.heapDict[self.heapNum] = [Variable.Variable('-', type, None, self.scope) for i in range(int(size))]
		self.heapNum += 1
		if flag == 1: #assign
			obj = self.varDicts[-1][name]
			obj.value = self.heapNum - 1
			obj.type = '$P'
			obj.scope = self.scope
		else: #declare
			obj = Variable.Variable(name, '$P', self.heapNum - 1, self.scope)
			self.varDicts[-1][name] = obj
		return self.heapNum - 1


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
#		print(self.lines)
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

	def evalFunctionParams(self, s):
		s = s[1:-1] #removes the open and close parentheses around the parameters
		s = s.split(",")
		params = []
		for param in s:
			params.append(self.evalExpression(param).value)
	#	print("params", params)
		return params

	def evalExpression(self, s):
	#	print("evaling: ", s)
		valueStack = []
		operatorStack = []
		for x in operators:
			s = s.replace(x, " "+x+" ")
		tokens = s.split()
	#	print('tokens: ', tokens)
		print('varDicts', self.varDicts[-1])
		y = 0
		while y < len(tokens):
			#print y, tokens[y], operatorStack, valueStack
			token = tokens[y]
			if stringIsInt(token):
				valueStack.append(Variable.Variable(None, None, int(token), None)) 
			elif token in self.varDicts[-1].keys():
				valueStack.append(self.varDicts[-1][token])
			elif token == "(":
				operatorStack.append(token)
			elif token == ")":
				x = operatorStack.pop()
				while x != "(":
					v1 = valueStack.pop()
					v2 = valueStack.pop()
					valueStack.append(applyOperator(x, v1, v2))
					x = operatorStack.pop()
			elif token in operators:
				while len(operatorStack) > 0 and precedence[operatorStack[-1]] >= precedence[token]:
					x = operatorStack.pop()
					v1 = valueStack.pop()
					v2 = valueStack.pop()
					valueStack.append(applyOperator(x, v1, v2))
				operatorStack.append(token)
			elif token in self.funcDict.keys():
				paramstring = ""
				i = 0
				for z in range(y+1, len(tokens)):
					y += 1
					if tokens[z] == "(":
						i += 1
					elif tokens[z] == ")":
						i -= 1
					paramstring += tokens[z]
					if i == 0:
						valueStack.append(self.getFuncValue(token, self.evalFunctionParams(paramstring)))
						break
			y += 1
		while len(operatorStack) != 0:
			x = operatorStack.pop()
			v1 = valueStack.pop()
			v2 = valueStack.pop()
			valueStack.append(applyOperator(x, v1, v2))
	#	print("returning", valueStack[0])
		return valueStack[0]

p = Program('cfile.txt')
print(p.getFuncValue('main', []))
