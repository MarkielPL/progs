import inspect
import shlex
from abc import abstractmethod
import sqlite3
import pytest
import os
import pathlib

database_name = "statki.db"


class DatabaseInterface:
    @staticmethod
    def insert(sql):
        db = sqlite3.connect(database_name)
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()

    @staticmethod
    def select(sql):
        db = sqlite3.connect(database_name)
        cur = db.cursor()
        cur.execute(sql)
        retVal = cur.execute(sql).fetchall()
        cur.close()
        db.close()
        return retVal


def DatabaseCheck():
    if DatabaseInterface.select("SELECT name FROM sqlite_master"):
        return True  # database exist, ready to import
    else:
        db = sqlite3.connect(database_name)
        cur = db.cursor()
        cur.execute("CREATE TABLE statki(\
                    nazwa TEXT,\
                    rok_produkcji TEXT,\
                    stan TEXT,\
                    paliwo NUMERIC\
                    )")
        cur.execute("CREATE TABLE lodzie_podwodne(\
                    nazwa TEXT,\
                    rok_produkcji TEXT,\
                    stan TEXT,\
                    stan_zanurzenia TEXT\
                    )")
        cur.execute("CREATE TABLE zaglowce(\
                    nazwa TEXT,\
                    rok_produkcji TEXT,\
                    stan TEXT,\
                    stan_zagli TEXT\
                    )")
        cur.execute("CREATE TABLE kapitanowie(\
                    nazwa TEXT,\
                    licencja TEXT,\
                    pojazd_przypisany TEXT\
                    )")
        cur.execute("CREATE TABLE port(\
                    statek TEXT\
                    )")
        db.close()
        return False  # database absent


class PojazdWodny:
    m_nazwa = str()
    m_rok_produkcji = str()
    m_stan = str("rozladowany")
    m_typ = str()

    def __init__(self, nazwa, rok_produkcji):
        self.m_nazwa = nazwa
        self.m_rok_produkcji = rok_produkcji

    @abstractmethod
    def wypisz_info(self):
        pass

    @abstractmethod
    def rozladunek(self):
        pass

    @abstractmethod
    def zaladunek(self):
        pass

    @abstractmethod
    def eksport_do_bazy(self):
        pass


class Statek(PojazdWodny):

    def __init__(self, nazwa, rok_produkcji, paliwo=0):
        super().__init__(nazwa, rok_produkcji)
        self.m_paliwo = paliwo
        self.m_typ = "Statek"
        self.m_paliwo = paliwo

    def wypisz_info(self):
        return f'ilosc paliwa: {self.m_paliwo}, stan: {self.m_stan}'

    def rozladunek(self):
        print(f'Statek {self.m_nazwa} rozadowuje sie')
        self.m_stan = "rozladowany"
        self.eksport_do_bazy()

    def zaladunek(self):
        print(f'Statek {self.m_nazwa} laduje sie')
        self.m_stan = "zaladowany"
        self.eksport_do_bazy()

    def zatankuj(self, paliwo):
        print(f'Statek {self.m_nazwa} tankuje {paliwo} paliwa')
        self.m_paliwo += paliwo
        self.eksport_do_bazy()

    def eksport_do_bazy(self):
        if DatabaseInterface.select(f'SELECT nazwa FROM statki WHERE nazwa="{self.m_nazwa}"'):
            sql = f'UPDATE statki SET stan = "{self.m_stan}", paliwo = "{self.m_paliwo}" WHERE nazwa = "{self.m_nazwa}"'
        else:
            sql = f'INSERT INTO statki VALUES("{self.m_nazwa}", "{self.m_rok_produkcji}", "{self.m_stan}", "{self.m_paliwo}")'
        DatabaseInterface.insert(sql)


