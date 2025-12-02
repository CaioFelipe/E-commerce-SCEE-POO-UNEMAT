-- Limpa dados antigos para evitar conflitos (ordem importa por causa das chaves estrangeiras)
DELETE FROM itens_pedido;
DELETE FROM pedidos;
DELETE FROM itens_carrinho;
DELETE FROM carrinhos;
DELETE FROM produtos;
DELETE FROM categorias;

-- Reinicia a contagem dos IDs (Funciona no SQLite)
DELETE FROM sqlite_sequence WHERE name='produtos';
DELETE FROM sqlite_sequence WHERE name='categorias';
DELETE FROM sqlite_sequence WHERE name='pedidos';

-- 1. Inserir Categorias
INSERT INTO categorias (nome) VALUES 
('Hardware'), 
('Periféricos'), 
('Monitores'), 
('Computadores');

-- 2. Inserir Produtos (Associados às Categorias acima)
-- Nota: Assumindo que os IDs gerados serão 1, 2, 3, 4 na ordem de inserção.

INSERT INTO produtos (sku, nome, descricao, preco, estoque, categoria_id, imagem_url) VALUES
-- Categoria: Hardware (ID 1)
('GPU-RTX-3060', 'Placa de Vídeo RTX 3060 12GB', 'Placa gráfica com Ray Tracing e DLSS, ideal para jogos em 1080p e 1440p no ultra.', 1899.00, 5, 1, ''),
('CPU-RYZEN-5600', 'Processador AMD Ryzen 5 5600X', 'Processador de 6 núcleos e 12 threads, clock boost de até 4.6GHz. Cooler Wraith Stealth incluso.', 999.00, 20, 1, ''),
('SSD-KING-1TB', 'SSD Kingston NV2 1TB NVMe', 'Armazenamento ultra-rápido M.2 2280 PCIe 4.0. Leitura de 3500MB/s e Gravação de 2100MB/s.', 349.90, 100, 1, ''),
('RAM-FURY-16GB', 'Memória RAM Kingston Fury 16GB', 'Módulo único DDR4 3200MHz com dissipador de calor de perfil baixo. Intel XMP Ready.', 229.90, 40, 1, ''),

-- Categoria: Periféricos (ID 2)
('MOUSE-LOG-G502', 'Mouse Gamer Logitech G502', 'Mouse de alto desempenho com 25.600 DPI, pesos ajustáveis e 11 botões programáveis.', 299.90, 50, 2, ''),
('KB-HYPERX-ALLOY', 'Teclado Mecânico HyperX Alloy', 'Teclado mecânico compacto ultra-resistente com switches Red lineares para jogos FPS.', 449.90, 30, 2, ''),
('HEAD-JBL-Q400', 'Headset JBL Quantum 400', 'Headset gamer com som surround QuantumSURROUND, microfone flip-up e conforto para longas sessões.', 399.00, 25, 2, ''),

-- Categoria: Monitores (ID 3)
('MON-LG-24GL', 'Monitor LG UltraGear 24GL600F', 'Monitor Gamer LED 24" com taxa de atualização de 144Hz e tempo de resposta de 1ms.', 1299.00, 15, 3, '');

-- Confirmação
SELECT count(*) as total_produtos FROM produtos;