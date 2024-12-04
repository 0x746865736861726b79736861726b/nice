from web3 import Web3


class EthereumNonce:
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum network.")

    def get_nonce(self, wallet_address: str) -> int:
        return self.web3.eth.get_transaction_count(wallet_address)
