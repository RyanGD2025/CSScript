# Arquivo: src/environment.py

class Environment:
    """Gerencia o escopo de variáveis (locais e globais)."""
    def __init__(self, parent=None):
        # 'parent' permite criar escopos aninhados (ex: dentro de uma função)
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        """Declara ou redefine uma variável no escopo atual."""
        self.variables[name] = value

    def lookup(self, name):
        """Busca uma variável, subindo a cadeia de escopos."""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.lookup(name)

        raise NameError(f"Variável '{name}' não definida.")
      
