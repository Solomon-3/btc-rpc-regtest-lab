
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
def list_transactions(wallet_name, count=5):
  url = "http://127.0.0.1:18443/"

try:
   rpc("loadwallet", [wallet_name])
except Exception:
   pass

txs = rpc("list_transactions", ["*",count], wallet = spencer)

print(f"====== exercise 4 =======")
print(f"=== Last{count} transactions ({wallet_name}) ===")

for tx in txs:
   if tx['category'] in ('receive','generate'):
        direction = "IN "
   else:
        direction="OUT"
   print(f" {direction} {tx['amount']:+.8f} BTC")
   print(f" txid: {tx['txid'][:32]}...")

# exercise 5
