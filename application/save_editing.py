import os
import json
import shutil
import base64
import streamlit as st
import zipfile

game_name3 = base64.b64decode("TWlyNEdsb2JhbA==").decode("utf-8")

def save_config(save_dir : str, selected_config : str):
  delete_crashlogs()
  savedata_folder = os.path.join(st.session_state.chosen_dir, "SaveData")
  filename = os.path.join(save_dir, selected_config) + ".zip"
  if not os.path.exists(savedata_folder):
    print(f"Erro: O diretório base '{savedata_folder}' não existe.")

  with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(savedata_folder):
      print(root, dirs, files)
      for file in files:
        # Caminho completo do arquivo
        file_path = os.path.join(root, file)
        # Caminho relativo para manter a estrutura no ZIP
        arcname = os.path.relpath(file_path, savedata_folder)
        # Adiciona o arquivo ao ZIP
        zipf.write(file_path, arcname)
        print(f"Compactando: {arcname}")
  print(f"Arquivo ZIP '{filename}' criado com sucesso a partir de '{savedata_folder}'.")

def load_config(save_dir: str, selected_config: str):
  delete_savedata()
  save_data_path = os.path.join(st.session_state.chosen_dir, "SaveData")
  # Criar a pasta SaveData:
  if not os.path.exists(save_data_path):
    try:
      os.makedirs(save_data_path)
      print(f"Pasta '{save_data_path}' criada com sucesso.")
    except Exception as e:
      print(f"Erro ao criar a pasta '{save_data_path}': {e}")
      return
  # Abrir o arquivo ZIP e extrair a pasta Save:
  try:
    zip_path = os.path.join(save_dir, selected_config) + ".zip"
    with zipfile.ZipFile(zip_path, 'r') as zipf:
      # Filtra apenas os arquivos que pertencem à pasta 'Save/'
      save_files = [item for item in zipf.namelist() if item.startswith("Saved/")]
      if not save_files:
          print(f"A pasta 'Saved' não foi encontrada no arquivo '{zip_path}'.")
          return
      # Extrai os arquivos da pasta 'Save' para 'SaveData'
      zipf.extractall(path=save_data_path)
      print(f"Conteúdo da pasta 'Save' extraído para '{save_data_path}'.")
  except Exception as e:
    print(f"Erro ao extrair o arquivo '{zip_path}': {e}")


def create_config(save_dir: str, selected_config: str):
  empty_zip = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
  filename = os.path.join(save_dir, selected_config) + ".zip"
  if selected_config:
    if not os.path.exists(filename):
      with open(filename, 'wb') as zip:
        zip.write(empty_zip)
      st.session_state.create_config = True
    else:
      st.session_state.create_config = False

def save_options():
  json_filename = os.path.join(st.session_state.neo_account_dir, "config.json")
  data = {
    "global_path": st.session_state.global_path,
    "steam_path": st.session_state.steam_path
  }
  with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False)
    json_file.close()

def load_options():
  json_filename = os.path.join(st.session_state.neo_account_dir, "config.json")
  if os.path.exists(json_filename):
    with open(json_filename, "r") as json_file:
      data = json.load(json_file)
      st.session_state.global_path = data["global_path"]
      st.session_state.steam_path = data["steam_path"]

def delete_crashlogs():
  # Deletar crash logs:
  crashlogs_path = os.path.join(st.session_state.chosen_dir, "SaveData", "Saved", "Crashes")
  audiologs_path = os.path.join(st.session_state.chosen_dir, "SaveData", "Saved", "GME_LOG")
  paths_to_be_deleted = [crashlogs_path, audiologs_path]

  for subfolder in paths_to_be_deleted:
    dir_path = os.path.join(subfolder)

    # Verifica se o diretório existe
    if not os.path.exists(dir_path):
      print(f"O diretório '{dir_path}' não existe. Nada para deletar.")
      continue

    # Itera e deleta todo o conteúdo da subpasta
    for item in os.listdir(dir_path):
      item_path = os.path.join(dir_path, item)
      try:
        if os.path.isfile(item_path) or os.path.islink(item_path):
          os.unlink(item_path)
          print(f"Arquivo deletado: {item_path}")
        elif os.path.isdir(item_path):
          shutil.rmtree(item_path)
          print(f"Pasta deletada: {item_path}")
      except Exception as e:
        print(f"Erro ao deletar '{item_path}': {e}")

    print(f"Todos os arquivos na pasta '{dir_path}' foram deletados.")

def delete_savedata():
  savedata_path = os.path.join(st.session_state.chosen_dir, "SaveData")
  if not os.path.exists(savedata_path):
    print(f"A pasta '{savedata_path}' não existe.")
    return
  try:
    shutil.rmtree(savedata_path)
    print(f"A pasta '{savedata_path}' foi deletada com sucesso.")
  except Exception as e:
    print(f"Erro ao tentar deletar a pasta '{savedata_path}': {e}")

def validate_folder(save_dir: str, is_steam : bool):
  required_folders = ["Binaries", "Content", "Patches"]
  if is_steam and f"{game_name3}" in save_dir:
    return False
  if not is_steam and "steamapps" in save_dir:
    return False
  flag = True
  for folder in required_folders:
    folder_path = os.path.join(save_dir, folder)
    if not os.path.isdir(folder_path):
      flag = False
      break
  return flag