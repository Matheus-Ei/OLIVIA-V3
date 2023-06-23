import os

def findFileEx(nome_arquivo):
    diretorio = "files/"
    def procurar_arquivo(nome_arquivo, diretorio):
        for root, dirs, files in os.walk(diretorio):
            if nome_arquivo in files:
                return os.path.join(root, nome_arquivo)
        return None

    caminho_arquivo = procurar_arquivo(nome_arquivo, diretorio)

    if caminho_arquivo:
        return caminho_arquivo
    else:
        return None


def findFile(nome_arquivo):
    diretorio = "files/"
    def procurar_arquivo(nome_arquivo, diretorio):
        caminhos_encontrados = []
        for root, dirs, files in os.walk(diretorio):
            for file in files:
                if os.path.splitext(file)[0] == nome_arquivo:
                    caminhos_encontrados.append(os.path.join(root, file))
        return caminhos_encontrados

    caminhos_arquivos = procurar_arquivo(nome_arquivo, diretorio)

    if caminhos_arquivos:
        return caminhos_arquivos
    else:
        return None


arquivo = findFile("image")
print(arquivo)