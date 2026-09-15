import json

def aggregate_portfolio_risks(evaluated_decisions_list: list) -> dict:
    """
    Aggregates evaluated decisions into portfolio-level risk metrics,
    summary counts, department distribution, and top priority actions.
    """
    total_decisions = len(evaluated_decisions_list)
    if total_decisions == 0:
        return {"total_decisions": 0, "portfolio_risk_score": 0, "risk_breakdown": {}}
    
    # Calculate risk level counts
    risk_breakdown = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    department_risks = {}
    total_score = 0
    
    for item in evaluated_decisions_list:
        score = item.get("risk_score", 0)
        total_score += score
        
        level = item.get("risk_level", "Low")
        if level in risk_breakdown:
            risk_breakdown[level] += 1
            
        # Track department-wise aggregation
        dept = item.get("business_area", "General")
        if dept not in department_risks:
            department_risks[dept] = {"total_items": 0, "cumulative_score": 0}
        department_risks[dept]["total_items"] += 1
        department_risks[dept]["cumulative_score"] += score

    # Compute average scores per department
    dept_summary = {}
    for dept, data in department_risks.items():
        avg_score = round(data["cumulative_score"] / data["total_items"], 2)
        dept_summary[dept] = {
            "decisions_count": data["total_items"],
            "average_risk_score": avg_score
        }

    average_portfolio_score = round(total_score / total_decisions, 2)
    
    # Portfolio Health status
    if average_portfolio_score >= 60:
        portfolio_health = "Critical Alert"
    elif average_portfolio_score >= 40:
        portfolio_health = "At Risk"
    elif average_portfolio_score >= 20:
        portfolio_health = "Stable"
    else:
        portfolio_health = "Healthy"

    dashboard_summary = {
        "total_decisions": total_decisions,
        "average_portfolio_risk_score": average_portfolio_score,
        "portfolio_health": portfolio_health,
        "risk_breakdown": risk_breakdown,
        "department_summary": dept_summary,
        "top_priorities": evaluated_decisions_list[:3] # Top 3 highest risk decisions to address
    }
    
    return dashboard_summary