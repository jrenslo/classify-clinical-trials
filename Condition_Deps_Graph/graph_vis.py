#!/usr/bin/python

import graphviz
import pandas as pd
import json

with open('NEW_clinical_trial_data.json', 'r') as f:
    data = json.load(f)

conds = set()

cond_clus_pairs = set()

j = 0

for i in data:
    for cond in data[i]['conditions']:
        conds |= set(str(cond['slug']))
        pairs = set((str(cond['slug']),
                                str(i)) for i in cond['clusters'])
        cond_clus_pairs |= pairs
df = pd.DataFrame(list(cond_clus_pairs), columns = ['Condition','Cluster'])

# drop any row that does not have a repeated condition
conds = df['Condition'].value_counts()[
    df['Condition'].value_counts() > 1].index.values

to_plot = df.loc[df['Condition'].isin(conds),:]


# graphviz
def graphviz_plot():
    d = graphviz.Digraph('mygraph',engine='fdp', format='svg',
                       graph_attr={#'mode':'KK',
                             'overlap':'100:false',
                             #'pack':'True',
                            'sep':'0'})
    # engine: osage, sfdp, neato, dot
    # overlap: ortho, orthoxy, scalexy,

    nodes = set()

    for i,row in to_plot.iterrows():
        if str(row['Condition']) not in nodes:
            d.node(str(row['Condition']), margin='0.01,0.01')
        if str(row['Cluster']) not in nodes:
            d.node(str(row['Cluster']), penwidth='4.0',color='blue', shape='box', margin='0.1,0.1')
        nodes |= set((str(row['Condition']), str(row['Cluster'])))
        d.edge(str(row['Condition']), str(row['Cluster']))
    d.render()
    d.save()

# graphviz_plot()

#networkx
import networkx as nx
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
plt.switch_backend('tkagg')

def networkx_plot():
    g = nx.Graph()
    g.add_nodes_from(to_plot['Condition'].unique())
    for cluster in to_plot['Cluster'].unique():
        g.add_node(cluster, nodecolor='blue', shape='box')
    # g.add_nodes_from(to_plot['Cluster'].unique())
    g.add_edges_from(to_plot.values)

    nx.drawing.nx_pylab.draw_kamada_kawai(g, with_labels=True)
    plt.figure()
    nx.drawing.nx_pylab.draw(g, with_labels=True)
    plt.figure()
    nx.drawing.nx_pylab.draw_shell(g, with_labels=True)
    plt.figure()
    nx.drawing.nx_pylab.draw_spring(g, with_labels=True)

    plt.show()


networkx_plot()



