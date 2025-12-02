# Unique PNE payoffs in 3-player game
**Article Title**: Discovering three-player games with unique pure Nash equilibrium payoffs


This repository contains code for generating and analyzing three-player game matrices to verify uniqueness conditions of Nash equilibrium payoffs, as presented in the associated article.

## Generate the sentences to be verified
 ```bash
   python gene_omega.py
   ```
## Single-File Execution  

   Run the entire analysis pipeline with one command:
   ```bash
   python PNEpayoff.py
   ```
## Pipeline Stages  

The script executes these steps sequentially:  

1. **Check PNE Existence**  
   - *Action*: Filters rules that admit at least one Pure Nash Equilibrium  
   - *Input*: `generate_combination_sat.csv`  
   - *Outputs*:  
     - `havePNE.csv` (rules with ≥1 PNE)  


2. **Verify Unique PNE Payoffs**  
   - *Action*: Identifies rules with unique PNE in symmetric games  
   - *Input*: `havePNE.csv`  
   - *Outputs*:  
     - `uniqueUNE.csv` (rules with exactly unique PNEs payoff)  
     - `failUNE.csv` (rules with multiple/non-unique PNEs payoff)

   
## Testing Specific Conditions
To check if a random combination satisfies unique PNE payoff conditions:
   ```bash
   python test.py
   ```


