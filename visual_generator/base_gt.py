import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from loging.logger import setup_logger
from .charts_gt import (
    create_market_share_chart, 
    create_territory_priority_matrix, 
    create_investment_allocation_pie,
    create_roi_progression_chart, 
    create_risk_assessment_matrix,
    create_implementation_timeline
)

logger = setup_logger("GTDashboardGenerator")


class GTDashboardGenerator:
    def __init__(self, data, brand_name, logger=logger):
        self.data = data
        self.brand_name = brand_name
        self.logger = logger
        
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
        try:
            self.logger.info("Generating market share chart for brand=%s", self.brand_name)
            chart = create_market_share_chart(self.data, self.brand_name, self.colors)
            self.logger.info("Market share chart generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate market share chart for brand=%s", self.brand_name)
            raise

    def territory_priority_matrix(self):
        try:
            self.logger.info("Generating territory priority matrix")
            chart = create_territory_priority_matrix(self.data, self.tier_colors, self.colors)
            self.logger.info("Territory priority matrix generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate territory priority matrix")
            raise

    def investment_allocation(self):
        try:
            self.logger.info("Generating investment allocation chart")
            allocation_data = self.data.get("investment_allocation_data", {})
            chart = create_investment_allocation_pie(allocation_data, self.colors, self.tier_colors)
            self.logger.info("Investment allocation chart generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate investment allocation chart")
            raise

    def roi_progression(self):
        try:
            self.logger.info("Generating ROI progression chart")
            roi_data = self.data.get("roi_scenarios_data", {})
            chart = create_roi_progression_chart(roi_data, self.colors)
            self.logger.info("ROI progression chart generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate ROI progression chart")
            raise

    def risk_assessment(self):
        try:
            self.logger.info("Generating risk assessment matrix")
            risk_data = self.data['risk_assessment_data']
            chart = create_risk_assessment_matrix(risk_data)
            self.logger.info("Risk assessment matrix generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate risk assessment matrix")
            raise

    def implementation_timeline(self):
        try:
            self.logger.info("Generating implementation timeline")
            timeline_data = self.data.get("implementation_timeline_data", {})
            chart = create_implementation_timeline(timeline_data, self.colors)
            self.logger.info("Implementation timeline generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate implementation timeline")
            raise
