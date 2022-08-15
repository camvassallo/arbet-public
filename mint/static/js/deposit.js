var accounts = []
var depositAmtLock = 0;

window.onload = function() {
    connectWallet()
    if (window.ethereum !== "undefined") {
        this.ethereum.on("accountsChanged", handleAccountsChanged)
    }
}

const handleAccountsChanged = (a) => {
    console.log("accounts changed")
    accounts = a
}

async function connectWallet() {
    accounts = await window.ethereum.request({method: 'eth_requestAccounts',}).catch(console.error);
    console.log("Wallet Address: " + accounts);
}

function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

async function deposit() {
    document.getElementById("place-bet-button").setAttribute("disabled","")
    var depositAmountEth = document.getElementById('deposit-amount').value.toString(16);
    var depositAmountWei = depositAmountEth * (10 ** 18);
    depositAmtLock = depositAmountWei;

    let params = [{
        "from": accounts[0],
        "to": "0xB16F8A2c9F9e126A59aF3107304E14584f6aDd96",
        "value": depositAmountWei.toString(16),
    }]

    let result = await window.ethereum.request({method: "eth_sendTransaction", params}).catch(console.error);
    console.log(result)

    if (result != undefined) {
        document.getElementById("progress").style.display = "block"
        document.getElementById("etherscan").setAttribute("href", "https://rinkeby.etherscan.io/tx/" + result)
        window.setTimeout(() => {

        var url = "https://deep-index.moralis.io/api/v2/transaction/" + result + "?chain=rinkeby";

        var xhr = new XMLHttpRequest();
        xhr.open("GET", url);

        xhr.setRequestHeader("accept", "application/json");
        xhr.setRequestHeader("X-API-Key", "LZX9u5BLEeqaTFUaoYbAFX41dmlmhXu4YFlg6dbKuQV1OxOSk3lURLA2cS3dVbwB");

        xhr.onreadystatechange = function () {
           if (xhr.readyState === 4) {
              console.log(xhr.status);
              console.log(xhr.responseText);

              var response = xhr.responseText

              while (xhr.status == 200 && response == "") {
                  console.log('awaiting transaction validation, checking again in 15 seconds')
                  window.setTimeout(() => {

                  xhr.send();
                  response = xhr.responseText
                  }, 15000);

              }
              var json = JSON.parse(response);
              if (json.to_address == "0xb16f8a2c9f9e126a59af3107304e14584f6add96") {
                document.getElementById("depositVal").value = json.value;
                document.forms['deposit'].submit();
              }
           }};

        xhr.send();
        }, 30000);
    } else {
        document.getElementById("error").style.display = "block"
    }
}

