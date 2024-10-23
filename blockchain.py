import requests

def get_bitcoin_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}/balance"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        balance_in_btc = data['balance'] / 100000000
        return f"Balance: {balance_in_btc:.6f} BTC"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

address = 'tb1q2uasj6kp25psryp7xdgn0906vlr2szlqyyuadg'
balance_info = get_bitcoin_balance(address)
print(balance_info)
