# three-player-game-with-unique-PNE-payoff
# Code Repository: Discovering Theorems in Game Theory  
**Article Title**: Discovering Theorems in Game Theory: The Nash Equilibrium in a Three-Person Game is Unique  

This repository contains code for generating and analyzing three-player game matrices to verify uniqueness conditions of Nash equilibrium payoffs, as presented in the associated article.

## Single-File Execution  

   Run the entire analysis pipeline with one command:
   ```bash
   python PNEpayoff.py
   ```
## Pipeline Stages  

The script executes these steps sequentially:  

1. **Generate Combinations**
   
   Creates all possible rule combinations and saves to generate_combination.csv
   
2. **Check for Pure Nash Equilibrium (PNE) existence**
   
  Filters rules that admit at least one Pure Nash Equilibrium

  Outputs: havePNE.csv (satisfiable) and noPNE.csv (unsatisfiable)
  
3. **Complete symmetric payoff generation (adds x2/y2/z2 strategies)**
   
   Generates symmetric payoff rules (adds x2/y2/z2 strategies)
   
   Output: sy_generate_combination.csv
   
4. **Verify unique PNE payoffs**
   
   Identifies rules with unique PNE in symmetric games
   
   Outputs: unique_PNE_payoff.csv (unique) and no_unique_PNE_payoff.csv (non-unique)
   
5. **Generate human-readable results**
   
   Processes rules into interpretable condition formats
   
   Output: conditions_unique_PNE_payoff.csv
   
## Testing Specific Conditions
To check if a random combination satisfies unique PNE payoff conditions:
   ```bash
   python test.py
   ```


