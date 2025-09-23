import matplotlib.pyplot as plt

def create_investment_allocation_pie( allocation_data,colors,tier_colors):
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
	# by tier
	tier_data = allocation_data['allocation_by_tier']
	tier_labels = [i['tier'].replace(' - ', '\n') for i in tier_data]
	tier_sizes  = [i['percentage'] for i in tier_data]
	tier_colors = [tier_colors.get(f'Tier {i+1}', colors['neutral']) for i in range(len(tier_data))]
	ax1.pie(tier_sizes, labels=tier_labels, autopct='%1.0f%%', colors=tier_colors, startangle=90, textprops={'fontsize': 9})
	ax1.set_title('Investment Allocation by Tier', fontweight='bold', pad=20)
	# by strategy
	strategy_data = allocation_data['allocation_by_strategy']
	strategy_labels = [i['strategy'].replace(' & ', '\n& ') for i in strategy_data]
	strategy_sizes  = [i['percentage'] for i in strategy_data]
	strategy_colors = [colors['primary'], colors['secondary'], colors['success'], colors['neutral']][:len(strategy_data)]
	ax2.pie(strategy_sizes, labels=strategy_labels, autopct='%1.0f%%', colors=strategy_colors, startangle=90, textprops={'fontsize': 9})
	ax2.set_title('Investment Allocation by Strategy', fontweight='bold', pad=20)
	fig.tight_layout()
	plt.close(fig)
	return fig
