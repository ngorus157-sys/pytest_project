# test_functions.py
# Импортируем функцию, которую хотим протестировать
import pytest
from functions import add, get_user_full_name, is_valid_password, get_age_group, calculate_cart_total, get_value_from_dict, Wallet, InsufficientFundsError
# Объявляем тестовую функцию
def test_add():
    """
    Проверяем, что функция add() правильно складывает два числа.
    """
    # Используем assert, чтобы проверить результат
    assert add(2, 3) == 5
    assert add(2, 3) == 5
    assert add(10, -5) == 5

# ШАГ 1: Создаем фикстуру
@pytest.fixture
def sample_user_data():
    """Фикстура, которая возвращает словарь с данными пользователя."""
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    }

# ШАГ 2: Используем фикстуру в тестах
def test_get_user_full_name_with_fixture(sample_user_data):
    # Pytest автоматически вызовет фикстуру и передаст ее результат
    # в аргумент sample_user_data
    assert get_user_full_name(sample_user_data) == "Jane Doe"
def test_user_has_email_with_fixture(sample_user_data):
    assert "email" in sample_user_data


# Создаем список тестовых сценариев
# Каждый кортеж - это один набор данных: (аргумент_1, аргумент_2, ожидаемый_результат)
test_cases = [
    (1, 2, 3), # Обычное сложение
    (-1, -1, -2), # Сложение отрицательных чисел
    (5, 0, 5), # Сложение с нулем
    (-1, 1, 0), # Противоположные числа
    (3.5, 2.5, 6.0) # Сложение чисел с плавающей точкой
]
@pytest.mark.parametrize("a, b, expected", test_cases)
def test_add_parametrized(a, b, expected):
    """Проверяем функцию add() с разными наборами данных."""
    assert add(a, b) == expected


from functions import divide
def test_divide_by_zero_raises_error():
    """Проверяем, что деление на ноль вызывает ValueError."""
    with pytest.raises(ValueError):
        divide(10, 0)

@pytest.mark.skip(reason="Эта функция еще в разработке") 
def test_new_feature(): 
    # Код теста для новой, еще не готовой функции 
    assert False 

@pytest.mark.xfail(reason="Известный баг с точностью float, тикет #123")
def test_float_precision_bug():
    assert (0.1 + 0.2) == 0.3 # Этот тест упадет из-за особенностей float




@pytest.mark.math
def test_add(): 
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(10, -5) == 5

@pytest.mark.math
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, -1, -2),
    (5, 0, 5),
    (-1, 1, 0),
    (3.5, 2.5, 6.0)
])
def test_add_parametrized(a, b, expected): 
    assert add(a, b) == expected

@pytest.mark.user_profile 
def test_get_user_full_name_with_fixture(sample_user_data): 
    assert get_user_full_name(sample_user_data) == "Jane Doe"

@pytest.mark.user_profile 
def test_user_has_email_with_fixture(sample_user_data): 
    assert "email" in sample_user_data

# Задание 1
def test_password_valid_length():
    """Пароль корректной длины (10 символов) — True."""
    assert is_valid_password("abcdefghij") is True


def test_password_too_short():
    """Пароль слишком короткий (5 символов) — False."""
    assert is_valid_password("abcde") is False


def test_password_boundary_length():
    """Пароль ровно 8 символов — граница, должно быть True."""
    assert is_valid_password("abcdefgh") is True
    # И на всякий случай — 7 символов, уже False
    assert is_valid_password("abcdefg") is False



# Задание 2
age_cases = [
    (5, "ребенок"),     # обычный ребенок
    (12, "ребенок"),    # граница: еще ребенок
    (13, "подросток"),  # граница: уже подросток
    (17, "подросток"),  # граница: еще подросток
    (18, "взрослый"),   # граница: уже взрослый

]


@pytest.mark.parametrize("age, expected_group", age_cases)
def test_get_age_group(age, expected_group):
    """Проверяем get_age_group на разных возрастах, включая пограничные."""
    assert get_age_group(age) == expected_group


# Задание 3
@pytest.fixture
def sample_cart():
    """Фикстура: тестовая корзина с тремя товарами."""
    return [
        {"name": "Яблоки", "price": 50.0, "quantity": 2},
        {"name": "Хлеб", "price": 40.0, "quantity": 1},
        {"name": "Молоко", "price": 80.0, "quantity": 3},
    ]


def test_calculate_cart_total(sample_cart):
    """Итоговая сумма: 50*2 + 40*1 + 80*3 = 100 + 40 + 240 = 380."""
    assert calculate_cart_total(sample_cart) == pytest.approx(380.0)


def test_cart_contains_bread(sample_cart):
    """В корзине есть товар с именем 'Хлеб'."""
    names = [item["name"] for item in sample_cart]
    assert "Хлеб" in names



# Задание 4
def test_get_value_from_dict_success():
    """Успешный сценарий: ключ существует."""
    data = {"name": "Alice", "age": 30}
    assert get_value_from_dict(data, "name") == "Alice"
    assert get_value_from_dict(data, "age") == 30


def test_get_value_from_dict_missing_key_raises():
    """Сценарий с ошибкой: несуществующий ключ вызывает KeyError."""
    data = {"name": "Alice", "age": 30}
    with pytest.raises(KeyError):
        get_value_from_dict(data, "email")





# Задание 5
@pytest.fixture
def wallet():
    """Фикстура: кошелек с начальным балансом 20."""
    return Wallet(initial_balance=20)


def test_wallet_deposit_success(wallet):
    """Успешное пополнение счета."""
    wallet.deposit(30)
    assert wallet.balance == 50


def test_wallet_withdraw_success(wallet):
    """Успешное снятие средств."""
    wallet.withdraw(15)
    assert wallet.balance == 5


def test_wallet_withdraw_insufficient_funds(wallet):
    """Попытка снять больше, чем есть, вызывает InsufficientFundsError."""
    with pytest.raises(InsufficientFundsError):
        wallet.withdraw(100)
    # Баланс не должен измениться после неудачной попытки
    assert wallet.balance == 20


invalid_amount_cases = [
    ("__init__", -10),
    ("__init__", -0.01),
    ("deposit", 0),
    ("deposit", -5),
    ("withdraw", 0),
    ("withdraw", -5),
]


@pytest.mark.parametrize("method, invalid_value", invalid_amount_cases)
def test_wallet_invalid_values_raise_value_error(method, invalid_value):
    """
    Проверяем, что __init__, deposit и withdraw вызывают ValueError
    при отрицательных или нулевых значениях.
    """
    if method == "__init__":
        with pytest.raises(ValueError):
            Wallet(initial_balance=invalid_value)
    elif method == "deposit":
        w = Wallet(initial_balance=20)
        with pytest.raises(ValueError):
            w.deposit(invalid_value)
    elif method == "withdraw":
        w = Wallet(initial_balance=20)
        with pytest.raises(ValueError):
            w.withdraw(invalid_value)