import json
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.provider_url = os.getenv("PROVIDER_URL")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        self.chain_id = int(os.getenv("CHAIN_ID"))
        self.from_address = os.getenv("FROM_ADDRESS")
        self.gas_limit = int(os.getenv("GAS_LIMIT", 200000))
        self.private_key = os.getenv("PRIVATE_KEY")
        with open(os.path.join(os.path.dirname(__file__), "abi.json"), "r") as abi_file:
            self.abi = json.load(abi_file)
