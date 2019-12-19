import json
import requests
import io
import sys

url = "https://cloudbroker2019.herokuapp.com/{route}"
# url = "http://localhost:5000/{route}"
url_provedor = "http://localhost:{provedor}/{route}"
maquinas_em_uso = []


def procura():
    vcpu = int(input('Insira uma quantidade mínima de vCPU que deseja: '))
    ram = int(input('Insira uma quantidade mínima de RAM que deseja: '))
    disco = int(input('Insira uma quantidade mínima de disco que deseja: '))

    r = None
    maquina = {
        "qtd_vcpu": vcpu,
        "qtd_ram": ram,
        "qtd_disco": disco
    }

    # print(maquina)

    r = requests.post(url.format(route='encontrar'),
                      data=io.StringIO(json.dumps(maquina)))

    if r.status_code == 200:
        maquina = r.json()
        vcpu = maquina['qtd_vcpu']
        ram = maquina['qtd_ram']
        disco = maquina['qtd_disco']
        preco = maquina['preco']
        provedor = maquina['provedor']
        id = maquina['maquina']
        acesso = maquina['acesso']
        print('Encontramos uma máquina com as seguintes especificações:')
        print(f'Provedor: {provedor} - ID {id}')
        print(f"vCPU's: {vcpu}")
        print(f'RAM: {ram}')
        print(f'disco: {disco}')
        print(f'preco: R$ {preco}')
        print('Deseja utilizar esta máquina?\nY/yes/y or N/no/n')
        op = input()
        if op == 'Y' or op == 'y' or op == 'yes':
            usa(acesso=acesso, id=id, provedor=provedor)
        else:
            print('OK.')

    else:
        print('Nenhuma máquina foi encontrada')


def usa(acesso, id, provedor):
    try:
        r = requests.post(acesso, json={"id": id})

        if r.status_code == 200:
            maquinas_em_uso.append((provedor, id))
            print(
                f'A máquina com Provedor: {provedor} e ID: {id} está pronta para uso.\n')
        else:
            print(r.json()['mensagem'])
    except:
        print('Provedor está offline no momento.')


def libera():
    global maquinas_em_uso

    provedor = input(
        'Qual o provedor responsável pela máquina que deseja liberar?\n> ')
    id = input('Qual ID dá maquina que deseja liberar?\n> ')

    try:
        r = requests.post(url_provedor.format(
            provedor=provedor, route='liberar'), json={"id": id})

        if r.status_code == 200:
            maquinas_em_uso = list(
                filter(lambda x: x[0] != provedor and x[1] != id, maquinas_em_uso))
            print(
                f'A máquina com Provedor: {provedor} e ID: {id} foi liberada com sucesso.\n')
        else:
            print(r.json()['mensagem'])
    except:
        print('Provedor está offline no momento.')
        return


def listar():
    print('Máquinas em uso:')
    [print(f'Provedor: {i[0]} - ID: {i[1]}') for i in maquinas_em_uso]
    print()


if __name__ == "__main__":
    while True:
        menu = 'Seleciona a opção desejada\n\n'
        menu += '[1] - Encontrar máquina:\n'
        #menu += '[2] - Utilizar máquina:\n'
        menu += '[2] - Listar máquinas em uso\n'
        menu += '[3] - Liberar máquina\n'
        menu += '[0] - Sair\n'

        option = input(menu)

        if option == '1':
            procura()
        # elif option == '2':
        #     usa()
        elif option == '2':
            listar()
        elif option == '3':
            libera()
        elif option == '0':
            sys.exit()
        else:
            print('Opção inválida\n')
