# streamlit run application/main.py
# pyinstaller launcher.spec --clean
import streamlit as st
import os
import base64
import save_editing

# Eu não quero que strings relacionadas ao jogo apareçam nas buscas de código do GitHub.
game_name = base64.b64decode("TUlSNA==").decode("utf-8")
game_name2 = base64.b64decode("TWlyTW9iaWxl").decode("utf-8")

def update_global_path():
  global_path = st.session_state.global_path
  if global_path:
    if save_editing.validate_folder(global_path, False):
      st.session_state.global_path = global_path
      st.session_state.invalid_global = False
    else:
      st.session_state.invalid_global = True
  else:
    st.session_state.invalid_global = False

def update_steam_path():
  steam_path = st.session_state.steam_path
  if steam_path:
    if save_editing.validate_folder(steam_path, True):
      st.session_state.steam_path = steam_path
      st.session_state.invalid_steam = False
    else:
      st.session_state.invalid_steam = True
  else:
    st.session_state.invalid_steam = False

def page_setup():
  # Pra não recarregar:
  if not 'invalid_global' in st.session_state:
    st.session_state.invalid_global = False
    st.session_state.invalid_steam = False
  # Instalações:
  st.subheader("Defina o caminho das instalações:")
  global_path = st.text_input(f"Caminho {game_name} Global", key="global_path", placeholder=f"Digite o caminho do {game_name} Global (Pasta {game_name2})", on_change=update_global_path)
  steam_path = st.text_input(f"Caminho {game_name} Steam", key="steam_path", placeholder=f"Digite o caminho do {game_name} Steam (Pasta {game_name2})", on_change=update_steam_path)
  if st.session_state.global_path:
    if not st.session_state.invalid_global:
      st.success("Pasta Global validada com sucesso!")
    else:
      st.error("Pasta Global inválida!")
  else:
      st.info("Pasta Global não informada.")
  if st.session_state.steam_path:
    if not st.session_state.invalid_steam:
      st.success("Pasta Steam validada com sucesso!")
    else:
      st.error("Pasta Steam inválida!")
  else:
      st.info("Pasta Steam não informada.")
  save_editing.save_options()

def page_editing():
  st.subheader("Selecione a versão para gerenciar:")
  # Ver se os diretórios do jogo já foram informados:
  options = []
  if st.session_state.global_path:
    options.append("global")
  if st.session_state.steam_path:
    options.append("steam")
  if not options:
    st.info("Configure as pastas primeiro.")
  else:
    # Escolher qual dos dois vai mexer:
    st.session_state["global"] = False
    st.session_state["steam"] = False
    chosen_version = st.radio(label="Versão:", options=options, index=None, horizontal=True, key="RadioConfigEdit")
    # Mostrar configurações salvas:
    if chosen_version:
      save_dir = st.session_state.save_dir_global if ("global" in chosen_version) else st.session_state.save_dir_steam
      st.session_state.chosen_dir = st.session_state.global_path if ("global" in chosen_version) else st.session_state.steam_path
      saved_configs = [f.replace(".zip", "") for f in os.listdir(save_dir) if f.endswith(".zip")]
      selected_config = st.selectbox("Selecione uma configuração salva", ["N/A"] + saved_configs)
      if st.button("Salvar Configuração") and selected_config != "N/A":
        if os.path.isdir(save_dir):
          print("Diretório:", save_dir)
          save_editing.save_config(save_dir, selected_config)
          st.success(f"Configuração '{selected_config}' salva com sucesso!")
      if st.button("Carregar Configuração"):
        if os.path.isdir(save_dir):
          save_editing.load_config(save_dir, selected_config)
          st.success(f"Configuração '{selected_config}' carregada com sucesso!")

def page_create():
  # Criar slot novo de configuração:
  st.subheader("Criar slot de configuração:")
  # Ver se os diretórios do jogo já foram informados:
  options = []
  if st.session_state.global_path:
    options.append("global")
  if st.session_state.steam_path:
    options.append("steam")
  if not options:
    st.info("Configure as pastas primeiro.")
  else:
    slot_name = st.text_input("Nome do slot:")
    save_dir = None
    st.session_state["global"] = False
    st.session_state["steam"] = False
    chosen_version = st.radio(label="Versão:", options=options, index=None, horizontal=True, key="RadioConfigAdd")
    if chosen_version:
      save_dir = st.session_state.save_dir_global if ("global" in chosen_version) else st.session_state.save_dir_steam
      st.session_state.chosen_dir = st.session_state.global_path if ("global" in chosen_version) else st.session_state.steam_path
      st.button("Criar slot vazio", on_click=save_editing.create_config, args=(save_dir, slot_name))
      if "create_config" in st.session_state:
        if st.session_state.create_config == True:
          st.success("Slot criado com sucesso!")
        if st.session_state.create_config == False:
          st.info("O slot já existe!")
        st.session_state.create_config = None
      st.subheader("Extras:")
      st.button("Deletar configuração atual do jogo -- APAGAR TUDO", on_click=save_editing.delete_savedata)
      st.subheader("Utilidade:")
      st.button("Deletar crash logs", on_click=save_editing.delete_crashlogs)

def run():
  # Pasta do programa:
  neo_account_dir = os.path.join(os.getenv("APPDATA"), "NeoAccount")
  os.makedirs(neo_account_dir, exist_ok=True)
  # Pastas em que as configurações são salvas:
  save_dir_global = os.path.join(neo_account_dir, "configs_global")
  save_dir_steam = os.path.join(neo_account_dir, "configs_steam")
  os.makedirs(save_dir_global, exist_ok=True)
  os.makedirs(save_dir_steam, exist_ok=True)
  # Deixar acessível ao resto do programa:
  st.session_state.neo_account_dir = neo_account_dir
  st.session_state.save_dir_global = save_dir_global
  st.session_state.save_dir_steam = save_dir_steam
  # Inicializar variáveis:
  if "global_path" not in st.session_state:
    st.session_state.global_path = None
  if "steam_path" not in st.session_state:
    st.session_state.steam_path = None
  # Carregar opções salvas:
  # Evitar variáveis sendo redefinidas no refresh:
  if not 'initialized' in st.session_state:
    st.session_state.initialized = True
    save_editing.load_options()
  # Tirar a margem horrorosa do Streamlit:
  hide_streamlit_style = """
  <style>
      .stMainBlockContainer {padding-top: 0rem;}
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stAppDeployButton {visibility: hidden;}
      .stAppHeader {visibility: hidden;}
  </style>
  """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)
  # Criar as páginas:
  tab1, tab2, tab3 = st.tabs(["Gerenciar saves", "Configuração do jogo", "Adicionar saves"])
  with tab1:
    page_editing()
  with tab2:
    page_setup()
  with tab3:
    page_create()
  st.markdown("<sup class=\"watermark-text\"><b>Agradecimentos especiais aos jogadores do SA54, SA81 e EU24.</sup></b>", unsafe_allow_html=True)
  st.markdown(
    """
    <style>
    .watermark-text{
        position:fixed;
        bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True
  )



if __name__ == "__main__":
  run()
