import os
import shutil
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
def encontrar_e_mover_arquivos(origem, numeros_nf):
destino = os.path.join(origem, 'Arquivo(s) encontrado(s)')
os.makedirs(destino, exist_ok=True)
for numero_nf in numeros_nf:
for root, _, files in os.walk(origem):
for file in files:
if numero_nf in file:
origem_arquivo = os.path.join(root, file)
nome_arquivo, extensao = os.path.splitext(file)
destino_arquivo = os.path.join(destino, file)
if not os.path.exists(destino_arquivo):
shutil.copy2(origem_arquivo, destino_arquivo)
estilo_texto = {'font': ('Helvetica', 16)}
sg.theme('DefaultNoMoreNagging')
imagem_path = "locaolizador.png"
layout = [
[sg.Stretch(),sg.Image(key="-IMAGE-"), sg.Stretch()],
[sg.Stretch(),sg.Text("LOCÃOLIZADOR DE ARQUIVO", justification="center", **estilo_texto),sg.Stretch()],
[sg.Text("Digite o nome do(s) arquivos que deseja buscar (Separados por Enter):")],
[sg.Multiline(key='numeros_nf', size=(57, 5))],
[sg.Button("Selecionar Pasta"), sg.Exit()],
[sg.Text("", size=(40, 1), key='resultado')],
]
window = sg.Window("LocãoLizador", layout,finalize=True)
# Carregue a imagem com Pillow
imagem = Image.open(imagem_path)
# Redimensione a imagem para se ajustar a uma dimensão máxima de 200x200
largura_max = 200
altura_max = 200
imagem.thumbnail((largura_max, altura_max))
# Converta a imagem do Pillow para bytes
imagem_bytes = io.BytesIO()
imagem.save(imagem_bytes, format="PNG")
imagem_bytes.seek(0)
# Crie um objeto ImageTk a partir da imagem redimensionada
imagem_tk = ImageTk.PhotoImage(file=imagem_bytes)
# Atualize o elemento sg.Image com a imagem
window["-IMAGE-"].update(data=imagem_tk)
while True:
event, values = window.read()
if event == sg.WINDOW_CLOSED or event == 'Exit':
break
if event == 'Selecionar Pasta':
pasta_origem = sg.popup_get_folder("Selecione a pasta de origem")
if pasta_origem:
numeros_nf = values['numeros_nf'].split('\n')
encontrar_e_mover_arquivos(pasta_origem, numeros_nf)
window['resultado'].update("Arquivos movidos com sucesso para a área de trabalho na pasta 'Arquivo(s) Encontrado(s)' ")
window.close()