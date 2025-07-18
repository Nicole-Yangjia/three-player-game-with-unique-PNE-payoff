# Unique PNE payoffs in 3-player game
**Article Title**: Beyond Duopoly: Computational Discovery on Unique Pure-Strategy Nash Equilibrium Payoffs in Triopoly 

This repository contains code for generating and analyzing three-player game matrices to verify uniqueness conditions of Nash equilibrium payoffs, as presented in the associated article.

## Single-File Execution  

   Run the entire analysis pipeline with one command:
   ```bash
   python PNEpayoff.py
   ```
## Pipeline Stages  

The script executes these steps sequentially:  


1. **Generate Rule Combinations**
   
   - *Action*: Creates all possible rule combinations from predefined option sets
     
   - *Input*: None (generates from internal definitions)
     
   - *Output*: `generate_combination.csv` (all rule combinations)

3. **Check PNE Existence**  
   - *Action*: Filters rules that admit at least one Pure Nash Equilibrium  
   - *Input*: `generate_combination.csv`  
   - *Outputs*:  
     - `havePNE.csv` (rules with ≥1 PNE)  
     - `noPNE.csv` (rules with no PNE)

4. **Create Symmetric Rules**  
   - *Action*: Generates symmetric payoff rules (adds x2/y2/z2 strategies)  
   - *Input*: `havePNE.csv`  
   - *Output*: `sy_generate_combination.csv` (symmetric rules)

5. **Verify Unique PNE Payoffs**  
   - *Action*: Identifies rules with unique PNE in symmetric games  
   - *Input*: `sy_generate_combination.csv`  
   - *Outputs*:  
     - `unique_PNE_payoff.csv` (rules with exactly one PNE)  
     - `no_unique_PNE_payoff.csv` (rules with multiple/non-unique PNE)

6. **Extract Human-Readable Conditions**  
   - *Action*: Processes rules into interpretable condition formats  
   - *Input*: `unique_PNE_payoff.csv`  
   - *Output*: `conditions_unique_PNE_payoff.csv` (final human-readable conditions)
   
## Testing Specific Conditions
To check if a random combination satisfies unique PNE payoff conditions:
   ```bash
   python test.py
   ```


