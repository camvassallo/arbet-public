# NOTA Sports
• Django Web3 application combining fantasy sports and online sportsbooks, built on the Ethereum blockchain. Utilizes DALL-E-2 (artwork), The Odds API (live odds and scores), and a Moralis Dapp
• Enables users to purchase digital assets (ERC-721 Tokens) representing their favorite sports team
• Market values are correlated to the efficiency of the team's real-life performances against the spread

# Todo
- Add User - login/logout/register functionality (DONE)
- Create bet from sportsbook screen (DONE)
- Attach bet to user object (DONE)
- Get result of bet / live score (if available)
- Add bet to user's bet history (DONE)
- If user wins bet, display pack/nft image in user's account
- Add scores (DONE)
- Setup DALLE API (DONE)
- Add balance updating and deposits (DONE)
- Change bets to subtract from balance (DONE)
- Add gallery
- Add redeem pack button (view NFT in gallery)
- Link Minting API to gallery
- Add liquidation feature to NFT
- Add support for other Sports
- Update left menu in sportsbook
- Tweak UI for mobile user experience
- Add team logos and more graphics in general
- LOTS OF DEBUG sessions :)

# Ideas for Mint
- always store every bet
- add field in bet called "mint-status"
- if bet wins and mint-status is "pending", link to mint page
- if mint-status is "minted", then show link to token
- if mint-status is "liquidated", then show "liquidated", and link to

- # second thoughts:
- still store every bet
- add a one-to-one key from bet to a token model
- create token if bet wins and display link to token
- token has image (get from game), balance (get from bet), and mint-status (either "pending", "minted", or "liquidated")