
def bubble_sort(lista):
    n = len(lista)

    for i in range(n):
        trocou = False

        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True

        if not trocou:
            break

    return lista

if __name__ == "__main__":
    numeros = [5, 3, 8, 1, 9, 2]

    print("Lista original:", numeros)

    bubble_sort(numeros)

    print("Lista ordenada:", numeros)
