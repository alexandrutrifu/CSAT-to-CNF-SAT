from tree import TreeNode

# big_formula = TreeNode.get_sat_form(TreeNode.root)
extra_var = 0
final_sat = ""


def only_conjunctions(operand):
	if operand.index("OR") >= 0:
		# Check if items are single variables; if not, step in deeper
		return False


# def cleanup_sat(sat: list):
# 	global final_sat
#
# 	if len(sat) != 1:
# 		for index in range(1, len(sat), 2):
# 			operator = sat[index]
#
# 			if type(sat[index - 1]) is list:
# 				cleanup_sat(sat[index - 1])
#
# 			if type(sat[index + 1]) is list:
# 				cleanup_sat(sat[index + 1])
#
# 			if operator == "OR":
# 				final_sat += "(" + str(sat[index - 1]) + " " + operator + " " + str(sat[index + 1]) + ")"
# 			else:
# 				final_sat += str(sat[index - 1]) + " " + operator + " " + str(sat[index + 1])
#
# 	print(final_sat)

def print_sat(sat):
	if len(sat) != 1:
		for index in range(1, len(sat), 2):
			operator = sat[index]  # Index of current operator

			# Check if operands are single variables
			if index == 1:
				if type(sat[index - 1]) is list:
					print_sat(sat[index - 1])
				else:
					print(sat[index - 1], end=" ")

			if operator == "AND":
				print()

			if type(sat[index + 1]) is list:
				print_sat(sat[index + 1])
			else:
				print(str(sat[index + 1]), end=" ")


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
			if index == 1:
				if type(sat[index - 1]) is list:
					sat_to_cnf(sat[index - 1])

			if type(sat[index + 1]) is list:
				sat_to_cnf(sat[index + 1])

			if operator == "OR":
				sat[index] = "AND"

				if type(sat[index - 1]) is list:
					for p in range(1, len(sat[index - 1]), 2):
						if sat[index - 1][p] == "AND":
							if p == 1:
								if type(sat[index - 1][p - 1]) is list:
									sat[index - 1][p - 1].append("OR_done")
									sat[index - 1][p - 1].append(extra_var)
								else:
									sat[index - 1][p - 1] = [sat[index - 1][p - 1], "OR_done", extra_var]
							if type(sat[index - 1][p + 1]) is list:
								sat[index - 1][p + 1].append("OR_done")
								sat[index - 1][p + 1].append(extra_var)
							else:
								sat[index - 1][p + 1] = [sat[index - 1][p + 1], "OR_done", extra_var]
						else:
							sat[index - 1].append("OR_done")
							sat[index - 1].append(extra_var)
				else:
					sat[index - 1] = [sat[index - 1], "OR_done", extra_var]

				if type(sat[index + 1]) is list:
					for p in range(1, len(sat[index + 1]), 2):
						if sat[index + 1][p] == "AND":
							if p == 1:
								if type(sat[index + 1][p - 1]) is list:
									sat[index + 1][p - 1].append("OR_done")
									sat[index + 1][p - 1].append(-extra_var)
								else:
									sat[index + 1][p - 1] = [sat[index + 1][p - 1], "OR_done", -extra_var]
							if type(sat[index + 1][p + 1]) is list:
								sat[index + 1][p + 1].append("OR_done")
								sat[index + 1][p + 1].append(-extra_var)
							else:
								sat[index + 1][p + 1] = [sat[index + 1][p + 1], "OR_done", -extra_var]
						else:
							sat[index + 1].append("OR_done")
							sat[index + 1].append(extra_var)
				else:
					sat[index + 1] = [sat[index + 1], "OR_done", -extra_var]

				extra_var += 1

	return sat


def collapse_conjunctions(sat):
	if len(sat) != 1:
		for index in range(1, len(sat), 2):
			operator = sat[index]  # Index of current operator

			if operator == "AND":
				# Check if operands are single variables
				if index == 1:
					if type(sat[index - 1]) is list:
						for j in range(1, len(sat[index - 1]), 2):
							if sat[index - 1][j] == "AND":
								new_sat = []
								for i in range(3):
									new_sat.append(sat[index - 1][i])
								new_sat.append(operator)
								for i in range(index + 1, len(sat)):
									new_sat.append(sat[i])

								return collapse_conjunctions(new_sat)

				if type(sat[index + 1]) is list:
					for j in range(1, len(sat[index + 1]), 2):
						if sat[index + 1][j] == "AND":
							new_sat = []
							for i in range(0, index):
								new_sat.append(sat[i])
							new_sat.append(operator)
							for i in range(3):
								new_sat.append(sat[index + 1][i])
							for i in range(index + 2, len(sat)):
								new_sat.append(sat[i])

							return collapse_conjunctions(new_sat)

			if type(sat[index - 1]) is list:
				sat[index - 1] = collapse_conjunctions(sat[index - 1])
			if type(sat[index + 1]) is list:
				sat[index + 1] = collapse_conjunctions(sat[index + 1])
	return sat
