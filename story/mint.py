from web3 import AsyncWeb3
from .config import Config


class AsyncBlockchainLibrary:
    def __init__(self, config: Config):
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(config.provider_url))
        self.contract = self.w3.eth.contract(
            address=config.contract_address, abi=config.abi
        )
        self.chain_id = config.chain_id
        self.from_address = config.from_address
        self.gas_limit = config.gas_limit

    async def get_gas_price(self):
        """
        Get the current gas price.

        Returns:
            int: The current gas price in wei.
        """
        return await self.w3.eth.gas_price

    async def get_nonce(self):
        """
        Get the current nonce for the from address.

        Returns:
            int: The current nonce for the from address.
        """
        return await self.w3.eth.get_transaction_count(self.from_address)

    async def build_and_send_transaction(
        self, function_name: str, private_key: str, *args
    ):
        """
        Build, sign, and send a transaction to the Ethereum blockchain.

        Args:
            function_name (str): The name of the contract function to call.
            private_key (str): The private key to sign the transaction.
            *args: The arguments to pass to the contract function.

        Returns:
            str: The transaction hash.
        """
        nonce = await self.w3.eth.get_transaction_count(self.from_address)
        gas_price = await self.get_gas_price()

        contract_function = getattr(self.contract.functions, function_name)(*args)
        transaction = await contract_function.build_transaction(
            {
                "chainId": self.chain_id,
                "gas": self.gas_limit,
                "gasPrice": gas_price,
                "nonce": await self.get_nonce(),
                "from": self.from_address,
            }
        )

        signed_txn = await self.sign_transaction(transaction, private_key)

        tx_hash = await self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash

    async def get_transaction_receipt(self, tx_hash):
        """
        Get the transaction receipt for a given transaction hash.

        Args:
            tx_hash (str): The transaction hash to retrieve the receipt for.

        Returns:
            dict: The transaction receipt.
        """

        return await self.w3.eth.wait_for_transaction_receipt(tx_hash)

    async def sign_transaction(self, tx, private_key):
        """
        Sign the transaction using the provided private key.

        Args:
            tx (dict): The transaction to sign.
            private_key (str): The private key to sign the transaction.

        Returns:
            SignedTransaction: The signed transaction object.
        """
        return self.w3.eth.account.sign_transaction(tx, private_key)
