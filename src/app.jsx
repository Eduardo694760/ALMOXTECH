import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dasboard";
import Produtos from "./pages/Produtos";
import Usuarios from "./pages/Usuarios";
import Movimentacoes from "./pages/Movimentacoes";
import Logs from "./pages/Logs";

function App() {
  return (
    <Router>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Sidebar />
        <div style={{ marginLeft: "240px", flex: 1, padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/produtos" element={<Produtos />} />
            <Route path="/usuarios" element={<Usuarios />} />
            <Route path="/movimentacoes" element={<Movimentacoes />} />
            <Route path="/logs" element={<Logs />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
