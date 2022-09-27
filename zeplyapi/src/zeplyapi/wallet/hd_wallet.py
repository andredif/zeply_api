from anyio import get_all_backends

from py_crypto_hd_wallet import (
    HdWalletBip44Coins, HdWalletBipDataTypes, HdWalletBipKeyTypes, HdWalletBipFactory, HdWalletBipWordsNum
)
from .encrypter import encrypt, decrypt

from ..utils import load_data, save_data
from ..schemas import Coin
from ..config import settings


mnemonic_password = settings.ZEPLY_MNEMONIC_KEY

class HdWalletHandler(object):

    def __init__(self, coin: Coin=Coin.ETH):
        self.mnemonic_prefix = coin.value
        if coin == Coin.ETH:
            self.hd_wallet_fact = HdWalletBipFactory(HdWalletBip44Coins.ETHEREUM)
        elif coin == Coin.BTC:
            self.hd_wallet_fact = HdWalletBipFactory(HdWalletBip44Coins.BITCOIN)
        self.wallet = self.get_wallet()

    def get_wallet(self):
        mnemonic_name = f"{self.mnemonic_prefix}_mnemonic"
        data = load_data()
        mnemonic_bytes = data.get(mnemonic_name)
        if mnemonic_bytes:
            password_bytes = mnemonic_password.encode()
            mnemonic = decrypt(password_bytes, mnemonic_bytes).decode()
            return self.hd_wallet_fact.CreateFromMnemonic("my_wallet_name", mnemonic)
        else:
           hd_wallet = self.hd_wallet_fact.CreateRandom("my_wallet_name", HdWalletBipWordsNum.WORDS_NUM_12)
           mnemonic = hd_wallet.GetData(HdWalletBipDataTypes.MNEMONIC)
           print(f"generated mnemonic is: {mnemonic}")
           self.save_mnemonic(mnemonic_name, mnemonic_password, mnemonic)


    def save_mnemonic(self, mnemonic_name: str, password: str, mnemonic: str):
        data = load_data()
        mnemonic_bytes = mnemonic.encode()
        password_bytes = password.encode()
        mnemonic_encrypted = encrypt(password_bytes, mnemonic_bytes)
        data[mnemonic_name] = mnemonic_encrypted
        return save_data(data)
    
    def generate_new_address(self, id: str = 1):
        self.wallet.Generate(addr_num=id)
        self.addresses = self.addresses_list()

    def get_all_addresses(self):
        return self.wallet.GetData(HdWalletBipDataTypes.ADDRESS)

    def addresses_list(self):
        addresses = self.get_all_addresses()
        return [addr.GetKey(HdWalletBipKeyTypes.ADDRESS) for addr in self.wallet.GetData(HdWalletBipDataTypes.ADDRESS)]

    def get_address_key(self, address):
        addresses = self.get_all_addresses()
        for addr in addresses:
            curr_address = addr.GetKey(HdWalletBipKeyTypes.ADDRESS)
            if curr_address == address:
                return f"0x{addr.GetKey(HdWalletBipKeyTypes.RAW_PRIV)}"