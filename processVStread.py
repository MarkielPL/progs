import random
import concurrent.futures
import time
from statistics import mean, median
from numpy import percentile
from tabulate import tabulate
import os

# Funkcja generująca duże dane
def generate_large_data(size, value_range=(1, 1000000)):
    """
    Generuje listę losowych danych o określonym rozmiarze i zakresie wartości;

    Args:
        size (int): Rozmiar generowanych danych;
        value_range (tuple): Zakres wartości dla danych;

    Returns:
        list: Lista losowych danych;
    """
    return [random.randint(*value_range) for _ in range(size)]


# Funkcja przeprowadzająca analizę równoległą
def parallel_analysis(data, analysis_type):
    """
    Przeprowadza różne rodzaje analizy na danych;

    Args:
        data (list): Dane do analizy;
        analysis_type (str): Rodzaj analizy, to suma, średnia, mediana, wartość maxymalna, wartość minimalna,
        percentyl dziesiętny (percentile_10), percentyl 90% (percentile_90);

    Returns:
        float: Wynik analizy;
    """
    if analysis_type == "sum":
        return sum(data)
    elif analysis_type == "mean":
        return mean(data)
    elif analysis_type == "median":
        return median(data)
    elif analysis_type == "max":
        return max(data)
    elif analysis_type == "min":
        return min(data)
    elif analysis_type == "percentile_10":
        return percentile(data, 10)
    elif analysis_type == "percentile_90":
        return percentile(data, 90)


# Funkcja sortująca dane równolegle
def parallel_sorting(data_chunk, reverse=False):
    """
    Sortuje dane w sposób równoległy;

    Args:
        data_chunk (list): Fragment danych do posortowania;
        reverse (bool): Określa, czy sortowanie ma być malejące, domyślnie nie;

    Returns:
        list: Posortowany fragment danych;
    """
    return sorted(data_chunk, reverse=reverse)


# Funkcja mierząca czas wykonania
def measure_execution_time(func, *args):
    """
    Mierzy czas wykonania funkcji;

    Args:
        func (function): Funkcja, której czas wykonania ma być zmierzony;
        *args: Argumenty przekazywane do funkcji;

    Returns:
        float: Czas wykonania funkcji.
    """
    start_time = time.time()
    func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


# Funkcja przetwarzająca dane za pomocą procesów
def parallel_process(data, chunkSize, sort_reverse=False):
    """
    Przetwarza dane równolegle za pomocą procesów;

    Args:
        data (list): Dane do przetworzenia;
        chunkSize (int): Rozmiar fragmentu danych do przetworzenia w jednym procesie;
        sort_reverse (bool): Określa, czy sortowanie ma być malejące, domyślnie nie;

    Returns:
        list: Posortowane dane;
    """
    results = []
    with concurrent.futures.ProcessPoolExecutor() as exe:
        futures = []
        for i in range(0, len(data), chunkSize):
            chunk = data[i:i + chunkSize]
            futures.append(exe.submit(parallel_sorting, chunk, sort_reverse))
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())
    return results


if __name__ == "__main__":
    # Generowanie danych do analizy
    data_to_analyze = generate_large_data(10000000, value_range=(1, 100000000))

    # Konfiguracja parametrów testowych
    chunk_sizes = [100000, 500000, 1000000]
    analysis_types = ["min", "max", "mean", "sum", "median", "percentile_10", "percentile_90"]
    num_threads = [2, 4, 8, os.cpu_count() or 1]
    num_processes = [2, 4, 8, os.cpu_count() or 1]

    results = []

    # Test równoległy z wykorzystaniem wątków
    thread_results = []
    for num_thread in num_threads:
        for chunk_size in chunk_sizes:
            thread_row = [f"Wątki ({num_thread})", chunk_size]
            analysis_results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_thread) as executor:
                for analysis_type in analysis_types:
                    execution_time = measure_execution_time(parallel_analysis, data_to_analyze, analysis_type)
                    analysis_results.append(execution_time)
                    print(f"Wątki ({num_thread}), Chunk: {chunk_size}, Analiza: {analysis_type}, Czas: {execution_time:.4f}")
            thread_row.extend(analysis_results)
            thread_results.append(thread_row)

    # Test równoległy z wykorzystaniem procesów
    process_results = []
    for num_process in num_processes:
        for chunk_size in chunk_sizes:
            process_row = [f"Procesy ({num_process})", chunk_size]
            analysis_results = []
            execution_time = measure_execution_time(parallel_process, data_to_analyze, chunk_size)
            for analysis_type in analysis_types:
                execution_time = measure_execution_time(parallel_analysis, data_to_analyze, analysis_type)
                analysis_results.append(execution_time)
                print(f"Procesy ({num_process}), Chunk: {chunk_size}, Analiza: {analysis_type}, Czas: {execution_time:.4f}")
            process_row.extend(analysis_results)
            process_results.append(process_row)

    # Sumy czasów dla wątków i procesów
    thread_sum_row = ["Suma wątków", ""]
    process_sum_row = ["Suma procesów", ""]
    for i in range(len(analysis_types)):
        thread_sum_row.append(sum(row[i+2] for row in thread_results))
        process_sum_row.append(sum(row[i+2] for row in process_results))

    # Wyświetlanie wyników
    headers = ["", "Chunk"] + [f"{analysis_type} (s)" for analysis_type in analysis_types]
    print(tabulate(thread_results + process_results, headers=headers, tablefmt="fancy_grid"))
    headers = [f"{analysis_type} (s)" for analysis_type in analysis_types]
    print(tabulate([thread_sum_row, process_sum_row], headers=headers, tablefmt="rounded_outline"))
    total_execution_time = sum(thread_sum_row[2:]) + sum(process_sum_row[2:])
    print(f"\nCałkowity czas wykonania skryptu: {total_execution_time:.4f} s")