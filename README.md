
# 🧠 Renomeador Inteligente de Arquivos com IA

Este projeto utiliza OCR (Tesseract) e a API da Groq (com modelo LLaMA 4) para **renomear automaticamente arquivos de imagem e PDF com base no conteúdo textual extraído**. Ideal para organizar documentos com nomes descritivos e únicos.

## ✨ Funcionalidades

- 📄 Leitura de PDFs e imagens (`.png`, `.jpg`, `.jpeg`)
- 🔎 Extração de texto com **Tesseract OCR**
- 🧠 Geração de nome para o arquivo via **Groq (LLaMA 4)** com base no conteúdo
- 🪪 Inclusão automática de CNPJ ou placa de veículo + data, se encontrados
- 🚚 Movimentação automática dos arquivos renomeados para uma pasta de destino
- 🚫 Evita sobrescrever arquivos já existentes

---

## 📁 Estrutura Esperada

```
📂 renamer/
├── arquivos/       <- Coloque aqui os arquivos a serem processados
├── renomeados/     <- Os arquivos renomeados serão movidos para cá
├── rename.py   <- Código principal
```

---

## 🚀 Como Usar

### 1. Clone o repositório

```bash
git clone https://github.com/ryanpichiteli/renamer.git
cd seurepositorio
```

### 2. Instale as dependências

Você pode usar um ambiente virtual (recomendado):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install pytesseract pillow pymupdf groq
```

### 3. Configure o Tesseract OCR

- Instale o Tesseract: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Altere no código o caminho para o executável do Tesseract, se necessário:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 4. Adicione sua chave da API Groq

No código, substitua:

```python
API_KEY = "SUA_API_KEY_AQUI"
```

Por sua chave válida da [Groq API](https://console.groq.com).

---

## 🧠 Como a IA nomeia os arquivos?

O modelo da Groq analisa o texto extraído e responde com:

- Um nome curto e descritivo (máx. 3 palavras)
- CNPJ detectado no texto (se houver)
- Placa de veículo + data, se presente

Exemplo de entrada:
> PDF com conteúdo de uma nota fiscal com CNPJ 12.345.678/0001-90

Saída:
> `NotaFiscal_12345678000190.pdf`

---

## 🛡️ Observações

- Apenas arquivos `.pdf`, `.jpg`, `.jpeg` e `.png` são suportados.
- Arquivos já renomeados não são sobrescritos — são ignorados.
- Caso o modelo falhe, o arquivo permanece inalterado.

---

## 📌 Licença

Este projeto é open-source e está licenciado sob a [MIT License](LICENSE).

---

## 💡 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou PRs com melhorias, sugestões ou correções.

---

## 👨‍💻 Autor

Desenvolvido por **[Seu Nome](https://github.com/ryanpichiteli)** 🧠🚀
