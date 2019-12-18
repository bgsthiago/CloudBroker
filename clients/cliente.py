import json
import requests
import io

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

    print(maquina)

    r = requests.post(url.format(route='encontrar'), data=io.StringIO(json.dumps(maquina)))

    if r.status_code == 200:
        maquina = r.json()
        vcpu = maquina['qtd_vcpu']
        ram = maquina['qtd_ram']
        disco = maquina['qtd_disco']
        preco = maquina['preco']
        provedor = maquina['provedor']
        id = maquina['maquina']

        print('Encontramos uma máquina com as seguintes especificações:')
        print(f'Provedor: {provedor} - ID {id}')
        print(f"vCPU's: {vcpu}")
        print(f'RAM: {ram}')
        print(f'disco: {disco}')
        print(f'preco: R$ {preco}')
    else:
        print('Nenhuma máquina foi encontrada')


def usa():
    provedor = input('Qual o provedor responsável pela máquina que deseja utilizar?\n> ')
    id = input('Qual ID dá maquina que deseja utilizar?\n> ')

    r = requests.post(url_provedor.format(
        provedor=provedor, route='usar'), json={"id": id})

    maquinas_em_uso.append((provedor, id))

    print(f'A máquina com Provedor: {provedor} e ID: {id} está pronta para uso.\n')


def libera():
    provedor = input('Qual o provedor responsável pela máquina que deseja liberar?\n> ')
    id = input('Qual ID dá maquina que deseja liberar?\n> ')

    r = requests.post(url_provedor.format(
        provedor=provedor, route='liberar'), json={"id": id})

    maquinas_em_uso = list(filter(lambda x: x[0] != provedor and x[1] != id))

    print(f'A máquina com Provedor: {provedor} e ID: {id} foi liberada com sucesso.\n')


def listar():
    print('Máquinas em uso:')
    [ print(i) for i in maquinas_em_uso ]
    print()


if __name__ == "__main__":
    while True:

        menu = 'Seleciona a opção desejada\n\n'
        menu += '[1] - Encontrar máquina:\n'
        menu += '[2] - Utilizar máquina:\n'
        menu += '[3] - Listar máquinas em uso\n'
        menu += '[4] - Liberar máquina\n'

        option = input(menu)

        menu_options: {
            '1': procura(),
            '2': usa(),
            '3': listar(),
            '4': libera(),
        }

        try: 
            menu_options[option]
        except:
            print('Opção inválida\n')