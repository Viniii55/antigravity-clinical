# Antigravity Clinical Writer

Assistente Clínico para o Dr. Rodrigo Abel Gomes, construído com Streamlit e OpenAI GPT-4o.

## Configuração

1.  **Instalar dependências:**
    Certifique-se de estar na pasta do projeto e execute:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Executar a aplicação:**
    ```bash
    streamlit run app.py
    ```

## Funcionalidades

- **Transcrição de Áudio:** Utiliza o modelo Whisper da OpenAI para transcrever áudios de casos.
- **Análise de Imagens:** Processa fotos de anotações manuscritas usando GPT-4o Vision.
- **Geração de Laudo:** Combina as informações em um laudo clínico formal ("História Clínica").
- **Exportação:** Permite baixar o resultado final em formato `.docx`.

## Requisitos

- Uma chave de API da OpenAI (necessária para rodar os modelos).
