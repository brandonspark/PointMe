import numpy as np
#from evalexpression import *
import Variable
import string
import re
import shlex
import copy

functionTypes = ['$I', '$S', '$B', '$F', '$D', '$V', '$L']
actualTypes = ['int', 'string', 'char', 'bool', 'float', 'double', 'long']
typeMap = [('int', '$I'), ('string', '$S'), ('bool', '$B'), ('float', '$F'), ('double', '$D'), ('void', '$V'), ('long', '$L')]
typeMap2 = {'$I': 'int', '$S': 'string', '$B': 'bool', '$F': 'float', '$D': 'double', '$L': 'long'}
castMap = {'$I': type(5), '$S': type(''), '$B': type(True), '$F': type(1.1), '$D': type(1.1), '$L': type(1)}

operators = ["+","-","*","/","(",")","==",'>>','<<','<', '>','>=','<=','!=']
opReturns = {'+': '$I', '-': '$I', '*': '$I', '/': '$I', '==': '$B', '>>': '$I', '<<': '$I','<':'$B','>':'$B','>=':'$B','<=':'$B','!=':'$B'}
spacedThings = ["+","/","(",")","==",'>>','<<','>=','<=','!=','[',']','->']
precedence = {"*":5, "/":5, "+":3, "-":3,"==":1,"(":-1,'>>':4,'<<':4,'<':1,'>':1,'>=':1,'<=':1,'!=':2}

def stringIsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def applyOperator(op, v1, v2):
	if op in operators:
		#print("types: ", (v1.type), v2.type)
		if v1.type == '$I' or v1.type == '$B':
			#print("evaluating", (str(v2.value)+op+str(v1.value)))
			return Variable.Variable(None, opReturns[op], castMap[v1.type](eval(str(v2.value)+op+str(v1.value))), None)
		elif v1.type == '$S':
			return Variable.Variable(None, opReturns[op], castMap[v1.type](eval("'"+str(v2.value)+"'"+op+"'"+str(v1.value)+"'")), None)

def concat(l):
	newStr = ''
	for string in l:
		newStr += string
	return newStr

def skipToBraceLevel (braceLevel, y, funcCode):
	i = braceLevel
	braceLevel += 1
	y += 2
	while braceLevel != i:				
		thisLine = funcCode[y]
		#print("this in if", braceLevel, i, thisLine, y)
		if '{' in thisLine:
			braceLevel += 1
		#	print("bracelevel went up to", braceLevel)
		if '}' in thisLine:
			braceLevel -= 1
		#	print("bracelevel went down to", braceLevel)
		y += 1
	return y

