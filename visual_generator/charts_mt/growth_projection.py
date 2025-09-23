import matplotlib.pyplot as plt
import pandas as pd



def growth_projection_creator(data):
    """Create 90-day growth projection chart and return figure object"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    # fig.suptitle(f'{brand} - {data["title"]}', fontsize=16, fontweight='bold')
    data=data['growth_projection']
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = df.index.rename('time')
    df.reset_index(inplace=True)
    months = list(df['time'])
    revenues = list(df['revenue'])
    shares = list(df['market_share'])
    
    # Revenue projection
    bars1 = ax1.bar(months, [r/1000000 for r in revenues], color='darkgreen', alpha=0.7)
    ax1.plot(months, [r/1000000 for r in revenues], color='darkgreen', marker='o', 
             linewidth=2, markersize=8)
    ax1.set_ylabel('Revenue (KES Millions)', fontsize=12)
    ax1.set_title('Revenue Growth Projection')
    
    # Add value labels
    for bar, val in zip(bars1, revenues):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{val/1000000:.1f}M', ha='center', va='bottom')
    
    # Add growth percentage annotations
    for i in range(1, len(revenues)):
        growth = ((revenues[i] - revenues[i-1]) / revenues[i-1]) * 100
        ax1.annotate(f'+{growth:.1f}%', 
                     xy=(i-0.5, max([r/1000000 for r in revenues]) * 0.5),
                     ha='center', color='red', weight='bold')
    
    # Market share projection
    bars2 = ax2.bar(months, shares, color='darkblue', alpha=0.7)
    ax2.plot(months, shares, color='darkblue', marker='o', linewidth=2, markersize=8)
    ax2.set_ylabel('Value Share (%)', fontsize=12)
    ax2.set_xlabel('Timeline')
    ax2.set_title('Value Share Growth Projection')
    
    # Add value labels
    for bar, val in zip(bars2, shares):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                 f'{val:.1f}%', ha='center', va='bottom')
    
    # Add target line
    ax2.axhline(y=35, color='red', linestyle='--', alpha=0.5, label='Target: 35%')
    ax2.legend()
    
    fig.tight_layout()
    plt.close(fig)
    
    return fig