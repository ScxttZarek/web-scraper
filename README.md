# Web Scraper de Citações

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org/)
[![Requests](https://img.shields.io/badge/Requests-2.32.3-green)](https://requests.readthedocs.io/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12.3-yellow)](https://www.crummy.com/software/BeautifulSoup/)

Scraper que extrai citações do site [quotes.toscrape.com](http://quotes.toscrape.com) e salva em SQLite.

## 🚀 Funcionalidades

- Raspagem de múltiplas páginas
- Extração de texto, autor e tags
- Armazenamento em banco SQLite
- Controle de páginas via argumento

## 📦 Como rodar

```bash
pip install -r requirements.txt
python web_scraper.py --pages 3 --db quotes.db
```

## 🧪 Exemplo de saída

```
Raspando página 1...
Raspando página 2...
Raspando página 3...
Salvas 30 citações em quotes.db
```

## 📄 Licença

MIT