class LodzPodwodna(PojazdWodny):

    def __init__(self, nazwa, rok_produkcji):
        super().__init__(nazwa, rok_produkcji)
        self.m_typ = "Lodz podwodna"
        self.m_stan_zanurzenia = str("wynurzony")

    def wypisz_info(self):
        return f'stan zanurzenia: {self.m_stan_zanurzenia}, stan: {self.m_stan}'

    def rozladunek(self):
        print(f'LodzPodwodna {self.m_nazwa} rozadowuje sie')
        self.m_stan = "rozladowany"
        self.eksport_do_bazy()

    def zaladunek(self):
        print(f'LodzPodwodna {self.m_nazwa} laduje sie')
        self.m_stan = "zaladowany"
        self.eksport_do_bazy()

    def zanurz(self):
        print(f'LodzPodwodna {self.m_nazwa} zanurza sie')
        self.m_stan_zanurzenia = "zanurzony"
        self.eksport_do_bazy()

    def wynurz(self):
        print(f'LodzPodwodna {self.m_nazwa} wynurza sie')
        self.m_stan_zanurzenia = "wynurzony"
        self.eksport_do_bazy()

    def eksport_do_bazy(self):
        if DatabaseInterface.select(f'SELECT nazwa FROM lodzie_podwodne WHERE nazwa="{self.m_nazwa}"'):
            sql = f'UPDATE lodzie_podwodne SET stan = "{self.m_stan}", stan_zanurzenia = "{self.m_stan_zanurzenia}" WHERE nazwa = "{self.m_nazwa}"'
        else:
            sql = f'INSERT INTO lodzie_podwodne VALUES("{self.m_nazwa}", "{self.m_rok_produkcji}", "{self.m_stan}", "{self.m_stan_zanurzenia}")'
        DatabaseInterface.insert(sql)


class Zaglowiec(PojazdWodny):

    def __init__(self, nazwa, rok_produkcji):
        super().__init__(nazwa, rok_produkcji)
        self.m_typ = "Zaglowiec"
        self.m_stan_zagli = str("zlozone")

    def wypisz_info(self):
        return f'stan zagli: {self.m_stan_zagli}, stan: {self.m_stan}'

    def rozladunek(self):
        print(f'Zaglowiec {self.m_nazwa} rozadowuje sie')
        self.m_stan = "rozladowany"
        self.eksport_do_bazy()

    def zaladunek(self):
        print(f'Zaglowiec {self.m_nazwa} laduje sie')
        self.m_stan = "zaladowany"
        self.eksport_do_bazy()

    def zloz_zagle(self):
        print(f'Zaglowiec {self.m_nazwa} sklada zagle')
        self.m_stan_zagli = "zlozone"
        self.eksport_do_bazy()

    def rozloz_zagle(self):
        print(f'Zaglowiec {self.m_nazwa} rozklada zagle')
        self.m_stan_zagli = "rozlozone"
        self.eksport_do_bazy()

    def eksport_do_bazy(self):
        if DatabaseInterface.select(f'SELECT nazwa FROM zaglowce WHERE nazwa="{self.m_nazwa}"'):
            sql = f'UPDATE zaglowce SET stan = "{self.m_stan}", stan_zagli = "{self.m_stan_zagli}" WHERE nazwa = "{self.m_nazwa}"'
        else:
            sql = f'INSERT INTO zaglowce VALUES("{self.m_nazwa}", "{self.m_rok_produkcji}", "{self.m_stan}", "{self.m_stan_zagli}")'
        DatabaseInterface.insert(sql)


class Kapitan:
    def __init__(self, nazwa, licencja):
        self.m_nazwa = nazwa
        self.m_licencja = licencja
        self.m_pojazd_przypisany = None

    def przypisz_pojazd(self, pojazd):
        print(f'Kapitan {self.m_nazwa}  przejmuje dowodzenie nad statkiem {pojazd.m_nazwa}')
        self.m_pojazd_przypisany = pojazd
        self.eksport_do_bazy()

    def wypisz_info(self):
        if self.m_pojazd_przypisany:
            return f'Kapitan {self.m_nazwa} dowodzi statkiem: {self.m_pojazd_przypisany.m_nazwa} ' + self.m_pojazd_przypisany.wypisz_info()
        else:
            return f'Kapitan {self.m_nazwa} nie dowodzi zadnym statkiem'

    def eksport_do_bazy(self):
        if DatabaseInterface.select(f'SELECT nazwa FROM kapitanowie WHERE nazwa="{self.m_nazwa}"'):
            sql = f'UPDATE kapitanowie SET pojazd_przypisany = "{self.m_pojazd_przypisany.m_nazwa if self.m_pojazd_przypisany else "None"}" WHERE nazwa = "{self.m_nazwa}"'
        else:
            sql = f'INSERT INTO kapitanowie VALUES("{self.m_nazwa}", "{self.m_licencja}", "{self.m_pojazd_przypisany.m_nazwa if self.m_pojazd_przypisany else "None"}")'
        DatabaseInterface.insert(sql)


