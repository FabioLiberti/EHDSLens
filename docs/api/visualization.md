# Visualization API Reference

## EHDSVisualizer

Create charts and diagrams from study data.

```python
from ehdslens.visualization import EHDSVisualizer
```

### Constructor

```python
viz = EHDSVisualizer(database: StudyDatabase)
```

### Methods

#### create_prisma_diagram_data()

Get data for PRISMA 2020 flow diagram.

**Returns:** Dictionary with identification, screening, eligibility, and included counts.

```python
prisma = viz.create_prisma_diagram_data()

print(prisma['identification']['total_database'])  # 847
print(prisma['screening']['duplicates_removed'])   # 234
print(prisma['included']['total'])                 # 52
```

#### create_year_distribution_chart(format)

Create year distribution chart.

**Parameters:**
- `format`: "ascii", "data", or "plotly"

```python
# ASCII chart
print(viz.create_year_distribution_chart(format="ascii"))

# Raw data
data = viz.create_year_distribution_chart(format="data")
# Returns: {2020: 5, 2021: 8, 2022: 10, ...}
```

#### create_axis_distribution_chart(format)

Create thematic axis distribution chart.

**Parameters:**
- `format`: "ascii", "data", or "plotly"

```python
data = viz.create_axis_distribution_chart(format="data")
# Returns: {'governance_rights_ethics': 15, ...}
```

#### create_quality_distribution_chart(format)

Create quality rating distribution chart.

**Parameters:**
- `format`: "ascii", "data", or "plotly"

```python
data = viz.create_quality_distribution_chart(format="data")
# Returns: {'high': 18, 'moderate': 20, 'low': 8, 'not_applicable': 6}
```

#### export_for_plotly(path)

Export all chart data to JSON for Plotly.

```python
from pathlib import Path
viz.export_for_plotly(Path("chart_data.json"))
```

#### export_for_latex(path)

Export data formatted for LaTeX/TikZ.

```python
viz.export_for_latex(Path("chart_data.tex"))
```

### Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `"ascii"` | Text-based chart | Terminal, logs |
| `"data"` | Raw dictionary | Matplotlib, Plotly |
| `"plotly"` | Plotly figure | Interactive web |
