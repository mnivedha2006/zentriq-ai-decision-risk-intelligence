import json
import os

def generate_markdown_report(portfolio_dashboard: dict, output_filepath: str = "reports/executive_summary.md") -> str:
    """
    Takes the aggregated portfolio dashboard data and generates a professional,
    executive-ready Markdown report.
    """
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    
    total = portfolio_dashboard.get("total_decisions", 0)
    avg_score = portfolio_dashboard.get("average_portfolio_risk_score", 0)
    health = portfolio_dashboard.get("portfolio_health", "Unknown")
    breakdown = portfolio_dashboard.get("risk_breakdown", {})
    dept_summary = portfolio_dashboard.get("department_summary", {})
    top_priorities = portfolio_dashboard.get("top_priorities", [])
    
    markdown_content = f"# Zentriq Executive Risk Intelligence Report\n"
    markdown_content += f"**Portfolio Health Status:** **{health}**\n"
    markdown_content += f"**Total Decisions Evaluated:** {total}\n"
    markdown_content += f"**Average Portfolio Risk Score:** {avg_score} / 100\n\n---\n\n"
    
    markdown_content += "## Risk Level Breakdown\n"
    markdown_content += f"- **Critical Risk:** {breakdown.get('Critical', 0)}\n"
    markdown_content += f"- **High Risk:** {breakdown.get('High', 0)}\n"
    markdown_content += f"- **Medium Risk:** {breakdown.get('Medium', 0)}\n"
    markdown_content += f"- **Low Risk:** {breakdown.get('Low', 0)}\n\n---\n\n"
    
    markdown_content += "## Departmental Summary\n"
    for dept, data in dept_summary.items():
        markdown_content += f"- **{dept}**: {data['decisions_count']} decisions, Avg Risk Score: {data['average_risk_score']}/100\n"
        
    markdown_content += "\n---\n\n## Top Priority Actions Required\n"
    
    for idx, item in enumerate(top_priorities, 1):
        owner_str = item.get('owner') or 'Unassigned ⚠️'
        markdown_content += f"\n### {idx}. {item.get('decision')}\n"
        markdown_content += f"- **Business Area:** {item.get('business_area')}\n"
        markdown_content += f"- **Status:** {item.get('status')} | **Owner:** {owner_str}\n"
        markdown_content += f"- **Risk Score:** {item.get('risk_score')} ({item.get('risk_level')} Risk)\n"
        markdown_content += f"- **Recommendation:** *{item.get('recommendation')}*\n"

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"Executive report successfully generated and saved to {output_filepath}")
    return markdown_content