class Port:

    def __init__(self):
        self.m_statki = {}

    def zaladuj_statki(self):
        print(f'Zaladunek statkow w porcie:')
        for nazwa in self.m_statki:
            self.m_statki[nazwa].zaladunek()

    def rozladuj_statki(self):
        print(f'Rozladunek statkow w porcie:')
        for nazwa in self.m_statki:
            self.m_statki[nazwa].rozladunek()

    def zatankuj_statek(self, nazwa, paliwo):
        self.m_statki[nazwa].zatankuj(paliwo)

    def przyjmij_pojazd(self, pojazd):
        print(f'Port przyjmuje statek: {pojazd.m_nazwa}, rok produkcji {pojazd.m_rok_produkcji} ' + pojazd.wypisz_info())
        self.m_statki[pojazd.m_nazwa] = pojazd
        sql = f'INSERT INTO port VALUES("{pojazd.m_nazwa}")'
        DatabaseInterface.insert(sql)

    def wypusc_pojazd(self, pojazd):
        print(f'Port wypuszcza statek: {pojazd.m_nazwa}, rok produkcji {pojazd.m_rok_produkcji} ' + pojazd.wypisz_info())
        del self.m_statki[pojazd.m_nazwa]
        sql = f'DELETE FROM port WHERE statek = "{pojazd.m_nazwa}"'
        DatabaseInterface.insert(sql)

    def wypisz_statki(self):
        statki = []
        for nazwa in self.m_statki:
            statki.append([nazwa, self.m_statki[nazwa].m_typ, self.m_statki[nazwa].m_rok_produkcji,
                           self.m_statki[nazwa].wypisz_info()])
        return statki

    def eksport_do_bazy(self):
        for statek in self.m_statki:
            if DatabaseInterface.select(f'SELECT statek FROM port WHERE statek="{self.m_statki[statek].m_nazwa}"'):
                pass # already added to table
            else:
                sql = f'INSERT INTO port VALUES("{self.m_statki[statek].m_nazwa}")'
                DatabaseInterface.insert(sql)


def tabela(naglowki, rzedy):
    print(tabulate.tabulate(rzedy, naglowki, "rounded_outline"), sep="\n")


def parametry(funkcja) -> str:
    return funkcja.__name__ + "".join(f" [{x}]" for x in inspect.getfullargspec(funkcja)[0][1:])


