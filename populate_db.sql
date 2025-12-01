-- Limpa produtos antigos para evitar conflitos
DELETE FROM produtos;

-- Reinicia a contagem do ID (Opcional, funciona no SQLite)
DELETE FROM sqlite_sequence WHERE name='produtos';

-- Inserir Produtos (Hardware e Periféricos)
INSERT INTO produtos (sku, nome, descricao, preco, estoque, categoria_id, imagem_url) VALUES
('MOUSE-LOG-G502', 'Mouse Gamer Logitech G502', 'Mouse de alto desempenho com 25.600 DPI, pesos ajustáveis e 11 botões programáveis.', 299.90, 50, 1, ''),

('KB-HYPERX-ALLOY', 'Teclado Mecânico HyperX Alloy', 'Teclado mecânico compacto ultra-resistente com switches Red lineares para jogos FPS.', 449.90, 30, 1, ''),

('MON-LG-24GL', 'Monitor LG UltraGear 24GL600F', 'Monitor Gamer LED 24" com taxa de atualização de 144Hz e tempo de resposta de 1ms.', 1299.00, 15, 2, ''),

('GPU-RTX-3060', 'Placa de Vídeo RTX 3060 12GB', 'Placa gráfica com Ray Tracing e DLSS, ideal para jogos em 1080p e 1440p no ultra.', 1899.00, 5, 3, ''),

('CPU-RYZEN-5600', 'Processador AMD Ryzen 5 5600X', 'Processador de 6 núcleos e 12 threads, clock boost de até 4.6GHz. Cooler Wraith Stealth incluso.', 999.00, 20, 3, ''),

('SSD-KING-1TB', 'SSD Kingston NV2 1TB NVMe', 'Armazenamento ultra-rápido M.2 2280 PCIe 4.0. Leitura de 3500MB/s e Gravação de 2100MB/s.', 349.90, 100, 3, ''),

('RAM-FURY-16GB', 'Memória RAM Kingston Fury 16GB', 'Módulo único DDR4 3200MHz com dissipador de calor de perfil baixo. Intel XMP Ready.', 229.90, 40, 3, ''),

('HEAD-JBL-Q400', 'Headset JBL Quantum 400', 'Headset gamer com som surround QuantumSURROUND, microfone flip-up e conforto para longas sessões.', 399.00, 25, 1, '');

-- Confirmação
SELECT count(*) as total_produtos FROM produtos;