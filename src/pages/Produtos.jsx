import React, { useState, useEffect } from "react";
import GlassCard from "../components/GlassCard";

const Produtos = () => {
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

  // Adicionar produto
  const adicionarProduto = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");

    const novoProduto = {
      nome: e.target.nome.value,
      sku: e.target.sku.value,
      quantidade: parseInt(e.target.quantidade.value),
      estoqueMinimo: parseInt(e.target.estoqueMinimo.value),
      estoqueMaximo: parseInt(e.target.estoqueMaximo.value),
    };

    await fetch("http://localhost:5000/api/produtos", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: token },
      body: JSON.stringify(novoProduto),
    });

    setProdutos([...produtos, novoProduto]);
    e.target.reset();
  };

  // Editar produto
  const editarProduto = async (id) => {
    const token = localStorage.getItem("token");
    await fetch(`http://localhost:5000/api/produtos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", Authorization: token },
      body: JSON.stringify({
        nome: "Produto Editado",
        sku: "EDITADO",
        quantidade: 99,
        estoqueMinimo: 10,
        estoqueMaximo: 200,
      }),
    });
    alert("Produto atualizado!");
  };

  // Deletar produto
  const deletarProduto = async (id) => {
    const token = localStorage.getItem("token");
    await fetch(`http://localhost:5000/api/produtos/${id}`, {
      method: "DELETE",
      headers: { Authorization: token },
    });
    setProdutos(produtos.filter(p => p.id !== id));
  };

  return (
    <div className="produtos-page">
      <h1 style={{ color: "#fff", textAlign: "center" }}>Gerenciamento de Produtos</h1>

      {/* Formulário de cadastro */}
      <div className="produtos-form">
        <GlassCard width="400px">
          <h3>Adicionar Produto</h3>
          <form onSubmit={adicionarProduto} className="form-produto">
            <input type="text" name="nome" placeholder="Nome" required />
            <input type="text" name="sku" placeholder="SKU" required />
            <input type="number" name="quantidade" placeholder="Quantidade" required />
            <input type="number" name="estoqueMinimo" placeholder="Estoque Mínimo" required />
            <input type="number" name="estoqueMaximo" placeholder="Estoque Máximo" required />
            <button type="submit">Salvar</button>
          </form>
        </GlassCard>
      </div>

      {/* Lista de produtos */}
      <div className="produtos-shelves">
        {produtos.map((p, index) => (
          <GlassCard key={index} width="300px">
            <h3>{p.nome}</h3>
            <p>SKU: {p.sku}</p>
            <p>Quantidade: {p.quantidade}</p>
            <p>Min: {p.estoqueMinimo} | Max: {p.estoqueMaximo}</p>
            <button onClick={() => editarProduto(p.id)}>Editar</button>
            <button onClick={() => deletarProduto(p.id)}>Excluir</button>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};

export default Produtos;
