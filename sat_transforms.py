from tree import TreeNode

# big_formula = TreeNode.get_sat_form(TreeNode.root)
extra_var = 0


def only_conjunctions(operand):
	if operand.index("OR") >= 0:
		# Check if items are single variables; if not, step in deeper
		return False


def sat_to_cnf(sat: list or str):
	""" Treat formula based on number of operands:
	- length == 1 -> single variable
	- length == 3 -> conjunction/disjunction

	:param sat: SAT formula
	:return:
	"""
	global extra_var

	if extra_var == 0:
		extra_var = TreeNode.root.index + 1

	if len(sat) != 1:
		for index in range(1, len(sat), 2):
			operator = sat[index]  # Index of current operator

			# Check if operands are single variables
			if type(sat[index - 1]) is list:
				sat_to_cnf(sat[index - 1])

			if type(sat[index + 1]) is list:
				sat_to_cnf(sat[index + 1])

			if operator == "OR":
				sat[index] = "AND"

				sat[index - 1] = [sat[index - 1], "OR_done", extra_var]

				sat[index + 1] = [sat[index + 1], "OR_done", -extra_var]

				extra_var += 1

	return sat

