# Arquivo: src/ast.py

class ASTNode:
    """Classe base para todos os nós da Árvore de Sintaxe Abstrata (AST)."""
    pass

class Programa(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Identificador(ASTNode):
    def __init__(self, name):
        self.name = name

class BinOp(ASTNode):
    """Operação Binária (ex: a + b, x == y)"""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Atribuicao(ASTNode):
    def __init__(self, target, expression):
        self.target = target  # Pode ser Identificador ou AcessoPropriedade
        self.expression = expression

class AcessoPropriedade(ASTNode):
    """Representa algo como Objeto.Name ou Objeto.Pos.x"""
    def __init__(self, base, property_name):
        self.base = base
        self.property_name = property_name

# Adicione outras classes de nós conforme a necessidade (IfStatement, WhileLoop, FuncaoDef, etc.)
# ...
