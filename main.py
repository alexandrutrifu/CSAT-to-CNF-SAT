import sys
from tree import TreeNode, sat_form, de_morgan

root = None


def parse_input():
	inputs = 0
	info_list = []

	with open(sys.argv[1], "r") as input_file:
		for line in input_file:
			arguments = line.split()

			if inputs == 0:
				inputs = int(arguments[0])
				output = int(arguments[1])

				TreeNode.root = TreeNode(output)
			else:
				info_list.append(arguments)

	for node in info_list[::-1]:
		current_index = int(node[-1])
		target = TreeNode.find_by_index(TreeNode.root, current_index)

		target.gate_type = node[0]  # Assign gate type

		for child_index in node[1:-1]:
			target.add_child(int(child_index))

	return info_list


if __name__ == "__main__":
	info_list = parse_input()  # List of node details extracted from input file

	# TreeNode.traverse(TreeNode.root)

	sat_form = TreeNode.get_sat_form(TreeNode.root)

	with open("output.txt", "w") as output:
		output.write(str(sat_form))

	# list1 = ['NOT', [['NOT', 1], 'OR', ['NOT', 2]]]
	# print(de_morgan(list1))
