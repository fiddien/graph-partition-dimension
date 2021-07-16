# graph-partition-dimension

Working with not-so-easy graphs is challenging. Determining its partition dimension is even more challenging.

In my undergraduate thesis, I studied the generalization of strong product graphs, that is k-strong product graphs, with focusing on 2-strong one. The "k-strong edges" stratched my head because it was hard to visualize. In addition to that, the work of labeling every vertexes with the corresponding representation in respect of a certain partition was taking my focus from actual analysis. So my hand itched and create this program in python.

Before creating the GUI program, I was tweaking around the functions in notebook. Here's a view of the sample notebook I provided in this repo:
![notebook](/screenshots/program_1_notebook.png)

Then I used the functions to create a GUI program with PyQt5. Here's how it looks like:
![gui](/screenshots/program_2_gui.png)

## What you can do with this program
- Visualize two graphs from some common classes of graph. We call them graph G and graph H.
  - currently added: path, cycle, complete, complete bipartite
- Visualize a product graph from graph G and graph H, we call them graph P.
  - currently added: cartesian product, k-strong product
- Find a minimum resolving partition from these three graphs with naive approach. Beware that for graph with more than 13 vertices, it will take a significantly longer time to compute.

## Running the script
I haven't managed to produce an executable file succesfully. So you have to set up your own python environment to run this program.

1. Install Python version 3.6 or newer.

2. Open the terminal. Clone this repo. Make sure your system has Git installed.
```
git clone https://github.com/ilmaaliyaf/graph-partition-dimension.git
```
Another option is by extract downloaded zip file of this repo (click the green "Code" button above).

3. Navigate to the `graph-partition-dimension` folder. Install all required packages.
```
cd graph-partition-dimension
pip install -r "requirements.txt"
```

4. Run the script.
```
python main.py
```
or
```
python3 main.py
```

## Possible futher development
- add the option to find metric dimension of the graphs

## License
MIT
