-- Inserir usuários
INSERT INTO usuarios (nome, login, senha_hash, permissao, ativo) VALUES
('Eduardo Silva', 'eduardo', 'senha123', 'OPERADOR', 1),
('Admin Almox', 'admin', 'admin456', 'ADMIN', 1);

-- Inserir produtos
INSERT INTO produtos (nome, sku, quantidade, descricao) VALUES
('Notebook Dell', 'NB001', 10, 'Core i5, 16GB RAM, SSD 512GB'),
('Mouse Sem Fio', 'MS001', 50, 'Mouse óptico ergonômico'),
('Teclado Mecânico', 'TC001', 25, 'Teclado RGB switch blue');

-- Inserir movimentações
INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao) VALUES
(1, 'ENTRADA', 10, 'Estoque inicial'),
(2, 'ENTRADA', 50, 'Compra fornecedor');