class HMI:

    def __init__(self):
        self.m_main_loop = True
        self.m_statki = {}
        self.m_kapitanowie = {}
        self.m_port = Port()

    def __del__(self):
        for statek in self.m_statki:
            self.m_statki[statek].eksport_do_bazy()

        for kapitan in self.m_kapitanowie:
            self.m_kapitanowie[kapitan].eksport_do_bazy()

        self.m_port.eksport_do_bazy()


    def lista_statkow(self):
        print(f'\nLista statkow w systemie:')
        tabela(["nazwa", "typ", "rok produkcji", "stan"],
               [[k, v.m_typ, v.m_rok_produkcji, v.wypisz_info()] for i, [k, v] in enumerate(self.m_statki.items(), 1)])
        return self

    def dodaj_statek(self, nazwa: str, rok_produkcji: str, paliwo=0):
        if nazwa in self.m_statki: raise RuntimeError(nazwa)
        self.m_statki[nazwa] = Statek(nazwa, rok_produkcji, paliwo)
        self.m_statki[nazwa].eksport_do_bazy()
        print(f"Dodano statek {nazwa}")
        return self

    def dodaj_lodz_podw(self, nazwa: str, rok_produkcji: str):
        if nazwa in self.m_statki: raise RuntimeError(nazwa)
        self.m_statki[nazwa] = LodzPodwodna(nazwa, rok_produkcji)
        self.m_statki[nazwa].eksport_do_bazy()
        print(f"Dodano lodz podwodna {nazwa}")
        return self

    def dodaj_zaglowiec(self, nazwa: str, rok_produkcji: str):
        if nazwa in self.m_statki: raise RuntimeError(nazwa)
        self.m_statki[nazwa] = Zaglowiec(nazwa, rok_produkcji)
        self.m_statki[nazwa].eksport_do_bazy()
        print(f"Dodano zaglowiec {nazwa}")
        return self

    def lista_kapitanow(self):
        print(f'\nLista kapitanów w systemie:')
        tabela(["nazwa", "licencja", "statek"],
               [[k, v.m_licencja, v.wypisz_info()] for i, [k, v] in enumerate(self.m_kapitanowie.items(), 1)])
        return self

    def dodaj_kapitana(self, nazwa: str, licencja: str, ):
        if nazwa in self.m_kapitanowie: raise RuntimeError(nazwa)
        self.m_kapitanowie[nazwa] = Kapitan(nazwa, licencja)
        self.m_kapitanowie[nazwa].eksport_do_bazy()
        print(f"Dodano kapitana {nazwa}")
        return self

    def przypisz_kapitana(self, nazwa: str, statek: str):
        if nazwa not in self.m_kapitanowie or statek not in self.m_statki: raise KeyError(nazwa)
        self.m_kapitanowie[nazwa].przypisz_pojazd(self.m_statki[statek])
        return self

    def port_przyjmij_statki(self, *statki):
        if isinstance(statki[0], str):
            for statek in statki:
                if statek not in self.m_statki: raise KeyError(statek)
                self.m_port.przyjmij_pojazd(self.m_statki[statek])
        elif isinstance(statki[0], list):
            for statek in statki[0]:
                if statek not in self.m_statki: raise KeyError(statek)
                self.m_port.przyjmij_pojazd(self.m_statki[statek])
        return self

    def port_wypusc_statki(self, *statki):
        if isinstance(statki[0], str):
            for statek in statki:
                if statek not in self.m_statki: raise KeyError(statek)
                self.m_port.wypusc_pojazd(self.m_statki[statek])
        elif isinstance(statki[0], list):
            for statek in statki[0]:
                if statek not in self.m_statki: raise KeyError(statek)
                self.m_port.wypusc_pojazd(self.m_statki[statek])
        return self

    def port_wypisz(self):
        print(f'\nStatki zacumowane w Porcie:')
        tabela(["nazwa", "typ", "rok produkcji", "stan"],
               [[nazwa, typ, rok, info]
                for i, [nazwa, typ, rok, info] in enumerate(self.m_port.wypisz_statki())]
               )
        return self

    def port_zaladuj_statki(self):
        self.m_port.zaladuj_statki()
        return self

    def port_rozladuj_statki(self):
        self.m_port.rozladuj_statki()
        return self

    def port_zatankuj_statek(self, nazwa, paliwo):
        if nazwa not in self.m_statki: raise KeyError(nazwa)
        if self.m_statki[nazwa].m_typ == "Statek":
            self.m_port.zatankuj_statek(nazwa, paliwo)
        else:
            print(f'Statek {nazwa} nie potrzebuje paliwa')
        return self

    def pomoc(self):
        tabela(["polecenie", "opis"],
               [[parametry(key), value] for key, value in self.opisy().items()])
        print(f'*ciągi zawierajace spacje nalezy otoczyc cudzyslowami')
        return self

    def wyjdz(self):
        self.m_main_loop = False
        return self

    def import_bazy_danych(self):
        for nazwa, rok_produkcji, stan, paliwo, in DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, paliwo FROM statki'):
            tmp_statek = Statek(nazwa, rok_produkcji, paliwo)
            tmp_statek.m_stan = stan
            self.m_statki[nazwa] = tmp_statek

        for nazwa, rok_produkcji, stan, stan_zanurzenia, in DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, stan_zanurzenia FROM lodzie_podwodne'):
            tmp_lodz_podwodna = LodzPodwodna(nazwa, rok_produkcji)
            tmp_lodz_podwodna.m_stan = stan
            tmp_lodz_podwodna.m_stan_zanurzenia = stan_zanurzenia
            self.m_statki[nazwa] = tmp_lodz_podwodna

        for nazwa, rok_produkcji, stan, stan_zagli, in DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, stan_zagli FROM zaglowce'):
            tmp_zaglowiec = Zaglowiec(nazwa, rok_produkcji)
            tmp_zaglowiec.m_stan = stan
            tmp_zaglowiec.m_stan_zagli = stan_zagli
            self.m_statki[nazwa] = tmp_zaglowiec

        for nazwa, licencja, pojazd_przypisany, in DatabaseInterface.select(f'SELECT nazwa, licencja, pojazd_przypisany FROM kapitanowie'):
            tmp_kapitan = Kapitan(nazwa, licencja)
            if pojazd_przypisany != 'None' and self.m_statki[pojazd_przypisany]:
                tmp_kapitan.m_pojazd_przypisany = self.m_statki[pojazd_przypisany]
            self.m_kapitanowie[nazwa] = tmp_kapitan

        for statek, in DatabaseInterface.select(f'SELECT statek FROM port'):
            if self.m_statki[statek]:
                self.m_port.m_statki[statek] = self.m_statki[statek]

        return self

    def opisy(self):
        print(f'\n Lista polecen systemu:')
        return {self.lista_statkow: "wyswietla pojazwy wodne",
                self.dodaj_statek: "dodaje statek",
                self.dodaj_lodz_podw: "dodaje lodz powdowna",
                self.dodaj_zaglowiec: "dodaje zaglowiec",
                self.lista_kapitanow: "wyswietla kapitanow w systemie",
                self.dodaj_kapitana: "dodaje kapitana do systemu",
                self.przypisz_kapitana: "przypisuje kapitana do statku",
                self.port_przyjmij_statki: "cumuje wybrane stateki do portu",
                self.port_wypusc_statki: "wyplywa wybranymi statkami z portu",
                self.port_wypisz: "wyswietla statki w porcie",
                self.port_zaladuj_statki: "laduje statki w porcie",
                self.port_rozladuj_statki: "rozladowuje statki w porcie",
                self.port_zatankuj_statek: "tankuje okreslony statek",
                self.pomoc: "wyswietl liste polecen",
                self.wyjdz: "wyjscie z programu i zapis bazy danych",
                }

    def interfejs(self):
        komendy = {key.__name__: key for key in self.opisy()}
        while self.m_main_loop:
            try:
                komenda: list[str] = shlex.split(input("\n> "))
            except (EOFError, KeyboardInterrupt):
                print("\ndo widzenia")
                exit()
            try:
                komendy.get(komenda[0])(*komenda[1:])
            except (AttributeError, IndexError, TypeError):
                print("Nieprawidłowe polecenie, wpisz 'pomoc'")
            except KeyError as e:
                print("Brak statku w bazie")
                print(e)
            except RuntimeError as e:
                print("Statek juz istnieje")
                print(e)


