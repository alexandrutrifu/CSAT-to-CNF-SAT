import sys
from tree import TreeNode, sat_form, de_morgan
from sat_transforms import sat_to_cnf, print_sat

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


if __name__ == "__main__":
	[i, n] = parse_input()  # List of node details extracted from input file

	# TreeNode.traverse(TreeNode.root)

	sat_form = TreeNode.get_sat_form(TreeNode.root)
	# print(sat_form)

	with open("output.txt", "w") as output:
		output.write(str(sat_to_cnf(sat_form)))

	print(sat_to_cnf(sat_form))
	print("")
	print_sat(sat_to_cnf(sat_form))

	# print("Variabile suplimentare de la " + str(n + 1))
	# print(sat_to_cnf(sat_form, n + 1))

	# list1 = ['NOT', [['NOT', 1], 'OR', ['NOT', 2]]]
	# print(de_morgan(list1))
