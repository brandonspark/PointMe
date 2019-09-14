import numpy as np
#from evalexpression import *
import Variable
import string
import re

functionTypes = ['$I', '$S', '$B', '$F', '$D', '$V', '$L']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', '$I'), ('string', '$S'), ('bool', '$B'), ('float', '$F'), ('double', '$D'), ('void', '$V'), ('long', '$L')]
typeMap2 = {'$I': 'int', '$S': 'string', '$B': 'bool', '$F': 'float', '$D': 'double', '$L': 'long'}
castMap = {'$I': type(5), '$S': type(''), '$B': type(True), '$F': type(1.1), '$D': type(1.1), '$L': type(1)}
operators = ["+","-","*","/","(",")","==",'>>']
spacedOperators = ["+","-","/","(",")","==",'>>']
precedence = {"*":5, "/":5, "+":3, "-":3,"==":1,"(":-1,'>>':4 }

def stringIsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def applyOperator(op, v1, v2):
	if op in operators:
		return Variable.Variable(None, None, int(eval(str(v2.value)+op+str(v1.value))), None)

class Program():
	def __init__(self, cfile):
		"""
		Initializes all the program data.
		"""
		self.lines = self.splitLines(self.cleanText(self.readText(cfile)))
		print(self.lines)
		self.shortenTypes()
		self.structDict = self.getStructs()
		self.typedefSearch()
		for type in self.structDict.keys():
			type = type[1:]
			for i, line in enumerate(self.lines):
				line = line.replace(type, '$' + type)
				self.lines[i] = line
<<<<<<< HEAD
=======
		self.loopPositions = self.getLoops() # key: line number of start of loop, value: line number of end of loop
		self.loopPositionsReverse = {v: k for k, v in self.loopPositions.items()} # key, value switched from loopPositions
		self.loopList = [] # stores tuple (line, scope) that contains for loops we are currently inside
		self.funcDict = self.getFunctions()
>>>>>>> 40caf27b0f1146d222e3df3557739fafc4449c7d
		self.loopPositions = self.getLoopPositions() # key: line number of start of loop, value: line number of end of loop
		self.loopPositionsReverse = {v: k for k, v in self.loopPositions.items()} # key, value switched from loopPositions
		self.loopList = [] # stores tuple (line, scope) that contains "for" loops we are currently inside
		self.conditionalPositions = self.getConditionalPositions()
		self.varDicts = [{"nope":"hi"}]
		self.funcDict = self.getFunctions()
		self.scope = 0
		self.heapDict = {}
		self.heapNum = 0

		#self.mallocParser(0, '*x', 	'malloc(sizeof(myStruct))', '$I')
		print('ourlines', self.lines)
		print(self.heapDict)
		print(self.heapNum)
		print(self.mallocParser(0, 'x', 'malloc(sizeof($struct_t))', '$struct_t'))
		print('current heap', self.heapDict)
		print('var', self.varDicts[-1]['x'].value)
		print("woah")
		#print("hello", self.lines)
		#print("func", self.funcDict)
		#self.readLine('for($I i = 0;')

	def execute(self):
		index = 0
		while(i < len(self.lines)):
			# we have encountered start of a loop, evaluate loop and react accordingly
			if i in [location[0] for location in loopLocations]:
				# loop guard evaluated to true
				if (self.loop(self.lines[i])):
					i += 1
				else:
					self.scope += 1
					i = self.loopPositions[i]
			# we have encountered end of a loop, go back to start of loop
			elif i in [location[1] for location in loopLocations]:
				self.scope -= 1
				i = self.loopPositionsReverse[i]
			self.readLine(self.lines[i])
			i += 1

	def getFuncValue(self, funcName, params):
		self.varDicts.append({})
		funcCode = self.funcDict[funcName]
		returnType = funcCode[0].split()[0]
		numParams = len(funcCode[0].split(','))
		#print("num params", numParams)
		if numParams != 0:
			#print("declaring params")
			paramStrings = ['$' + (param.translate(str.maketrans('', '', string.punctuation)).strip()) for param in funcCode[0].split('$')[2:]]
			for i in range(0, len(params)):
				self.readLine(paramStrings[i] + " = " + str(params[i]) + ';')
		for line in funcCode:
			self.readLine(line)
			if 'return' in line:
				rest = line.replace('return', '')[:-1]
				return Variable.Variable(None, None, self.evalExpression(rest).value, None)

	def readLine(self, line):
		print(line)
		if line[0] == '$' and line[-1] == ';': #its a declare
			line = line[:-1]
			split = line.split()
			if split[2] != '=':
				raise Exception('Not a valid assign.')
			if split[0] not in castMap.keys() and split[0] not in self.structDict.keys():
				raise Exception('Not a valid type.')
			expr = split[3:]
			curStr = ''
			for exp in expr:
				curStr += exp
			print('banana', split)
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
			if split[0] not in self.varDicts[-1].keys() and split[0].strip('*') not in self.varDicts[-1].keys():
				raise Exception('Variable doesn\'t exist')
			self.assign(split[0], curStr)
		elif line == '{':
			self.scope += 1
			return line
		elif line == '}':
			self.scope -= 1
			self.scopeClear()
			return line

	def scopeClear(self):
		for var in varDicts[-1].keys():
			if self.scope < var.scope:
				varDicts[-1].pop(var)

	def assign(self, name, expression):
		#print("expression is", expression)
		if 'malloc' in expression:
			self.mallocParser(1, name, expression, mtype)
			return
		newValue = self.evalExpression(expression)
		#print("new value: ", newValue)
		if name[0] == '*' and name[1] != '*': #dereferencing 1x
			print(name)
			self.heapDict[(self.varDicts[-1][name[1:]]).value][0] = Variable.Variable(None, None, newValue.value, None)
