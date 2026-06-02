# -*- coding: utf-8 -*-
"""Mensagens padronizadas para o terminal."""

from __future__ import annotations

def show_error(message: str) -> None:
    """Exibe mensagem de erro padronizada."""
    print(f"[ERRO] {message}")

def show_success(message: str) -> None:
    """Exibe mensagem de sucesso padronizada."""
    print(f"[OK] {message}")

def show_warning(message: str) -> None:
    """Exibe mensagem de aviso padronizada."""
    print(f"[AVISO] {message}")

def show_info(message: str) -> None:
    """Exibe mensagem informativa padronizada."""
    print(f"[INFO] {message}")
