
from ASTree import *

def get_local_vars(node, vars=set()):

    if isinstance(node, ASTree):
        vars |= get_local_vars(node.module, vars)
    
    elif isinstance(node, Module):
        vars |= get_local_vars(node.body, vars)
    
    elif isinstance(node, Assign):
        vars |= {node.targets[0].id}
        vars |= get_local_vars(node.value, vars)
    
    elif isinstance(node, Call):
        vars |= get_local_vars(node.args, vars)
    
    elif isinstance(node, BinOp):
        vars |= get_local_vars(node.left, vars)
        vars |= get_local_vars(node.right, vars)
    
    elif isinstance(node, UnaryOp):
        vars |= get_local_vars(node.operand), vars
    
    elif isinstance(node, list):
        for elem in node:
            vars |= get_local_vars(elem, vars)
    
    elif isinstance(node, Name):
        vars |= {node.id}
    
    return vars


def is_simple_BinOp(node):
    if isinstance(node, BinOp):
        return (isinstance(node.left, Constant) or isinstance(node.left, Name)) and (isinstance(node.right, Constant) or (isinstance(node.right, Name)))
    return False



def is_simple_UnaryOp(node):
    if isinstance(node, UnaryOp):
        return isinstance(node.operand, Constant) or isinstance(node.operand, Name)
    return False



def is_simple_Expr(node):
    return isinstance(node, Constant) or is_simple_BinOp(node) or is_simple_UnaryOp(node)



def is_simple_statement(node):

    if isinstance(node, Assign):
        return is_simple_Expr(node.value)
    
    if isinstance(node, BinOp):
        return is_simple_BinOp(node)
    
    if isinstance(node, UnaryOp):
        return is_simple_UnaryOp(node)

    if isinstance(node, Expr):
        return is_simple_BinOp(node) or is_simple_UnaryOp(node)
    
    if isinstance(node, Constant):
        return True
    
    if isinstance(node, Name):
        if node.id != "print":
            return True



def is_atomic(node):
    if isinstance(node, Constant) or isinstance(node, Name):
        return True


def new_assign_node(node, temp_id):
    if is_simple_BinOp(node) or is_simple_UnaryOp(node):
        return Assign(targets = [Name(id = temp_id, ctx = Store())],
                          value = node)



class FlattenAST():

    def __init__(self):

        self.counter = 0 
        self.flattened_body = [] 

    def flatten(self, node):

        if isinstance(node, ASTree):
            node = self.flatten(node.module)

        elif isinstance(node, Module):

            for child_node in node.body:
                child_node = self.flatten(child_node)
                self.flattened_body.append(child_node)

        elif is_atomic(node) or is_simple_statement(node):
            return node


        elif isinstance(node, Assign):
            node.value = self.flatten(node.value)


        elif isinstance(node, Expr):
            node.value = self.flatten(node.value)


        elif isinstance(node, BinOp):

            self.flatten(node.left)
            if not is_atomic(node.left):
                node.left = self.get_temp_assign_node(node.left)
                
            self.flatten(node.right)
            if not is_atomic(node.right):
                node.right = self.get_temp_assign_node(node.right)
        
        elif isinstance(node, UnaryOp):

            node.operand = self.flatten(node.operand)

            if not is_atomic(node.operand):
                node.operand = self.get_temp_assign_node(node.operand)
                

        elif isinstance(node, Call):

            for i in range(len(node.args)):
                node.args[i] = self.flatten(node.args[i])
                if not is_atomic(node.args[i]):
                    node.args[i] = self.get_temp_assign_node(node.args[i])

        return node

    
    def get_temp_assign_node(self, node):
        temp_id = f"temp_{self.counter}"
        self.counter = self.counter + 1
        self.flattened_body.append(new_assign_node(node, temp_id))
        return Name(id = temp_id, ctx = Load())



def flatten(tree):
    flattener = FlattenAST()
    flattener.flatten(tree)
    return ASTree(Module(body=flattener.flattened_body))