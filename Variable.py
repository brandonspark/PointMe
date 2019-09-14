class Variable:

	def __init__(self, name, mtype, value, scope):
		self.name = name
		self.type = mtype
		self.value = value
		self.scope = scope # if variableScope > functionScope, this var should be deleted