import numpy as np
#from evalexpression import *
import Variable

functionTypes = ['$I', '$S', '$B', '$F', '$D', '$V', '$L']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', '$I'), ('string', '$S'), ('bool', '$B'), ('float', '$F'), ('double', '$D'), ('void', '$V'), ('long', '$L')]
typeMap2 = {'I': 'int', 'S': 'string', 'B': 'bool', 'F': 'float', 'D': 'double', 'L': 'long'}
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
	print("v1 and v2 are: ", v1.value, v2.value)
	if op in operators:
		return v2.value+v1.value

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
		self.tmpstate = 0

		#print("hello", self.lines)
		#print("func", self.funcDict)
		#self.readLine('for($I i = 0;')

	def execute(self):
		index = i
		while(i < len(self.lines)):
			self.readLine(self.lines[i])
			i += 1

	def getFuncValue(self, funcName, params):
		self.varDicts.append({})
		funcCode = self.funcDict[funcName]
		returnType = funcCode[0].split()[0]
		numParams = len(funcCode[0].split(','))
		if numParams != 1:
			assert(numParams == len(params))
			paramStrings = ['$' + (param.translate(str.maketrans('', '', string.punctuation)).strip()) for param in funcCode[0].split('$')[2:]]
			for i in range(0, len(params)):
				declare(paramStrings[i] + " = " + str(params[i]) + ';')
		for line in funcCode:
			try:
				self.readLine(line)
				if 'return' in line:
					self.ret(line)
			except ValueError as err:
				print("returning", str(err))
				return err
	
	def ret(self, line):
		rest = line.replace('return', '')[:-1]
		raise ValueError((self.evalExpression(rest)).value)

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
			if split[0] not in self.varDicts[-1].keys():
				raise Exception('Variable doesn\'t exist')
			self.assign(split[0], curStr)
		elif line == '{' or line == '}':
			None

	def readLine2(self, line):
		#flag, condition, (name, expressionString) = self.isValidAssign(line)
		condition = ['declare', 'assign', 'ret'][self.tmpstate]
		name = ['y', 'y', None][self.tmpstate]
		expressionString = ['1', 'y+1', None][self.tmpstate]
		self.tmpstate += 1
		#print('fuck', flag, condition, name, expressionString)
		if True: #then it is a declare or assign
			if condition == 'declare': # it is a declare
				self.declare(name, expressionString, line[:2])
			elif condition == 'assign': # it is an assign
				self.assign(name, expressionString)
 
		#if 'for' in line[:len('for')]:
		#	self.scope += 1
		#	rest = line[len('for'):]
		#	type = rest[1:2]
		#	assignString = rest[4:].split()
		#	if rest[1] != '$':
		#		raise Exception('Didn\'t have a type.')
		#	else:
		#		name = assignString[0]
		#		expression = assignString[2][:-1]
		#		self.assign(name, expressionString)
		#	print(rest)
		#elif 'while' == line[:len('while')]:
		#	None

	def assign(self, name, expression):
		print("expression is", expression)
		newValue = self.evalExpression(expression)
		var = self.varDicts[-1][name]
		var.value = newValue
		self.varDicts[-1].update({name : var})

	def declare(self, name, expression, mtype):
		value = self.evalExpression(expression)
		scope = self.scope
		newVar = Variable.Variable(mtype, name, value.value, scope)
		self.varDicts[-1].update({name : newVar})

	def isValidAssign(self, line):
		hasType = False
		print("line is: ", line)
		if line[0] == '$':
			hasType = True
		
		if line[-1] != ';':
			pass
		#	raise Exception('No semicolon.')
		else:
			line = line[:-1]

		split = line.split()
		if hasType and split[2] != '=':
			pass
			#raise Exception('Not a valid assign.')
		
		if hasType:	
			if split[0] not in castMap.keys():
				pass
				#raise Exception('Not a valid type.')
			expr = split[3:]
			curStr = ''
			for exp in expr:
				curStr += exp
			return True, 'declare', (split[1], curStr)
		else:
			expr = split[2:]
			curStr = ''
			for exp in expr:
				curStr += exp
			return True, 'assign', (split[0], curStr)
		return False, None, None

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

	def evalFunctionParams(self, s):
		s = s[1:-1] #removes the open and close parentheses around the parameters
		s = s.split(",")
		params = []
		for param in s:
			params.append(self.evalExpression(param))
		return params

	def evalExpression(self, s):
		print("evaling: ", s)
		valueStack = []
		operatorStack = []
		for x in operators:
			s = s.replace(x, " "+x+" ")
		tokens = s.split()
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
		return valueStack[0]

p = Program('cfile.txt')
print(p.getFuncValue('main', []))