def main():
    menu = HMI()
    if DatabaseCheck() is False:
        print("Brak bazy danych, dodawanie danych ze skryptu.")
        (menu
         .dodaj_statek("Kormoran", "1975", 50)
         .dodaj_statek("Albatros", "1983", 200)
         .dodaj_lodz_podw("USS Regan", "1969")
         .dodaj_zaglowiec("Marysienka", "1990")
         .lista_statkow()
         .dodaj_kapitana("Bogdan Boner", "Egzorcysta")
         .przypisz_kapitana("Bogdan Boner", "USS Regan")
         .dodaj_kapitana("Rafal Duda", "Dlugopis")
         .przypisz_kapitana("Rafal Duda", "Marysienka")
         .dodaj_kapitana("Mikolaj Kopernik", "Astrolog")
         .lista_kapitanow()
         .port_przyjmij_statki("Kormoran")
         .port_przyjmij_statki(["Albatros", "USS Regan", "Marysienka"])
         .port_wypisz()
         .port_zaladuj_statki()
         .port_zatankuj_statek("Kormoran", 500)
         .port_wypusc_statki(["Kormoran", "Albatros"])
         .port_rozladuj_statki()
         .lista_statkow()
         .lista_kapitanow()
         .port_wypisz()
         .pomoc()
         .interfejs()
         )
    else:
        print("Baza danych dostepna, importowanie wpisow.")
        (menu
         .import_bazy_danych()
         .lista_statkow()
         .lista_kapitanow()
         .port_wypisz()
         .pomoc()
         .interfejs()
         )


