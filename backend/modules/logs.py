# -*- coding: utf-8 -*-
"""Registro e consulta de logs do sistema."""

from __future__ import annotations
from typing import Any

# Importa conexão e tratamento de erros
from backend.db.connection import get_connection
from backend.utils.errors import show_error


def registrar_log(
    acao: str,
    descricao: str,
    connection: Any | None = None,
    commit: bool = True,
) -> None:
    """Registra uma ação no banco de logs."""
    owns_connection = connection is None
    if owns_connection:
        connection = get_connection()

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO logs (acao, descricao) VALUES (%s, %s)",
            (acao, descricao),
        )
        if commit:
            connection.commit()
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def listar_logs(connection: Any | None = None) -> list[dict[str, Any]]:
    """Lista os últimos 100 registros de log."""
    owns_connection = connection is None
    if owns_connection:
        connection = get_connection()

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, acao, descricao, criado_em FROM logs ORDER BY id DESC LIMIT 100"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def menu(connection: Any | None = None) -> None:
    """Exibe o menu de consulta de logs."""
    try:
        logs = listar_logs(connection)
        if not logs:
            print("Nenhum log encontrado.")
            return

        print("ID | Ação | Descrição | Criado em")
        print("-" * 80)
        for item in logs:
            print(
                f"{item['id']} | {item['acao']} | "
                f"{item['descricao']} | {item.get('criado_em', '')}"
            )
    except Exception as exc:
        show_error(str(exc))
    finally:
        input("\nPressione Enter para voltar...")
