Moralis.initialize("7a18RZTQDbcHe3wlXP83d9xazxQkbtpjhlembc9a"); // Application id from moralis.io
Moralis.serverURL = "https://z3o4spngnema.usemoralis.com:2053/server"; //Server url from moralis.io

const nft_contract_address = "0x0Fb6EF3505b9c52Ed39595433a21aF9B5FCc4431" //NFT Minting Contract Use This One "Batteries Included", code of this contract is in the github repository under contract_base for your reference.
/*
Available deployed contracts
Ethereum Rinkeby 0x0Fb6EF3505b9c52Ed39595433a21aF9B5FCc4431
Polygon Mumbai 0x351bbee7C6E9268A1BF741B098448477E08A0a53
BSC Testnet 0x88624DD1c725C6A95E223170fa99ddB22E1C6DDD
*/

const web3 = new Web3(window.ethereum);

//frontend logic

async function mint_token(){
    await login();
    const metadata = {
        "name":document.getElementById("name").innerHTML,
        "description":document.getElementById("description").innerHTML,
        "image":document.getElementById("art").src
        }
        console.log(metadata);
        const metadataFile = new Moralis.File("metadata.json", {base64 : btoa(JSON.stringify(metadata))});
        await metadataFile.saveIPFS();
        const metadataURI = metadataFile.ipfs();
        const txt = await mintToken(metadataURI)
        console.log(txt);
//        Add delay to confirm the transaction, get token id from the transaction hash, generate opensea link
        document.getElementById("opensea-link").setAttribute("href", "https://testnets.opensea.io/assets/rinkeby/" + txt);
        document.forms['mint'].submit();
}

async function login() {
  let user = Moralis.User.current();
  if (!user) {
    user = await Moralis.authenticate({
      signingMessage: "Log in using Moralis",
    })
      .then(function (user) {
        console.log("logged in user:", user);
        console.log(user.get("ethAddress"));
      })
      .catch(function (error) {
        console.log(error);
      });
  }
}

async function mintToken(_uri){
  const encodedFunction = web3.eth.abi.encodeFunctionCall({
    name: "mintToken",
    type: "function",
    inputs: [{
      type: 'string',
      name: 'tokenURI'
      }]
  }, [_uri]);

  const transactionParameters = {
    to: nft_contract_address,
    from: ethereum.selectedAddress,
    data: encodedFunction
  };
  const txt = await ethereum.request({
    method: 'eth_sendTransaction',
    params: [transactionParameters]
  });
  return txt
}
