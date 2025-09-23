import matplotlib.pyplot as plt


def create_roi_progression_chart( roi_data,colors):
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
	# scenarios bar
	scenarios = roi_data['scenarios']
	names = [s['scenario'] for s in scenarios]
	vals = [s['roi_percentage'] for s in scenarios]
	cols = [colors['warning'], colors['primary'], colors['success']][:len(vals)]
	bars = ax1.bar(names, vals, color=cols, alpha=0.8)
	for b, v in zip(bars, vals):
		ax1.text(b.get_x()+b.get_width()/2., b.get_height()+10, f'{v}%', ha='center', va='bottom', fontweight='bold')
	ax1.set_ylabel('ROI (%)', fontweight='bold')
	ax1.set_title('ROI Scenarios - 90 Day Projections', fontweight='bold', pad=20)
	ax1.grid(axis='y', alpha=0.3)
	# monthly progression
	monthly = roi_data['monthly_progression']
	months = [f"Month {m['month']}" for m in monthly]
	revenues = [float(m['revenue_target'].replace('KES ', '').replace('M', '').replace('B', '000')) for m in monthly]
	rois = [m['cumulative_roi'] for m in monthly]
	ax2_t = ax2.twinx()
	line1 = ax2.plot(months, revenues, marker='o', linewidth=3, color=colors['primary'], label='Revenue (KES M)')
	line2 = ax2_t.plot(months, rois, marker='s', linewidth=3, color=colors['success'], label='Cumulative ROI (%)')
	ax2.set_ylabel('Revenue (KES M)', color=colors['primary'], fontweight='bold')
	ax2_t.set_ylabel('Cumulative ROI (%)', color=colors['success'], fontweight='bold')
	ax2.set_title('90-Day Revenue & ROI Progression', fontweight='bold', pad=20)
	lines = line1 + line2
	labels = [l.get_label() for l in lines]
	ax2.legend(lines, labels, loc='upper left')
	ax2.grid(True, alpha=0.3)
	fig.tight_layout()
	plt.close(fig)
	return fig