# ####################   TESTY   #####################
# Kazdy test per klasa testuje cala funkcjonalnosc klasy zamiast rozbijac kazdą metode na osobny test

def test_tworzenie_bazy():
    print(f'\ntest_tworzenie_bazy')
    global database_name
    database_name = "test.db"
    try:
        os.remove(database_name)
    except OSError:
        pass

    assert ~pathlib.Path(database_name).exists()

    DatabaseCheck()
    assert pathlib.Path(database_name).exists()


def test_statek():
    print(f'\ntest_statek')
    global database_name
    database_name = "test.db"

    nazwa = "testStatek"
    rok_produkcji = "1234"
    paliwo = 99

    testStatek = Statek(nazwa, rok_produkcji, paliwo)

    assert testStatek.m_nazwa == nazwa
    assert testStatek.m_rok_produkcji == rok_produkcji
    assert testStatek.m_paliwo == paliwo
    assert testStatek.m_stan == "rozladowany"

    testStatek.zaladunek()
    assert testStatek.m_stan == "zaladowany"

    testStatek.rozladunek()
    assert testStatek.m_stan == "rozladowany"

    paliwoTankowane = 10
    testStatek.zatankuj(paliwoTankowane)
    assert testStatek.m_paliwo == paliwo + paliwoTankowane

    # test eksportu do bazy
    testStatek.eksport_do_bazy()
    db_nazwa, db_rok_produkcji, db_stan, db_paliwo = DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, paliwo FROM statki')[0]
    assert db_nazwa == testStatek.m_nazwa
    assert db_rok_produkcji == testStatek.m_rok_produkcji
    assert db_stan == testStatek.m_stan
    assert db_paliwo == testStatek.m_paliwo


def test_lodz_podwodna():
    print(f'\ntest_lodz_podwodna')
    global database_name
    database_name = "test.db"

    nazwa = "testLodzPodwodna"
    rok_produkcji = "5432"

    testLodzPodwodna = LodzPodwodna(nazwa, rok_produkcji)

    assert testLodzPodwodna.m_nazwa == nazwa
    assert testLodzPodwodna.m_rok_produkcji == rok_produkcji
    assert testLodzPodwodna.m_stan == "rozladowany"
    assert testLodzPodwodna.m_stan_zanurzenia == "wynurzony"

    testLodzPodwodna.zaladunek()
    assert testLodzPodwodna.m_stan == "zaladowany"

    testLodzPodwodna.rozladunek()
    assert testLodzPodwodna.m_stan == "rozladowany"

    testLodzPodwodna.zanurz()
    assert testLodzPodwodna.m_stan_zanurzenia == "zanurzony"

    testLodzPodwodna.wynurz()
    assert testLodzPodwodna.m_stan_zanurzenia == "wynurzony"

    testLodzPodwodna.eksport_do_bazy()
    db_nazwa, db_rok_produkcji, db_stan, db_stan_zanurzenia = DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, stan_zanurzenia FROM lodzie_podwodne')[0]
    assert db_nazwa == testLodzPodwodna.m_nazwa
    assert db_rok_produkcji == testLodzPodwodna.m_rok_produkcji
    assert db_stan == testLodzPodwodna.m_stan
    assert db_stan_zanurzenia == testLodzPodwodna.m_stan_zanurzenia


