import  matplotlib.pyplot as plt

def investment_matrix_creator( data):
        """Create investment prioritization matrix"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        investments = data['investment_matrix']
        
        
        
        # Extract data for plotting
        opportunities = [inv['opportunity'] for inv in investments]
        roi = [inv['roi_percentage'] for inv in investments]
        investment = [inv['investment_required'] / 1000000 for inv in investments]  # In millions
        
        # Color by risk level
        risk_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
        colors = [risk_colors.get(inv['risk_level'], 'gray') for inv in investments]
        
        # Create bubble chart
        scatter = ax.scatter(investment, roi, s=[inv['expected_return']/10000 for inv in investments],
                           c=colors, alpha=0.6, edgecolors='black', linewidth=2)
        
        # Add labels
        for i, opp in enumerate(opportunities):
            ax.annotate(opp, (investment[i], roi[i]), xytext=(5, 5), 
                       textcoords='offset points', fontsize=9)
        
        # Add threshold lines
        ax.axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='100% ROI Line')
        ax.axvline(x=2, color='gray', linestyle='--', alpha=0.5, label='KES 2M Investment')
        
        ax.set_xlabel('Investment Required (KES Millions)', fontsize=12)
        ax.set_ylabel('Expected ROI (%)', fontsize=12)
        ax.set_title(f'Investment Priority Matrix', fontsize=14, fontweight='bold')
        
        # Add legend for risk levels
        for risk, color in risk_colors.items():
            ax.scatter([], [], c=color, alpha=0.6, edgecolors='black', s=100, label=f'{risk} Risk')
        ax.legend(loc='upper left')
        
        # Add quadrant labels
        ax.text(0.98, 0.98, 'HIGH ROI\nHIGH INVESTMENT', transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right', 
                fontsize=9, alpha=0.5, weight='bold')
        ax.text(0.02, 0.98, 'HIGH ROI\nLOW INVESTMENT', transform=ax.transAxes,
                verticalalignment='top', fontsize=9, alpha=0.5, weight='bold')
        ax.text(0.98, 0.02, 'LOW ROI\nHIGH INVESTMENT', transform=ax.transAxes,
                horizontalalignment='right', fontsize=9, alpha=0.5, weight='bold')
        ax.text(0.02, 0.02, 'LOW ROI\nLOW INVESTMENT', transform=ax.transAxes,
                fontsize=9, alpha=0.5, weight='bold')
        
        # plt.tight_layout()
        
        fig.tight_layout()
        plt.close(fig)
        
        return fig