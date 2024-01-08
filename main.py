from datetime import date, timedelta

# Функція для отримання дня тижня
def get_day_of_week(date_obj):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[date_obj.weekday()]

# Функція для отримання списку користувачів, яких потрібно привітати на наступному тижні
def get_birthdays_per_week(users):    
    today = date.today()
    next_week_start = today + timedelta(days=(7 - today.weekday() + 7) % 7)  # Наступний понеділок
    next_week_end = next_week_start + timedelta(days=7)  # Кінець наступного тижня

    birthdays = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    if users:
        for user in users:
            user_birthday = user['birthday'].replace(year=today.year)  # Задана дата народження в поточному році

            if today <= user_birthday < next_week_end:
                day_of_week = get_day_of_week(user_birthday)
                if day_of_week in birthdays:
                    birthdays[day_of_week].append({'name': user['name'], 'birthday': user_birthday})

        # Обробка днів народження наступного тижня, які припадають на вихідні (Saturday та Sunday)
        next_weekend_birthdays = [user for user in users if next_week_start <= user['birthday'].replace(year=today.year + 1) < next_week_start + timedelta(days=2)]

        for user in next_weekend_birthdays:
            user_birthday = user['birthday'].replace(year=today.year + 1)
            day_of_week = get_day_of_week(user_birthday)
            if day_of_week in birthdays:
                birthdays["Monday"].append({'name': user['name'], 'birthday': user_birthday})

    # Видалення днів, в які не має народжень
    birthdays = {day: users for day, users in birthdays.items() if users}

    return birthdays

# Функція для виводу результату
def print_birthday_result(result):
    for day, users in result.items():
        if users:
            print(f"On {day}, the following users have birthdays:")
            for user in users:
                print(f"- {user['name']} ({user['birthday'].strftime('%Y-%m-%d')})")
            print()
        else:
            print(f"On {day}, no birthdays.\n")

# Тестування функції get_birthdays_per_week
def test_all_future_birthdays_no_weekend():
    users = [
        {'name': 'Alice', 'birthday': date.today() + timedelta(days=3)},
        {'name': 'Bob', 'birthday': date.today() + timedelta(days=5)},
    ]
    result = get_birthdays_per_week(users)
    assert result["Monday"] == [{'name': 'Alice', 'birthday': users[0]['birthday']}]
    assert result["Wednesday"] == [{'name': 'Bob', 'birthday': users[1]['birthday']}]

def test_some_birthdays_on_weekend():
    users = [
        {'name': 'Alice', 'birthday': date.today() + timedelta(days=3)},
        {'name': 'Bob', 'birthday': date.today() + timedelta(days=6)},
    ]
    result = get_birthdays_per_week(users)
    assert result["Monday"] == [{'name': 'Alice', 'birthday': users[0]['birthday']}]
    assert result["Wednesday"] == [{'name': 'Bob', 'birthday': users[1]['birthday']}]

def test_some_birthdays_passed_this_year():
    users = [
        {'name': 'Alice', 'birthday': date.today().replace(month=1, day=3)},
        {'name': 'Bob', 'birthday': date.today().replace(month=12, day=28)},
        {'name': 'Charlie', 'birthday': date.today().replace(month=12, day=29)},
        {'name': 'David', 'birthday': date.today().replace(month=1, day=6)}
    ]
    result = get_birthdays_per_week(users)
    assert result["Monday"] == [{'name': 'Alice', 'birthday': users[0]['birthday']}]
    assert result["Thursday"] == [{'name': 'David', 'birthday': users[3]['birthday']}]

def test_no_users():
    users = []
    result = get_birthdays_per_week(users)
    assert result == {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

def test_all_birthdays_passed_this_year():
    today = date.today()
    users = [
        {'name': 'Alice', 'birthday': today.replace(year=today.year - 1, month=1, day=3)},
        {'name': 'Bob', 'birthday': today.replace(year=today.year - 1, month=12, day=28)},
        {'name': 'Charlie', 'birthday': today.replace(year=today.year - 1, month=12, day=29)},
        {'name': 'David', 'birthday': today.replace(year=today.year - 1, month=1, day=6)}
    ]
    result = get_birthdays_per_week(users)
    assert result == {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

if __name__ == "__main__":
    test_all_future_birthdays_no_weekend()
    test_some_birthdays_on_weekend()
    test_some_birthdays_passed_this_year()
    test_no_users()
    test_all_birthdays_passed_this_year()
    print("All tests passed!")

# Приклад використання
users = [
    {'name': 'Alice', 'birthday': date.today().replace(month=1, day=3)},
    {'name': 'Bob', 'birthday': date.today().replace(month=12, day=28)},
    {'name': 'Charlie', 'birthday': date.today().replace(month=12, day=29)},
    {'name': 'David', 'birthday': date.today().replace(month=1, day=6)}
    # додайте інших користувачів за потреби
]

result = get_birthdays_per_week(users)
print_birthday_result(result)
