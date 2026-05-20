from app.services.developer_knowledge import build_developer_knowledge_hub


def test_developer_knowledge_hub_reports_aligned_payee() -> None:
    aligned_case = {
        "payment_instruction_payee": "Siam Riverside Living Co., Ltd.",
    }

    payload = build_developer_knowledge_hub(aligned_case)

    assert payload["knowledge_vs_agent_gap"]["status"] == "aligned"
    assert payload["knowledge_vs_agent_gap"]["agent_claimed_payee"] == "Siam Riverside Living Co., Ltd."
