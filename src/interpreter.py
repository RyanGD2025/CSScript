# Arquivo: src/interpreter.py

from .ast import *
from .environment import Environment
import sys

class Interpreter:
    def __init__(self):
        self.global_env = self._setup_globals()

    def _setup_globals(self):
        env = Environment()
        
        # Funções Built-in (printinConsole e Add)
        def builtin_printinconsole(args):
            print(*args, file=sys.stdout)
            return None
            
        def builtin_add(args):
            if args:
                print(f">>> Objeto '{args[0]}' Adicionado! (Simulação)")
                # Retorna um objeto simulado com a propriedade Name
                return {'Type': args[0], 'Name': f'Novo{args[0]}', 'Pos': {'x': 0, 'y': 0}}
            return None

        env.define("printinConsole", builtin_printinconsole)
        env.define("Add", builtin_add)
        return env

    # --- Métodos de Visita ---
    
    def interpret(self, ast):
        return self._visit_program(ast, self.global_env)
        
    def _visit(self, node, env):
        node_type = type(node).__name__
        visitor_method = getattr(self, f'_visit_{node_type}', self._visit_unknown)
        return visitor_method(node, env)

    def _visit_unknown(self, node, env):
        raise TypeError(f"Não há método de visita para o nó: {type(node)}")

    def _visit_Programa(self, node, env):
        last_result = None
        for statement in node.statements:
            last_result = self._visit(statement, env)
        return last_result
        
    # --- Execução de Tipos de Nó ---
    
    def _visit_Literal(self, node, env):
        return node.value

    def _visit_Identificador(self, node, env):
        return env.lookup(node.name)

    def _visit_BinOp(self, node, env):
        left = self._visit(node.left, env)
        right = self._visit(node.right, env)
        if node.op == '+': return left + right
        if node.op == '==': return left == right
        # Adicione outros operadores
        raise ValueError(f"Operador binário desconhecido: {node.op}")

    def _visit_Atribuicao(self, node, env):
        value = self._visit(node.expression, env)
        
        if isinstance(node.target, Identificador):
            env.define(node.target.name, value)
            return value
        
        elif isinstance(node.target, AcessoPropriedade):
            # Simulação de atribuição a Propriedade
            base_object = self._visit(node.target.base, env)
            prop_name = node.target.property_name
            if isinstance(base_object, dict) and prop_name in base_object:
                 base_object[prop_name] = value
                 return value
        
        raise Exception(f"Alvo de atribuição inválido: {type(node.target)}")

    # --- Execução de Estruturas Customizadas ---

    def _visit_ExtensaoClasse(self, node, env):
        print(f"Iniciando extensão para a classe: {node.class_name}")
        # Executa o corpo da extensão no escopo global/classe
        for statement in node.body:
            self._visit(statement, env)

    def _visit_DeclaracaoVar(self, node, env):
        value = self._visit(node.expression, env)
        env.define(node.name, value)
        return value

    def _visit_FuncaoChamada(self, node, env):
        func_name = node.func.name
        args = [self._visit(arg, env) for arg in node.args]
        func = env.lookup(func_name)
        
        if callable(func):
            return func(args)
        
        raise TypeError(f"'{func_name}' não é uma função chamável.")

    def _visit_ComparacaoTripla(self, node, env):
        """Implementa a lógica da sua regra: Player_movement = Key = A&D"""
        print(f">>> Executando lógica de movimento para {node.right_tokens[0]} ou {node.right_tokens[1]}")
        # No jogo real, checaria se a tecla A OU D está pressionada.
        # Por ser uma simulação, apenas retornamos True (Simulando sucesso na checagem)
        return True 

    def _visit_IfStatement(self, node, env):
        condition_result = self._visit(node.condition, env)
        
        if condition_result:
            # Cria um novo escopo para o bloco 'if'
            if_env = Environment(parent=env)
            for statement in node.body:
                self._visit(statement, if_env)
                
