# Arquivo: src/parser.py

from ply import yacc
# Importa tokens e classes AST
from .lexer import tokens, lexer
from .ast import * # --- 1. Precedência de Operadores ---
precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
    ('right', 'ATRIBUICAO'),
)

# --- 2. Regras de Gramática ---

def p_programa(p):
    """programa : statements"""
    p[0] = Programa(p[1])

def p_statements(p):
    """
    statements : statement statements
               | statement
               | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

# Um statement pode ser Extensao, If, Var, Atribuicao, ou FuncaoChamada
def p_statement(p):
    """
    statement : extensao_classe
              | if_statement
              | var_declaration PONTO_VIRGULA
              | atribuicao PONTO_VIRGULA
              | expressao PONTO_VIRGULA  # Para chamadas de função (ex: Destroy();)
    """
    p[0] = p[1]

# --- Regras Customizadas (Sua Sintaxe) ---

def p_extensao_classe(p):
    """
    extensao_classe : EXTENTS IDENTIFICADOR PONTO_VIRGULA CHAVE_ESQ statements CHAVE_DIR
    """
    # extents Sprite; { statements }
    p[0] = ExtensaoClasse(p[2], p[5])

def p_var_declaration(p):
    """
    var_declaration : VAR IDENTIFICADOR ATRIBUICAO expressao
    """
    # var speed = 16
    p[0] = DeclaracaoVar(p[2], p[4])

def p_if_statement(p):
    """
    if_statement : IF comparacao_tripla CHAVE_ESQ statements CHAVE_DIR
    """
    # if condicao { statements }
    p[0] = IfStatement(p[2], p[4])

def p_comparacao_tripla(p):
    """
    comparacao_tripla : IDENTIFICADOR ATRIBUICAO IDENTIFICADOR ATRIBUICAO IDENTIFICADOR E_COMERCIAL IDENTIFICADOR
    """
    # Player_movement = Key = A & D
    p[0] = ComparacaoTripla(
        left=p[1],
        middle=p[3],
        right_tokens=[p[5], p[7]] # A e D
    )

# --- Regras Básicas ---

def p_atribuicao(p):
    """
    atribuicao : expressao ATRIBUICAO expressao
               | LOCAL IDENTIFICADOR ATRIBUICAO expressao # local MyVar = Valor
    """
    # MySprite.Name = "NovoNome" ou x = 5
    if len(p) == 4:
        p[0] = Atribuicao(p[1], p[3])
    else: # Caso 'local'
         p[0] = Atribuicao(Identificador(p[2]), p[4])

def p_expressao_binaria(p):
    """
    expressao : expressao SOMA expressao
              | expressao IGUAL expressao
              # ... (adicione outros operadores)
    """
    p[0] = BinOp(p[2], p[1], p[3])

def p_expressao_literal(p):
    """
    expressao : NUMERO
              | TEXTO
              | TRUE
              | FALSE
    """
    p[0] = Literal(p[1])

def p_expressao_identificador(p):
    """expressao : IDENTIFICADOR"""
    p[0] = Identificador(p[1])

def p_expressao_propriedade(p):
    """
    expressao : expressao PONTO IDENTIFICADOR
    """
    # Ex: MySprite.Name
    p[0] = AcessoPropriedade(p[1], p[3])

def p_expressao_funcao_chamada(p):
    """
    expressao : IDENTIFICADOR PARENTESE_ESQ arg_list PARENTESE_DIR
    """
    # printinConsole(valor)
    p[0] = FuncaoChamada(Identificador(p[1]), p[3])

def p_arg_list(p):
    """
    arg_list : expressao VIRGULA arg_list
             | expressao
             | empty
    """
    if len(p) == 4: # expressao , arg_list
        p[0] = [p[1]] + p[3]
    elif len(p) == 2: # expressao
        p[0] = [p[1]]
    else: # empty
        p[0] = []

# --- Tratamento de Erros e Vazio ---

def p_error(p):
    if p:
        print(f"Erro de Sintaxe em '{p.value}' (Tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de Sintaxe no final da entrada (EOF).")

def p_empty(p):
    'empty :'
    pass

# Constrói o parser
parser = yacc.yacc()
