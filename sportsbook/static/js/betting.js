var bets = new Set()

function addToSlip(e, id, bet_type) {

    betId = id + "_" + bet_type;

    if (bets.has(betId)) {
          const oldBet = document.getElementById(betId);
          oldBet.remove();
          bets.delete(betId)
    }
    else {
      game = games[id];
      console.log(game);

      var bet_team, bet_odds;
      switch (bet_type) {
          case 'away_spread':
              bet_team = game.away_team + " " + game.away_team_spread;
              bet_odds = game.away_team_odds;
              bet_subtext = "SPREAD"
              break;
          case 'away_ml':
              bet_team = game.away_team;
              bet_odds = game.away_team_ml;
              bet_subtext = "MONEYLINE"
              break;
          case 'over_total':
              bet_team = "Over 100";
              bet_odds = "-110";
              bet_subtext = "TOTAL POINTS"
              break;
          case 'home_spread':
              bet_team = game.home_team + " " + game.home_team_spread;
              bet_odds = game.home_team_odds;
              bet_subtext = "SPREAD"
              break;
          case 'home_ml':
              bet_team = game.home_team;
              bet_odds = game.home_team_ml;
              bet_subtext = "MONEYLINE"
              break;
          case 'under_total':
              bet_team = "Under 100";
              bet_odds = "-110";
              bet_subtext = "TOTAL POINTS"
              break;
      }

      var c, r, t;
      panel = document.createElement('div');
      panel.setAttribute("class", "panel-block");
      panel.setAttribute("id", betId);
      t = document.createElement('table');
      t.setAttribute("class", "table");
      t.setAttribute("style", "width:100%; white-space: nowrap;");


      // 1st row, 1st col
      r = t.insertRow(-1);
      c = r.insertCell(0);
      c.innerHTML = bet_team

      // 1st row, 2nd col
      c = r.insertCell(1);
      c.innerHTML = bet_odds
      c.setAttribute("style", "text-align: right;")


      // 2nd row, 1st col
      r = t.insertRow(-1);
      c = r.insertCell(0);
      c.innerHTML = bet_subtext;
      c.setAttribute("style", "font-size: 12px; color:#808080; text-align: left;")

      // 2nd row, 2nd col
      c = r.insertCell(1);
      const d = new Date(game.commence_time);
      c.innerHTML = d.toLocaleString();
      c.setAttribute("style", "font-size: 12px; color:#808080; text-align: right;")

      // 3rd row, 1st col
      r = t.insertRow(-1);
      c = r.insertCell(0);
      c.innerHTML = game.away_team + " @ " + game.home_team;
      c.setAttribute("style", "font-size: 12px; color:#808080; text-align: left;")

      panel.appendChild(t);
      endl = document.createElement('br');
      panel.appendChild(endl);

      document.getElementById("betslip-panel").appendChild(panel);
      bets.add(betId)
    }

    betsString = [...bets].join(',')

    document.getElementById("place-bet-button").setAttribute("onclick", "location.href='/sportsbook/place-bet/" + betsString + "'")
}
