import random
from collections import defaultdict, deque


# Generowanie losowych ciągów kartek
def generate_test_data(num_sequences=100, sequence_length=100, num_pages=20):
    # Funkcja generuje testowe dane do symulacji odwołań do stron w pamięci.
    random.seed(3)
    test_data = []
    # Pętla iteruje "num_sequences" razy, tworząc osobne ciągi odwołań do stron.
    for _ in range(num_sequences):
        # Tworzenie pojedynczego ciągu odwołań do stron o długości "sequence_length".
        sequence = [random.randint(0, num_pages - 1) for _ in range(sequence_length)]
        # Dodanie wygenerowanego ciągu do listy "test_data".
        test_data.append(sequence)
    # Zwrócenie listy zawierającej wszystkie wygenerowane ciągi odwołań do stron.
    return test_data

# LRU: Wyrzucamy najdłużej nieużywaną kartkę
def lru(pages, frames):
    # Inicjalizacja pustej kolejki deque "frame_list", która będzie przechowywać numery stron w ramkach pamięci.
    frame_list = deque()
    # Inicjalizacja zmiennej "page_faults" jako licznika błędów strony.
    page_faults = 0

    # Pętla iteruje przez każdą stronę ("page") w ciągu odwołań ("pages").
    for page in pages:
        # Sprawdzenie, czy strona "page" nie jest obecna w "frame_list".
        if page not in frame_list:
            # Jeśli "page" nie jest w `frame_list`:
            # Sprawdzenie, czy liczba ramek ("len(frame_list)") osiągnęła maksymalną liczbę "frames".
            if len(frame_list) >= frames:
                # Jeśli tak, usuwa najstarszą stronę z lewej strony kolejki "frame_list".
                frame_list.popleft()
            # Zwiększa licznik błędów strony, ponieważ strona "page" nie była w pamięci RAM i musiała być wczytana.
            page_faults += 1
            # Dodaje "page" na koniec kolejki "frame_list".
            frame_list.append(page)
        else:
            # Jeśli "page" jest już w "frame_list", usuwa go z bieżącej pozycji.
            frame_list.remove(page)
            # Dodaje "page" ponownie na koniec kolejki, aby oznaczyć jego aktualność użycia.
            frame_list.append(page)

    # Zwraca liczbę "page_faults", która reprezentuje całkowitą liczbę błędów strony (ilość wymian stron).
    return page_faults


# LFU: Wyrzucamy kartkę używaną najmniej razy
def lfu(pages, frames):
    # Inicjalizacja pustego słownika "frame_list", który będzie przechowywać numery stron w ramkach pamięci.
    frame_list = {}
    # Inicjalizacja defaultdict "page_frequency" typu int, który będzie przechowywać liczbę odwołań do każdej strony.
    page_frequency = defaultdict(int)
    # Inicjalizacja zmiennej "page_faults" jako licznika błędów strony.
    page_faults = 0

    # Pętla iteruje przez każdą stronę ("page") w ciągu odwołań ("pages").
    for page in pages:
        # Sprawdzenie, czy strona "page" nie jest obecna w "frame_list".
        if page not in frame_list:
            # Jeśli "page" nie jest w "frame_list":
            # Sprawdzenie, czy liczba ramek ("len(frame_list)") osiągnęła maksymalną liczbę "frames".
            if len(frame_list) >= frames:
                # Jeśli tak, wybiera stronę "lfu_page", która jest najrzadziej używaną stroną w ramkach.
                # Używa do tego funkcji "min" z argumentem "key=lambda p: (page_frequency[p], frame_list[p])",
                # która sortuje ramki według częstotliwości odwołań (najpierw według "page_frequency", a jeśli są równe, to według indeksu w "frame_list").
                lfu_page = min(frame_list, key=lambda p: (page_frequency[p], frame_list[p]))
                # Usuwa "lfu_page" z "frame_list`" i odpowiadający mu wpis w "page_frequency".
                del frame_list[lfu_page]
                del page_frequency[lfu_page]
            # Zwiększa licznik błędów strony, ponieważ strona "page" nie była w pamięci RAM i musiała być wczytana.
            page_faults += 1
        # Dodaje "page" do "frame_list" pod odpowiednim indeksem i zwiększa liczbę odwołań do "page" w "page_frequency".
        frame_list[page] = len(frame_list)
        page_frequency[page] += 1

    # Zwraca liczbę "page_faults", która reprezentuje całkowitą liczbę błędów strony (ilość wymian stron).
    return page_faults


