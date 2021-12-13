# How to mint tokens on top of Cardano Blockchain

# 1. Environment configuration

Deadalus wallet allow to run a full cardano node and allow to run a cardano-cli

**Mac Path:**

/Applications/Daedalus Mainnet.app/Contents/MacOS

/Applications/Daedalus Testnet.app/Contents/MacOS

**Update Environment variables**

```bash
export PATH=$PATH:"/Applications/Daedalus Testnet.app/Contents/MacOS"
```

**How works daedalus**

*Daedalus is the UI of cardano-wallet →  cardano-wallet interact with cardano-node* 

**Cardano socket file**

get it with command: 

```bash
ps -ef | grep cardano-node
```

output example

> 501 59465 59454   0  8:54AM ??       149:12.43 cardano-node run --socket-path cardano-node.socket --shutdown-ipc 3 --topology /Applications/Daedalus Testnet.app/Contents/Resources/topology.yaml --database-path chain --port 60215 --config /Applications/Daedalus Testnet.app/Contents/Resources/config.yaml
501 59466 59454   0  8:54AM ??        68:41.57 cardano-wallet serve --shutdown-handler --port 60216 --database /Users/valeriomellini/Library/Application Support/Daedalus Testnet/wallets --tls-ca-cert /Users/valeriomellini/Library/Application Support/Daedalus Testnet/tls/server/ca.crt --tls-sv-cert /Users/valeriomellini/Library/Application Support/Daedalus Testnet/tls/server/server.crt --tls-sv-key /Users/valeriomellini/Library/Application Support/Daedalus Testnet/tls/server/server.key --token-metadata-server [https://metadata.cardano-testnet.iohkdev.io](https://metadata.cardano-testnet.iohkdev.io/) --sync-tolerance 300s --testnet /Applications/Daedalus Testnet.app/Contents/Resources/genesis.json --node-socket ***/Users/valeriomellini/Library/Application Support/Daedalus Testnet/cardano-node.socket***
> 

```bash
export CARDANO_NODE_SOCKET_PATH="/Users/valeriomellini/Library/Application Support/Daedalus Testnet/cardano-node.socket"
```

### Query to blockchain
To check if everything works fine

```bash
cardano-cli query tip --testnet-magic 1097911063

cardano-cli query tip --mainnet
```

### Environment variables

```bash
export magicnumber="1097911063"
```

## Wallet Keys

```bash
cardano-cli address key-gen --verification-key-file payment.vkey --signing-key-file payment.skey
```

```bash
#TESTNET
cardano-cli address build --payment-verification-key-file payment.vkey --out-file payment.addr --testnet-magic=$magicnumber

#MAINNET
cardano-cli address build --payment-verification-key-file payment.vkey --out-file payment.addr --testnet-magic=$magicnumber
```

```bash
export address=[INSERT DESTINATION ADDRESS]
```
## UTxO query

```bash
#TESTNET
cardano-cli query utxo --address $(< payment.addr) --testnet-magic=$magicnumber

#MAINNET
cardano-cli query utxo --address $(< payment.addr) --mainnet
```

## Protocol parameters

```bash
#TESTNET
cardano-cli query protocol-parameters --testnet-magic=$magicnumber --out-file protocol.json

#MAINNET
cardano-cli query protocol-parameters --mainnet --out-file protocol.json
```

# 2. **Policies**

**Every asset on Cardano has a policy.**

The policy-id is required to create a unique token on cardano blockchain

```bash
mkdir policy
```

```bash
cardano-cli address key-gen \
    --verification-key-file policy/policy.vkey \
    --signing-key-file policy/policy.skey
```

## Policy.script creation

```bash
touch policy/policy.script && echo "" > policy/policy.script
```

the hash of the key has to be inserted into the json file "policy.script"

```bash
echo "{" >> policy/policy.script 
echo "  \"keyHash\": \"$(cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey)\"," >> policy/policy.script 
echo "  \"type\": \"sig\"" >> policy/policy.script 
echo "}" >> policy/policy.script
```

## PolicyId calculation

```bash
cardano-cli transaction policyid --script-file ./policy/policy.script >> policy/policyID
```

# 3. **Minting**
## UTXO Query
Call the command: 

```bash
#TESTNET
cardano-cli query utxo --address $(< payment.addr) --testnet-magic=$magicnumber

#MAINNET
cardano-cli query utxo --address $(< payment.addr) --mainnet
```

## Variables definitions
```bash
export txhash="insert your txhash here"
export txix="insert your TxIx here"
export funds="insert Amount here"
export policyid=$(cat policy/policyID)
export tokenname="ZEN"
export tokenamount="100000000"
export fee="0"
export output="0"
```

## Raw transaction
```bash
cardano-cli transaction build-raw \
 --fee $fee \
 --tx-in $txhash#$txix \
 --tx-out $address+$output+"$tokenamount $policyid.$tokenname" \
 --mint="$tokenamount $policyid.$tokenname" \
 --minting-script-file policy/policy.script \
 --out-file matx.raw
```

> Here is where part one of the magic happens. For the --tx-out, we need to specify which address will receive our transaction. In our case, we send the tokens to our own address.
> 
> 
> **NOTE**
> 
> The syntax is very important, so here it is word for word. There are no spaces unless explicitly stated:
> 
> 1. address hash
> 2. a plus sign
> 3. the output in Lovelace (ada) (output = input amount — fee)
> 4. a plus sign
> 5. quotation marks
> 6. the amount of the token
> 7. a blank/space
> 8. the policy id
> 9. a dot
> 10. the token name (optional if you want multiple/different tokens: a blank, a plus, a blank, and start over at 6.)
> 11. quotation marks

## Fees calculation 
```bash
# TESTNET
export fee=$(cardano-cli transaction calculate-min-fee --tx-body-file matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 --testnet-magic=$magicnumber --protocol-params-file protocol.json | cut -d " " -f1)

#MAINNET
export fee=$(cardano-cli transaction calculate-min-fee --tx-body-file matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 --mainnet --protocol-params-file protocol.json | cut -d " " -f1)
```

## ADA output calculation
```bash
export output=$(expr $funds - $fee)
```

Do the transaction again

```bash
cardano-cli transaction build-raw \
--fee $fee  \
--tx-in $txhash#$txix  \
--tx-out $address+$output+"$tokenamount $policyid.$tokenname" \
--mint="$tokenamount $policyid.$tokenname" \
--minting-script-file policy/policy.script \
--out-file matx.raw

```

Sign the transaction la transazione 

```bash
#TESTNET
cardano-cli transaction sign  \
--signing-key-file payment.skey  \
--signing-key-file policy/policy.skey  \
--testnet-magic $magicnumber --tx-body-file matx.raw  \
--out-file matx.signed

#MAINNET
cardano-cli transaction sign  \
--signing-key-file payment.skey  \
--signing-key-file policy/policy.skey  \
--mainnet --tx-body-file matx.raw  \
--out-file matx.signed

```

## Transaction submit

```bash
#TESTNET
cardano-cli transaction submit --tx-file matx.signed --testnet-magic $magicnumber

#MAINNET
cardano-cli transaction submit --tx-file matx.signed --mainnet
```


## Special thanks to this tutorial 
[ADA MakerSpace](https://www.youtube.com/watch?v=rhAgBLJnwP0)