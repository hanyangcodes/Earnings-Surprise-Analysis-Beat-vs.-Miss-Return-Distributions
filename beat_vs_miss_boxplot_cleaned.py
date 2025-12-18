
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Placeholder: Replace with actual DataFrame loading
# df = pd.read_csv("your_data.csv")

# Define these variables appropriately
plotly_template = 'plotly_white'
return_columns = ['Return1', 'Return2', 'Return3', 'Return4', 'Return5']  # Replace with your actual column names

def remove_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col].isna()) | ((df[col] >= lower_bound) & (df[col] <= upper_bound))]

# Clean the data by removing outliers
df_clean = df.copy()
for col in return_columns:
    df_clean = remove_outliers_iqr(df_clean, col)

# Filter Beat and Miss
df_beat_clean = df_clean[df_clean['Beat'] == 1]
df_miss_clean = df_clean[df_clean['Miss'] == 1]

# Create subplots
fig = make_subplots(
    rows=len(return_columns), cols=1,
    subplot_titles=return_columns,
    vertical_spacing=0.1
)

for i, col in enumerate(return_columns, start=1):
    fig.add_trace(
        go.Box(
            y=df_beat_clean[col],
            name='Beat',
            marker_color='blue',
            boxmean=True,
            boxpoints=False
        ),
        row=i, col=1
    )
    fig.add_trace(
        go.Box(
            y=df_miss_clean[col],
            name='Miss',
            marker_color='red',
            boxmean=True,
            boxpoints=False
        ),
        row=i, col=1
    )
    fig.update_xaxes(
        tickvals=['Beat', 'Miss'],
        row=i, col=1
    )

fig.update_layout(
    template=plotly_template,
    height=3000,
    width=600,
    title_text="Beat vs Miss Distributions (Cleaned)",
    showlegend=False
)

fig.show()
