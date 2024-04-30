# SpellCast Solver
An application for the Discord Game SpellCast. Spellcast is very similar to Boggle, where you try to find the best word possible

I saw some existing solutions out there and wanted to make a faster and cleaner solution. My application can support up to 4 substitions within a minute. 

![image](https://github.com/AllanKoder/SpellCastSolver/assets/74692833/decd5829-2dc3-41b7-b8ad-1de6b02c21b9)

_blue tile is the start of the word_

_red tile is a tile that needs to be substituted_


### Speed Improvements 

Using a heap and priority prefix tree, where prefixes that lead to a higher word at the leaf are prioritized more, we can navigate through all the best words first. Afterwards, we will reach a point where the word in the heap, even with the double word multiplier and triple letter bonus, cannot beat the existing best solution. This is where we can halt.

![early stopping  (for real)](https://github.com/AllanKoder/SpellCastSolver/assets/74692833/b1e08a64-6958-4030-b45a-e8c301164ae9)

In this diagram, we have a example of early stopping. There can be other heuristics added to this, where if we reach too small of a slope, we can stop the search.

### How to run:
**For Backend:**
```
cd spellCastSolverBackend
py -m uvicorn main:app
```
**For Frontend:**
```
cd spellCastUI
npm run dev
```

### Features:
- up to 4 substitions
- fast
- clean and easy UI


### Potential Improvements:
- Using Monte Carlo for determining if shuffle is optimal
- Accounting for gems and optimal gem collection
