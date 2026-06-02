import React from "react";
import { Bar } from "react-chartjs-2";

const EstoqueChart = ({ produtos }) => {
  const data = {
    labels: produtos.map(p => p.nome),
    datasets: [
      {
        label: "Quantidade em Estoque",
        data: produtos.map(p => p.quantidade),
        backgroundColor: "rgba(54, 162, 235, 0.6)",
        borderRadius: 8,
      },
      {
        label: "Estoque Mínimo",
        data: produtos.map(p => p.estoqueMinimo),
        backgroundColor: "rgba(255, 99, 132, 0.6)",
        borderRadius: 8,
      },
      {
        label: "Estoque Máximo",
        data: produtos.map(p => p.estoqueMaximo),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#fff" }, // deixa legenda visível em fundo escuro
      },
    },
    scales: {
      x: {
        ticks: { color: "#fff" },
      },
      y: {
        ticks: { color: "#fff" },
      },
    },
  };

  return (
    <div style={{ background: "rgba(255,255,255,0.1)", padding: "20px", borderRadius: "12px" }}>
      <h3 style={{ color: "#fff" }}>Relatório de Estoque</h3>
      <Bar data={data} options={options} />
    </div>
  );
};

export default EstoqueChart;
