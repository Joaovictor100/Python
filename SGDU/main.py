import json
import os
from json import JSONDecodeError
from tabulate import tabulate

class UserManagement:
    def __init__(self, json_archiver):
        self.json_archiver = json_archiver
        self.data_json = {"usuarios": []}
        self.index = None

        if not os.path.exists(self.json_archiver):
            with open(self.json_archiver, "w") as arq:
                json.dump(self.data_json, arq, indent=4)
            self.index = 0
        
        try:
            with open(self.json_archiver, "r") as arq:
                self.data_json = json.load(arq)
            if self.index != 0:
                self.index = len(self.data_json["usuarios"])
        except JSONDecodeError:
            print("Erro ao carregar JSON. Iniciando vazio.")

    def manage(self):
        print("Bem vindo ao SGDU – Sistema de Gerenciamento de Dados do Usuário")

        while True:
            option = input("""\nDigite o número da opção:
1. Cadastrar
2. Excluir
3. Pesquisar
4. Listar
5. Editar
6. Sair\n>> """).sleep()

            if option == "1":
                nome = input("Nome: ")
                data = input("Data de nascimento: ")
                cpf = input("CPF: ")
                telefone = input("Telefone: ")

                if self._register_user(self.index, nome, data, cpf, telefone):
                    print("Usuário cadastrado com sucesso!")
                else:
                    print("Erro ao cadastrar usuário.")
            elif option == "2":
                self.display_user()
                index = int(input("Digite o ID do usuário que deseja excluir: "))
                if self._remove_user(index):
                    print("Usuário excluído.")
                else:
                    print("Erro ao excluir.")
            elif option == "3":
                pesquisa = input("""\nEscolha o que deseja pesquisar:
1. Nome
2. CPF
3. Telefone
4. Data de nascimento
>>""").sleep()
                
            elif option == "4":
                self.display_user()
            elif option == "6":
                print("Até mais!")
                break
            else:
                print("Função ainda não implementada ou inválida.")

    def _register_user(self, index, nome, data_nasc, cpf, telefone):
        novo_usuario = {
            "id": index,
            "nome": nome,
            "data_nasc": data_nasc,
            "cpf": cpf,
            "telefone": telefone
        }
        self.index += 1
        self.data_json["usuarios"].append(novo_usuario)
        return self.save_archiver(self.data_json, self.json_archiver)
    def _remove_user(self, index):
        try:
            del self.data_json["usuarios"][index]
            self.update_ids(self.data_json["usuarios"])
            self.index = len(self.data_json["usuarios"])
            return self.save_archiver(self.data_json, self.json_archiver)
        except IndexError:
            print("ID inválido.")
            return False
    def display_user(self):
        print("\nUsuários cadastrados:")
        print(tabulate(self.data_json["usuarios"], headers="keys", tablefmt="fancy_grid"))
    @staticmethod
    def save_archiver(data, filename):
        try:
            with open(filename, 'w') as arq:
                json.dump(data, arq, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False
    @staticmethod
    def update_ids(lista):
        for i, item in enumerate(lista):
            item["id"] = i

SGD = UserManagement('dado.json')
SGD.manage()
