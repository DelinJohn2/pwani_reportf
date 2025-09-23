import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

def partner_performance_chart_creator(intelligence,brand):

    """Create multi-metric partner performance comparison and return the figure."""

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle(f"{brand} - MT partner performance ", fontsize=16, fontweight='bold')

    df=pd.read_csv(io.StringIO(intelligence['target_partner']))
    
    partners=list(df['MT_PARTNER'])
  
    colors = sns.color_palette("Set2", n_colors=len(partners))
    
    
    revenues = list(df['total_revenue'] /1000)
    bars1 = ax1.bar(partners, revenues, color=colors)
    ax1.set_title('Revenue by Partner (KES \'000)', fontweight='bold')
    ax1.set_ylabel('Revenue (KES \'000)')
    
    max_revenue = max(revenues)
    ax1.set_ylim(0, max_revenue * 1.3)
    
    for bar, v in zip(bars1, revenues):
        label = f'{v/1000:.1f}M' if v >= 1000 else f'{v:,.0f}'
        if bar.get_height() > max_revenue * 0.8:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 0.9,
                     label, ha='center', va='top', fontweight='bold', color='white')
        else:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_revenue * 0.02,
                     label, ha='center', va='bottom')
    

    market_shares = list(df['average_value_share'])
    bars2 = ax2.bar(partners, market_shares, color=colors)
    ax2.set_title('Average Value Share by Partner (%)', fontweight='bold')
    ax2.set_ylabel('Value Share (%)')
    ax2.set_ylim(0, max(market_shares) * 1.3)
    
    for bar, v in zip(bars2, market_shares):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(market_shares) * 0.02,
                 f'{v:.1f}%', ha='center', va='bottom')
    

    ws_scores = list(df['average_ws_score'])
    bars3 = ax3.bar(partners, ws_scores, color=colors)
    ax3.set_title('White Space Opportunity Score', fontweight='bold')
    ax3.set_ylabel('WS Score')
    ax3.set_ylim(0, 100)
    
    ax3.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='High Opportunity Threshold')
    ax3.legend()
    
    for bar, v in zip(bars3, ws_scores):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 f'{v:.1f}', ha='center', va='bottom')
   
    
    values= list(df['store_coverage'])
    bars4 = ax4.bar(partners, values, color=colors)
    ax4.set_title('Store Presence by Partner', fontweight='bold')
    ax4.set_ylabel('Number of Stores')
    
    max_stores = max(values)
    ax4.set_ylim(0, max_stores * 1.3)
    
    for bar, v in zip(bars4, values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max_stores * 0.02,
                 str(v), ha='center', va='bottom')
    
    plt.subplots_adjust(hspace=0.3, wspace=0.3, top=0.93, bottom=0.07)
    plt.close(fig)
    
    return fig