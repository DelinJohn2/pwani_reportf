from .charts_mt import (
    competitive_chart_creator,
    geographic_heatmap_creator,
    growth_projection_creator,
    investment_matrix_creator,
    opportunity_matrix_creator,
    partner_performance_chart_creator,
)
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from loging.logger import setup_logger

logger = setup_logger("MTDashboardGenerator")


class MTDashboardGenerator:
    def __init__(self, data, brand, logger=logger):
        self.data = data
        self.brand = brand
        self.logger = logger

    def create_partner_performance_chart(self):
        try:
            self.logger.info("Generating partner performance chart for brand=%s", self.brand)
            chart = partner_performance_chart_creator(self.data, self.brand)
            self.logger.info("Partner performance chart generated successfully for brand=%s", self.brand)
            return chart
        except Exception:
            self.logger.exception("Failed to generate partner performance chart for brand=%s", self.brand)
            raise

    def create_opportunity_matrix(self):
        try:
            self.logger.info("Generating opportunity matrix for brand=%s", self.brand)
            chart = opportunity_matrix_creator(self.data, self.brand)
            self.logger.info("Opportunity matrix generated successfully for brand=%s", self.brand)
            return chart
        except Exception:
            self.logger.exception("Failed to generate opportunity matrix for brand=%s", self.brand)
            raise

    def create_competitive_chart(self):
        try:
            self.logger.info("Generating competitive chart for brand=%s", self.brand)
            chart = competitive_chart_creator(self.data, self.brand)
            self.logger.info("Competitive chart generated successfully for brand=%s", self.brand)
            return chart
        except Exception:
            self.logger.exception("Failed to generate competitive chart for brand=%s", self.brand)
            raise


class MTDashboardFromAi:
    def __init__(self, data, logger=logger):
        self.data = data
        self.logger = logger

    def create_geographic_heatmap(self):
        try:
            self.logger.info("Generating geographic heatmap")
            chart = geographic_heatmap_creator(self.data)
            self.logger.info("Geographic heatmap generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate geographic heatmap")
            raise

    def create_investment_martix(self):
        try:
            self.logger.info("Generating investment matrix")
            chart = investment_matrix_creator(self.data)
            self.logger.info("Investment matrix generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate investment matrix")
            raise

    def create_growth_projection(self):
        try:
            self.logger.info("Generating growth projection chart")
            chart = growth_projection_creator(self.data)
            self.logger.info("Growth projection chart generated successfully")
            return chart
        except Exception:
            self.logger.exception("Failed to generate growth projection chart")
            raise
