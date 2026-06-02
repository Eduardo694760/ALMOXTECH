import React, { useState, useEffect } from "react";
import GlassCard from "../components/GlassCard";
import { Line } from "react-chartjs-2";

const Movimentacoes = () => {
  const [movimentacoes, setMovimentacoes] = useState([]);

  // Carregar movimentações do backend
  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:5000/api/movimentacoes", {
      headers: { Authorization: token }
    })
      .then(res => res.json())
      .then(data => setMovimentacoes(data))
      .catch(err => console.error("Erro ao carregar movimentações:", err));
  }, []);

  // Registrar movimentação
  const registrarMovimentacao = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    const novaMov = {
      produto: e.target.produto.value,
      tipo: e.target.tipo.value,
      quantidade: parseInt(e.target.quantidade.value),
      observacao: e.target.observacao.value,
      data: new Date().toLocaleString(),
    };

    await fetch("http://localhost:5000/api/movimentacoes", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: token },
      body: JSON.stringify(novaMov),
    });

    setMovimentacoes([...movimentacoes, novaMov]);
    e.target.reset();
  };

  // Dados para gráfico
  const chartData = {
    labels: movimentacoes.map(m => m.data),
    datasets: [
      {
        label: "Entradas",
        data: movimentacoes.map(m => m.tipo === "entrada" ? m.quantidade : 0),
        borderColor: "rgba(54, 162, 235, 0.8)",
        fill: false,
      },
      {
        label: "Saídas",
        data: movimentacoes.map(m => m.tipo === "saida" ? m.quantidade : 0),
        borderColor: "rgba(255, 99, 132, 0.8)",
        fill: false,
      },
    ],
  };

  return (
    <div className="movimentacoes-page">
      <h1 style={{ color: "#fff", textAlign: "center" }}>Movimentações de Estoque</h1>

      {/* Formulário */}
      <div className="movimentacoes-form">
        <GlassCard width="500px">
          <h3>Registrar Movimentação</h3>
          <form onSubmit={registrarMovimentacao} className="form-mov">
            <input type="text" name="produto" placeholder="Produto" required />
            <select name="tipo" required>
              <option value="entrada">Entrada</option>
              <option value="saida">Saída</option>
            </select>
            <input type="number" name="quantidade" placeholder="Quantidade" required />
            <textarea name="observacao" placeholder="Observações"></textarea>
            <button type="submit">Salvar</button>
          </form>
        </GlassCard>
      </div>

      {/* Histórico */}
      <div className="movimentacoes-list">
        <GlassCard width="700px">
          <h3>Histórico de Movimentações</h3>
          <ul>
            {movimentacoes.map((m, index) => (
              <li key={m.id || index}>
                <strong>{m.tipo.toUpperCase()}</strong> — {m.produto} | Qtd: {m.quantidade}
                <br />
                <small>{m.data}</small> | {m.observacao}
              </li>
            ))}
          </ul>
        </GlassCard>
      </div>

      {/* Gráfico */}
      <div className="movimentacoes-chart">
        <GlassCard width="800px">
          <h3>Relatório de Movimentações</h3>
          <Line data={chartData} />
        </GlassCard>
      </div>
    </div>
  );
};

export default Movimentacoes;
