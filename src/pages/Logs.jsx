import React, { useEffect, useState } from "react";
import GlassCard from "../components/GlassCard";

const Logs = () => {
  const [logs, setLogs] = useState([]);

  // Carregar logs do backend
  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:5000/api/logs", {
      headers: { Authorization: token }
    })
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(err => console.error("Erro ao carregar logs:", err));
  }, []);

  return (
    <div className="logs-page">
      <h1 style={{ color: "#fff", textAlign: "center" }}>Histórico de Ações</h1>

      <div className="logs-list">
        <GlassCard width="800px">
          <h3>Logs do Sistema</h3>
          <table className="logs-table">
            <thead>
              <tr>
                <th>Ação</th>
                <th>Usuário</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody>
              {logs.length > 0 ? (
                logs.map((log, index) => (
                  <tr key={log.id || index}>
                    <td>{log.acao}</td>
                    <td>{log.usuario}</td>
                    <td>{log.data}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" style={{ textAlign: "center" }}>
                    Nenhum log encontrado
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </GlassCard>
      </div>
    </div>
  );
};

export default Logs;
