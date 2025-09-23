import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns





def geographic_heatmap_creator(data):
    data=data['geographic_heatmap']
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.rename('sub_county', inplace=True)
    df.reset_index(inplace=True)
    df['current_revenue'] = df['current_revenue'] / 1000000
    df['priority_rank'] = df['priority_rank']
    df['white_space'] = df['white_space'] / 10

    top_data = df.sort_values('white_space', ascending=False)[
        ['current_revenue', 'market_share', 'white_space', "priority_rank", 'sub_county']
    ]

    # Rename columns for display
    rename_map = {
        'current_revenue': 'Revenue × 1,000,000',
        'market_share': 'Market Share',
        'white_space': 'White Space × 10',
        'priority_rank': 'Competition'
    }
    top_data = top_data.rename(columns=rename_map)

    # Reshape data for heatmap
    heatmap_data = top_data.set_index('sub_county')

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        heatmap_data,
        annot=True,           # show values on cells
        fmt=".2f",            # 2 decimal places
        cmap="RdYlGn_r",      # color palette
        linewidths=0.5,       # cell borders
        cbar_kws={'label': 'Value'},
        ax=ax
    )

    ax.set_title("Top 5 Counties by White Space - Metric Heatmap", fontsize=14)
    ax.set_xlabel("Metrics")
    ax.set_ylabel("Sub County")
    fig.tight_layout()
    plt.close(fig)

    return fig