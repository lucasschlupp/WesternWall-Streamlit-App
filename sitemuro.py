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

# #imagem de plano de fundo em bin
# def get_base64_of_bin_file(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# # Definindo background com a devida imagem
# bg_image = get_base64_of_bin_file("muronoite.png")

# # Apply CSS styling with the background image
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/jpg;base64,{bg_image}");
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Imagem título
st.image("nomenomuro.jpg")
st.divider()
# Imagem promo
# st.image("promo.jpg")
# st.divider()
# Frase inicial
st.header('''Você pode ter seu nome e uma oração colocados no Muro das Lamentaçãos em Jerusalém!''')
st.divider()
st.header('Como funciona:')
st.subheader('Você insere seu nome, e-mail e uma oração. Uma equipe do ministério em Jerusalém imprime, coloca no muro e lhe envia um e-mail para informar que sua oração foi colocadan o muro.')
st.subheader('Por fim, você pode contribuir com o ministério com a quantia que Deus lhe tocar o coração e ajudar a manter esse trabalho lindo de levar a oração das pessoas direto para Jerusalém!')
st.divider()
# Texto apresentação
st.subheader("Mas por quê colocar um bilhete com meu nome no Muro das Lamentações?")
st.header("Sobre o Muro:")
'''
O Muro das Lamentações, também conhecido como Kotel, é um local de extrema importância religiosa para os judeus. Trata-se do único vestígio remanescente do antigo Templo de Herodes, 
construído no lugar do Templo de Jerusalém original. Localizado no monte do Templo, é considerado o segundo local mais sagrado do judaísmo, atrás apenas do Santo dos Santos.\n
“Nesse lugar, de acordo com a tradição judaica, todas as orações de todas as pessoas no mundo sobem daqui. Aqui os portões do céu estão abertos a judeus e não judeus, da Terra ou da 
diáspora, fazem seus pedidos aqui por meio de anotações que eles inseriram entre as (pedras) do Muro das Lamentações”, diz Shmuel Rabinovitch, rabino do Muro das Lamentações e dos locais sagrados de Jerusalém.
'''
st.image("oracaonomuro.jpg", width=400)
st.subheader('Até mesmo pedidos não presenciais chegam ao local, pois as pessoas podem ter sua oração adicionada ao Muro das Lamentações por diversos meios.')
st.subheader('Se os judeus e os de outras religiões não puderem chegar ao Kotel, eles podem enviar seus pedidos por correio, e-mail ou texto.')
st.image("bilhetes.jpg", width=400)

st.subheader("Para ter seu nome colocado no muro das lamentações, insira seu NOME, E-MAIL e um PEDIDO DE ORAÇÃO:")
# st.subheader("Em seguida pague a pequena taxa para cobrir os custos de manutenção do site.")
# "ATENÇÃO: O pagamento será confirmado comparando o nome inserido no campo do proprietário da conta e o nome informado pelo depósito no banco."

# Input dados do usuário
form = st.form("Dados", True)
with form:
    pagador = st.text_input("Nome Completo do proprietário da conta do pagamento")
    name = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    message = st.text_area("Pedido de Oração (máximo de 300 caracteres)", max_chars=300)
#Botão de enviar
submit = form.form_submit_button("ENVIAR")
imagem_papel = False
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
        st.success("Dados gravados com sucesso! Seu nome será colocado no Muro das Lamentações e em seguida receberás um e-mail de confirmação.")
        imagem_papel = True
        # Após enviar os dados, limpar os campos
        st.session_state.pagador = ""
        st.session_state.name = ""
        st.session_state.email = ""
        st.session_state.message = ""
    else:
        st.error("Por favor, preencha todos os campos antes de enviar.")

# Chave PIX
st.subheader('''Contribua com o nosso Ministério utilizando a Chave PIX (qualuqer valor):
             '00020126830014br.gov.bcb.pix0136f5217104-8f82-4c69-9481-86875b09904b0221Muro das Lamentacoes 5204000053039865802BR5913Lucas Schlupp6008Brasilia62090505hiafw630428B9' ''')
# Imagem do QR Code
st.image("qrsemvalor.jpg", width=200)
 # Imagem de sucesso
if imagem_papel == True:
    st.image('papel.jpg', width=400)
    
