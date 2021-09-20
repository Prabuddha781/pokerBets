# pokerBets
A user-intuitive game where players can bet on multiple hands of poker at different stage of the game.

FYI:
users - the human playing the game - most likely you 
players - the two players in the table

- The flow of the game:
1. Betting round 1: The cards are hidden and users can bet on either player (there are two players on the table). The odds initially are 1 to 1.
2. Betting round 2: The hole cards are dealt and the odds are shown. Odds are approximate at this point because of the amount of time brute forcing 48C5 combination 
takes. (If you want to see why it is an approximate, go to the preFlopChecker.py file and read the comment.) 
3. Betting round 3: The flop is shown and users can bet again on players. Odds are precise at this point but modified slightly from the original odds. It is the 
users' job to identify this discrepancy. Bet for inflated odds and against inflated odds.
...
After the river, the cards are shown and the result is displayed.

- The most difficult challenge (anyone wants to solve it is more than welcome to):
Challenge 1: Brute Forcing efficiently to calculate pre-flop odds. Or maybe there is a non-brute force way you could think of. I have used a hack for preFlop
adds which is almost similar to what this guy/girl here wrote --> link (https://www.cardplayer.com/poker-tools/odds-and-outs#:~:text=Odds%20of%20two,73.3%25%20vs.%2026.7%25)

Challenges:
- Can you write more efficient ways to check the rank of the cards? I used an algorithm that scores the cards. Maybe there is something different.
- How would you organize the main gui class if you wrote it from the scratch? I crammed everything under a single class and the instances are quite packed imo.

Let me know how the design of the program is. It is simple and beautiful in my opinion.
