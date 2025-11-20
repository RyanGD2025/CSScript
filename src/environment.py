# Arquivo: src/environment.py

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def define(self, name, value):
        self.variables[name] = value

    def lookup(self, name):
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.lookup(name)

        raise NameError(f"Variável/Função '{name}' não definida.")
        
