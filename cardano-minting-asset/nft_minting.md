# How to mint tokens on top of Cardano Blockchain

# 1. **Wallet configuration**
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
cardano-cli address build --payment-verification-key-file payment.vkey --out-file payment.addr --mainnet
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

### Policy anti-minting
```bash
echo "{" >> policy/policy.script
echo "  \"type\": \"all\"," >> policy/policy.script 
echo "  \"scripts\":" >> policy/policy.script 
echo "  [" >> policy/policy.script 
echo "   {" >> policy/policy.script 
echo "     \"type\": \"before\"," >> policy/policy.script 
echo "     \"slot\": $(expr $(cardano-cli query tip --mainnet | jq .slot) + 10000)" >> policy/policy.script
echo "   }," >> policy/policy.script 
echo "   {" >> policy/policy.script
echo "     \"type\": \"sig\"," >> policy/policy.script 
echo "     \"keyHash\": \"$(cardano-cli address key-hash --payment-verification-key-file policy/policy.vkey)\"" >> policy/policy.script 
echo "   }" >> policy/policy.script
echo "  ]" >> policy/policy.script 
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
export txhash="9a326db1e2c65b56bbfd76014acaf727f783ed251e1d986c12deb7fe4302b447"
export txix=0
export funds="5000000"
export policyid=$(cat policy/policyID)
export tokenname="ENSO"
export tokenamount="100000000"
export fee="0"
export output="0"
export slotnumber=$(cardano-cli query tip --mainnet | jq .slot)
export address=addr1qyryskes59f2mwqtzes6mpwtc6lj48l4q3ft08gxmvtnjfadzyzjrxf4d47e00rnwmjmlrkx95czvwa369spk72cvwtqp53adl
export ipfs_hash="QmPRayXKgC4zX8L3NXpX3nZVgtMPj4SnWHVbkwdjMb64t2"
```

## Metadata file
```bash
touch metadata.json
```
```bash
echo "{" >> metadata.json
echo "  \"721\": {" >> metadata.json 
echo "    \"$(cat policy/policyID)\": {" >> metadata.json 
echo "      \"$(echo $tokenname)\": {" >> metadata.json
echo "        \"description\": \"ENSO is the token related to the Karma blockchain foundation.\"," >> metadata.json
echo "        \"name\": \"Karma blockchain foundation\"," >> metadata.json
echo "        \"id\": \"1\"," >> metadata.json
echo "        \"image\": \"ipfs://$(echo $ipfs_hash)\"" >> metadata.json
echo "      }" >> metadata.json
echo "    }" >> metadata.json 
echo "  }" >> metadata.json 
echo "}" >> metadata.json
```

## Variable verification
```bash
 echo $fee
 echo $address
 echo $output
 echo $tokenamount
 echo $policyid
 echo $tokenname
 echo $slotnumber
 echo $script
```

## Raw transaction
```bash
cardano-cli transaction build \
 --mainnet \
 --alonzo-era \
 --tx-in $txhash#$txix \
 --tx-out $address+$output+"$tokenamount $policyid.$tokenname" \
 --change-address $address \
 --mint="$tokenamount $policyid.$tokenname" \
 --minting-script-file policy/policy.script \
 --metadata-json-file metadata.json  \
 --invalid-hereafter $slotnumber \
 --witness-override 2 \
 --out-file matx.raw

export fee=$(cardano-cli transaction calculate-min-fee --tx-body-file matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 --mainnet --protocol-params-file protocol.json | cut -d " " -f1)
```

## Sign
```bash
cardano-cli transaction sign  \
 --signing-key-file payment.skey  \
 --signing-key-file policy/policy.skey  \
 --mainnet --tx-body-file matx.raw  \
 --out-file matx.signed
```

## Submit

```bash
cardano-cli transaction submit --tx-file matx.signed --mainnet
```

## 4. **Delivery the NFT**

```bash
 cardano-cli transaction build-raw \
--fee $fee  \
--tx-in $txhash#0  \
--tx-in $txhash#1  \
--tx-out $address+$output+"$tokenamount $policyid.$tokenname" \
--out-file matx.raw
```
```bash
# TESTNET
export fee=$(cardano-cli transaction calculate-min-fee --tx-body-file matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 --testnet-magic=$magicnumber --protocol-params-file protocol.json | cut -d " " -f1)

#MAINNET
export fee=$(cardano-cli transaction calculate-min-fee --tx-body-file matx.raw --tx-in-count 1 --tx-out-count 1 --witness-count 1 --mainnet --protocol-params-file protocol.json | cut -d " " -f1)
```

```bash
cardano-cli transaction sign  \
 --signing-key-file payment.skey  \
 --mainnet --tx-body-file matx.raw  \
 --out-file matx.signed
```
```bash
  cardano-cli transaction submit --tx-file matx.signed --mainnet
```
## Fees calculation 


## ADA output calculation
```bash
export output=$(expr $funds - $fee)
```

## Special thanks to this tutorial 
[ADA MakerSpace](https://www.youtube.com/watch?v=rhAgBLJnwP0) <br>
[Cardano Dev Portal](https://developers.cardano.org/docs/native-tokens/minting-nfts/)