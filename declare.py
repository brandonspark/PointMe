# Creates a new variable from the given expression and stores it to varDict
def declare(expression):
	sidesOfExpression = expression.split('=')
	type = sidesOfExpression[0][0:1]
	name = sidesOfExpression[0][3:].rstrip()
	value = evalExpression(sidesOfExpression[1])
	scope = # TODO: find out where to get this!
	newVar = Variable(type, name, value, scope)

	varDict[-1].update({name : newVar})