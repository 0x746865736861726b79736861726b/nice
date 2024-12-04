from story import AsyncBlockchainLibrary, Config


async def main():
    config = Config()
    library = AsyncBlockchainLibrary(config)

    try:
        tx_hash = await library.build_and_send_transaction("mint")
        print(f"Transaction sent: {tx_hash.hex()}")

        receipt = await library.get_transaction_receipt(tx_hash)
        print("Transaction successful:", receipt)
    except Exception as e:
        print("Error during transaction:", str(e))
