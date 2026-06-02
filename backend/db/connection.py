# -*- coding: utf-8 -*-
"""
Módulo de conexão com o banco de dados.
"""

from typing import Any
import mysql.connector
from mysql.connector import Error

# IMPORTAÇÃO CORRIGIDA: Direto do arquivo local config.py
from config import DB_CONFIG

def get_connection() -> Any:
    """
    Cria e retorna uma conexão ativa com o banco de dados.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if not connection.is_connected():
            raise RuntimeError("A conexão com o banco foi criada, mas não está ativa.")

        return connection
    except Error as exc:
        raise RuntimeError(f"Falha ao conectar ao banco de dados: {exc}") from exc

# ATALHO: Faz o app.py continuar funcionando sem precisar alterar as rotas
def get_db():
    return get_connection()
