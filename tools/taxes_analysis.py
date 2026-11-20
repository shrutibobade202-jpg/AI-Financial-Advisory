
from langchain.tools import tool

def _analyze_tax_scenario(income:float,gains:float,deductions:float,tax_rate:float,cg_rate:float) ->dict:
    taxable_income = max(0, income - deductions)
    income_tax = taxable_income * tax_rate
    cg_tax = gains * cg_rate

    total_tax = income_tax + cg_tax
    after_tax_income = income + gains - total_tax

    return {
        "taxable_income": taxable_income,
        "income_tax": round(income_tax, 2),
        "capital_gains_tax": round(cg_tax, 2),
        "total_tax": round(total_tax, 2),
        "after_tax_income": round(after_tax_income, 2),
    }

@tool
def analyze_tax_scenario(income:float,gains:float,deductions:float,tax_rate:float,cg_rate:float) -> dict:
    """
    Use for tax calculations:
    - taxable income
    - capital gains tax
    - scenario comparison
    - after-tax return estimation
    """
    return _analyze_tax_scenario(income,gains,deductions,tax_rate,cg_rate)