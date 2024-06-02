import threading
import numpy as np
import matplotlib.pyplot as plt


class Labirynt:
    def __init__(self, size, maze):
        self.__locks = np.array([[threading.Lock() for j in range(size)] for i in range(size)])
        self.__guard = threading.Lock()
        self.__thread_guard = threading.Lock()
        self.__maze = maze
        self.__size = size

    def is_index_valid(self, x, y):
        """Sprawdź, czy podane indeksy mieszczą się w prawidłowym zakresie labiryntu."""
        return 0 <= x < self.__size and 0 <= y < self.__size

    def is_place_free(self, x, y):
        """Sprawdź, czy miejsce przy indeksach (x, y) jest wolne."""
        if not self.is_index_valid(x, y):
            return False
        self.__locks[x, y].acquire()
        value = self.__maze[x, y]
        self.__locks[x, y].release()
        return value == 0

    def update_maze_place(self, x, y, value):
        """Zaktualizuj miejsce przy indeksach (x, y) w labiryncie o podaną wartość."""
        if not self.is_index_valid(x, y):
            return
        self.__guard.acquire()
        self.__maze[x, y] = value
        self.__guard.release()

    def show_maze(self):
        plt.rcParams['figure.figsize'] = (8, 8)
        plt.imshow(self.__maze)
        plt.show()

    def traverse_maze(self, x, y, thread_id=1):
        '''lista wątków'''
        threads = list()

        while True:
            '''aktualizacja pola labiryntu'''
            self.update_maze_place(x, y, thread_id)

            possibleMoves = False
            newX, newY = x, y

            '''sprawdzenie możliwych do przejścia kierunków'''

            '''kierunek bierzącego wątka - w dół'''
            if x + 1 < self.__size and self.is_place_free(x + 1, y):
                possibleMoves = True
                newX += 1

            '''sprawdzenie pozostałych kierunków w wątkach potomnych'''
            if x - 1 >= 0 and self.is_place_free(x - 1, y):  # w górę
                if possibleMoves:
                    self.__thread_guard.acquire()
                    thread_id += 1
                    self.__thread_guard.release()
                    t = threading.Thread(target=self.traverse_maze, args=(x - 1, y, thread_id))
                    threads.append(t)
                    t.start()
                else:
                    possibleMoves = True
                    newX -= 1
            if y + 1 < self.__size and self.is_place_free(x, y + 1):  # w prawo
                if possibleMoves:
                    self.__thread_guard.acquire()
                    thread_id += 1
                    self.__thread_guard.release()
                    t = threading.Thread(target=self.traverse_maze, args=(x, y + 1, thread_id))
                    threads.append(t)
                    t.start()
                else:
                    possibleMoves = True
                    newY += 1
            if y - 1 >= 0 and self.is_place_free(x, y - 1):  # w lewo
                if possibleMoves:
                    self.__thread_guard.acquire()
                    thread_id += 1
                    self.__thread_guard.release()
                    t = threading.Thread(target=self.traverse_maze, args=(x, y - 1, thread_id))
                    threads.append(t)
                    t.start()
                else:
                    possibleMoves = True
                    newY -= 1

            if possibleMoves is False:
                '''połączenie wątków'''
                for thread in threads:
                    thread.join()
                '''wyczyszczenie listy wątków'''
                threads = []
                break

            x, y = newX, newY


def na_ocene_3():
    ''' Na ocene 3 '''
    size = 100
    maze = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i % 5 == 0 and j % 4 == 0:
                maze[i, j] = -1
    labirynt_3 = Labirynt(size, maze)
    labirynt_3.traverse_maze(0, 0)
    labirynt_3.show_maze()


def na_ocene_4():
    ''' Na ocene 4 '''
    size = 100
    maze = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i % 5 == 0 and j % 4 == 0:
                maze[i, j] = -1
    labirynt_4_1 = Labirynt(size, maze)
    labirynt_4_1.traverse_maze(0, 0)
    labirynt_4_1.show_maze()


    size = 200
    maze = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i % 5 == 0 and j % 4 == 0:
                maze[i, j] = -1
    labirynt_4_2 = Labirynt(size, maze)
    labirynt_4_2.traverse_maze(0, 0)
    labirynt_4_2.show_maze()


def na_ocene_5():
    ''' Na ocene 5 '''
    size = 100
    maze = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i % 2 == 0 and j % 5 == 0:
                maze[i, j] = -1
    labirynt_5_1 = Labirynt(size, maze)
    labirynt_5_1.traverse_maze(0, 0)
    labirynt_5_1.show_maze()

    size = 100
    maze = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            if i % 3 == 0 and j % 2 == 0:
                maze[i, j] = -1

    size = np.shape(maze)[1]
    labirynt_5_2 = Labirynt(size, maze)
    labirynt_5_2.traverse_maze(0, 0)
    labirynt_5_2.show_maze()
    my_maze = [
        [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0],
        [0, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0],
        [0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0],
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0],
        [0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0],
        [0, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0],
        [0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0],
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0],
        [0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, -1, -1, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, -1, -1, 0],
        [0, 0, 0, 0, -1, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0]
    ]
    size = 20
    maze = np.array(my_maze)
    labirynt_5_3 = Labirynt(size, maze)
    labirynt_5_3.traverse_maze(0, 0)
    labirynt_5_3.show_maze()


if __name__ == '__main__':
    na_ocene_3()
    na_ocene_4()
    na_ocene_5()