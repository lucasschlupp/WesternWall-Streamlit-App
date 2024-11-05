import base64
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit as st

#título da página
st.set_page_config(page_title="Seu Nome no Muro das Lamentações", layout="centered")

# Connecta com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="dados", usecols= list(range(4)), ttl=5)
existing_data = existing_data.dropna(how="all")

contador = conn.read(worksheet="cont", usecols= list(range(1)), ttl=5)
contador = contador.dropna(how="all")
contador += 1
conn.update(worksheet="cont", data=contador)

# worksheet_name = "cont"

# # Função para ler a contagem atual e incrementá-la
# def incrementar_contador():
#     try:
#         # Ler a contagem atual da célula A1 da aba "cont"
#         df = conn.read(worksheet=worksheet_name, usecols=[0], ttl=5)  # ttl controla o cache para a leitura
        
#         # Verifica se o DataFrame não está vazio
#         if not df.empty and df.iloc[0, 0] is not None:
#             contador_atual = int(df.iloc[0, 0])  # Lê o valor atual da contagem
#         else:
#             contador_atual = 0  # Inicializa como 0 caso a célula A1 esteja vazia
#     except Exception as e:
#         st.error(f"Erro ao ler o contador: {e}")
#         contador_atual = 0  # Define 0 caso ocorra um erro de leitura

#     # Incrementa a contagem
#     contador_atualizado = contador_atual + 1
    
#     # Atualiza o valor na planilha
#     try:
#         conn.update(worksheet=worksheet_name, data=str(contador_atualizado))  # Atualiza na célula A1
#         st.write(f"Visitas atualizadas para: {contador_atualizado}")
#     except Exception as e:
#         st.error(f"Erro ao atualizar contador: {e}")

# Incrementar contador uma vez por sessão do usuário
# if 'contador_incrementado' not in st.session_state:
#     incrementar_contador()
#     st.session_state.contador_incrementado = True


#imagem de plano de fundo em bin
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Definindo background com a devida imagem
bg_image = get_base64_of_bin_file("muronoite.png")

# Apply CSS styling with the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Imagem título
st.image("nomenomuro.jpg")
st.divider()
# Imagem promo
st.image("promo.jpg")
st.divider()
# Frase inicial
st.header('''Você pode ter seu nome e uma oração colocados no Muro das Lamentaçãos em Jerusalém!''')
st.divider()

# Texto apresentação
st.header("Sobre o Muro:")
'''
O Muro das Lamentações, também conhecido como Kotel, é um local de extrema importância religiosa para os judeus. Trata-se do único vestígio remanescente do antigo Templo de Herodes, 
construído no lugar do Templo de Jerusalém original. Localizado no monte do Templo, é considerado o segundo local mais sagrado do judaísmo, atrás apenas do Santo dos Santos.\n
“Nesse lugar, de acordo com a tradição judaica, todas as orações de todas as pessoas no mundo sobem daqui. Aqui os portões do céu estão abertos a judeus e não judeus, da Terra ou da 
diáspora, fazem seus pedidos aqui por meio de anotações que eles inseriram entre as (pedras) do Muro das Lamentações”, diz Shmuel Rabinovitch, rabino do Muro das Lamentações e dos locais sagrados de Jerusalém.
'''
st.image("oracaonomuro.jpg")
st.subheader('Até mesmo pedidos não presenciais chegam ao local, pois as pessoas podem ter sua oração adicionada ao Muro das Lamentações por diversos meios.')
st.subheader('Se os judeus e os de outras religiões não puderem chegar ao Kotel, eles podem enviar seus pedidos por correio, e-mail ou texto.')
st.image("bilhetes.jpg")

st.subheader("Para ter seu nome colocado no muro das lamentações, insira seu NOME, E-MAIL e um PEDIDO DE ORAÇÃO:")
st.subheader("Em seguida pague a pequena taxa para cobrir os custos de manutenção do site.")
"ATENÇÃO: O pagamento será confirmado comparando o nome inserido no campo do proprietário da conta e o nome informado pelo depósito no banco."

# Input dados do usuário
form = st.form("Dados", True)
with form:
    pagador = st.text_input("Nome Completo do proprietário da conta do pagamento")
    name = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    message = st.text_area("Pedido de Oração (máximo de 300 caracteres)", max_chars=300)
#Botão de enviar
submit = form.form_submit_button("Faça o PIX com o código abaixo e clique aqui para ENVIAR")

if submit:
    # Verificação de entrada do usuário antes de salvar
    if name and email:  # Verifica se todos os campos foram preenchidos
        new_row = pd.DataFrame(
            [
                {
                    "Pagador": pagador,
                    "Nome": name,
                    "Email": email,
                    "Pedido de Oração": message
                }
            ]
        )
        # Junta os dados da planilha com novos dados
        dados_atualizados = pd.concat([existing_data, new_row], ignore_index=True)
        # Insere todos os dados na planilha
        conn.update(worksheet="dados", data=dados_atualizados)
        # Mensagem de sucesso
        st.success("Dados gravados com sucesso! Seu nome será colocado no Muro das Lamentações após confirmação do pagamento e em seguida receberás um e-mail de confirmação.")
       
        # Após enviar os dados, limpar os campos
        st.session_state.pagador = ""
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.message = ""
    else:
        st.error("Por favor, preencha todos os campos antes de enviar.")

# Chave PIX
st.subheader('''Chave PIX:
             '00020126780014br.gov.bcb.pix0136f5217104-8f82-4c69-9481-86875b09904b0216Meu Nome No Muro52040000530398654047.005802BR5913Lucas Schlupp6008Brasilia62090505mc7sw63048BF0' ''')
# Imagem do QR Code
st.image("qr.jpg", width=200)
 # Imagem de sucesso
st.image('papel.jpg')

# st.dataframe(existing_data)