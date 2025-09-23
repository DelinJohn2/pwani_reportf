
import matplotlib.pyplot as plt


def create_market_share_chart(data,brand_name,colors):
	
	fig, ax = plt.subplots(figsize=(10, 6))
	brands, shares, bar_colors = [], [], []
	competitive_data=data['competitive_landscape_data']['market_share_comparison']
	for comp in competitive_data:
		brands.append(comp['brand'])
		shares.append(comp['market_share'])
		if comp['brand'] == brand_name:
			bar_colors.append(colors['highlight'])
		elif comp.get('position') == 'Market Leader':
			bar_colors.append(colors['warning'])
		else:
			bar_colors.append(colors['neutral'])
	bars = ax.barh(brands, shares, color=bar_colors)
	for bar, s in zip(bars, shares):
		ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{s:.1f}%', ha='left', va='center', fontweight='bold')
	ax.set_xlabel('Market Share (%)')
	ax.set_title(f'Market Share Comparison - {brand_name} Competitive Landscape', fontweight='bold', pad=20)
	ax.set_xlim(0, max(shares) * 1.2 if shares else 1)
	ax.grid(axis='x', alpha=0.3)
	fig.tight_layout()
	plt.close(fig)
	return fig