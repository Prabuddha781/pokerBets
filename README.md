# pokerBets
A user-intuitive game where players can bet on multiple hands of poker at different stage of the game.

If you don't know how to use a tkinter file:
- Clone the repo into your desktop.
- Install the packages that are in the requirements.txt. Google how to install python packages if you don't know how.
- Open the gui-final.py file and run it.

FYI:
users - the human playing the game - most likely you 

players - the two players in the table

- The flow of the game:
1. Betting round 1: The cards are hidden and users can bet on either player (there are two players on the table). The odds initially are 1 to 1.
2. Betting round 2: The hole cards are dealt and the odds are shown. Odds are approximate at this point because of the amount of time brute forcing 48C5 combination 
takes. (If you want to see why it is an approximate, go to the preFlopChecker.py file and read the comment.) 
3. Betting round 3: The flop is shown and users can bet again on players. Odds are precise at this point but modified slightly from the original odds. It is the 
users' job to identify this discrepancy. Bet for inflated odds and against deflated odds.
...
After the river, the cards are shown and the result is displayed.

- The most difficult challenge (anyone wants to solve it is more than welcome to):
Challenge 1: Brute Forcing efficiently to calculate pre-flop odds. Or maybe there is a non-brute force way you could think of. I have used a hack for preFlop
odds which is almost similar to what this guy/girl here wrote --> link (https://www.cardplayer.com/poker-tools/odds-and-outs#:~:text=Odds%20of%20two,73.3%25%20vs.%2026.7%25)

Other challenges:
- Can you write more efficient ways to check the rank of the cards? I used an algorithm that scores the cards. Maybe there is a better technique.
- How would you organize the main gui class if you wrote it from the scratch? I crammed everything under a single class and the instances are quite packed.

Let me know how the design of the program is. It is simple and beautiful in my opinion.
Open the screenshots below in a new tab for better visibility.
![image](https://user-images.githubusercontent.com/74695186/143719563-f541a481-e75d-408a-9d3b-ebefd35dcc42.png)
![image](https://user-images.githubusercontent.com/74695186/143719561-dcc52440-a504-4401-af42-7a3f2d55a799.png)
![image](https://user-images.githubusercontent.com/74695186/143719560-fbfa80be-6c96-472b-b7d0-02d7209425f0.png)
![image](https://user-images.githubusercontent.com/74695186/143719559-19a87069-8334-4519-ad36-e566e20b57b1.png)
![image](https://user-images.githubusercontent.com/74695186/143719558-27163dfb-03b6-485b-8252-9bb4d5e1e93a.png)
