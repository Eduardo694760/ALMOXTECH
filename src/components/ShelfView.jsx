import React from "react";
import "../styles/shelves.css";

const ShelfView = ({ items }) => {
  return (
    <div className="shelf-container">
      {items.map((item, index) => {
        // Define status visual com base na quantidade
        let statusClass = "status-ok";
        if (item.quantidade <= item.estoqueMinimo) {
          statusClass = "status-critical";
        } else if (item.quantidade < item.estoqueMaximo * 0.3) {
          statusClass = "status-warning";
        }

        return (
          <div key={item.id || index} className={`shelf-item ${statusClass}`}>
            <h4>{item.nome}</h4>
            <p>SKU: {item.sku}</p>
            <p>Qtd: {item.quantidade}</p>
            <p>
              Min: {item.estoqueMinimo} | Max: {item.estoqueMaximo}
            </p>
          </div>
        );
      })}
    </div>
  );
};

export default ShelfView;