def test_zaglowiec():
    print(f'\ntest_zaglowiec')
    global database_name
    database_name = "test.db"

    nazwa = "testZaglowiec"
    rok_produkcji = "0987"

    testZaglowiec = Zaglowiec(nazwa, rok_produkcji)

    assert testZaglowiec.m_nazwa == nazwa
    assert testZaglowiec.m_rok_produkcji == rok_produkcji
    assert testZaglowiec.m_stan == "rozladowany"
    assert testZaglowiec.m_stan_zagli == "zlozone"

    testZaglowiec.zaladunek()
    assert testZaglowiec.m_stan == "zaladowany"

    testZaglowiec.rozladunek()
    assert testZaglowiec.m_stan == "rozladowany"

    testZaglowiec.rozloz_zagle()
    assert testZaglowiec.m_stan_zagli == "rozlozone"

    testZaglowiec.zloz_zagle()
    assert testZaglowiec.m_stan_zagli == "zlozone"

    testZaglowiec.eksport_do_bazy()
    db_nazwa, db_rok_produkcji, db_stan, db_stan_zagli = DatabaseInterface.select(f'SELECT nazwa, rok_produkcji, stan, stan_zagli FROM zaglowce')[0]
    assert db_nazwa == testZaglowiec.m_nazwa
    assert db_rok_produkcji == testZaglowiec.m_rok_produkcji
    assert db_stan == testZaglowiec.m_stan
    assert db_stan_zagli == testZaglowiec.m_stan_zagli


def test_kapitan():
    print(f'\ntest_kapitan')
    global database_name
    database_name = "test.db"

    nazwa = "test kapitan"
    licencja = "grabaz"

    testKapitan = Kapitan(nazwa, licencja)

    assert testKapitan.m_nazwa == nazwa
    assert testKapitan.m_licencja == licencja
    assert testKapitan.m_pojazd_przypisany is None

    testKapitan.eksport_do_bazy()
    db_nazwa, db_licencja, db_pojazd_przypisany = DatabaseInterface.select(f'SELECT nazwa, licencja, pojazd_przypisany FROM kapitanowie')[0]
    assert db_nazwa == testKapitan.m_nazwa
    assert db_licencja == testKapitan.m_licencja
    assert db_pojazd_przypisany == "None"

    nazwa_statku = "testStatek"
    rok_produkcji = "1234"
    paliwo = 99
    testStatek = Statek(nazwa_statku, rok_produkcji, paliwo)

    testKapitan.przypisz_pojazd(testStatek)
    assert testKapitan.m_pojazd_przypisany == testStatek

    testKapitan.eksport_do_bazy()
    db_nazwa, db_licencja, db_pojazd_przypisany = DatabaseInterface.select(f'SELECT nazwa, licencja, pojazd_przypisany FROM kapitanowie')[0]
    assert db_nazwa == testKapitan.m_nazwa
    assert db_licencja == testKapitan.m_licencja
    assert db_pojazd_przypisany == nazwa_statku


