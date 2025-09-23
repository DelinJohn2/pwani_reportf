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

class MTDashboardGenerator:
    def __init__(self,data,brand):
       
        self.data=data
        self.brand=brand
    def create_partner_performance_chart(self):
        return partner_performance_chart_creator(self.data,self.brand)

    def create_opportunity_matrix(self):
        return opportunity_matrix_creator(self.data,self.brand)

    def create_competitive_chart(self):
        return competitive_chart_creator(self.data,self.brand)

      


class MTDashboardFromAi:
    def __init__(self,data):
        self.data=data

    def create_geographic_heatmap(self):
        return geographic_heatmap_creator(self.data)

    def create_investment_martix(self):
        return investment_matrix_creator(self.data)
    
    def create_growth_projection(self):
        return growth_projection_creator(self.data) 