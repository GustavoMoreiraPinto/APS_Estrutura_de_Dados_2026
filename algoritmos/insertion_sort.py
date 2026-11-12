
def insertion_sort(lista):
    n = len(lista)

    for i in range(1, n):
        chave = lista[i]
        j = i - 1

        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1

        lista[j + 1] = chave

    return lista


if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]

    print("Lista original:", numeros)

    insertion_sort(numeros)

    print("Lista ordenada:", numeros)
