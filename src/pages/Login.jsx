import React, { useState } from "react";
import GlassCard from "../components/GlassCard";

const Login = () => {
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, senha }),
      });

      const data = await response.json();

      if (data.status === "ok") {
        // Salva token JWT no localStorage
        localStorage.setItem("token", data.token);
        alert("Login realizado com sucesso!");
        window.location.href = "/dashboard"; // redireciona para dashboard
      } else {
        alert(data.mensagem || "Usuário ou senha inválidos!");
      }
    } catch (error) {
      console.error("Erro no login:", error);
      alert("Erro de conexão com o servidor.");
    }
  };

  return (
    <div className="login-container">
      <GlassCard width="350px">
        <h2 style={{ textAlign: "center" }}>Login</h2>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Usuário"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
          <button type="submit">Entrar</button>
        </form>
      </GlassCard>
    </div>
  );
};

export default Login;
