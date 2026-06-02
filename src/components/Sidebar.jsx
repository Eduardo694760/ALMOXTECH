import React from "react";
import { Link } from "react-router-dom";
import "../styles/glass.css";
import { jwtDecode } from 'jwt-decode';


const Sidebar = () => {
  const token = localStorage.getItem("token");
  let permissao = null;

  if (token) {
    try {
      const decoded = jwt_decode(token);
      permissao = decoded.permissao;
    } catch (error) {
      console.error("Erro ao decodificar token:", error);
    }
  }

  return (
    <aside className="glass sidebar">
      <ul className="sidebar-links">
        <li><Link to="/dashboard">🏠 Dashboard</Link></li>
        <li><Link to="/produtos">📦 Produtos</Link></li>
        {permissao === "ADMIN" && <li><Link to="/usuarios">👤 Usuários</Link></li>}
        <li><Link to="/movimentacoes">🔄 Movimentações</Link></li>
        <li><Link to="/logs">📝 Logs</Link></li>
      </ul>
    </aside>
  );
};

export default Sidebar;
