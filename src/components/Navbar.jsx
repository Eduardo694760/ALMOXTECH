import React from "react";
import { Link } from "react-router-dom";
import "../styles/glass.css";
import { jwtDecode } from 'jwt-decode';

const Navbar = () => {
  const token = localStorage.getItem("token");
  let permissao = null;

  if (token) {
    try {
      const decoded = jwtDecode(token);
      permissao = decoded.permissao;
    } catch (error) {
      console.error("Erro ao decodificar token:", error);
    }
  }

  return (
    <nav className="glass navbar">
      <h2 className="logo">Almoxarifado Inteligente</h2>
      <ul className="nav-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/produtos">Produtos</Link></li>
        <li><Link to="/movimentacoes">Movimentações</Link></li>
        <li><Link to="/logs">Logs</Link></li>
        {permissao === "ADMIN" && <li><Link to="/usuarios">Usuários</Link></li>}
      </ul>
    </nav>
  );
};

export default Navbar;
