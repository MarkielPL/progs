import numpy as np
import threading
from matplotlib import pyplot as plt
from tabulate import tabulate
import time

size: int
max_level: int
matrix: np.array

start_script_time = time.time()

def drawSquare(x, y, level, size):
    x = int(x)
    y = int(y)
    size = int(size)

    '''sprawdzanie poziomu zagłębienia'''
    if level == max_level:
        return

    '''wstawianie odpowiednich wartości do maciezy'''
    offsetX = size // 3
    offsetY = size // 3
    for i in range(offsetX, 2 * offsetX):
        for j in range(offsetY, 2 * offsetY):
            matrix[x + i][y + j] = 1

    '''lista wątków'''
    threads = list()

    '''pierwszy rząd
    punkt startowy LEWY GORNY'''
    t1 = threading.Thread(target=drawSquare, args=(x, y, level + 1, offsetX))
    threads.append(t1)
    t1.start()

    '''punkt startowy ŚRODEK GÓRNY'''
    t2 = threading.Thread(target=drawSquare, args=(x, y + offsetX, level + 1, offsetX))
    threads.append(t2)
    t2.start()

    '''punkt startowy PRAWY GÓRNNY'''
    t3 = threading.Thread(target=drawSquare, args=(x, y + 2 * offsetX, level + 1, offsetX))
    threads.append(t3)
    t3.start()

    '''drugi rząd
    punkt startowy LEWY ŚRODEK'''
    t4 = threading.Thread(target=drawSquare, args=(x + offsetX, y, level + 1, offsetX))
    threads.append(t4)
    t4.start()

    '''punkt startowy PRAWY ŚRODEK'''
    t5 = threading.Thread(target=drawSquare, args=(x + offsetX, y + 2 * offsetY, level + 1, offsetX))
    threads.append(t5)
    t5.start()

    '''trzeci rząd
    punkt startowy LEWY DÓŁ'''
    t6 = threading.Thread(target=drawSquare, args=(x + 2 * offsetX, y, level + 1, offsetX))
    threads.append(t6)
    t6.start()

    '''punkt startowy ŚRODEK DÓŁ'''
    t7 = threading.Thread(target=drawSquare, args=(x + 2 * offsetX, y + offsetX, level + 1, offsetX))
    threads.append(t7)
    t7.start()

    '''punkt startowy PRAWY DÓŁ'''
    t8 = threading.Thread(target=drawSquare, args=(x + 2 * offsetX, y + 2 * offsetY, level + 1, offsetX))
    threads.append(t8)
    t8.start()

    '''Łączenie działania wszystkich wątków'''
    for thread in threads:
        thread.join()


def rysuj_dywan():
    global size, max_level, matrix
    size = 100
    max_level = 5
    matrix = np.zeros((size, size))

    '''Wyświetlanie dywanu Sierpińskiego'''
    from matplotlib.colors import ListedColormap
    drawSquare(0, 0, 0, size)

    '''Definiowanie mapy kolorów dla wartości 0 i 1'''
    custom_cmap = ListedColormap(['yellow', 'purple'])
    plt.figure(figsize=(6, 6))
    plt.imshow(matrix, cmap=custom_cmap, interpolation='none')
    plt.axis('off')
    plt.title("Dywan Sierpińskiego")
    plt.show(block=False)
    plt.pause(1)


def naOcene3():
    global size, max_level, matrix
    size = 100
    max_level = 5
    matrix = np.zeros((size, size))

    '''Liczenie czasów obliczeń dla 10 przebiegów'''
    times = []
    for _ in range(10):
        start_time = time.time()
        drawSquare(0, 0, 0, size)
        times.append(round(time.time() - start_time, 4))
        print(f"Zakończono {_ +1}. przebieg z czasem {times[-1]} s.")

    '''Średni czas obliczeń'''
    average_time = round(sum(times) / len(times), 4)

    ''''Wyswietlanie czasow w tabelce'''
    print("Czasy wykonania dla 10 przebiegów: ")
    print(tabulate(enumerate(times, 1), headers=["Przebieg", "Czas (s)"], tablefmt='double_grid'))
    print("Średni czas wykonania:", average_time, "s")

    '''Tworzenie wykresu'''
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), times, marker='o', linestyle='-')
    plt.title("Czasy obliczeń dla 10 przebiegów")
    plt.xlabel("Przebieg")
    plt.ylabel("Czas (s)")
    plt.grid(True)
    plt.xticks(range(1, 11))
    plt.axhline(y=average_time, color='r', linestyle='--', label=f"Średni czas: {average_time} s")
    plt.legend()
    plt.show(block=False)
    plt.pause(1)


'''Funkcja badająca czasy dla różnych rozmiarów dywanu'''
def naOcene5():
    global max_level, matrix

    max_levels = [3, 4, 5]
    sizes = [50, 100, 150]
    results = []

    for max_level in max_levels:
        size_results = []
        for size in sizes:
            size_times = []
            matrix = np.zeros((size, size))
            for _ in range(10):
                start_time = time.time()
                drawSquare(0, 0, 0, size)
                elapsed_time = round(time.time() - start_time, 4)
                size_times.append(elapsed_time)
                print(f"{_ +1}. Zakończono obliczenia dla dywanu o rozmiarze {size} i poziomie {max_level} w {elapsed_time} s.")

            average_time = round(sum(size_times) / len(size_times), 4)
            size_results.append((size, size_times, average_time))

        results.append((max_level, size_results))

    '''Tworzenie tabeli z wynikami'''
    table_data = []
    for max_level, size_results in results:
        for size, size_times, average_time in size_results:
            dotHead = [None] * (10 - len(size_times))
            size_times.extend(dotHead)
            table_data.append([max_level, size] + size_times + [average_time])

    print("\nWyniki dla różnych rozmiarów dywanu:")
    print(tabulate(table_data, headers=['Poziom', 'Rozmiar'] + [f'Przebieg {_}' for _ in range(1, 11)] + ['Średni czas (s)'],
                   tablefmt='double_grid'))

    '''Tworzenie wykresu'''
    plt.figure(figsize=(12, 6))
    for i, (max_level, size_results) in enumerate(results):
        plt.subplot(1, len(results), i+1)
        for size, size_times, _ in size_results:
            plt.plot(range(1, 11), size_times[:10], marker='o', linestyle='-', label=f'Rozmiar: {size}')
        plt.title(f'Poziom: {max_level}')
        plt.xlabel('Przebieg')
        plt.ylabel('Czas (s)')
        plt.grid(True)
        plt.xticks(range(1, 11))
        plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Rozpoczynam rysowanie dywanu Sierpińskiego")
    rysuj_dywan()
    print("Rozpoczynam obliczenia dla zadania na ocenę 3: ")
    naOcene3()
    print("Rozpoczynam obliczenia dla zadania na ocenę 5: ")
    naOcene5()

    end_script_time = time.time()
    total_script_time = round(end_script_time - start_script_time)
    print("Całkowity czas wykonania skryptu:", total_script_time, "s.")

'''
IdeaPad 3 15ABA7- CPU: AMD Ryzen 5 5625U, RAM: 8BG: Całkowity czas wykonania skryptu: 505 s.
Dell Latitude 5431- CPU: i7-1270P, RAM: 32 GB: Całkowity czas wykonania skryptu: 197 s.
'''