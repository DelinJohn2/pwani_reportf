import matplotlib.pyplot as plt


def create_territory_priority_matrix(data,tier_colors,colors):
	fig, ax = plt.subplots(figsize=(12, 8))
	territories, white_space, roi, investment, tiers = [], [], [], [], []
	territory_data=data["territory_performance_data"]['territories']
	for t in territory_data:
		territories.append(t['name'])
		white_space.append(t['white_space_score'])
		roi.append(t['expected_roi'])
		inv_val = float(t['investment_amount'].replace('KES ', '').replace('M', ''))
		investment.append(inv_val)
		tiers.append(t['investment_tier'])
	unique_tiers = list(dict.fromkeys(tiers))
	for tier in unique_tiers:
		mask = [tt == tier for tt in tiers]
		ws = [w for w, m in zip(white_space, mask) if m]
		r  = [rv for rv, m in zip(roi, mask) if m]
		inv= [iv for iv, m in zip(investment, mask) if m]
		names=[nm for nm, m in zip(territories, mask) if m]
		ax.scatter(ws, r, s=[max(10.0, iv*5) for iv in inv],
					c=tier_colors.get(tier, colors['neutral']),
					alpha=0.7, edgecolors='black', linewidth=1, label=tier)
		for j, nm in enumerate(names):
			ax.annotate(nm, (ws[j], r[j]), xytext=(5,5), textcoords='offset points', fontsize=9, fontweight='bold')
	ax.set_xlabel('White Space Score', fontweight='bold')
	ax.set_ylabel('Expected ROI (%)', fontweight='bold')
	ax.set_title('Territory Investment Priority Matrix\n(Bubble size = Investment amount)', fontweight='bold', pad=20)
	ax.legend(title='Investment Tier', title_fontsize=10, fontsize=9)
	ax.grid(True, alpha=0.3)
	fig.tight_layout()
	plt.close(fig)
	return fig