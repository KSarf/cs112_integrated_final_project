# Grid Analysis Findings and Limitations

## Network Summary

- Number of substations: **44**
- Number of transmission/distribution lines: **55**
- Connected components: **3**
- Average clustering coefficient: **0.367**
- Global network efficiency: **0.244**

## Centrality

The highest-betweenness substation in this synthetic network is
**Cape Coast Substation**.

Its calculated betweenness centrality is
**0.525**.

High betweenness means the node lies on many shortest paths in the graph.
For this coursework this can be interpreted as a structural indicator of
network importance, but it does not directly measure electrical loading.

## N-1 Node Analysis

**17** of **44** individual substation removals
increased the number of connected components.

## N-1 Line Analysis

**21** of **55** individual line removals
increased the number of connected components.

## Geographical Analysis

Substation latitude and longitude values are used to display the synthetic
network geographically. Regional comparisons can help identify where grid
assets and high-capacity substations are concentrated.

## Important Limitations

This analysis is a graph-based educational approximation.

It does **not** perform:

- AC or DC power-flow analysis
- Voltage-stability analysis
- Protection-coordination studies
- Frequency-stability studies
- Real-time load analysis
- Security-constrained contingency analysis

Centrality and N-1 graph fragmentation are therefore structural reliability
proxies only. They should not be presented as evidence that a real electrical
network is safe or operationally secure.
