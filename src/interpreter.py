# Arquivo: src/interpreter.py

from .ast import *
from .environment import Environment
import sys

class Interpreter:
    def __init__(self):
        # O escopo global que armazena as variáveis de nível superior
        self.global_env = self._setup_globals()

    def _setup_globals(self):
        """Popula o ambiente global com funções built-in (como printinConsole)."""
        env = Environment()
        
        # Adicionar a função printinConsole
        def builtin_printinconsole(args):
            # args é uma lista de valores resolvidos (já interpretados)
            if args:
                # printinConsole("texto") -> args[0] é o valor do texto
                print(args[0], file=sys.stdout)
            else:
                print("", file=sys.stdout)
            return None # Funções que não retornam nada retornam None
            
        # Adicionar outras funções built-in do CSScript (Add, Vector, Angle, etc.)
        def builtin_add(args):
            # Lógica de Add("Sprite")
            if args and args[0] == "Sprite":
                print(">>> Objeto 'Sprite' Adicionado! (Simulação)")
                # Retorna uma representação de um objeto do jogo
                return {'Type': 'Sprite', 'Name': 'NovoSprite', 'Pos': {'x': 0, 'y': 0}}
            return None

        # Define as funções no ambiente
        env.define("printinConsole", builtin_printinconsole)
        env.define("Add", builtin_add)
        
        return env

    # --- Métodos de Visita para cada tipo de nó da AST ---

    def interpret(self, ast):
        """Inicia a interpretação do nó principal (Programa)."""
        return self._visit_program(ast, self.global_env)
        
    def _visit_program(self, node, env):
        """Executa todos os statements do programa."""
        last_result = None
        for statement in node.statements:
            last_result = self._visit(statement, env)
        return last_result

    def _visit(self, node, env):
        """Método de despacho: chama a função específica para o tipo de nó."""
        node_type = type(node).__name__
        visitor_method = getattr(self, f'_visit_{node_type}', self._visit_unknown)
        return visitor_method(node, env)

    def _visit_unknown(self, node, env):
        raise TypeError(f"Não há método de visita para o nó: {type(node)}")
        
    # --- Execução de Tipos de Nó ---

    def _visit_Literal(self, node, env):
        """Retorna o valor do literal (número, string, booleano)."""
        return node.value

    def _visit_Identificador(self, node, env):
        """Busca o valor da variável no ambiente."""
        return env.lookup(node.name)

    def _visit_BinOp(self, node, env):
        """Executa uma operação binária (ex: a + b)."""
        left = self._visit(node.left, env)
        right = self._visit(node.right, env)
        
        if node.op == '+': return left + right
        if node.op == '-': return left - right
        if node.op == '*': return left * right
        if node.op == '/': return left / right
        if node.op == '==': return left == right
        # Adicione outros operadores (>, <, !=, etc.)
        
        raise ValueError(f"Operador binário desconhecido: {node.op}")

    def _visit_Atribuicao(self, node, env):
        """Processa a atribuição de valor a uma variável ou propriedade."""
        value = self._visit(node.expression, env)
        
        if isinstance(node.target, Identificador):
            # Atribuição simples: local x = 5; ou x = 5;
            env.define(node.target.name, value)
            return value
        
        elif isinstance(node.target, AcessoPropriedade):
            # Atribuição a Propriedade: MySprite.Name = "NovoNome";
            base_object = self._visit(node.target.base, env)
            prop_name = node.target.property_name # Nome é o string
            
            # Aqui você deve ter a lógica real de atualização de um objeto do jogo
            if isinstance(base_object, dict) and prop_name in base_object:
                 base_object[prop_name] = value
                 print(f">>> Propriedade '{prop_name}' de objeto atualizada para: {value}")
                 return value

        raise Exception(f"Alvo de atribuição inválido: {type(node.target)}")

    def _visit_FuncaoChamada(self, node, env):
        """Chamada de função (ex: printinConsole(...))."""
        func_name = node.func.name
        
        # 1. Resolver os argumentos
        args = [self._visit(arg, env) for arg in node.args]
        
        # 2. Buscar a função (built-in ou definida pelo usuário)
        func = env.lookup(func_name)
        
        # 3. Executar
        if callable(func):
            # Para funções built-in (que são funções Python)
            return func(args)
        
        # Se for uma função CSScript (FuncaoDef):
        # Aqui você criaria um novo ambiente aninhado, definiria os parâmetros
        # e chamaria _visit_block para executar o corpo da função.
        
        raise TypeError(f"'{func_name}' não é uma função chamável.")
        
    # O seu parser precisará de um nó FuncaoChamada para esta parte funcionar!

  
