class Variable:

	def __init__(self, type, value, scope):
		self.type = type
		self.value = value
		self.scope = scope # if variableScope > functionScope, this var should be deleted