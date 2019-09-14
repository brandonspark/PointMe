funcDict = {'main': ['$I main()', '{', '$I y = 1;', '$I x = y + 2;', '$S z = "hi there\n";', 'return f(x);', '}'], 'f': ['$I f($I x, $I y)', '{', 'return x + y +5;', '}']}
import string
import evalexpression
varDicts = []

def declare(x):
	return 0
def readLine(x):
	return 0

def getFuncValue(funcName, params):
	varDicts.append([])
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

def ret(line):
	rest = line.replace('return', '')[:-1]
	print(rest)
	print(evalexpression.evalExpression(rest))
	raise ValueError((evalexpression.evalExpression(rest)))

print(getFuncValue('f', [1,2]))
print(getFuncValue('main', []))