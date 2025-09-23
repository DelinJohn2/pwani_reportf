import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from .charts_gt import create_market_share_chart, create_territory_priority_matrix, create_investment_allocation_pie,create_roi_progression_chart, create_risk_assessment_matrix,create_implementation_timeline




class GTDashboardGenerator:
    def __init__(self, data, brand_name):
        self.data = data
        self.brand_name = brand_name
        
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'warning': '#C73E1D',
            'neutral': '#8B9DC3',
            'highlight': '#F4D03F'
        }
        self.tier_colors = {
            'Tier 1': self.colors['primary'],
            'Tier 2': self.colors['secondary'],
            'Tier 3': self.colors['warning']
        }

        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        })


    def market_share_chart(self):
        return create_market_share_chart(self.data, self.brand_name, self.colors)
    
    def territory_priority_matrix(self):
        return create_territory_priority_matrix(self.data, self.tier_colors, self.colors)

  
    def investment_allocation(self):
        allocation_data = self.data.get("investment_allocation_data", {})
        return create_investment_allocation_pie( allocation_data,self.colors,self.tier_colors)

    def roi_progression(self):
        roi_data = self.data.get("roi_scenarios_data", {})
        return create_roi_progression_chart(roi_data,self.colors)

    def risk_assessment(self):
        risk_data = self.data['risk_assessment_data']
        return create_risk_assessment_matrix( risk_data)

    def implementation_timeline(self):
        timeline_data = self.data.get("implementation_timeline_data", {})
        return create_implementation_timeline(timeline_data,self.colors)