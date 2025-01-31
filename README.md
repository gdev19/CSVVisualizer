# CSV/Excel Visualizer

This is a simple tool to visualize CSV and Excel files. It is built using [Dash](https://dash.plotly.com/), a Python framework for building analytical web applications.

Application is deployed at [codeff.nl](https://www.codeff.nl/apps/csv).

## Features

- Upload CSV or simple Excel file
- It accepts Drag & Drop as well
- Application will automatically extract column names and display them in a dropdowns
- Select columns to visualize (X and Y axis)
- Select chart type (Scatter, Line)
- It has a built in world population dataset to play with taken from https://data.worldbank.org/

## Future work

- Input for specifying delimiter for CSV files
- Enhance the application to work with more complex Excel files

## Installation

For running application locally

```
uv run csv_visualizer.py
```

### Pre-commit

This project uses pre-commit hooks. To install pre-commit, run the following command

```
uv run pre-commit install
```

## Contributing

Feel free to contribute to this project. You can fork the repository and submit a pull request.
