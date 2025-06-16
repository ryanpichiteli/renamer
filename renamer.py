import os
import pytesseract
from PIL import Image
import fitz 
from groq import Groq
import shutil  

# MODIFICAR!!!!
pasta_arquivos = 'arquivos' # Pasta onde os arquivos originais estão localizados
pasta_saida = 'renomeados' # Pasta onde os arquivos renomeados serão salvos
API_KEY = "SUA_API_KEY_AQUI"  # Substitua pela sua chave de API Groq


# Configuração do Tesseract (ajuste o caminho se precisar)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\.exe'


client = Groq( api_key= API_KEY )

def limpar_nome(texto):
    return ''.join(c for c in texto if c.isalnum() or c in (' ', '_', '-')).strip()

def gerar_nome_por_groq(texto):
    prompt = f"""
Você é um assistente inteligente que cria nomes curtos e únicos para arquivos, baseado no conteúdo do texto fornecido.

Regras:
- Gere um nome simples, claro e descritivo.
- Use no máximo 3 palavras.
- Não use caracteres especiais, apenas letras, números, espaços, underscores ou hífens.
- Evite repetir palavras.
- O nome deve ajudar a identificar o conteúdo principal do arquivo.
- Você não deve incluir a extensão do arquivo no nome gerado.
- Você deve responder apenas o nome, nada de "com base em", introduções em geral, apenas responda o nome.
- Coloque o CNPJ que contem no arquivo(se houver).
- Se houver placa de veiculo, o nome deve ser a placa e a data.

Texto extraído:
{texto}

Nome do arquivo:
"""
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=20,
            top_p=1,
            stream=False,
            stop=None,
        )
        resposta = completion.choices[0].message.content
        return limpar_nome(resposta)
    except Exception as e:
        print(f"Erro ao chamar Groq: {e}")
        return None

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    doc = fitz.open(caminho_pdf)
    for pagina in doc:
        texto += pagina.get_text()
    return texto



# Verificações
if not os.path.isdir(pasta_arquivos):
    print(f"Pasta '{pasta_arquivos}' não encontrada. Crie a pasta e adicione os arquivos.")
    exit(1)

# Cria a pasta de saída se não existir
os.makedirs(pasta_saida, exist_ok=True)

# Processamento dos arquivos
for nome_arquivo in os.listdir(pasta_arquivos):
    caminho = os.path.join(pasta_arquivos, nome_arquivo)

    if os.path.isfile(caminho):
        texto_extraido = ""
        ext = nome_arquivo.lower().split('.')[-1]

        try:
            if ext in ['png', 'jpg', 'jpeg']:
                imagem = Image.open(caminho)
                texto_extraido = pytesseract.image_to_string(imagem, lang='por')

            elif ext == 'pdf':
                texto_extraido = extrair_texto_pdf(caminho)

            else:
                print(f"Extensão {ext} não suportada para {nome_arquivo}")
                continue

            if texto_extraido.strip():
                novo_nome = gerar_nome_por_groq(texto_extraido)
                if novo_nome:
                    novo_nome_com_ext = f"{novo_nome}.{ext}"
                    novo_caminho = os.path.join(pasta_saida, novo_nome_com_ext)

                    # Evitar sobrescrever arquivos existentes
                    if os.path.exists(novo_caminho):
                        print(f"Aviso: arquivo {novo_nome_com_ext} já existe em '{pasta_saida}'. Pulando renomeação de {nome_arquivo}")
                        continue

                    shutil.move(caminho, novo_caminho)
                    print(f'Renomeado e movido: {nome_arquivo} -> {novo_nome_com_ext}')
                else:
                    print(f"Não foi possível gerar nome para {nome_arquivo}")
            else:
                print(f'⚠️ Nenhum texto encontrado em {nome_arquivo}')
        except Exception as e:
            print(f'Erro ao processar {nome_arquivo}: {e}')