# Testowanie algorytmów
def test_algorithms(test_data, frame_sizes):
    # Inicjalizacja słownika "results" zawierającego wyniki dla algorytmów LRU i LFU.
    results = {"LRU": {}, "LFU": {}}

    # Iteracja przez różne liczby ramek ("frames") z listy "frame_sizes".
    for frames in frame_sizes:
        # Inicjalizacja list "lru_faults" i "lfu_faults" do przechowywania wyników błędów strony dla LRU i LFU.
        lru_faults = []
        lfu_faults = []
        reference_strings = []
        # Iteracja przez każdy ciąg odwołań ("sequence") w "test_data".
        for sequence in test_data:
            # Obliczenie błędów strony dla LRU i LFU dla danego ciągu odwołań ("sequence") i liczby ramek ("frames").
            lru_faults.append(lru(sequence, frames))
            lfu_faults.append(lfu(sequence, frames))
            reference_strings.append(sequence)

        # Obliczenie średnich błędów strony dla LRU i LFU dla wszystkich ciągów odwołań dla danej liczby ramek ("frames").
        average_lru_faults = sum(lru_faults) / len(lru_faults)
        average_lfu_faults = sum(lfu_faults) / len(lfu_faults)

        # Dodanie wyników dla LRU do słownika "results" pod kluczem "frames".
        results["LRU"][frames] = {
            "average_faults": average_lru_faults,
            "faults_list": lru_faults,
            "reference_string": reference_strings,
        }

        # Dodanie wyników dla LFU do słownika "results" pod kluczem "frames".
        results["LFU"][frames] = {
            "average_faults": average_lfu_faults,
            "faults_list": lfu_faults,
            "reference_string": reference_strings,
        }

    # Zwrócenie słownika "results" zawierającego wszystkie obliczone wyniki dla algorytmów LRU i LFU.
    return results


# Parametry
num_pages = 20
frame_sizes = [3, 5, 7]
test_data = generate_test_data()

results = test_algorithms(test_data, frame_sizes)
# Wywołanie funkcji testującej algorytmy z danymi testowymi "test_data" i listą rozmiarów ramek "frame_sizes". Zapisanie wyników do zmiennej "results".

for algo in results:
    # Pętla iterująca przez klucze (algorytmy) w słowniku "results`".
    print(f"\nWyniki dla {algo}:")
    # Wyświetlenie informacji o typie algorytmu (LRU lub LFU).

    for frames in results[algo]:
        # Pętla iterująca przez klucze (liczby ramek) w pod-słowniku dla danego algorytmu.
        avg_faults = results[algo][frames]["average_faults"]
        # Pobranie średniej liczby błędów strony dla danego algorytmu i liczby ramek.
        print(f"\n  Liczba ramek: {frames}")
        # Wyświetlenie informacji o liczbie ramek.
        print(f"  Średnia liczba brakujących stron: {avg_faults:.2f}")
        # Wyświetlenie średniej liczby błędów strony zaokrąglonej do dwóch miejsc po przecinku.
        print(f"  Szczegółowe wyniki dla każdego testu:")
        for idx, faults in enumerate(results[algo][frames]["faults_list"]):
            # Pętla iterująca przez indeksy i błędy strony w liście błędów strony dla danego algorytmu i liczby ramek.
            print(f"    Test {idx + 1}: Liczba brakujących stron: {faults}")
            #Wyświetlenie numeru testu i liczby błędów strony dla tego testu.
            print(f"Ciąg odwołań {idx + 1}: {results[algo][frames]["reference_string"][idx]}")
            # Wyświetlenie ciągu odwołań dla tego testu.