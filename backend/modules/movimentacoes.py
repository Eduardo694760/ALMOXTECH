# -*- coding: utf-8 -*-
"""Controle de movimentações de estoque (entradas e saídas)."""

from __future__ import annotations
from typing import Any

# Imports padronizados
from backend.db.connection import get_connection
from backend.modules.logs import registrar_log
from backend.utils.errors import show_error, show_success
from backend.utils.validators import (
    validar_id,
    validar_quantidade,
    validar_texto_obrigatorio,
)


def _get_connection(connection: Any | None) -> tuple[Any, bool]:
    """Retorna conexão ativa e flag se é própria."""
    if connection is not None:
        return connection, False
    return get_connection(), True


def registrar_movimentacao(
    produto_id: int,
    tipo: str,
    quantidade: int,
    observacao: str = "",
    connection: Any | None = None,
) -> int:
    """Registra uma movimentação de entrada ou saída."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        produto_id = validar_id(produto_id)
        tipo = validar_texto_obrigatorio(tipo, "Tipo").upper()
        quantidade = validar_quantidade(quantidade)
        observacao = str(observacao).strip()

        if tipo not in {"ENTRADA", "SAIDA"}:
            raise ValueError("Tipo de movimentação deve ser ENTRADA ou SAIDA.")

        # Atualiza estoque
        if tipo == "ENTRADA":
            cursor.execute(
                "UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s",
                (quantidade, produto_id),
            )
        else:  # SAIDA
            cursor.execute(
                "UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s",
                (quantidade, produto_id),
            )

        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")

        # Registra movimentação
        cursor.execute(
            """
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
            VALUES (%s, %s, %s, %s)
            """,
            (produto_id, tipo, quantidade, observacao),
        )
        mov_id = cursor.lastrowid

        registrar_log(
            "MOVIMENTACAO",
            f"Movimentação registrada: id={mov_id}, produto_id={produto_id}, tipo={tipo}, qtd={quantidade}",
            connection=connection,
            commit=False,
        )
        connection.commit()
        return mov_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def listar_movimentacoes(connection: Any | None = None) -> list[dict[str, Any]]:
    """Lista as últimas movimentações registradas."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT m.id, p.nome AS produto, m.tipo, m.quantidade, m.observacao, m.criado_em
            FROM movimentacoes m
            JOIN produtos p ON p.id = m.produto_id
            ORDER BY m.id DESC LIMIT 50
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def _print_movimentacoes(movs: list[dict[str, Any]]) -> None:
    """Exibe lista de movimentações formatada."""
    if not movs:
        print("Nenhuma movimentação registrada.")
        return

    print("ID | Produto | Tipo | Quantidade | Observação | Criado em")
    print("-" * 100)
    for mov in movs:
        print(
            f"{mov['id']} | {mov['produto']} | {mov['tipo']} | "
            f"{mov['quantidade']} | {mov.get('observacao') or ''} | {mov.get('criado_em', '')}"
        )


def _input_movimentacao() -> tuple[int, str, int, str]:
    """Solicita dados de movimentação via input."""
    produto_id = int(input("ID do produto: "))
    tipo = input("Tipo (ENTRADA/SAIDA): ")
    quantidade = int(input("Quantidade: "))
    observacao = input("Observação: ")
    return produto_id, tipo, quantidade, observacao


def menu(connection: Any | None = None) -> None:
    """Menu interativo de movimentações."""
    while True:
        print("\n" + "-=" * 30)
        print("Menu de Movimentações")
        print("-=" * 30)
        print("1 - Registrar movimentação")
        print("2 - Listar movimentações")
        print("0 - Voltar")

        option = input("\nEscolha uma opção: ").strip()

        try:
            match option:
                case "1":
                    mov_id = registrar_movimentacao(*_input_movimentacao(), connection=connection)
                    show_success(f"Movimentação registrada com ID {mov_id}.")
                case "2":
                    _print_movimentacoes(listar_movimentacoes(connection))
                case "0":
                    return
                case _:
                    show_error("Opção inválida. Tente novamente.")
        except Exception as exc:
            show_error(str(exc))

        input("\nPressione Enter para continuar...")
