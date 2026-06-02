# -*- coding: utf-8 -*-
"""CRUD de usuários do sistema de almoxarifado."""

from __future__ import annotations
import hashlib
from typing import Any

# Imports padronizados
from backend.db.connection import get_connection
from backend.modules.logs import registrar_log
from backend.utils.errors import show_error, show_success
from backend.utils.validators import (
    validar_ativo,
    validar_id,
    validar_login,
    validar_login_unico,
    validar_permissao,
    validar_texto_obrigatorio,
)


def _get_connection(connection: Any | None) -> tuple[Any, bool]:
    """Retorna conexão ativa e flag se é própria."""
    if connection is not None:
        return connection, False
    return get_connection(), True


def _hash_senha(senha: str) -> str:
    """Gera hash SHA-256 da senha."""
    senha = validar_texto_obrigatorio(senha, "Senha")
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def cadastrar_usuario(
    nome: str,
    login: str,
    senha: str,
    permissao: str,
    ativo: Any = True,
    connection: Any | None = None,
) -> int:
    """Cadastra um novo usuário no banco."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        nome = validar_texto_obrigatorio(nome, "Nome")
        login = validar_login(login)
        senha_hash = _hash_senha(senha)
        permissao = validar_permissao(permissao)
        ativo = validar_ativo(ativo)
        validar_login_unico(connection, login)

        cursor.execute(
            """
            INSERT INTO usuarios (nome, login, senha_hash, permissao, ativo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome, login, senha_hash, permissao, ativo),
        )
        user_id = cursor.lastrowid
        registrar_log(
            "CADASTRAR_USUARIO",
            f"Usuário cadastrado: id={user_id}, login={login}, permissao={permissao}",
            connection=connection,
            commit=False,
        )
        connection.commit()
        return user_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def listar_usuarios(connection: Any | None = None) -> list[dict[str, Any]]:
    """Lista todos os usuários cadastrados."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nome, login, permissao, ativo
            FROM usuarios
            ORDER BY nome
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        if owns_connection:
            connection.close()


def atualizar_usuario(
    user_id: int,
    nome: str,
    login: str,
    permissao: str,
    ativo: Any,
    senha: str | None = None,
    connection: Any | None = None,
) -> bool:
    """Atualiza dados de um usuário existente."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        user_id = validar_id(user_id)
        nome = validar_texto_obrigatorio(nome, "Nome")
        login = validar_login(login)
        permissao = validar_permissao(permissao)
        ativo = validar_ativo(ativo)
        validar_login_unico(connection, login, user_id)

        if senha:
            cursor.execute(
                """
                UPDATE usuarios
                SET nome = %s, login = %s, senha_hash = %s, permissao = %s, ativo = %s
                WHERE id = %s
                """,
                (nome, login, _hash_senha(senha), permissao, ativo, user_id),
            )
        else:
            cursor.execute(
                """
                UPDATE usuarios
                SET nome = %s, login = %s, permissao = %s, ativo = %s
                WHERE id = %s
                """,
                (nome, login, permissao, ativo, user_id),
            )

        if cursor.rowcount == 0:
            raise ValueError("Usuário não encontrado.")

        registrar_log(
            "ATUALIZAR_USUARIO",
            f"Usuário atualizado: id={user_id}, login={login}, permissao={permissao}",
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


def desativar_usuario(user_id: int, connection: Any | None = None) -> bool:
    """Desativa um usuário no banco."""
    connection, owns_connection = _get_connection(connection)
    cursor = connection.cursor()

    try:
        user_id = validar_id(user_id)
        cursor.execute("SELECT login FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            raise ValueError("Usuário não encontrado.")

        login = user[0]
        cursor.execute("UPDATE usuarios SET ativo = %s WHERE id = %s", (False, user_id))
        registrar_log(
            "DESATIVAR_USUARIO",
            f"Usuário desativado: id={user_id}, login={login}",
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


def _print_usuarios(usuarios: list[dict[str, Any]]) -> None:
    """Exibe lista de usuários formatada."""
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print("ID | Nome | Login | Permissão | Status")
    print("-" * 80)
    for usuario in usuarios:
        status = "Ativo" if usuario["ativo"] else "Inativo"
        print(
            f"{usuario['id']} | {usuario['nome']} | {usuario['login']} | "
            f"{usuario['permissao']} | {status}"
        )


def _input_usuario(include_password: bool = True) -> tuple[Any, ...]:
    """Solicita dados de usuário via input."""
    nome = input("Nome: ")
    login = input("Login: ")
    permissao = input("Permissão (ADMIN/OPERADOR): ")
    ativo = input("Ativo? (1-Sim/0-Não): ")

    if include_password:
        senha = input("Senha: ")
        return nome, login, senha, permissao, ativo

    senha = input("Nova senha (deixe vazio para manter): ").strip()
    return nome, login, permissao, ativo, senha or None


def menu(connection: Any | None = None) -> None:
    """Menu interativo de usuários."""
    while True:
        print("\n" + "-=" * 30)
        print("Menu de Usuários")
        print("-=" * 30)
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Atualizar usuário")
        print("4 - Desativar usuário")
        print("0 - Voltar")

        option = input("\nEscolha uma opção: ").strip()

        try:
            match option:
                case "1":
                    user_id = cadastrar_usuario(*_input_usuario(), connection=connection)
                    show_success(f"Usuário cadastrado com ID {user_id}.")
                case "2":
                    _print_usuarios(listar_usuarios(connection))
                case "3":
                    user_id = input("ID do usuário: ")
                    atualizar_usuario(user_id, *_input_usuario(False), connection=connection)
                    show_success("Usuário atualizado com sucesso.")
                case "4":
                    user_id = input("ID do usuário: ")
                    desativar_usuario(user_id, connection=connection)
                    show_success("Usuário desativado com sucesso.")
                case "0":
                    return
                case _:
                    show_error("Opção inválida. Tente novamente.")
        except Exception as exc:
            show_error(str(exc))

        input("\nPressione Enter para continuar...")
