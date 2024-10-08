import random

# Карты и их значения
cards = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11  # Туз может считаться за 1, но пока 11
}

# Функция для получения случайной карты
def get_card():
    return random.choice(list(cards.keys()))

# Подсчет суммы с учетом туза
def calculate_score(hand):
    score = sum([cards[card] for card in hand])
    if "A" in hand and score > 21:
        score -= 10  # Учитываем, что туз может считаться как 1
    return score

# Функция для начала игры
def play_game():
    player_hand = [get_card(), get_card()]
    dealer_hand = [get_card(), get_card()]

    print(f"Карты игрока: {player_hand[0]} {player_hand[1]}, сумма: {calculate_score(player_hand)}")
    print(f"Одна карта дилера: {dealer_hand[0]}")

    # Ход игрока
    while calculate_score(player_hand) < 21:
        action = input("Хотите взять еще карту? (да/нет): ").lower()
        if action == "да":
            player_hand.append(get_card())
            print(f"Карты игрока: {player_hand}, сумма: {calculate_score(player_hand)}")
        else:
            break

    player_score = calculate_score(player_hand)
    if player_score > 21:
        print("Перебор! Вы проиграли.")
        return

    # Ход дилера
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(get_card())

    dealer_score = calculate_score(dealer_hand)
    print(f"Карты дилера: {dealer_hand}, сумма: {dealer_score}")

    # Определение победителя
    if dealer_score > 21 or player_score > dealer_score:
        print("Поздравляю, вы выиграли!")
    elif player_score < dealer_score:
        print("Вы проиграли.")
    else:
        print("Ничья.")

# Запуск игры
if __name__ == "__main__":
    play_game()
