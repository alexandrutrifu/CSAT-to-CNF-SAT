from tree import TreeNode

big_formula = TreeNode.get_sat_form(TreeNode.root)


def only_conjunctions(operand):
	if operand.index("OR") >= 0:
		# Check if items are single variables; if not, step in deeper
		return False


def sat_to_cnf(sat: list or str, relation: str, extra_var: int, index: int, negated: int):
	""" Treat formula based on number of operands:
	- length == 1 -> single variable
	- length == 3 -> conjunction/disjunction

	:param negated:
	:param index:
	:param extra_var:
	:param relation:
	:param sat: SAT formula
	:return:
	"""

	if type(sat) is int:  # Single variable
		if relation == "OR":
			big_formula[index] = [sat, "AND", extra_var * negated]

	else:
		for operator in big_formula[1::2]:
			op_index = sat.index(operator)  # Index of current operator

			# Check if operands are single variables
			if type(sat[op_index - 1]) is list:
				sat_to_cnf(sat[index - 1], operator, extra_var, op_index - 1, 1)

			if type(sat[op_index + 1]) is list:
				sat_to_cnf(sat[index + 1], operator, extra_var, op_index + 1, -1)



