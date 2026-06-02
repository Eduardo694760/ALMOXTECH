import React, { useEffect, useState } from "react";
import GlassCard from "../components/GlassCard";

const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([]);

  // Carregar usuários do backend
  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:5000/api/usuarios", {
      headers: { Authorization: token }
    })
      .then(res => res.json())
      .then(data => setUsuarios(data))
      .catch(err => console.error("Erro ao carregar usuários:", err));
  }, []);

  // Adicionar usuário
  const adicionarUsuario = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    const novoUsuario = {
      nome: e.target.nome.value,
      login: e.target.login.value,
      senha: e.target.senha.value,
      permissao: "USER", // padrão
    };

    await fetch("http://localhost:5000/api/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: token },
      body: JSON.stringify(novoUsuario),
    });

    setUsuarios([...usuarios, { ...novoUsuario, ativo: true }]);
    e.target.reset();
  };

  return (
    <div className="usuarios-page">
      <h1 style={{ color: "#fff", textAlign: "center" }}>Gerenciamento de Usuários</h1>

      {/* Formulário */}
      <div className="usuarios-form">
        <GlassCard width="400px">
          <h3>Adicionar Usuário</h3>
          <form onSubmit={adicionarUsuario} className="form-usuario">
            <input type="text" name="nome" placeholder="Nome" required />
            <input type="text" name="login" placeholder="Login" required />
            <input type="password" name="senha" placeholder="Senha" required />
            <button type="submit">Salvar</button>
          </form>
        </GlassCard>
      </div>

      {/* Lista */}
      <div className="usuarios-list">
        <GlassCard width="600px">
          <h3>Lista de Usuários</h3>
          <ul>
            {usuarios.map((u, index) => (
              <li key={u.id || index}>
                {u.nome} ({u.login}) — {u.ativo ? "Ativo" : "Inativo"} | Permissão: {u.permissao}
              </li>
            ))}
          </ul>
        </GlassCard>
      </div>
    </div>
  );
};

export default Usuarios;
