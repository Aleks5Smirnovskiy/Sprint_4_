from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2



    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

# Набор тестов для класса BooksCollector.
# Покрывает все методы: добавление книг, установка жанров,
# фильтрация по жанрам, детские книги и работа с избранным.

from main import BooksCollector
import pytest


class TestBooksCollectorAddNewBook:

    def test_add_new_book_add_two_different_books(self):
       # Проверяем, что две разные книги добавляются в словарь books_genre."""
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        books = collector.get_books_genre()

        assert len(books) == 2
        assert 'Гордость и предубеждение и зомби' in books
        assert 'Что делать, если ваш кот хочет вас убить' in books

    @pytest.mark.parametrize(
        'name',
        [
            '',          # слишком короткое название
            'A' * 41,    # слишком длинное название
        ],
    )
    def test_add_new_book_name_invalid_by_length(self, name):
        # Проверяем, что книга не добавляется, если длина названия некорректна.
        collector = BooksCollector()

        collector.add_new_book(name)

        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_cannot_add_same_twice(self):
        #  Проверяем, что одна и та же книга не добавляется дважды.
        collector = BooksCollector()

        collector.add_new_book('1984')
        collector.add_new_book('1984')

        books = collector.get_books_genre()

        assert len(books) == 1
        assert '1984' in books


class TestBooksCollectorSetBookGenre:

    @pytest.mark.parametrize(
        'genre',
        ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'],
    )
    def test_set_book_genre_success_for_existing_book_and_valid_genre(self, genre):
        # Проверяем, что существующей книге можно установить допустимый жанр.
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')

        collector.set_book_genre('Гарри Поттер', genre)

        assert collector.get_book_genre('Гарри Поттер') == genre

    def test_set_book_genre_not_set_for_unknown_book(self):
        # Проверяем, что жанр не устанавливается для несуществующей книги.
        collector = BooksCollector()

        collector.set_book_genre('Несуществующая книга', 'Ужасы')

        assert collector.get_book_genre('Несуществующая книга') is None

    def test_set_book_genre_not_set_for_invalid_genre(self):
        #  Проверяем, что жанр не устанавливается, если он не из списка допустимых.
        collector = BooksCollector()
        collector.add_new_book('Книга без жанра')

        collector.set_book_genre('Книга без жанра', 'Документалистика')

        assert collector.get_book_genre('Книга без жанра') == ''


class TestBooksCollectorGetBookGenre:

    def test_get_book_genre_returns_genre_if_set(self):
        # Проверяем, что для существующей книги возвращается её жанр.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        assert collector.get_book_genre('Оно') == 'Ужасы'

    def test_get_book_genre_returns_none_for_unknown_book(self):
        #  Проверяем, что для неизвестной книги возвращается None.
        collector = BooksCollector()

        assert collector.get_book_genre('Неизвестная книга') is None


class TestBooksCollectorGetBooksWithSpecificGenre:

    def test_get_books_with_specific_genre_returns_only_that_genre(self):
        # Проверяем, что возвращаются только книги с указанным жанром.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Корпорация монстров')

        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.set_book_genre('Корпорация монстров', 'Мультфильмы')

        horror_books = collector.get_books_with_specific_genre('Ужасы')

        assert horror_books == ['Оно']

    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self):
        # Проверяем, что для недопустимого жанра возвращается пустой список.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        result = collector.get_books_with_specific_genre('Документалистика')

        assert result == []


class TestBooksCollectorGetBooksForChildren:

    def test_get_books_for_children_excludes_age_restricted_genres(self):
        # Проверяем, что в список детских книг не попадают Ужасы и Детективы.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')
        collector.add_new_book('Корпорация монстров')
        collector.add_new_book('Один дома')

        collector.set_book_genre('Оно', 'Ужасы')                # 18+
        collector.set_book_genre('Шерлок Холмс', 'Детективы')   # 18+
        collector.set_book_genre('Корпорация монстров', 'Мультфильмы')
        collector.set_book_genre('Один дома', 'Комедии')

        children_books = collector.get_books_for_children()

        assert 'Оно' not in children_books
        assert 'Шерлок Холмс' not in children_books
        assert 'Корпорация монстров' in children_books
        assert 'Один дома' in children_books


class TestBooksCollectorFavorites:

    def test_add_book_in_favorites_adds_only_existing_book(self):
        #  Проверяем, что в избранное добавляются только существующие книги.
        collector = BooksCollector()
        collector.add_new_book('Оно')

        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Неизвестная книга')

        favorites = collector.get_list_of_favorites_books()

        assert favorites == ['Оно']

    def test_add_book_in_favorites_cannot_add_same_twice(self):
        #  Проверяем, что одна и та же книга не добавляется в избранное дважды.
        collector = BooksCollector()
        collector.add_new_book('Оно')

        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Оно')

        favorites = collector.get_list_of_favorites_books()

        assert favorites == ['Оно']

    def test_delete_book_from_favorites_remove_if_exists(self):
        # Проверяем, что книга удаляется из избранного, если она там есть.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')

        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Шерлок Холмс')

        collector.delete_book_from_favorites('Оно')

        favorites = collector.get_list_of_favorites_books()

        assert 'Оно' not in favorites
        assert 'Шерлок Холмс' in favorites

    def test_delete_book_from_favorites_ignored_if_not_in_favorites(self):
        # Проверяем, что удаление книги, которой нет в избранном, игнорируется.
        collector = BooksCollector()
        collector.add_new_book('Оно')

        collector.delete_book_from_favorites('Оно')  # не добавляли в избранное

        favorites = collector.get_list_of_favorites_books()

        assert favorites == []

    def test_get_list_of_favorites_books_returns_current_favorites(self):
        # Проверяем, что возвращается актуальный список избранных книг.
        collector = BooksCollector()
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')

        collector.add_book_in_favorites('Оно')
        collector.add_book_in_favorites('Шерлок Холмс')

        favorites = collector.get_list_of_favorites_books()

        assert favorites == ['Оно', 'Шерлок Холмс']
