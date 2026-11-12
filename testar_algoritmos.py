
from algoritmos.bubble_sort import bubble_sort
from algoritmos.selection_sort import selection_sort
from algoritmos.insertion_sort import insertion_sort
from algoritmos.merge_sort import merge_sort
from algoritmos.quick_sort import quick_sort

algoritmos = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

numeros = [45, 12, 78, 3, 56, 21, 9]

resultado_esperado = sorted(numeros)

print("Lista original:", numeros)
print("Resultado esperado:", resultado_esperado)
print("-" * 45)

for nome, algoritmo in algoritmos.items():
    copia = numeros.copy()
    resultado = algoritmo(copia)

    if resultado == resultado_esperado:
        print(f"✅ {nome}: OK")
    else:
        print(f"❌ {nome}: ERRO")
