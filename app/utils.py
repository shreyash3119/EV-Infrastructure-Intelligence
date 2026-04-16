"""
Utility functions for EV Infrastructure Intelligence
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Optional
from datetime import datetime

def calculate_growth_rate(values: List[float]) -> float:
    """Calculate compound annual growth rate (CAGR)"""
    if len(values) < 2 or values[0] == 0:
        return 0.0
    
    start = values[0]
    end = values[-1]
    years = len(values) - 1
    
    cagr = (pow(end / start, 1 / years) - 1) * 100
    return round(cagr, 2)


def format_number(num: float, prefix: str = '', suffix: str = '') -> str:
    """Format number with thousand separators"""
    return f"{prefix}{num:,.0f}{suffix}"


def format_currency(amount: float, currency: str = '₹') -> str:
    """Format currency in Indian notation"""
    if amount >= 10000000:  # 1 Crore
        return f"{currency}{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"{currency}{amount/100000:.2f} L"
    else:
        return f"{currency}{amount:,.0f}"


def get_risk_level(ev_per_charger: float) -> Tuple[str, str]:
    """
    Determine risk level based on EV per charger ratio
    
    Returns:
    --------
    Tuple[str, str] : (risk_level, emoji)
    """
    if ev_per_charger <= 10:
        return 'LOW', '🟢'
    elif ev_per_charger <= 20:
        return 'MODERATE', '🟡'
    else:
        return 'HIGH', '🔴'


def calculate_investment(
    charger_gap: int,
    cost_per_charger: float = 500000
) -> Dict:
    """Calculate total investment requirements"""
    
    charger_cost = charger_gap * cost_per_charger
    training_cost = charger_gap * 2 * 50000
    contingency = (charger_cost + training_cost) * 0.15
    
    total = charger_cost + training_cost + contingency
    
    return {
        'charger_installation': charger_cost,
        'technician_training': training_cost,
        'contingency': contingency,
        'total_investment': total
    }


def generate_action_plan(rto: str, charger_gap: int, year: int) -> List[Dict]:
    """Generate actionable recommendations"""
    
    if charger_gap > 0:
        return [
            {
                'priority': 1,
                'action': f'Install {charger_gap} charging stations',
                'timeline': f'{year-1} to {year}',
                'responsible': 'Infrastructure Dept'
            },
            {
                'priority': 2,
                'action': f'Train {charger_gap * 2} EV technicians',
                'timeline': f'{year-2} to {year-1}',
                'responsible': 'Skill Development'
            },
            {
                'priority': 3,
                'action': 'Conduct site surveys',
                'timeline': f'{year-2}',
                'responsible': 'Planning Dept'
            }
        ]
    else:
        return [
            {
                'priority': 1,
                'action': 'Monitor and maintain infrastructure',
                'timeline': 'Ongoing',
                'responsible': 'Maintenance Dept'
            }
        ]
