

class ASTree:
    def __init__(self, module):
        self.module = module
    def __repr__(self):
        return ASTDump().dump(self.module)

class Module:
    def __init__(self, body):
        self.body = body
    def __repr__(self):
        return f"Module(body={self.body}"

class Assign:
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value
    def __repr__(self):
        return f"Assign(targets={self.targets}, value={self.value})"

class Name:
    def __init__(self, id, ctx):
        self.id = id
        self.ctx = ctx
    def __repr__(self):
        return f"Name(id=\'{self.id}\', ctx={self.ctx})"

class Constant:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Constant(value={self.value})"

class Expr:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Expr(value={self.value})"

class Call:
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __repr__(self):
        return f"Call(func={self.func}, args={self.args})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp(left={self.left}, op={self.op}, right={self.right})"

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp(op={self.op}, operand={self.operand})"

class USub:
    def __repr__(self):
        return "USub()"

class Add:
    def __repr__(self):
        return "Add()"

class Sub:
    def __repr__(self):
        return "Sub()"

class Load:
    def __repr__(self):
        return "Load()"

class Store:
    def __repr__(self):
        return "Store()"


#================================================================


class ASTDump:
    
    def __init__(self):
        self.indent = " "*3

    def takes_single_line(self, str):
        return "\n" not in str
    
    def dump(self, node, depth=0):

        if isinstance(node, Module):

            body = self.dump(node.body, depth+1)

            if self.takes_single_line(body):
                comma = ","
                nline = ""
                space=0
            else:
                comma = ""
                nline = "\n"
                space=1

            return f"Module({nline}{self.indent*space}body={body}\n)"

        if isinstance(node, list):

            dump_str = "["

            if len(node) == 0:
                return str(node) 

            s0 = self.indent * (depth)
            s1 = self.indent * (depth + 1)
            
            for i in range(len(node)):

                comma = "" if i == len(node) - 1 else ","
                
                str_elem = self.dump(node[i], depth + 1)
                nline = "\n"
                dump_str += f"{nline}{s1}{str_elem}{comma}" 
            
            return dump_str + f"\n{s0}]"
        
        if isinstance(node, Expr):
            s1 = self.indent * depth
            value = self.dump(node.value, depth+1)
            return f"Expr(\n{self.indent*(depth+1)}value={value}\n{s1})" 
    
        if isinstance(node, Constant):
            return f"Constant(value={node.value})"
        
        if isinstance(node, BinOp):
            s1 = self.indent * depth
            left = self.dump(node.left, depth+1)
            right = self.dump(node.right, depth+1)
            return f"BinOp(\n{self.indent*(depth+1)}left={left},\n{self.indent*(depth+1)}op={node.op},\n{self.indent*(depth+1)}right={right}\n{s1})"
        
        if isinstance(node, UnaryOp):
            
            s2 = self.indent * (depth + 1)
            operand = self.dump(node.operand, depth+1)
            return f"UnaryOp(\n{s2}op={node.op},\n{s2}operand={operand})"
        
        if isinstance(node, Call):
            s1 = self.indent * depth
            s2 = self.indent * (depth + 1)
            args = self.dump(node.args, depth + 1)
            return f"Call(\n{s2}func={node.func},\n{s2}args={args}\n{s1})"
    
        if isinstance(node, Assign):
            s1 = self.indent * depth
            s2 = self.indent * (depth + 1)
            targets = self.dump(node.targets, depth + 1)
            value = self.dump(node.value, depth + 1)
            return f"Assign(\n{s2}targets={targets}\n{s2}value={value}\n{s1})" 
        
        if isinstance(node, Name):
            s1 = self.indent * depth
            s2 = self.indent * (depth + 1)
            return f"{node}"