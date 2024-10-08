# Отрисовка игрового поля
def print_board(board):
    print("\n".join([" | ".join(row) for row in board]))
    print()

# Проверка на победу
def check_winner(board, player):
    # Проверяем ряды, колонки и диагонали
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Проверка на ничью
def check_draw(board):
    return all([cell != " " for row in board for cell in row])

# Основная логика игры
def play_game():
    # Инициализация пустого игрового поля
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)

        # Ввод хода
        try:
            row, col = map(int, input(f"Игрок {current_player}, введите свой ход (ряд и колонка через пробел): ").split())
            if board[row][col] != " ":
                print("Эта клетка уже занята. Попробуйте снова.")
                continue
        except (ValueError, IndexError):
            print("Некорректный ввод. Введите два числа от 0 до 2 через пробел.")
            continue

        # Обновление поля
        board[row][col] = current_player

        # Проверка на победу
        if check_winner(board, current_player):
            print_board(board)
            print(f"Игрок {current_player} победил!")
            break

        # Проверка на ничью
        if check_draw(board):
            print_board(board)
            print("Ничья!")
            break

        # Смена игрока
        current_player = "O" if current_player == "X" else "X"

# Запуск игры
if __name__ == "__main__":
    play_game()
