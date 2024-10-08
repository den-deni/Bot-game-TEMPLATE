import random
import okx.MarketData as MarketData


flag = "0"  # Production trading:0 , demo trading:1

marketDataAPI = MarketData.MarketAPI(flag=flag, debug=False)






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




def get_dict() -> dict:
    result = marketDataAPI.get_ticker(instId='BTC-USDT')
    data = result['data'][0]
    data_dict = {
        "index": data['instId'],
        "price": float(data['last'])
    }
    return data_dict
