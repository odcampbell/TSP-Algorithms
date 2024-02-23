# From Start All:

## Sources:
Debugging and base models for algorithms: OpenAI. (2024). ChatGPT (3.5) [Large language model]. https://chat.openai.com
Faster 2-Opt: https://stackoverflow.com/questions/53275314/2-opt-algorithm-to-solve-the-travelling-salesman-problem-in-python

# Guide to Run tests:

1. ### All (NN, 2opt, 2opt Prime):

Navigate to TSP_Project_Code directory

**Run w/ file:** 

    py run_algos_updated.py Graphs\470_Graphs\g100.graph

**Will Be Given CMD-Line Options:**

    py run_algos_updated.py

**Windows Scripts:**

    run_all.bat

Sends out to TSP_Output

2. ### Individually: 

**Brute Force:** 

py TSP_BruteForce.py
-Hard coded example_distance or manually change to random generated

**Heuristic (2 Opt):** 

py TSP_H.py Graphs\470_Graphs\g100.graph

py TSP_H.py Graphs\470_Graphs\g250.graph

py TSP_H.py Graphs\470_Graphs\g500.graph

py TSP_H.py Graphs\470_Graphs\g1000.graph

py TSP_H.py Graphs\MyGraphs\g500M.txt 


**Heuristic Prime (MST + 2Opt):** 

py TSP_HPrime.py Graphs\470_Graphs\g100.graph

py TSP_HPrime.py Graphs\470_Graphs\g250.graph

py TSP_HPrime.py Graphs\470_Graphs\g500.graph

py TSP_HPrime.py Graphs\470_Graphs\g1000.graph

py TSP_HPrime.py Graphs\MyGraphs\g500M.txt 

**Nearest Neighbor:** 

py TSP_NN.py Graphs\470_Graphs\g100.graph  

py TSP_NN.py Graphs\470_Graphs\g250.graph  

py TSP_NN.py Graphs\470_Graphs\g500.graph  

py TSP_NN.py Graphs\470_Graphs\g1000.graph  

py TSP_NN.py Graphs\MyGraphs\g500M.txt 

**Windows Scripts:** 

run_H.bat
run_HPrime.bat
run_NN.bat

Sends out to TSP_Output

(Alt + z) to format

Either clear file before running or recognize the last out to the file is
from your last run
