import matplotlib.pyplot as plt

def create_risk_assessment_matrix(risk_data):
	fig, ax = plt.subplots(figsize=(10, 8))
	prob_map = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
	impact_map = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
	risks = risk_data["risk_matrix"]
	names, probs, imps, scores = [], [], [], []
	for r in risks:
		names.append(r['risk'].replace(' ', '\n'))
		probs.append(prob_map[r['probability']])
		imps.append(impact_map[r['impact']])
		scores.append(r['risk_score'])
	sc = ax.scatter(probs, imps, s=[max(20, s*50) for s in scores], c=scores, cmap='Reds', alpha=0.7, edgecolors='black', linewidth=1)
	for i, n in enumerate(names):
		ax.annotate(n, (probs[i], imps[i]), xytext=(5,5), textcoords='offset points', fontsize=9, ha='left')
	ax.set_xlim(0.5, 3.5); ax.set_ylim(0.5, 3.5)
	ax.set_xticks([1,2,3]); ax.set_xticklabels(['LOW','MEDIUM','HIGH'])
	ax.set_yticks([1,2,3]); ax.set_yticklabels(['LOW','MEDIUM','HIGH'])
	ax.set_xlabel('Probability', fontweight='bold'); ax.set_ylabel('Impact', fontweight='bold')
	ax.set_title('Risk Assessment Matrix\n(Bubble size = Risk Score)', fontweight='bold', pad=20)
	cbar = plt.colorbar(sc); cbar.set_label('Risk Score', fontweight='bold')
	ax.grid(True, alpha=0.3)
	fig.tight_layout()
	plt.close(fig)
	return fig