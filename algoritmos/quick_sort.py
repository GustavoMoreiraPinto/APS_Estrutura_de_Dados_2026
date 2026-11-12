
import random


def quick_sort(lista):
    if len(lista) <= 1:
        return lista

    # Pilha para controlar as partições sem recursão
    pilha = [(0, len(lista) - 1)]

    while pilha:
        inicio, fim = pilha.pop()

        if inicio >= fim:
            continue

        # Escolher um pivô aleatório
        indice_pivo = random.randint(inicio, fim)

        # Colocar o pivô no final da partição
        lista[indice_pivo], lista[fim] = (
            lista[fim],
            lista[indice_pivo]
        )

        pivo = lista[fim]
        i = inicio - 1

        # Particionar a lista
        for j in range(inicio, fim):
            if lista[j] <= pivo:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]

        posicao_pivo = i + 1
        lista[posicao_pivo], lista[fim] = (
            lista[fim],
            lista[posicao_pivo]
        )

        # Guardar as partições restantes
        pilha.append((inicio, posicao_pivo - 1))
        pilha.append((posicao_pivo + 1, fim))

    return lista


if __name__ == "__main__":
    numeros = [8, 3, 5, 1, 9, 2]

    print("Lista original:", numeros)
    print("Lista ordenada:", quick_sort(numeros.copy()))
