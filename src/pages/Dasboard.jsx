import React, { useEffect, useState } from "react";
import GlassCard from "../components/GlassCard";
import ShelfView from "../components/ShelfView";
import EstoqueChart from "../components/EstoqueChart";

const Dashboard = () => {
  const [produtos, setProdutos] = useState([]);

  // Carregar produtos do backend
  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:5000/api/produtos", {
      headers: { Authorization: token }
    })
      .then(res => res.json())
      .then(data => setProdutos(data));
  }, []);

  return (
    <div className="dashboard-page">
      <h1 style={{ color: "#fff", textAlign: "center" }}>Painel do Almoxarifado</h1>

      {/* Cards de resumo */}
      <div className="dashboard-cards">
        <GlassCard width="300px">
          <h3>Resumo</h3>
          <p>Total de Produtos: {produtos.length}</p>
        </GlassCard>

        <GlassCard width="300px">
          <h3>Alertas</h3>
          <p>Produtos críticos: {produtos.filter(p => p.quantidade <= p.estoqueMinimo).length}</p>
        </GlassCard>
      </div>

      {/* Gráfico de estoque */}
      <div className="dashboard-chart">
        <EstoqueChart produtos={produtos} />
      </div>

      {/* Lista visual de produtos */}
      <div className="dashboard-shelves">
        <ShelfView items={produtos} />
      </div>
    </div>
  );
};

export default Dashboard;
