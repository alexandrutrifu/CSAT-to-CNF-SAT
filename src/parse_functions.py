import sys
from tree import TreeNode


def parse_input():
	inputs = 0
	no_nodes = 0
	info_list = []

	with open(sys.argv[1], "r") as input_file:
		for line in input_file:
			arguments = line.split()

			if inputs == 0:
				inputs = int(arguments[0])
				no_nodes = int(arguments[1])

				TreeNode.root = TreeNode(no_nodes)
			else:
				info_list.append(arguments)

	for node in info_list[::-1]:
		current_index = int(node[-1])
		target = TreeNode.find_by_index(TreeNode.root, current_index)

		target.gate_type = node[0]  # Assign gate type

		for child_index in node[1:-1]:
			target.add_child(int(child_index))

	return [inputs, no_nodes]


def print_sat(sat, output):
	if len(sat) != 1:
		for index in range(1, len(sat), 2):
			operator = sat[index]  # Index of current operator

			# Check if operands are single variables
			if index == 1:
				if type(sat[index - 1]) is list:
					print_sat(sat[index - 1], output)
				else:
					output.write(str(sat[index - 1]))
					output.write(" ")

			if operator == "AND":
				output.write("0\n")

			if type(sat[index + 1]) is list:
				print_sat(sat[index + 1], output)
			else:
				output.write(str(sat[index + 1]))
				output.write(" ")


def get_var_number(sat):
	args = []
	clause_number = 0

	for arg in sat[::2]:
		clause_number += 1
		if type(arg) is list:
			for little_arg in arg[::2]:
				if args.count(little_arg) == 0:
					args.append(little_arg)
					args.append(-little_arg)
		else:
			if args.count(arg) == 0:
				args.append(arg)
				args.append(-1 * arg)

	return [max(args), clause_number]
