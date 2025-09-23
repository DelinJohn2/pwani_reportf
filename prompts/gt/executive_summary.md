# Visual Executive Dashboard Synthesis Prompt - FIXED CHART ORDERING

You are creating a **Visual Executive Summary Report** for **{brand_name}**. 

## CRITICAL INSTRUCTIONS:
1. Write as a **flowing narrative report** - charts will be placed automatically based on content
2. **DO NOT USE** placeholder tags like [INSERT_CHART_X_HERE] 
3. Use **clear section headers** exactly as specified for chart placement logic
4. Include **specific data points** that will drive chart generation
5. Write **natural flowing sections** that read professionally


Input Data Description and Input Data

Below is GT-level feature data for one brand:
{gt_data}

And here is RTM sales data for the same brand:
{rtm_data}
This data is csv data subcounty wise aggregated

Enhanced with competitive intelligence data:
{external_comp}
This data top external competion the others are agregated and named as such

Internal competiton intelligence data
{internal_comp}
This data contains all the data that Pwani manufactures internal competiton give to the target brand

Territory Demographic 
{territory_demographic}
This is a brief demographic data of the {territory} Territory.

## OUTPUT STRUCTURE:

### PART 1: EXECUTIVE SUMMARY

Write a comprehensive executive summary following this exact structure:

#### Investment Recommendation: [APPROVE/CONDITIONAL/REJECT]
• Total Investment: [amount]  
• Expected ROI: [percentage] within [timeframe]  
• Strategic Rationale: [2-3 sentences explaining the strategic logic]

#### Market Opportunity Analysis

**Current Position:** Write detailed analysis of current market share, competitive positioning, and market dynamics. Include specific market share figures for the brand and main competitors.

**Key Opportunities:** 
- Geographic Concentration: [Detail about high-potential sub-counties and AWS scores]
- Competitive Gaps: [Analysis of market gaps and positioning opportunities]  
- Cultural Positioning: [Territory-specific cultural marketing opportunities]

**Competitive Landscape:** Write analysis of market fragmentation, competitor strengths/weaknesses, and strategic opportunities for market entry.

#### Territory Priority Ranking

Provide detailed territory-by-territory analysis in this format:

1. **[TERRITORY NAME]**: Tier [X] Investment (KES [X]M) - [Detailed explanation of AWS scores, market dynamics, and strategic opportunity]
2. **[TERRITORY NAME]**: Tier [X] Investment (KES [X]M) - [Detailed explanation of market conditions and investment rationale]
3. **[TERRITORY NAME]**: Tier [X] Investment (KES [X]M) - [Strategic analysis and positioning opportunity]
4. **[TERRITORY NAME]**: Tier [X] Investment (KES [X]M) - [Market challenge analysis and approach]
5. **[TERRITORY NAME]**: Tier [X] Investment (KES [X]M) - [Investment strategy and expected outcomes]

#### Strategic Implementation Approach

Write detailed implementation strategy with clear phases:

**Phase 1 (Month 1):** [Detailed activities including sub-county penetration, retail distribution, competitive pricing, specific territories and investments]

**Phase 2 (Month 2):** [Cultural marketing campaigns, community partnerships, supply chain optimization, specific activities and budget allocation]

**Phase 3 (Month 3):** [Performance assessment, scaling successful models, competitive response preparation, sustained growth preparation]

### 90 Days Implementation

#### Risk Assessment & Mitigation

Analyze key risks and mitigation strategies:

**Primary Risk:** [Detailed risk description] - **Mitigation:** [Specific mitigation strategy that cannot be easily replicated]

**Secondary Risk:** [Resource and execution risk description] - **Mitigation:** [Focused investment approach and resource concentration strategy]

#### Financial Projections

Present realistic financial scenarios with specific assumptions:

**Conservative Scenario:** [X]% ROI assuming [specific success rate and market conditions]  
**Expected Scenario:** [X]% ROI with [detailed assumptions about market penetration and competitive positioning]  
**Optimistic Scenario:** [X]% ROI if [conditions for optimal performance including cultural marketing success]

---

### PART 2: CHART DATA STRUCTURE

Generate complete JSON data structure for all charts:

