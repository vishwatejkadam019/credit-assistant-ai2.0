import pytest

def calculate_dti(monthly_expenses: float, monthly_income: float) -> float:
    if monthly_income <= 0:
        raise ValueError("Income must be positive")
    return (monthly_expenses / monthly_income) * 100

def calculate_utilization(total_debt: float, credit_limit: float) -> float:
    if credit_limit <= 0:
        raise ValueError("Credit limit must be positive")
    return (total_debt / credit_limit) * 100

def calculate_delta(current_score: int, previous_score: int) -> int:
    return current_score - previous_score

def test_dti_calculation():
    assert calculate_dti(30000, 100000) == 30.0
    assert round(calculate_dti(32000, 75000), 1) == 42.7

def test_utilization_calculation():
    assert calculate_utilization(30000, 100000) == 30.0
    assert calculate_utilization(180000, 300000) == 60.0

def test_score_delta():
    assert calculate_delta(720, 680) == 40
    assert calculate_delta(650, 680) == -30
    assert calculate_delta(680, 680) == 0