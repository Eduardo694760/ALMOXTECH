# -*- coding: utf-8 -*-
"""
Funções de validação de dados para o sistema.
"""

from typing import Any

VALID_PERMISSIONS = {"ADMIN", "OPERADOR"}

def validar_id(value: Any) -> int:
    """Valida se o ID é um número inteiro positivo."""
    try:
        id_int = int(value)
    except (TypeError, ValueError):
        raise ValueError("ID deve ser um número inteiro.")

    if id_int <= 0:
        raise ValueError("ID deve ser maior que zero.")

    return id_int


def validar_texto_obrigatorio(value: str, field_name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} é obrigatório.")
    return text


def validar_login(value: str) -> str:
    login = validar_texto_obrigatorio(value, "Login").lower()
    if len(login) > 80:
        raise ValueError("Login deve ter no máximo 80 caracteres.")
    return login


def validar_login_unico(connection: Any, login: str, user_id: int | None = None) -> None:
    query = "SELECT id FROM usuarios WHERE login = %s"
    params: tuple[Any, ...] = (login,)
    if user_id is not None:
        query += " AND id <> %s"
        params = (login, user_id)

    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if cursor.fetchone():
            raise ValueError("Login já cadastrado para outro usuário.")
    finally:
        cursor.close()


def validar_permissao(value: str) -> str:
    permission = validar_texto_obrigatorio(value, "Permissão").upper()
    if permission not in VALID_PERMISSIONS:
        valid_options = ", ".join(sorted(VALID_PERMISSIONS))
        raise ValueError(f"Permissão inválida. Use: {valid_options}.")
    return permission


def validar_ativo(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        raise ValueError("Ativo deve ser 1 para ativo ou 0 para inativo.")

    text = str(value).strip().lower()
    if text in {"1", "s", "sim", "true", "ativo"}:
        return True
    if text in {"0", "n", "nao", "não", "false", "inativo"}:
        return False

def validar_quantidade(value: Any, field_name: str = "Quantidade") -> int:
    """Valida se a quantidade é um número inteiro válido (maior ou igual a zero)."""
    try:
        qtd_int = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} deve ser um número inteiro.")

    if qtd_int < 0:
        raise ValueError(f"{field_name} não pode ser menor que zero.")

    return qtd_int


def validar_sku(value: str) -> str:
    """Valida o formato do SKU (obrigatório e remove espaços)."""
    sku = str(value).strip().upper()
    if not sku:
        raise ValueError("SKU é obrigatório.")
    return sku

def validar_sku_unico(connection: Any, sku: str, product_id: int | None = None) -> None:
    """Verifica se o SKU já existe no banco de dados para outro produto."""
    query = "SELECT id FROM produtos WHERE sku = %s"
    params: tuple[Any, ...] = (sku,)
    
    if product_id is not None:
        query += " AND id <> %s"
        params = (sku, product_id)

    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if cursor.fetchone():
            raise ValueError("SKU já cadastrado para outro produto.")
    finally:
        cursor.close()
    # A linha do "raise ValueError" do Ativo foi removida daqui! ✅

def validar_ativo(value: Any) -> bool:
    """Valida se o campo ativo foi informado corretamente."""
    # Se já for booleano, retorna direto
    if isinstance(value, bool):
        return value
        
    # Se for um número inteiro (0 ou 1)
    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        raise ValueError("Ativo deve ser 1 para ativo ou 0 para inativo.")
        
    # SE FOR STRING (Texto vindo do input do terminal)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("1", "sim", "s", "true"):
            return True
        if v in ("0", "nao", "não", "n", "false"):
            return False

    # Se não for nenhum dos formatos válidos
    raise ValueError("Ativo deve ser informado como sim/nao ou 1/0.")