```json
{{
  "executive_summary_data": {{
    "brand": "{brand_name}",
    "current_market_share": "[extract actual percentage from data]",
    "investment_proposal": {{
      "total_amount": "[calculate total from all territories]",
      "timeframe": "90 days",
      "expected_roi": "[calculate weighted average ROI]",
      "target_market_share": "[realistic target based on investment]",
      "success_probability": "[assess based on market conditions]"
    }},
    "opportunity_size": "[total market opportunity in KES]",
    "key_insight": "[main strategic insight driving recommendation]"
  }},
  "territory_performance_data": {{
    "territories": [
      {{
        "name": "[TERRITORY NAME]",
        "current_share": 0.0,
        "sku_cluster": "[Green A/Green B/Blue A/Blue B/White A/White B/Yellow A/Yellow B]",
        "white_space_score": 0.0,
        "investment_tier": "[Tier 1/2/3]",
        "investment_amount": "[KES XM format]",
        "target_share": 0.0,
        "expected_roi": 0,
        "key_opportunity": "[specific opportunity description]",
        "priority_level": "[HIGH/MEDIUM/LOW]",
        "main_competitor": "[competitor name]",
        "competitor_share": 0.0,
        "share_gap": 0.0
      }}
    ]
  }},
  "investment_allocation_data": {{
    "allocation_by_tier": [
      {{
        "tier": "Tier 1",
        "percentage": 0,
        "amount": "[KES XM]",
        "territories": ["[territory list]"],
        "rationale": "[strategic explanation]"
      }},
      {{
        "tier": "Tier 2", 
        "percentage": 0,
        "amount": "[KES XM]",
        "territories": ["[territory list]"],
        "rationale": "[strategic explanation]"
      }},
      {{
        "tier": "Tier 3",
        "percentage": 0,
        "amount": "[KES XM]",
        "territories": ["[territory list]"],
        "rationale": "[strategic explanation]"
      }}
    ],
    "allocation_by_strategy": [
      {{
        "strategy": "High-AWS Sub-County Penetration",
        "percentage": 0,
        "amount": "[KES XM]",
        "description": "[strategy description]"
      }},
      {{
        "strategy": "Competitive Displacement",
        "percentage": 0,
        "amount": "[KES XM]",
        "description": "[strategy description]"
      }},
      {{
        "strategy": "Cultural Marketing Campaigns",
        "percentage": 0,
        "amount": "[KES XM]",
        "description": "[strategy description]"
      }},
      {{
        "strategy": "Supply Chain Optimization",
        "percentage": 0,
        "amount": "[KES XM]",
        "description": "[strategy description]"
      }}
    ]
  }},
  "roi_scenarios_data": {{
    "scenarios": [
      {{
        "scenario": "Conservative",
        "success_rate": 60,
        "investment": "[KES XM]",
        "return": "[KES XM]",
        "roi_percentage": 0,
        "breakeven_months": 0
      }},
      {{
        "scenario": "Expected",
        "success_rate": 100,
        "investment": "[KES XM]",
        "return": "[KES XM]",
        "roi_percentage": 0,
        "breakeven_months": 0
      }},
      {{
        "scenario": "Optimistic", 
        "success_rate": 130,
        "investment": "[KES XM]",
        "return": "[KES XM]",
        "roi_percentage": 0,
        "breakeven_months": 0
      }}
    ],
    "monthly_progression": [
      {{
        "month": 1,
        "revenue_target": "[KES XM]",
        "investment_deployed": "[KES XM]",
        "cumulative_roi": 0
      }},
      {{
        "month": 2,
        "revenue_target": "[KES XM]",
        "investment_deployed": "[KES XM]",
        "cumulative_roi": 0
      }},
      {{
        "month": 3,
        "revenue_target": "[KES XM]",
        "investment_deployed": "[KES XM]",
        "cumulative_roi": 0
      }}
    ]
  }},
  "competitive_landscape_data": {{
    "market_share_comparison": [
      {{
        "brand": "{brand_name}",
        "market_share": 0.0,
        "position": "Challenger",
        "vulnerability": "[weakness analysis]",
        "threat_level": "LOW"
      }},
      {{
        "brand": "[Main Competitor 1]",
        "market_share": 0.0,
        "position": "Market Leader",
        "vulnerability": "[weakness that can be exploited]",
        "threat_level": "HIGH"
      }},
      {{
        "brand": "[Main Competitor 2]",
        "market_share": 0.0,
        "position": "Strong Challenger",
        "vulnerability": "[competitive weakness]",
        "threat_level": "MEDIUM"
      }},
      {{
        "brand": "OTHERS",
        "market_share": 0.0,
        "position": "Fragmented",
        "vulnerability": "Market fragmentation",
        "threat_level": "LOW"
      }}
    ]
  }},
  "risk_assessment_data": {{
    "risk_matrix": [
      {{
        "risk": "Competitive Price Wars",
        "probability": "HIGH",
        "impact": "HIGH",
        "risk_score": 9,
        "mitigation": "Quality differentiation strategy"
      }},
      {{
        "risk": "Resource Dispersion",
        "probability": "MEDIUM",
        "impact": "HIGH",
        "risk_score": 6,
        "mitigation": "Tier-based investment concentration"
      }},
      {{
        "risk": "Supply Chain Disruption",
        "probability": "LOW",
        "impact": "MEDIUM",
        "risk_score": 3,
        "mitigation": "Multi-supplier strategy"
      }},
      {{
        "risk": "Cultural Messaging Misalignment",
        "probability": "MEDIUM",
        "impact": "MEDIUM",
        "risk_score": 4,
        "mitigation": "Local market research and testing"
      }}
    ]
  }},
  "implementation_timeline_data": {{
    "phases": [
      {{
        "phase": "Market Entry Acceleration",
        "duration": "Days 1-30",
        "investment": "[KES XM]",
        "percentage_of_total": 0,
        "key_milestones": [
          "High-AWS sub-county penetration in NAIROBI and CENTRAL",
          "Retail distribution establishment in 25 priority sub-counties",
          "Competitive pricing implementation"
        ],
        "success_metrics": [
          {{
            "metric": "Sub-county penetration rate",
            "target": "60% of priority sub-counties",
            "territories": ["NAIROBI", "CENTRAL"]
          }},
          {{
            "metric": "Distribution points established",
            "target": "150 retail outlets",
            "territories": ["NAIROBI", "CENTRAL"]
          }}
        ]
      }},
      {{
        "phase": "Cultural Brand Building",
        "duration": "Days 31-60",
        "investment": "[KES XM]",
        "percentage_of_total": 0,
        "key_milestones": [
          "Cultural marketing campaigns launch",
          "Community partnership development",
          "Supply chain optimization for ERP-RTM balance"
        ],
        "success_metrics": [
          {{
            "metric": "Brand awareness increase",
            "target": "25% improvement",
            "territories": ["ALL"]
          }},
          {{
            "metric": "Community partnerships",
            "target": "10 partnerships per territory",
            "territories": ["ALL"]
          }}
        ]
      }},
      {{
        "phase": "Market Consolidation",
        "duration": "Days 61-90",
        "investment": "[KES XM]",
        "percentage_of_total": 0,
        "key_milestones": [
          "Performance assessment and optimization",
          "Successful model scaling",
          "Competitive response strategy implementation"
        ],
        "success_metrics": [
          {{
            "metric": "ROI achievement",
            "target": "180% cumulative ROI",
            "territories": ["ALL"]
          }},
          {{
            "metric": "Market share gain",
            "target": "2x current share",
            "territories": ["NAIROBI", "CENTRAL"]
          }}
        ]
      }}
    ]
  }}
}}
```

CHART PLACEMENT LOGIC:

The system will automatically place charts based on content sections:

- **Market Share Chart** → After "Current Position" analysis
- **Territory Matrix Chart** → After territory ranking list  
- **Investment Allocation Chart** → Before "Phase 1" description
- **ROI Progression Chart** → After "Financial Projections" section
- **Risk Matrix Chart** → After risk mitigation strategies
- **Timeline Chart** → After "Phase 3" description

**CRITICAL:** Write natural, flowing narrative sections. The system will detect these sections and place charts logically within the content flow. Do NOT use placeholder tags - they will break the intelligent placement system.