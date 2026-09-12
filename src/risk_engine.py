import json

def calculate_decision_risk(decision_item: dict) -> dict:
    """
    Evaluates a single structured decision item and computes a quantitative risk score,
    risk level, and actionable recommendations based on missing owners, status, and blockers.
    """
    score = 0
    reasons = []
    
    status = decision_item.get("status", "").lower()
    owner = decision_item.get("owner")
    unresolved_issue = decision_item.get("unresolved_issue")
    conflicts = decision_item.get("conflicts")
    dependencies = decision_item.get("dependencies")
    
    # 1. Status-based risk weight
    if status == "at risk":
        score += 40
        reasons.append("Status is explicitly marked as 'At Risk'.")
    elif status == "unresolved":
        score += 30
        reasons.append("Decision is currently unresolved.")
    elif status == "in progress":
        score += 15
    elif status == "planned":
        score += 10
    elif status == "resolved":
        score += 0
        
    # 2. Owner accountability check (missing owner adds heavy risk)
    if not owner or owner.lower() == "null" or owner == "":
        score += 30
        reasons.append("No responsible owner assigned.")
        
    # 3. Blockers and conflicts check
    if unresolved_issue and unresolved_issue.lower() != "null":
        score += 15
        reasons.append(f"Active unresolved issue/blocker: {unresolved_issue}")
        
    if conflicts and conflicts.lower() != "null":
        score += 15
        reasons.append(f"Conflicting info or blockers present: {conflicts}")
        
    # Cap score at 100 max
    score = min(score, 100)
    
    # Determine Risk Level category
    if score >= 75:
        risk_level = "Critical"
    elif score >= 50:
        risk_level = "High"
    elif score >= 25:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    # Generate recommendation
    recommendation = "Monitor progress."
    if not owner or owner.lower() == "null":
        recommendation = "Assign an owner immediately to drive accountability."
    elif status == "at risk" or score >= 75:
        recommendation = "Escalate to management and review timeline buffers."
    elif unresolved_issue:
        recommendation = "Resolve underlying blockers or dependencies."
        
    # Attach computed metrics back to the decision item
    decision_item["risk_score"] = score
    decision_item["risk_level"] = risk_level
    decision_item["risk_reasons"] = reasons
    decision_item["recommendation"] = recommendation
    
    return decision_item

def evaluate_all_decisions(decisions_list: list) -> list:
    """
    Batch processes a list of decisions through the risk engine.
    """
    evaluated = [calculate_decision_risk(d) for d in decisions_list]
    # Sort by risk score descending (highest risk first)
    evaluated.sort(key=lambda x: x["risk_score"], reverse=True)
    return evaluated