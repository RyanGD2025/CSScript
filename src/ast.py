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
        self.target = target
        self.expression = expression

class AcessoPropriedade(ASTNode):
    """Representa algo como Objeto.Name"""
    def __init__(self, base, property_name):
        self.base = base
        self.property_name = property_name

# --- Estruturas de Fluxo e Customizadas do CSScript ---

class ExtensaoClasse(ASTNode):
    """Representa a estrutura: extents Sprite; { ... }"""
    def __init__(self, class_name, body):
        self.class_name = class_name
        self.body = body

class DeclaracaoVar(ASTNode):
    """Representa a estrutura: var speed = 16;"""
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class IfStatement(ASTNode):
    """Representa a estrutura: if (condição) { ... }"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ComparacaoTripla(ASTNode):
    """Representa a sintaxe customizada: P1 = P2 = P3&P4 (Simulado)"""
    def __init__(self, left, middle, right_tokens):
        self.left = left
        self.middle = middle
        self.right_tokens = right_tokens # Ex: ['A', 'D']
        
class FuncaoChamada(ASTNode):
    """Representa uma chamada de função (ex: printinConsole(valor))"""
    def __init__(self, func, args):
        self.func = func # Identificador
        self.args = args # Lista de expressões
