from AST import *



def un_parse(node):

    un_parse_str = ""

    if isinstance(node, ASTree):
        un_parse_str += un_parse(node.module)

    if isinstance(node, Module):
        for child_node in node.body:
            un_parse_str += un_parse(child_node)

    if isinstance(node, BinOp):
        if isinstance(node.op, Add):
            op_str = "+"
        elif isinstance (node.op, Sub):
            op_str = "-"
        un_parse_str += un_parse(node.left) + f" {op_str} (" + un_parse(node.right) + ")"
    
    if isinstance(node, UnaryOp):
        un_parse_str += "-(" + un_parse(node.operand) + ")"

    if isinstance(node, Expr):
        un_parse_str += (un_parse(node.value) + "\n")
    
    if (isinstance(node, Assign)):
        un_parse_str += (node.targets[0].id + " = " + un_parse(node.value) + "\n")

    if (isinstance(node, Name)):
        un_parse_str += node.id

    if isinstance(node, Constant):
        un_parse_str += str(node.value)
    
    if isinstance(node, USub):
        un_parse_str += "-"

    if (isinstance(node, Call)):
        un_parse_str += node.func.id + "(" + un_parse_fun_args(node.args) + ")"

    
    return un_parse_str
    

def un_parse_fun_args(args):
    un_parse_str = ""
    for arg in args:
        un_parse_str += (un_parse(arg) + ", ")
    return un_parse_str[:-2]

