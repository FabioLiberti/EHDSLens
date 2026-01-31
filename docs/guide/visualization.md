# Visualization

Create charts and diagrams from the EHDS systematic review data.

## Setup

```python
from ehdslens import EHDSAnalyzer
from ehdslens.visualization import EHDSVisualizer

analyzer = EHDSAnalyzer()
analyzer.load_default_data()

viz = EHDSVisualizer(analyzer.db)
```

## PRISMA Flow Diagram

Get data for creating a PRISMA 2020 flow diagram:

```python
prisma = viz.create_prisma_diagram_data()

print(f"Records identified: {prisma['identification']['total_database']}")
print(f"Duplicates removed: {prisma['screening']['duplicates_removed']}")
print(f"Studies included: {prisma['included']['total']}")
```

## ASCII Charts

Terminal-friendly visualizations:

```python
# Year distribution
print(viz.create_year_distribution_chart(format="ascii"))

# Axis distribution
print(viz.create_axis_distribution_chart(format="ascii"))

# Quality distribution
print(viz.create_quality_distribution_chart(format="ascii"))
```

## Chart Data for External Tools

Export data for matplotlib, plotly, or other tools:

```python
# Get raw data
year_data = viz.create_year_distribution_chart(format="data")
axis_data = viz.create_axis_distribution_chart(format="data")
quality_data = viz.create_quality_distribution_chart(format="data")
```

## Matplotlib Examples

```python
import matplotlib.pyplot as plt

year_data = viz.create_year_distribution_chart(format="data")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(year_data.keys(), year_data.values(), color='steelblue')
ax.set_xlabel('Year')
ax.set_ylabel('Studies')
ax.set_title('Publications by Year')
plt.show()
```

## Plotly Examples

```python
import plotly.express as px

year_data = viz.create_year_distribution_chart(format="data")

fig = px.bar(
    x=list(year_data.keys()),
    y=list(year_data.values()),
    labels={'x': 'Year', 'y': 'Studies'},
    title='EHDS Studies by Year'
)
fig.show()
```

## Export for External Tools

```python
from pathlib import Path

# Export to JSON for Plotly
viz.export_for_plotly(Path("chart_data.json"))
```

## LaTeX/TikZ Export

Generate data formatted for LaTeX documents:

```python
axis_data = viz.create_axis_distribution_chart(format="data")

print(r"\begin{tabular}{lc}")
print(r"\toprule")
print(r"Thematic Axis & Studies \\")
print(r"\midrule")
for axis, count in axis_data.items():
    print(f"{axis} & {count} \\\\")
print(r"\bottomrule")
print(r"\end{tabular}")
```
