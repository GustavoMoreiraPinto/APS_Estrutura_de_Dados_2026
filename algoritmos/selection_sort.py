
def selection_sort(lista):
    n = len(lista)

    for i in range(n):
        indice_menor = i

        for j in range(i + 1, n):
            if lista[j] < lista[indice_menor]:
                indice_menor = j

        if indice_menor != i:
            lista[i], lista[indice_menor] = (
                lista[indice_menor],
                lista[i]
            )

    return lista


if __name__ == "__main__":
    numeros = [64, 25, 12, 22, 11]

    print("Lista original:", numeros)

    selection_sort(numeros)

    print("Lista ordenada:", numeros)
