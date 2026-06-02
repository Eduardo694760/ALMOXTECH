# -*- coding: utf-8 -*-
"""
Configurações globais do sistema.
"""

# Configurações de Banco de Dados
DB_CONFIG = {
    "host": "localhost",       # endereço do servidor
    "port": 3306,              # porta padrão MySQL
    "user": "root",            # usuário do banco
    "password": "",            # senha do banco
    "database": "almoxtech"    # nome do banco de dados
}

# Configurações gerais do sistema
SYSTEM_CONFIG = {
    "debug": True,             # modo debug (True/False)
    "log": "system.log",       # arquivo de log
    "timezone": "America/Sao_Paulo"  # fuso horário padrão
}
