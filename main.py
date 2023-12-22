import sys
from tree import TreeNode, sat_form, de_morgan
from sat_transforms import sat_to_cnf, collapse_conjunctions

root = None


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
				output.write("\n")

			if type(sat[index + 1]) is list:
				print_sat(sat[index + 1], output)
			else:
				output.write(str(sat[index + 1]))
				output.write(" ")


if __name__ == "__main__":
	[i, n] = parse_input()  # List of node details extracted from input file

	# TreeNode.traverse(TreeNode.root)

	sat_form = TreeNode.get_sat_form(TreeNode.root)
	sat_form = collapse_conjunctions(sat_form)
	sat_form = sat_to_cnf(sat_form)
	sat_form = collapse_conjunctions(sat_form)

	with open(sys.argv[2], "w") as output:
		print_sat(collapse_conjunctions(sat_form), output)
