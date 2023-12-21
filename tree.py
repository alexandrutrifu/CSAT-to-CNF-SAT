sat_form = []


def de_morgan(operand: list or str):
	if type(operand) is not list:  # Single variable
		match operand:
			case "AND":
				return "OR"
			case "OR":
				return "AND"
		return ["NOT", operand]

	# List of operands
	for item in operand:
		if item == "NOT":
			return operand[1]

		operand[operand.index(item)] = de_morgan(item)

	return operand


class TreeNode:
	root = None

	def __init__(self, index: int):
		self.gate_type = "Leaf"
		self.value = 0
		self.index = index

		self.children = []

	def add_child(self, index: int):
		""" Search for child node index and update caller's children list

		:param index:
		:return:
		"""
		child = TreeNode.find_by_index(TreeNode.root, index)

		self.children.append(child if child is not None else TreeNode(index))

	def remove_child(self, node):
		self.children.remove(node)

	@staticmethod
	def traverse(root: "TreeNode"):
		if root is None:
			return None

		print(root.index, root.gate_type)

		for node in root.children:
			TreeNode.traverse(node)

	@staticmethod
	def find_by_index(node: "TreeNode", index):
		""" Searches for the indexed node

		:param node: Current node
		:param index: Index of required node
		:return:
		"""
		if node is None:
			return None

		if node.index == index:
			return node

		for child in node.children:
			if result := TreeNode.find_by_index(child, index):
				return result

	@staticmethod
	def get_sat_form(node: "TreeNode"):
		# If current node is a leaf, return SAT index variable
		if node.gate_type == "Leaf":
			return node.index

		match node.gate_type:
			case "AND":
				and_output = []

				for child in node.children:
					and_output.append(TreeNode.get_sat_form(child))
					and_output.append("AND")
				and_output.pop()

				return and_output
			case "OR":
				or_output = []

				for child in node.children:
					or_output.append(TreeNode.get_sat_form(child))
					or_output.append("OR")
				or_output.pop()

				return or_output
			case "NOT":
				# Apply DeMorgan
				lower_output = TreeNode.get_sat_form(node.children[0])

				return de_morgan(lower_output)

