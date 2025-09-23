import matplotlib.pyplot as plt


def create_implementation_timeline( timeline_data,colors):
	fig, ax = plt.subplots(figsize=(14, 8))
	phases = timeline_data['phases']
	names = [p['phase'] for p in phases]
	colors = [colors['primary'], colors['secondary'], colors['success']]
	for i, p in enumerate(phases):
		if 'Days 1-30' in p['duration']:
			start, end = 0, 30
		elif 'Days 31-60' in p['duration']:
			start, end = 30, 60
		elif 'Days 61-90' in p['duration']:
			start, end = 60, 90
		else:
			start, end = i*30, (i+1)*30
		ax.barh(i, end-start, left=start, height=0.6, color=colors[i % len(colors)], alpha=0.8, edgecolor='black', linewidth=1)
		ax.text(start + (end-start)/2, i, p['phase'], ha='center', va='center', fontweight='bold', color='white')
		inv = p['investment']; pct = p['percentage_of_total']
		ax.text(end + 2, i, f'{inv}\n({pct}%)', ha='left', va='center', fontsize=9)
	ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
	ax.set_xlabel('Days', fontweight='bold'); ax.set_title('90-Day Implementation Timeline', fontweight='bold', pad=20)
	ax.set_xlim(0, 100)
	ax.axvline(30, color='gray', linestyle='--', alpha=0.5); ax.axvline(60, color='gray', linestyle='--', alpha=0.5)
	ax.text(15, len(names), 'Month 1', ha='center', fontweight='bold')
	ax.text(45, len(names), 'Month 2', ha='center', fontweight='bold')
	ax.text(75, len(names), 'Month 3', ha='center', fontweight='bold')
	ax.grid(axis='x', alpha=0.3)
	fig.tight_layout()
	plt.close(fig)
	return fig
