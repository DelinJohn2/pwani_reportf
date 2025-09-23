import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
import io

def competitive_chart_creator(result,brand):
    """Return a matplotlib Figure showing competitive landscape for a brand with consistent colors."""
    
    columns = ['average_value_share', 'BRAND']


    b_df = pd.read_csv(io.StringIO(result['overall_conclusion']))[columns]
    c_df = (
        pd.read_csv(io.StringIO(result['external_competition']))
        .sort_values('average_value_share', ascending=False)
        .reset_index(drop=True)[columns]
    )

    base_row = pd.DataFrame({
        "BRAND": ["Base (mean)"],
        "average_value_share": [b_df['average_value_share'].mean()]
    })

    top_4 = c_df.iloc[:4]

    others_row = pd.DataFrame({
        "BRAND": ["Others"],
        "average_value_share": round(c_df.iloc[4:]['average_value_share'].mean(), 4)
    })

    new_data = pd.concat([b_df, top_4, others_row], ignore_index=True)

   

    bar_data = new_data.sort_values(by='average_value_share', ascending=False)

    brands_list = new_data['BRAND'].tolist()
    palette = sns.color_palette("Set2", n_colors=len(brands_list))
    color_map = dict(zip(brands_list, palette))

    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle(f'{brand} - Competitive Landscape', fontsize=16, fontweight='bold')

    # Pie chart
    ax1.pie(
        new_data['average_value_share'],
        labels=new_data['BRAND'],
        autopct='%1.1f%%',
        startangle=90,
        colors=[color_map[b] for b in new_data['BRAND']]
    )
    ax1.set_title('Value Share Distribution')

    # Wrap brand names for barplot to avoid overlap
    wrapped_labels = [
        "\n".join(textwrap.wrap(label, width=10)) for label in bar_data['BRAND']
    ]

    sns.barplot(
        data=bar_data,
        x='BRAND', y='average_value_share',
        hue='BRAND',
        palette=color_map,
        dodge=False,
        ax=ax2,
        legend=False
    )
    ax2.set_title('Value Share Comparison')
    ax2.set_ylabel('Value Share (%)')

    # Replace labels with wrapped ones
    ax2.set_xticklabels(wrapped_labels, rotation=30, ha='right')

    # Add percentage annotations
    for p in ax2.patches:
        ax2.annotate(f'{p.get_height():.1f}%',
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom')

    fig.tight_layout()
    fig.subplots_adjust(top=0.88)
    plt.close(fig)

    return fig