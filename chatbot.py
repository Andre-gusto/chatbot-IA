import tkinter as tk
from tkinter import messagebox
import json
import openai
import os

# Configuração da chave da API OpenAI
openai.api_key = 'sua-chave-da-api-openai'

# Função para obter a resposta do modelo
def obter_resposta_pergunta(pergunta, materia):
    try:
        # Carrega os conteúdos da matéria a partir de um arquivo JSON
        with open('conteudos.json', 'r') as f:
            conteudos = json.load(f)
        
        # Verifica se a matéria existe e recupera seus conteúdos
        if materia in conteudos:
            conteudo_materia = conteudos[materia]
        else:
            return "Desculpe, não encontrei conteúdos para essa matéria."

        # Pergunta ao modelo, baseado no conteúdo da matéria
        prompt = f"Pergunta: {pergunta}\nConteúdo da matéria: {conteudo_materia}\nResposta:"
        
        response = openai.Completion.create(
            engine="text-davinci-003",  # Você pode mudar para outro modelo, como "gpt-4"
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Erro ao obter a resposta: {str(e)}"

# Função para adicionar novos conteúdos
def adicionar_conteudo(materia, conteudo):
    try:
        # Carrega o arquivo JSON de conteúdos
        if os.path.exists('conteudos.json'):
            with open('conteudos.json', 'r') as f:
                conteudos = json.load(f)
        else:
            conteudos = {}

        # Adiciona ou atualiza o conteúdo da matéria
        conteudos[materia] = conteudo

        # Salva novamente o arquivo JSON
        with open('conteudos.json', 'w') as f:
            json.dump(conteudos, f, indent=4)
        
        messagebox.showinfo("Sucesso", f"Conteúdo da matéria '{materia}' adicionado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o conteúdo: {str(e)}")

# Função para alternar entre os modos de revisão e administração
def alternar_tela():
    if modo.get() == "revisor":
        revisao_frame.pack_forget()
        administrador_frame.pack_forget()
        revisao_frame.pack(padx=10, pady=10)
    else:
        revisao_frame.pack_forget()
        administrador_frame.pack_forget()
        administrador_frame.pack(padx=10, pady=10)

# Função para responder a pergunta no modo revisor
def perguntar():
    materia = materia_entry.get()
    pergunta = pergunta_entry.get()
    resposta = obter_resposta_pergunta(pergunta, materia)
    resposta_label.config(text=resposta)

# Função para adicionar conteúdo no modo administrador
def adicionar_conteudo_administrador():
    materia = materia_admin_entry.get()
    conteudo = conteudo_admin_entry.get("1.0", "end-1c")
    adicionar_conteudo(materia, conteudo)

# Interface Gráfica
root = tk.Tk()
root.title("Chatbot para Revisão de Conteúdos")

# Variável para definir o modo (revisor ou administrador)
modo = tk.StringVar(value="revisor")

# Frame de Revisor
revisao_frame = tk.Frame(root)
materia_label = tk.Label(revisao_frame, text="Matéria:")
materia_label.pack()
materia_entry = tk.Entry(revisao_frame)
materia_entry.pack()

pergunta_label = tk.Label(revisao_frame, text="Pergunta:")
pergunta_label.pack()
pergunta_entry = tk.Entry(revisao_frame)
pergunta_entry.pack()

perguntar_button = tk.Button(revisao_frame, text="Perguntar", command=perguntar)
perguntar_button.pack()

resposta_label = tk.Label(revisao_frame, text="Resposta aparecerá aqui.")
resposta_label.pack()

# Frame de Administrador
administrador_frame = tk.Frame(root)

materia_admin_label = tk.Label(administrador_frame, text="Matéria:")
materia_admin_label.pack()
materia_admin_entry = tk.Entry(administrador_frame)
materia_admin_entry.pack()

conteudo_admin_label = tk.Label(administrador_frame, text="Conteúdo da Matéria:")
conteudo_admin_label.pack()
conteudo_admin_entry = tk.Text(administrador_frame, height=10, width=40)
conteudo_admin_entry.pack()

adicionar_button = tk.Button(administrador_frame, text="Adicionar Conteúdo", command=adicionar_conteudo_administrador)
adicionar_button.pack()

# Menu de Modo
modo_menu = tk.OptionMenu(root, modo, "revisor", "administrador", command=lambda x: alternar_tela())
modo_menu.pack(pady=10)

# Inicia com o modo revisor
revisao_frame.pack(padx=10, pady=10)

root.mainloop()
