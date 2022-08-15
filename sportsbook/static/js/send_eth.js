var accounts = []
var betAmtLock = 0;

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
    console.log(accounts);
}

function wait(ms){
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

async function placeBet() {
    var betAmountEth = document.getElementById('bet-input').value.toString(16);
    var betAmountWei = betAmountEth * (10 ** 18);
    betAmtLock = betAmountWei;

    let params = [{
        "from": accounts[0],
        "to": "0xB16F8A2c9F9e126A59aF3107304E14584f6aDd96",
        "value": betAmountWei.toString(16),
    }]

    let result = await window.ethereum.request({method: "eth_sendTransaction", params}).catch(console.error);
    console.log(result)

    console.log("sleeping 30 sec");
    wait(30000);

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
              wait(15000);

              xhr.send();
              response = xhr.responseText
          }
          var json = JSON.parse(response);
          if (json.to_address == "0xb16f8a2c9f9e126a59af3107304e14584f6add96") {
            document.getElementById("betVal").value = json.value;
            document.forms['lock-bet'].submit();
          }
       }};

    xhr.send();
}

