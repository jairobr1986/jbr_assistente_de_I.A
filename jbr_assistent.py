import os
import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="JBR AI Coder",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "jbr1986 ",
um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores iniciantes com dificuldades
REGRAS DE OPERAÇÃO:
1.  ** Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário tiver alguma outra pergunta pode responder tudo o que ele perguntar
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado e auto explicativo.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada Documentação de Referência" com um link direto e relevante para a documentação.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# criar conteúdo na barra lateral do streamlit
with st.sidebar:
    st.title("JBR1986 AI Coder")

    st.markdown("Um assistente de IA focado em progamação")
    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )
    # adicionar linha na barra latera
    st.markdown("---")
    st.markdown("Desenvolvido para ajudar nas dúvidas de programação com python. ")

    st.markdown("---")
    st.markdown("Venha fazer esse curso na DSA, e me siga no GIT ou LINKENDIN -> jairobr1986")
    st.markdown("[LinkedIn - jairobr1986](https://www.linkedin.com/in/jairobr1986)")
    st.markdown("[GitHub - jairobr1986](https://github.com/jairobr1986)")

    # botão de link para enviar email para suporte ou qualquer outro email
    st.link_button("📩 e-mail para suporte ou jbr1986", "malito:email@email.com")

# Titulo principal do APP
st.title("JBR1986 - Aprendendo streamlit")

# Titulo adicional 🐍
st.title("Assitente pessoal de programação python - JBR1986 ")

# Texto auxiliar abaixo do titulo
st.caption("faça sua pergunta sobre python e obtenha código, explicações e referências.".title())

# inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variavel do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave API da Groq
if groq_api_key:
    try:
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key=groq_api_key)
    except Exception as e:

        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq:{e}")
        st.stop()
elif st.session_state.messages:
    st.warning("Por favor, insira as sua API Key da Groq na barra lateral para continuar.")

# Capturando a entrada no chat feita pelo usuário
if prompt := st.chat_input("Qual sua dúvida sobre qualquer tema?"):
    # Se não houver cliente válido, mostra aviso e para a execução do app
    if not client:
        st.warning("Por favor, insira as sua API Key da Groq na barra lateral para continuar. ")
        st.stop()

        # Armazenando a mensagem do usuário na sessão
        st.session_state.mesages.append({"role":"user", "content": prompt})

    # Exibindo mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepara a mensagem para ser levada até a API, incluindo o prompt do sistema
    messages_for_api = [{"role":"system", "content":CUSTOM_PROMPT}]
    for msg in st.session_state.messages:

        messages_for_api.append(msg)

    # Aqui cria a resposta do assistente no chat
    with st.chat_message("assistant"):

        with st.spinner("analisando sua pergunta..."):

            try:
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b",
                    temperature = 0.7,
                    max_tokens = 2048,
                )

                # Aqui vai extrair a resposta gerada pela API
                jbr_ai_resposta = chat_completion.choices[0].message.content

                # Exibe a resposta no meu APP Streamlit
                st.markdown(jbr_ai_resposta)

                # Armazena a resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content":jbr_ai_resposta})
            except Exception as e:
                st.error(f"Houve um erro ao se comunicar com a API da Groq: {e}")
st.markdown(
    """ 
    <div style="text-align: center; color: gray;">
        <hr>
        <p>jbr1986 AI Coder - Parte Integrante do Curso Gratuito Fundamentos de Linguagem Python da Data Science Academy</p>
        </div>
    """,
    unsafe_allow_html=True
)
