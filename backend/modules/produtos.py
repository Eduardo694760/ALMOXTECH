# -*- coding: utf-8 -*-
"""CRUD de produtos do sistema de almoxarifado."""

from __future__ import annotations
from typing import Any

# Imports padronizados
from backend.db.connection import get_connection
from backend.modules.logs import registrar_log
from backend.utils.errors import show_error, show_success
from backend.utils.validators import (
    validar_id,
    validar_quantidade,
    validar_sku,
    validar_sku_unico,
    validar_texto_obrigatorio,
    validar_ativo,
)


def _get_connection(connection: Any | None) -> tuple[Any, bool]:
    """Retorna conexão ativa e flag se é própria."""
    if connection is not None:
        return connection, False
    return get_connection(), True


def cadastrar_produto(
    nome: str,
    sku: str,
    quantidade: int,
    descricao: str = "",
    ativo: Any = 1,
    connection: Any | None = None,
) -> int:
    """Cadastra um novo produto no banco."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        nome = validar_texto_obrigatorio(nome, "Nome")
        sku = validar_sku(sku)
        quantidade = validar_quantidade(quantidade)
        descricao = str(descricao).strip()
        ativo = validar_ativo(ativo)
        validar_sku_unico(connection, sku)

        cursor.execute(
            """
            INSERT INTO produtos (nome, sku, quantidade, descricao, ativo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, sku, quantidade, descricao, ativo),
        )
        product_id = cursor.lastrowid
        registrar_log(
            "CADASTRAR_PRODUTO",
            f"Produto cadastrado: id={product_id}, sku={sku}, ativo={ativo}",
            connection=connection,
            commit=False,
        )
        connection.commit()
        return product_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def listar_produtos(connection: Any | None = None) -> list[dict[str, Any]]:
    """Lista todos os produtos cadastrados."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nome, sku, quantidade, descricao, ativo
            FROM produtos
            ORDER BY nome
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def atualizar_produto(
    product_id: int,
    nome: str,
    sku: str,
    quantidade: int,
    descricao: str = "",
    ativo: Any = 1,
    connection: Any | None = None,
) -> bool:
    """Atualiza dados de um produto existente."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        product_id = validar_id(product_id)
        nome = validar_texto_obrigatorio(nome, "Nome")
        sku = validar_sku(sku)
        quantidade = validar_quantidade(quantidade)
        descricao = str(descricao).strip()
          # --- ALTERAÇÃO AQUI: Garante a conversão aceita pelo validador ---
        if ativo in [1, '1', True, 'sim', 's']:
            ativo_tratado = True  # ou '1' se o seu validador exigir string
        else:
            ativo_tratado = False # ou '0'
            
        ativo = validar_ativo(ativo_tratado)
        # -----------------------------------------------------------------
        
        validar_sku_unico(connection, sku)

        cursor.execute(
            """
            INSERT INTO produtos (nome, sku, quantidade, descricao, ativo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, sku, quantidade, descricao, ativo),
        )
        product_id = cursor.lastrowid
        # ... resto do código continua igual
        validar_sku_unico(connection, sku, product_id)

        cursor.execute(
            """
            UPDATE produtos
            SET nome = %s, sku = %s, quantidade = %s, descricao = %s, ativo = %s
            WHERE id = %s
            """,
            (nome, sku, quantidade, descricao, ativo, product_id),
        )

        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")

        registrar_log(
            "ATUALIZAR_PRODUTO",
            f"Produto atualizado: id={product_id}, sku={sku}, ativo={ativo}",
            connection=connection,
            commit=False,
        )
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def remover_produto(product_id: int, connection: Any | None = None) -> bool:
    """Remove um produto do banco."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        product_id = validar_id(product_id)
        cursor.execute("SELECT sku FROM produtos WHERE id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            raise ValueError("Produto não encontrado.")

        sku = product[0]
        cursor.execute("DELETE FROM produtos WHERE id = %s", (product_id,))
        registrar_log(
            "REMOVER_PRODUTO",
            f"Produto removido: id={product_id}, sku={sku}",
            connection=connection,
            commit=False,
        )
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def _print_produtos(produtos: list[dict[str, Any]]) -> None:
    """Exibe lista de produtos formatada."""
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("ID | Nome | SKU | Quantidade | Descrição | Ativo")
    print("-" * 100)
    for produto in produtos:
        status = "Ativo" if produto["ativo"] else "Inativo"
        print(
            f"{produto['id']} | {produto['nome']} | {produto['sku']} | "
            f"{produto['quantidade']} | {produto.get('descricao') or ''} | {status}"
        )


def _input_produto() -> tuple[str, str, int, str, Any]:
    """Solicita dados de produto via input."""
    nome = input("Nome: ")
    sku = input("SKU: ")
    quantidade = int(input("Quantidade: "))
    descricao = input("Descrição: ")
    # Lendo a entrada e limpando espaços/letras maiúsculas
    ativo_bruto = input("Ativo (1/0 ou sim/nao): ").strip().lower()
    
    # Forçando virar um INTEIRO puro (1 ou 0) antes de retornar
    if ativo_bruto in ['sim', 's', '1', 'true']:
        ativo = 1
    elif ativo_bruto in ['nao', 'não', 'n', '0', 'false']:
        ativo = 0
    else:
        # Se digitar errado, manda uma string inválida pro validador barrar
        ativo = "invalido"
        
    return nome, sku, quantidade, descricao, ativo


def menu(connection: Any | None = None) -> None:
    """Menu interativo de produtos."""
    while True:
        print("\n" + "-=" * 30)
        print("Menu de Produtos")
        print("-=" * 30)
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Remover produto")
        print("0 - Voltar")

        option = input("\nEscolha uma opção: ").strip()

        try:
            match option:
                case "1":
                    product_id = cadastrar_produto(*_input_produto(), connection=connection)
                    show_success(f"Produto cadastrado com ID {product_id}.")
                case "2":
                    _print_produtos(listar_produtos(connection))
                case "3":
                    product_id = input("ID do produto: ")
                    atualizar_produto(product_id, *_input_produto(), connection=connection)
                    show_success("Produto atualizado com sucesso.")
                case "4":
                    product_id = input("ID do produto: ")
                    remover_produto(product_id, connection=connection)
                    show_success("Produto removido com sucesso.")
                case "0":
                    return
                case _:
                    show_error("Opção inválida. Tente novamente.")
        except Exception as exc:
            show_error(str(exc))

        input("\nPressione Enter para continuar...")
