import sys
from tree import TreeNode, sat_form, de_morgan
from sat_transforms import sat_to_cnf, collapse_conjunctions
from parse_functions import *

root = None


if __name__ == "__main__":
	[i, n] = parse_input()  # List of node details extracted from input file

	sat_form = TreeNode.get_sat_form(TreeNode.root)
	sat_form = collapse_conjunctions(sat_form)
	sat_form = sat_to_cnf(sat_form)
	sat_form = collapse_conjunctions(sat_form)

	[arg_number, clause_number] = get_var_number(sat_form)

	with open(sys.argv[2], "w") as output:
		output.write(f"p cnf {arg_number} {clause_number}\n")
		print_sat(collapse_conjunctions(sat_form), output)
		output.write("0")