def test_port():
    print(f'\ntest_port')
    global database_name
    database_name = "test.db"

    testPort = Port()

    assert len(testPort.wypisz_statki()) == 0

    testStatek = Statek("testStatek", "1234", 99)
    testPort.przyjmij_pojazd(testStatek)
    assert len(testPort.wypisz_statki()) == 1

    testStatek2 = Statek("testStatek2", "2345", 88)
    testPort.przyjmij_pojazd(testStatek2)
    assert len(testPort.wypisz_statki()) == 2

    testPort.eksport_do_bazy()
    db_statki = DatabaseInterface.select(f'SELECT statek FROM port')
    assert len(db_statki) == len(testPort.m_statki)
    assert db_statki[0][0] == testStatek.m_nazwa
    assert db_statki[1][0] == testStatek2.m_nazwa

    assert testStatek.m_stan == "rozladowany"
    assert testStatek2.m_stan == "rozladowany"
    testPort.zaladuj_statki()
    assert testStatek.m_stan == "zaladowany"
    assert testStatek2.m_stan == "zaladowany"

    testPort.wypusc_pojazd(testStatek)
    assert len(testPort.wypisz_statki()) == 1

    testPort.rozladuj_statki()
    assert testStatek.m_stan == "zaladowany"
    assert testStatek2.m_stan == "rozladowany"

    testPort.zatankuj_statek("testStatek2", 2)
    assert testStatek2.m_paliwo == 88 + 2


def test_hmi():
    print(f'\ntest_hmi')
    global database_name
    database_name = "test.db"

    try:
        os.remove(database_name)
    except OSError:
        pass

    DatabaseCheck()

    testHMI = HMI()

    testHMI.import_bazy_danych()
    assert len(testHMI.m_statki) == 0
    assert len(testHMI.m_kapitanowie) == 0
    assert len(testHMI.m_port.m_statki) == 0

    testHMI.dodaj_statek("Kormoran", "1975", 50)
    testHMI.dodaj_statek("Albatros", "1983", 200)
    testHMI.dodaj_lodz_podw("USS Regan", "1969")
    testHMI.dodaj_zaglowiec("Marysienka", "1990")
    assert len(testHMI.m_statki) == 4

    testHMI.dodaj_kapitana("Bogdan Boner", "Egzorcysta")
    testHMI.przypisz_kapitana("Bogdan Boner", "USS Regan")
    assert testHMI.m_kapitanowie["Bogdan Boner"].m_pojazd_przypisany.m_nazwa == "USS Regan"

    testHMI.dodaj_kapitana("Rafal Duda", "Dlugopis")
    testHMI.przypisz_kapitana("Rafal Duda", "Marysienka")
    assert testHMI.m_kapitanowie["Rafal Duda"].m_pojazd_przypisany.m_nazwa == "Marysienka"
    testHMI.dodaj_kapitana("Mikolaj Kopernik", "Astrolog")
    assert len(testHMI.m_kapitanowie) == 3

    testHMI.port_przyjmij_statki("Kormoran")
    testHMI.port_przyjmij_statki(["Albatros", "USS Regan", "Marysienka"])
    assert len(testHMI.m_port.m_statki) == 4

    for statek in testHMI.m_port.m_statki:
        assert testHMI.m_statki[statek].m_stan == "rozladowany"
    testHMI.port_zaladuj_statki()
    for statek in testHMI.m_port.m_statki:
        assert testHMI.m_statki[statek].m_stan == "zaladowany"

    testHMI.port_zatankuj_statek("Kormoran", 500)
    assert testHMI.m_statki["Kormoran"].m_paliwo == 50 + 500

    testHMI.port_wypusc_statki(["Kormoran", "Albatros"])
    assert len(testHMI.m_port.m_statki) == 2
    assert testHMI.m_port.m_statki["USS Regan"] is not None
    assert testHMI.m_port.m_statki["Marysienka"] is not None

    testHMI.port_rozladuj_statki()
    for statek in testHMI.m_port.m_statki:
        assert testHMI.m_statki[statek].m_stan == "rozladowany"

    assert len(testHMI.m_statki) == 4
    assert len(testHMI.m_kapitanowie) == 3
    assert len(testHMI.m_port.m_statki) == 2

    db_testHMI = HMI()
    db_testHMI.import_bazy_danych()

    assert sorted(db_testHMI.m_statki) == sorted(testHMI.m_statki)
    assert sorted(db_testHMI.m_kapitanowie) == sorted(testHMI.m_kapitanowie)
    assert sorted(db_testHMI.m_port.m_statki) == sorted(testHMI.m_port.m_statki)


if __name__ == "__main__":
    main()
