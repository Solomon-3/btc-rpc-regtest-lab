
import requests, json

def rpc(method, params=None,wallet=None):
    url = "http://127.0.0.1:18443/"

    if wallet:
       url = f"{url}wallet/{wallet}"

    payload = json.dumps({
       "jsonrpc": "1.0", "id": "explorer",
       "method" : method, "params": params or []
    })

    r = requests.post(url, data=payload,
                 auth=("bootcamp", "bootcamp123"))
    r.raise_for_status()
    result = r.json()

    if result.get("error"):
        raise Exception(f"RPC error: {result['error']}")
    return result["result"]

info = rpc("getblockchaininfo")
print(f"Chain: {info['chain']}")
print(f"Blocks: {info['blocks']}")


balance = rpc("getbalance", wallet="spencer")
print(f"Spencer has {balance} BTC")


addr = rpc("getnewaddress",wallet = "spencer")
print(f"Address: {addr}")



# exercise 2

def show_blockchain_info():
   url = "http://127.0.0.1:18443/"

info =rpc("getblockchaininfo")
print(f"Chain: {info['chain']}")
print(f"Blocks: {info['blocks']}")
print(f"Difficulty: {info['difficulty']}")
print(f"Bestblockhash: {info['bestblockhash']}")


# exercise 3

def show_wallet_balance(wallet_name):
       url = "http://127.0.0.1:18443/"
try:
       rpc("loadwallet", [wallet_name])
except Exception:
       pass #wallet already loaded

balance = rpc("getbalance", wallet="spencer")
print(f"===wallet: Spencer===")
print(f"  Balance: {balance} BTC")

print(f"=======================================")




# execise 4
count = 5
wallet_name="spencer"
def list_transactions(wallet_name, count=5):
 url = "http://127.0.0.1:18443/"

try:
   rpc("loadwallet", [wallet_name])
except Exception :
   pass

txs = rpc("list_transactions", ["*",count], wallet=wallet_name)

print(f"====== exercise 4 =======")
print(f"=== Last {count} transactions ({wallet_name}) ===")

for tx in txs:
   if tx['category'] in ('receive','generate'):
        direction = "IN "
   else:
        direction="OUT"
   print(f" {direction} {tx['amount']:+.8f} BTC")
   print(f" txid: {tx['txid'][:32]}...")



# exercise 5 DECODE TRANSACTION
print(f"==== DAY 2 exercise 5 decode transaction ========")

def decode_transaction(txid):
  tx = rpc("getrawtransaction", [txid, True])
  print(f"=== Transaction ({tx['size']} bytes ===)")

  print("\nInputs:")
  for vin in tx['vin']:
      if 'coinbase' in vin:
           print("COINBASE (mining reward)")
      else:
           print(f" From: {vin['txid'][:24]}...")

  print("\nOutputs:")
  for vout in tx['vout']:
     addr = vout['scriptPubKey'].get('address', '?')
     print(f" {vout['value']:.8f} BTC -> {addr}")



# exercise 6  BLOCK DETAILS
print(f"=== Day 2 execise 6 block detais")

def show_block(blockhash=None):
    if blockhash is None:
        blockhash = rpc("getbestblockhash")
    block =rpc("getblock", [blockhash, 1])

    print(f"=== Block {block['height']} ===")
    print(f" Hash: {block['hash'][:32]}...")
    print(f" Time: {block['time']}")
    print(f" TXs: {block['nTx']}")
    print(f" Size: {block['size']} bytes")


# exercise 7  Embedded a message on-chain
print(f"=== day 2 exercise 7 embedded a message on-chain")

def embed_message(wallet_name, message):
   hex_msg = message.encode().hex()
   utxos = rpc("listunspent", [1], wallet=wallet_name)
   utxo = utxos[0]
   change = round(utxo['amount'] - 0.0001, 8)
   change_addr = rpc("getnewaddress", wallet=wallet_name)
   raw = rpc("createrawtransaction", [[{"txid": utxo[txid], "vout": utxo['vout']}], [{"data": hex_msg}, {change_addr: change}])
   signed = rpc("signrawtransactionwithwallet", [raw], wallet=wallet_name)
   txid = rpc("sendrawtransaction", [signed['hex']])
   print(f"Message '{message}' embedded! TX: {txid[:32]}...")



# exercise 8 MULTISIG
#print(f"=== day 2 exercise 8 multisig")

