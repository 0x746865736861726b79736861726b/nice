from web3 import Web3

# Параметри підключення до мережі Story Odyssey
provider_url = (
    "https://story-testnet-evm.itrocket.net"  # Замість цього вставте ваш RPC URL
)
contract_address = (
    "0xFFcCD25f12Bcb322816B099C6A0087cc7De711Bc"  # Вставте адресу вашого контракту
)
private_key = "0xYourPrivateKey"  # Ваш приватний ключ
wallet_address = "0xf72Ef00fbEe7fdBE4cc061c7d4A74c691063B869"  # Адреса вашого гаманця

# Підключення до мережі
web3 = Web3(Web3.HTTPProvider(provider_url))

# Перевірка з'єднання
if not web3.is_connected():
    raise Exception("Неможливо підключитися до мережі Story Odyssey")

# ABI контракту
contract_abi = [
    # Вставте ваш ABI тут
]

# Ініціалізація контракту
contract = web3.eth.contract(
    address=Web3.to_checksum_address(contract_address), abi=contract_abi
)


# Мінт токена
def mint_token(to_address=None):
    # Визначення функції мінта
    if to_address:
        mint_function = contract.functions.mint(Web3.to_checksum_address(to_address))
    else:
        mint_function = contract.functions.mint()

    # Формування транзакції
    transaction = mint_function.build_transaction(
        {
            "chainId": web3.eth.chain_id,
            "gas": 300000,  # Задайте відповідний ліміт газу
            "gasPrice": web3.toWei("10", "gwei"),  # Актуальна ціна газу
            "nonce": web3.eth.get_transaction_count(
                Web3.to_checksum_address(wallet_address)
            ),
        }
    )

    # Підписання транзакції
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Відправка транзакції
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"Транзакція надіслана. Hash: {web3.toHex(tx_hash)}")

    # Очікування підтвердження
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Токен успішно змінтовано. Транзакція підтверджена: {receipt}")


# Виклик функції мінта
# Для мінта без аргументів
mint_token()

# Для мінта на конкретну адресу
# mint_token("0xRecipientAddress")
