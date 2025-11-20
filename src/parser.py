# Arquivo: src/parser.py

from ply import yacc
from .lexer import tokens, lexer # Importa os tokens definidos anteriormente
from .ast import * # Importa as classes da AST

# --- 1. Definição de Precedência de Operadores ---
# PLY usa esta lista para resolver ambiguidades (ex: * antes de +)
precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
    ('right', 'ATRIBUICAO'),
)

# --- 2. Regras de Gramática (Funções p_...) ---

# O ponto de entrada: O programa é uma lista de statements
def p_programa(p):
    """programa : statements"""
    p[0] = Programa(p[1])

# Uma lista de statements
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

# Um statement é uma instrução seguida de ponto e vírgula
def p_statement(p):
    """
    statement : atribuicao PONTO_VIRGULA
              | expressao PONTO_VIRGULA
              | while_loop
              | if_statement
              | function_definition
    """
    p[0] = p[1]

# --- 3. Expressões e Operações ---

# EXPRESSÃO (O que produz um valor)
def p_expressao_binaria(p):
    """
    expressao : expressao SOMA expressao
              | expressao SUBTRACAO expressao
              | expressao MULTIPLICACAO expressao
              | expressao DIVISAO expressao
              | expressao IGUAL expressao
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

# Acesso à Propriedade (Objeto.Propriedade)
def p_expressao_propriedade(p):
    """
    expressao : expressao PONTO IDENTIFICADOR
    """
    # Ex: MySprite.Name -> AcessoPropriedade(MySprite, "Name")
    p[0] = AcessoPropriedade(p[1], p[3])

# --- 4. Comandos Específicos do CSScript ---

# ATRIBUIÇÃO (local MyVar = Valor; ou MyVar = Valor;)
def p_atribuicao(p):
    """
    atribuicao : IDENTIFICADOR ATRIBUICAO expressao
               | LOCAL IDENTIFICADOR ATRIBUICAO expressao
               | expressao ATRIBUICAO expressao  # Permite atribuir a propriedades: MySprite.Name = "Nova"
    """
    # A lógica aqui será mais complexa para distinguir entre os formatos,
    # mas o parser captura os tokens.
    if len(p) == 4:
        # MyVar = expressao (p[1] = target, p[3] = expression)
        p[0] = Atribuicao(p[1], p[3])
    elif len(p) == 5:
        # local MyVar = expressao (p[2] = target, p[4] = expression)
        p[0] = Atribuicao(Identificador(p[2]), p[4])

# --- 5. Tratamento de Erros e Vazio ---

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

# Exemplo de teste (Adicione no final de parser.py)
if __name__ == '__main__':
    codigo_teste = """
    local vida = 100;
    local nome = "Player1";
    
    objeto.Pos.x = 5 + 3 * 2; // Atribuicao complexa
    
    if true {
        printinConsole("Iniciando...");
    }
    """
    
    # É necessário que o PLY gere o arquivo 'parsetab.py'
    try:
        resultado_ast = parser.parse(codigo_teste, lexer=lexer)
        print("--- AST Gerada com Sucesso! ---")
        # Você precisaria de um método para imprimir a AST de forma bonita
        # Por enquanto, apenas confirmamos que não houve erro de sintaxe.
        print(type(resultado_ast))
    except Exception as e:
        print(f"Falha ao Analisar: {e}")
        
