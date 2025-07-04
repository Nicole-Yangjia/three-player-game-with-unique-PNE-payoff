# three-player-game-with-unique-PNE-payoff
# Code Repository: Discovering Theorems in Game Theory  
**Article Title**: Discovering Theorems in Game Theory: The Nash Equilibrium in a Three-Person Game is Unique  

This repository contains code for generating and analyzing three-player game matrices to verify uniqueness conditions of Nash equilibrium payoffs, as presented in the associated article.

## Code Execution Pipeline  
Follow these steps sequentially to reproduce the full analysis:

1. **Generate Combinations**  
   ```bash
   python generate.py
2.Check for Pure Nash Equilibrium (PNE) existence
   python havePNE.py
3.Complete symmetric payoff generation (adds x2/y2/z2 strategies)
   python sy_generate.py
4.Verify unique PNE payoffs
   python uni_payoff.py
5.Generate human-readable results
   python final_output.py

##Testing Specific Conditions
To check if a random combination satisfies unique PNE payoff conditions:
   ```bash
   python test.py