#			self.heapDict[(self.varDicts[-1][name[1:]]).value][0].value = newValue.value
		# TODO implement dereferencing 2x or more
		else:
			var = self.varDicts[-1][name]
			var.value = newValue.value
			self.varDicts[-1].update({name : var})

	def declare(self, name, expression, mtype):
		#print('!!', name)
		if 'malloc' in expression:
			self.mallocParser(0, name, expression, mtype)
			return
		value = self.evalExpression(expression)
		scope = self.scope
		newVar = Variable.Variable(mtype, name, value.value, scope)
		self.varDicts[-1].update({name : newVar})

	def loop(self, line):
		"""
		Evaluates the given loop expression. Returns true if the loop guard is true.
		"""
		# case that it's a while loop
		if "while" in line:
			expression = line.search("(.*)", line)
			if (evalExpression(expression)): # guard is true
				return True
			else: # guard is false
				return False

		# case that it's a for loop
		else:
			initialization, guard, update = line.search("(.*)", line).strip(';')
			if (line, self.scope) not in self.loopList: # loop seen for first time, do initialization and guard
				self.loopList.append((line, self.scope))
				self.declare(initialization)
				if evalExpression(guard):
					return True
				else: # expression is false, pop loop from loopList
					self.loopList.remove(line, self.scope)
					return False

			else: # loop seen before, do update and guard
				self.assign(update)
				if evalExpression(guard):
					return True
				else: # expression is false, pop loop from loopDict and go to end of loop
					self.loopList.remove(line, self.scope)
					return False

	def mallocParser(self, flag, name, expression, type):
		#print("expr", expression)
		hasDigit = False
		for char in expression:
			if char.isdigit():
				#print("found digit")
				hasDigit = True
				break
		expression = expression.replace('malloc', '')
		expression = expression.replace('(', '')
		expression = expression.replace(')', '')
		expression = expression.replace('sizeof', '')
		expression = expression.replace(' ', '')
		expression = expression.split('*')
		struct = {}
		if not hasDigit: #not found digit
			print('no digit')
			size = 1
			type = expression[0]
			if type in self.structDict.keys():
				size = len(self.structDict[type])
				for fieldName in self.structDict[type].keys():
					struct[fieldName] = Variable.Variable('-', self.structDict[type][fieldName], None, self.scope)
				print("found type", struct)
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
			for i in range(int(size)):
				struct[str(i)] = Variable.Variable('-', type, None, self.scope) 
		self.heapDict[self.heapNum] = struct
		self.heapNum += 1
		if flag == 1: #assign
			obj = self.varDicts[-1][name.strip('*')]
			obj.value = self.heapNum - 1
			obj.type = '$P'
			obj.scope = self.scope
		else: #declare
			obj = Variable.Variable(str(name).strip('*'), '$P', self.heapNum - 1, self.scope)
			self.varDicts[-1][str(name).strip('*')] = obj
		return self.heapNum - 1

	def isValidAssign(self, line):
		hasType = False
		#print("line is: ", line)
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
			self.varDicts[-1][name.strip('*')] = obj
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
		#print(self.lines)
		return functions

	def getConditionalPositions(self):
		conditionals = []
		positions = []
		scope = 0
		# A "conditional block" starts with if and ends with last bracket of else,
		# and may have else ifs in between
		inConditionalBlock = False
		inLastBlock = False

		for i, line in enumerate(self.lines):
			if "if" in line and "else" not in line:
				inConditionalBlock = True
				positions.append(i)
			elif "else if" in line:
				positions.append(i)
			elif "else" in line and "if" not in line:
				inLastBlock = True
				positions.append(i)
			elif "{" in line:
				scope += 1
			elif "}" in line:
				scope -= 1
			elif "}" in line and inLastBlock and scope == 1:
				inConditionalBlock = False
				inLastBlock == False
				scope -= 1
				positions.append(i)
				conditionals.append(positions)

		return conditionals


	def getLoopPositions(self):
		"""
		Determines the location of all loops in the program and stores the
		value of the starting line and end line (last bracket) in a dictionary
		"""
		loops = {}
		start = 0
		scope = 0
		inLoop = False

		for i, line in enumerate(self.lines):
			if "for" in line or "while" in line:
				inLoop = True
				start = i
			if "{" in line and inLoop:
				scope += 1
			if "}" in line and inLoop:
				scope -= 1
				if scope == 0:
					inLoop = False
					loops[start] = i
		return loops

	def getStructs(self):
		"""
		This function will go to all the line numbers of all the functions in the program, and store only the lines
		pertaining to that function in a list. It will then map the function's name to the list of the function's lines.
		"""

		structs = {}
		print("here", self.lines)
		for i, line in enumerate(self.lines): #gets all the struct lines
			if line[:len('struct')] == 'struct' and line[-1] != ';':
				print(line)
				split = line.split()
				structName = split[1]
				count = 0
				fields = {}
				for line in self.lines[i + 1:]:
					if line == '{':
						count += 1
					elif line == '}':
						count -= 1
						if count == 0:
							break
					if line[0] == '$':
						line = line[:-1]
						fieldName = line.split()[1]
						type = line.split()[0]
						fields[fieldName] = type
				structs[structName] = fields
		return structs

	def typedefSearch(self):
		print("chief", self.structDict)
		for line in self.lines:
			if 'typedef' == line[:len('typedef')]:
				split = line.split()
				mid = ''
				for string in split[1:-1]:
					mid += string + ' '
				mid = mid[:-1] 
				self.structDict['$' + split[-1][:-1]] = self.structDict.pop(split[-2])
		print("chief", self.structDict)
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
		progLines = [x.strip() for x in progLines]
		progLines = [x for x in progLines if x != '']
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
		#print("params", params)
		return params

	def evalExpression(self, s):
		#print("evaling: ", s)
		valueStack = []
		operatorStack = []
		for x in spacedOperators:
			s = s.replace(x, " "+x+" ")
		tokens = s.split()
		#print('tokens: ', tokens)
		print('varDicts', self.varDicts[-1])
		y = 0
		while y < len(tokens):
			#print y, tokens[y], operatorStack, valueStack
			token = tokens[y]
			if stringIsInt(token):
				valueStack.append(Variable.Variable(None, None, int(token), None))
			#if token in ['true', 'false']:
			#	valueStack.append(Variable.Variable(None, '$B', token=='true', None)) 
			elif token in self.varDicts[-1].keys():
				valueStack.append(self.varDicts[-1][token])
			elif token[1:] in self.varDicts[-1].keys() and token[0] == "*" and token[1] != '*': #dereferencing
				print("deref!")
				valueStack.append(self.heapDict[(self.varDicts[-1][token[1:]]).value][0])
			elif token.strip('*') in self.varDicts[-1].keys() and token[0] == "*": #dereferencing more than once
				print("deref! multiple!")
				valueStack.append(self.heapDict[self.evalExpression(token[1:]).value][0])
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
		print("returning", valueStack[0])
		return valueStack[0]

p = Program('cfile.txt')
print(p.getFuncValue('main', []).value)
