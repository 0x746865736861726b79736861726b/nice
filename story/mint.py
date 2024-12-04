from web3 import AsyncWeb3
from dotenv import load_dotenv

from .config import Config


class AsyncBlockchainLibrary:
    def __init__(self, config: Config):
        """
        Initialize the AsyncBlockchainLibrary with configuration parameters.

        Args:
            config (Config): Configuration object containing provider URL, contract address,
                            ABI, chain ID, from address, and gas limit.
        """
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(config.provider_url))
        self.contract = self.w3.eth.contract(
            address=config.contract_address, abi=config.abi
        )
        self.chain_id = config.chain_id
        self.from_address = config.from_address
        self.gas_limit = config.gas_limit

    async def get_gas_price(self):
        """
        Get the current gas price on the Ethereum network.

        Returns:
            int: The current gas price in wei.
        """
        return await self.w3.eth.gas_price

    async def build_and_send_transaction(self, function_name: str, *args):
        """
        Build a transaction for the given contract function and send it.

        Args:
            function_name (str): The name of the contract function to call.
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
                "nonce": nonce,
                "from": self.from_address,
            }
        )

        tx_hash = await self.w3.eth.send_transaction(transaction)
        return tx_hash

    async def get_transaction_receipt(self, tx_hash):
        """
        Wait for a transaction receipt for the given transaction hash.

        Args:
            tx_hash (str): The transaction hash.

        Returns:
            dict: The transaction receipt.
        """
        return await self.w3.eth.wait_for_transaction_receipt(tx_hash)
