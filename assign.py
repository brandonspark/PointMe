# Updates the variable in the expression and updates the varDict
def assign(name, expression):
	expressionSplit = expression.split('=')
	newValue = evalExpression(expressionSplit[1])
	
	var = varDict[-1][name]
	var.value = newValue
	varDict[-1].update({name : var})