class Program():
	def __init__(self, cfile):
		"""
		Initializes all the program data.
		"""
		self.lines = self.splitLines(self.cleanText(self.readText(cfile)))
		print(self.lines)
		self.shortenTypes()
		self.loopPositions = self.getLoopPositions() # key: line number of start of loop, value: line number of end of loop
		self.loopPositionsReverse = {v: k for k, v in self.loopPositions.items()} # key, value switched from loopPositions
		self.loopList = [] # stores tuple (line, scope) that contains for loops we are currently inside
		self.varDicts = [{}]
		self.structDict = self.getStructs()
		self.typedefSearch()
		for type in self.structDict.keys():
			type = type[1:]
			for i, line in enumerate(self.lines):
				line = line.replace(type, '$' + type)
				self.lines[i] = line
			functionTypes.append('$' + type)
		self.funcDict = self.getFunctions()
		print('after replace', self.structDict)
		self.loopPositions = self.getLoopPositions() # key: line number of start of loop, value: line number of end of loop
		self.loopPositionsReverse = {v: k for k, v in self.loopPositions.items()} # key, value switched from loopPositions
		self.loopList = [] # stores tuple (line, scope) that contains "for" loops we are currently inside
		self.conditionalPositions = self.getConditionalPositions()
		self.varDicts = [{}]
		self.funcDict = self.getFunctions()
		self.scope = 0
		self.heapDict = {}
		self.heapNum = 0

		#self.mallocParser(0, '*x', 	'malloc(sizeof(myStruct))', '$I')
		print('ourlines', self.lines)
		print(self.heapDict)
		print(self.heapNum)
		print('current heap', self.heapDict)
		print('cond', self.conditionalPositions)
		f = open('output.txt', 'w')
		for i, line in enumerate(self.lines):
			f.write(line + '\n')
		print(self.conditionalPositions)
		print("woah")
		#print("hello", self.lines)
		#print("func", self.funcDict)
		#self.readLine('for($I i = 0;')
		print('var', self.varDicts[-1])
		print('heap', self.heapDict)
		print('func', self.funcDict)

	def findMain(self):
		for i, line in enumerate(self.lines):
			if 'main' in line:
				return i

	def getFuncValue(self, funcName, params):
		print("=----------------starting funcion", funcName)
		funcCode = self.funcDict[funcName]
		returnType = funcCode[0].split()[0]
		numParams = len(funcCode[0].split(','))
		#print("num params", numParams)
		if len(params) != 0:
			print("declaring params")
			paramStrings = ['$' + (param.translate(str.maketrans('', '', string.punctuation)).strip()) for param in funcCode[0].split('$')[2:]]
			for i in range(0, len(params)):
				self.readLine(paramStrings[i] + " = " + str(params[i]) + ';')
		
		nowCopy = copy.deepcopy(self.varDicts[-1])
		self.varDicts.append(nowCopy)
		print("--------------------------------------------------------------------",self.varDicts[-1])
		
		braceLevel = 0
		loopBraceLevels = {}
		y = 0
		while y < len(funcCode):
			#print('=-----line', y, funcCode[y], self.scope, self.varDicts[-1])
			line = funcCode[y]
			if 'pstat' in line:
				print("pstat:\n", self.varDicts[-1])
				print(self.heapDict)
				print(self.scope)
				print(self.funcDict)
				1/0
			if '{' in line:
				braceLevel += 1
			if '}' in line:
				braceLevel -= 1
				if braceLevel in loopBraceLevels.keys(): #i.e. we're at the end of the loop
					print("Were at end of loop")
					loopGuard, linenum = loopBraceLevels[braceLevel]
					print(loopGuard)
					print(self.varDicts[-1])
					loopGuardTruthValue = self.evalExpression(loopGuard)
					if loopGuardTruthValue.value == 1:
						print("loop guard is true")
						print(funcCode[linenum+1])
						y = linenum+1
						print('lime', line)
						self.readLine(line)
						continue
			if 'return' in line:
				rest = line.replace('return', '')[:-1]
				print("i am returning the evaluation of", rest)
				print("helloooooooooooooooooo", self.varDicts)
				return self.evalExpression(rest)
			elif 'while' in line:
				loopGuard = self.evalExpression(line[6:])
				loopBraceLevels[braceLevel] = (line[6:], y)
				if not loopGuard:
					i = braceLevel
					y += 1
					while braceLevel != i:
						thisline = funcCode[y]
						if '{' in thisLine:
							braceLevel += 1
						if '}' in thisLine:
							braceLevel -= 1
						y += 1
				else: #loop guard true, only happens the first time thru
					pass
			elif 'if' in line:
				print("its an if!\n\n\n")
				ifCondTruthValue = self.evalExpression(line[2:]).value
				if ifCondTruthValue:
					pass
				else:
					y = skipToBraceLevel(braceLevel, y, funcCode)
					print("skipping to line: ", y, funcCode[y])
					if 'else' in funcCode[y]:
						y += 1
					y -= 1
			elif 'else' in line:
				print("it's an else that i want to skip!")
				y = skipToBraceLevel(braceLevel, y, funcCode)
				print("skipping to line: ", y, funcCode[y])
				y -= 1
			elif 'free' in line:
				rest = line.replace('free(', '')[:-2]
				#print("the thing to be freed is: ", rest)
				self.heapDict[self.varDicts[-1][rest].value] = None
				self.varDicts[-1][rest].value = None
				#print("the heap after freeing is", self.heapDict)
				#print("the stack after freeing is", self.varDicts[-1])
			self.readLine(line)
			#self.varDicts.pop()
			y += 1
		self.varDicts.pop()

	def readLine(self, line):
		if line[0] == '$' and line[-1] == ';': #its a declare
			line = line[:-1]
			split = shlex.split(line,posix=False)
			if split[2] != '=':
				raise Exception('Not a valid assign.')
			if split[0] not in castMap.keys() and split[0] not in self.structDict.keys():
				raise Exception('Not a valid type.')
			expr = split[3:]
			curStr = ''
			for exp in expr:
				curStr += exp
			print('declare this', split[1], curStr, split[0])
			self.declare(split[1], curStr, split[0])
		elif line[0] == '$' and line[-1] == ')': #its a function!
			#do some function magic here
			None
		elif '=' in line and line[-1] == ';': #tentatively, this is a assign
			line = line[:-1]
			split = line.split()
			if split[1] != '=':
				print("split:", split)
				#pass
				raise Exception('Not a valid assign.')
			expr = split[2:]
			curStr = ''
			for exp in expr:
				curStr += exp
			if split[0] not in self.varDicts[-1].keys() and split[0].strip('*') not in self.varDicts[-1].keys():
				pass
			self.assign(split[0], curStr)
		elif line == '{':
			self.scope += 1
		elif line == '}':
			self.scope -= 1
			#print('about to scope clear', self.scope, line, self.varDicts)
			self.scopeClear()
		else:
			print("******************************************************** THERE IS A LINE I DONT KNOW HOW TO PROCESS")
	
	def scopeClear(self):
		if len(self.varDicts[-1].keys()) == 0:
			return
		print('aout to clear', self.scope, self.varDicts[-1])
		for var in self.varDicts[-1].copy().keys():
			if self.scope < self.varDicts[-1][var].scope:
				self.varDicts[-1].pop(var)
		print('after clear', self.scope, self.varDicts[-1])

	def assign(self, name, expression):
		print("assign expression is", expression)
		if 'malloc' in expression:
			self.mallocParser(1, name, expression, mtype)
			return
		newValue = self.evalExpression(expression)
		#print("new value: ", newValue)
		#if name[0] == '*' and name[1] != '*': #dereferencing 1x
		#	print(name)
		#	self.heapDict[(self.varDicts[-1][name[1:]]).value]['0'] = Variable.Variable(None, None, newValue.value, None)
		# TODO implement dereferencing 2x or more
		if '*' in name or '[' in name or '->' in name:
			self.evalExpression(name).value = self.evalExpression(expression).value
			print("assigned to: ", self.heapDict)
		else:
			var = self.varDicts[-1][name.strip('*')]
			var.value = newValue.value
			self.varDicts[-1].update({name.strip('*') : var})

	def declare(self, name, expression, mtype):
		#print('!!', name)
		name = name.strip('*')
		print('declare', name, expression, mtype)
		if 'malloc' in expression:
			self.mallocParser(0, name, expression, mtype)
			return
		value = self.evalExpression(expression)
		scope = self.scope
		newVar = Variable.Variable(name.strip('*'), mtype, value.value, scope)
		self.varDicts[-1].update({name.strip('*') : newVar})

	def loop(self, cond):
		"""
		Return true if the given condition is true.
		"""
		return self.evalExpression(cond)

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
			size = 1
			type = expression[0]
			if type in self.structDict.keys():
				size = len(self.structDict[type])
				for fieldName in self.structDict[type].keys():
					struct[fieldName] = Variable.Variable('-', self.structDict[type][fieldName], None, self.scope)
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
			print('name', name)
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
			print(line, flag)
			if flag:
				functions[header.strip('*')] = i
			print(functions)
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

		currentBlock = {}
		pair = []
		stack = []
		for i, line in enumerate(self.lines):
			if "if" in line and "else" not in line:
				if inConditionalBlock: #we were in the middle of another if
					stack.append((currentBlock, pair))
					pair = []
					inConditionalBlock = True
					pair.append(i)
				else:
					inConditionalBlock = True
					pair.append(i)
			elif "else if" in line and inConditionalBlock:
				pair.append(i)
			elif "else" in line and "if" not in line and inConditionalBlock:
				inLastBlock = True
				pair.append(i)
			elif "{" in line:
				scope += 1
			elif '}' in line:
				scope -= 1
				if "}" in line and inConditionalBlock and not inLastBlock: 
					pair.append(i)
					currentBlock[pair[0]] = pair[1]
					pair = []
					if 'else if' not in self.lines[i + 1] and 'else' not in self.lines[i + 1]: #its the last
						print("no go")
						inConditionalBlock = False
						if len(stack) != 0:
							inConditionalBlock = True
							currentBlock, pair = stack.pop()
						return
				elif inLastBlock and inConditionalBlock: 
					inConditionalBlock = False
					inLastBlock == False
					scope -= 1
					currentBlock[pair[0]] = i
					pair = []
					conditionals.append(currentBlock)
					currentBlock = {}

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
				for j, line in enumerate(self.lines[i:]):
					if "{" in line and inLoop:
						scope += 1
					if "}" in line and inLoop:
						scope -= 1
						if scope == 0:
							inLoop = False
							loops[start] = i + j
		return loops

	def getStructs(self):
		"""
		This function will go to all the line numbers of all the functions in the program, and store only the lines
		pertaining to that function in a list. It will then map the function's name to the list of the function's lines.
		"""

		structs = {}
		for i, line in enumerate(self.lines): #gets all the struct lines
			if line[:len('struct')] == 'struct' and line[-1] != ';':
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
					else: 
						line = '$' + line
						line = line[:-1]
						fieldName = line.split()[1].strip('*')
						type = line.split()[0]
						fields[fieldName] = type
				structs[structName] = fields
		return structs

	def typedefSearch(self):
		for line in self.lines:
			if 'typedef' == line[:len('typedef')]:
				split = line.split()
				mid = ''
				for string in split[1:-1]:
					mid += string + ' '
				mid = mid[:-1] 
				self.structDict['$' + split[-1][:-1]] = self.structDict.pop(split[-2])

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
		print('funtypes', functionTypes)
		for type in functionTypes:
			if string[:len(type)] == type and string[-1] == ')':
				leftIndex = string.find('(')
				return True, string[len(type) + 1: leftIndex]
		return False, None

	def evalFunctionParams(self, s):
		if s == "()":
			return []
		s = s[1:-1] #removes the open and close parentheses around the parameters
		s = s.split(",")
		params = []
		for param in s:
			params.append(self.evalExpression(param).value)
		#print("params", params)
		return params

	def evalExpression(self, s):
		print("evaling: ", s)
		valueStack = []
		operatorStack = []
		for x in spacedThings:
			s = s.replace(x, " "+x+" ")
		tokens = shlex.split(s,posix=False)
		print('tokens: ', tokens)
		#print('varDicts', self.varDicts[-1])
		y = 0
		while y < len(tokens):
			print(y, tokens[y], operatorStack, valueStack, self.varDicts[-1])
			token = tokens[y]
			#print(token)
			if stringIsInt(token):
				valueStack.append(Variable.Variable(None, '$I', int(token), None))
			elif token in ['true', 'false']:
				valueStack.append(Variable.Variable(None, '$B', token=='true', None)) 
			elif token == 'NULL':
				valueStack.append(Variable.Variable(None, '$P', None, None))
			elif (token[0] == '"' and token[-1] == '"') or (token[0] == "'" and token[-1] == "'"):
				#print("added string", token)
				valueStack.append(Variable.Variable(None, '$S', token[1:-1], None))
			elif token in self.varDicts[-1].keys():
				valueStack.append(self.varDicts[-1][token])
			elif token[1:] in self.varDicts[-1].keys() and token[0] == "*" and token[1] != '*': #dereferencing
				#print("deref!")
				valueStack.append(self.heapDict[(self.varDicts[-1][token[1:]]).value]['0'])
			elif token.strip('*') in self.varDicts[-1].keys() and token[0] == "*": #dereferencing more than once
				#print("deref! multiple!")
				valueStack.append(self.heapDict[self.evalExpression(token[1:]).value]['0'])
			elif token == "[": #indexing into array
				array = valueStack.pop()
				indexexpr = ""
				print(self.heapDict)
				for nexttoken in tokens[y+1:]:
					if nexttoken == "]":
						valueStack.append(self.heapDict[array.value][str(self.evalExpression(indexexpr).value)])
						break
					indexexpr += nexttoken
					y += 1
			elif token == '->':
				y += 1
				array = valueStack.pop()
				structfield = tokens[y]
				valueStack.append(self.heapDict[array.value][str(structfield)])
				print("struct field: ", structfield)
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
		#print("------", self.varDicts[-1])
		print("heap", self.heapDict)
		print("returning", valueStack)
		return valueStack[0]

p = Program('cstack.txt')
print(p.getFuncValue('main', []).value)
print("=----------------------------------")
print('after', p.scope)
print('var', p.varDicts[-1])