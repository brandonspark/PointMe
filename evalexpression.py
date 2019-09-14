def getListOfVarNames():
	return ["x","y"]
def getVarValue(s):
	if s == "x":
		return 1
	elif s == "y":
		return -2
def getFuncValue(fname, params):
	return len(params)

operators = ["+","-","*","/","(",")","=="]
precedence = {"*":5, "/":5, "+":3, "-":3,"==":1,"(":-1}
varNames = getListOfVarNames()
funcNames = ["f"]

def stringIsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def applyOperator(op, v1, v2):
	if op in operators:
		return eval(str(v2)+str(op)+str(v1))

def evalFunctionParams(s):
	s = s[1:-1] #removes the open and close parentheses around the parameters
	s = s.split(",")
#	print(s)
	params = []
	for param in s:
		params.append(evalExpression(param))
#	print params
	return params

def evalExpression(s):
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
			valueStack.append(int(token)) 
		elif token in varNames:
			valueStack.append(getVarValue(token))
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
		elif token in funcNames:
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
					valueStack.append(getFuncValue(token, evalFunctionParams(paramstring)))
					break
		y += 1
	while len(operatorStack) != 0:
		x = operatorStack.pop()
		v1 = valueStack.pop()
		v2 = valueStack.pop()
		valueStack.append(applyOperator(x, v1, v2))		
	return valueStack[0]

'''
int x = 1
int y = -2
'''
s = "f(7) * f(1, 2, 3*3+2/4) + 14/7*2"

print evalExpression(s)