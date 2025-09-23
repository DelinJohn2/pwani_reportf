
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def opportunity_matrix_creator(intelligence,brand):
    """Return a matplotlib Figure for the Partner Opportunity Matrix with dynamic colors."""
    

    df = pd.read_csv(io.StringIO(intelligence['target_partner']))
    
    df['Revenue_M'] = df['total_revenue'] / 1_000_000  # Convert revenue to millions
    df['Size'] = df['average_value_share'] * 50  # Bubble size scale

    # Create color palette dynamically
    unique_partners = df['MT_PARTNER'].unique()
    palette = sns.color_palette("tab10", n_colors=len(unique_partners))
    color_map = dict(zip(unique_partners, palette))
    df['Color'] = df['MT_PARTNER'].map(color_map)

    # Seaborn theme
    sns.set_theme(style="whitegrid")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(
        df['Revenue_M'], df['average_ws_score'],
        s=df['Size'], c=df['Color'],
        alpha=0.6, edgecolors='black', linewidth=1
    )

    # Add partner labels
    for _, row in df.iterrows():
        ax.annotate(
        row['MT_PARTNER'],
        (row['Revenue_M'], row['average_ws_score']),
        xytext=(5, 5),
        textcoords='offset points',
        fontsize=9,
        fontweight='bold',
        color='black'
    )

    # Add quadrant lines
    ax.axhline(y=70, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=df['Revenue_M'].mean(), color='gray', linestyle='--', alpha=0.5)

    # Quadrant labels
    quadrant_texts = [
        (0.02, 0.98, 'HIGH OPPORTUNITY\nLOW REVENUE', 'top', 'left'),
        (0.98, 0.98, 'HIGH OPPORTUNITY\nHIGH REVENUE', 'top', 'right'),
        (0.02, 0.02, 'LOW OPPORTUNITY\nLOW REVENUE', 'bottom', 'left'),
        (0.98, 0.02, 'LOW OPPORTUNITY\nHIGH REVENUE', 'bottom', 'right')
    ]
    for x, y, text, va, ha in quadrant_texts:
        for x, y, text, va, ha in quadrant_texts:
                ax.text(
                        x, y, text,
                        transform=ax.transAxes,
                        verticalalignment=va,
                        horizontalalignment=ha,
                        fontsize=9,
                        color='gray',
                        alpha=0.3,        # More transparent
                        weight='normal'   # Lighter font weight
                )

    # Axis labels & title
    ax.set_xlabel('Current Revenue (KES Millions)', fontsize=12)
    ax.set_ylabel('White Space Score', fontsize=12)
    ax.set_title(f'{brand} - Partner Opportunity Matrix', fontsize=14, fontweight='bold')

    # Bubble size legend
    for size in [10, 20, 30]:
        ax.scatter([], [], s=size*50, c='gray', alpha=0.6, edgecolors='black',
                   label=f'{size}% Value Share')
    ax.legend(scatterpoints=1, frameon=True, labelspacing=1, loc='center left',
              bbox_to_anchor=(1, 0.5))
    
    plt.close(fig)

    return fig
