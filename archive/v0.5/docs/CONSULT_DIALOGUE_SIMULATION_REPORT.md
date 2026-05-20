# Consult Dialogue Simulation Report

> Generated: 2026-05-20 11:34 UTC · synthetic demo data · API v0.5.13

Multi-turn buyer consultation scripts. Source: `scripts/run_consult_dialogue_matrix.py --offline`.

## Summary

- Scripts: **9** · Turns: **17** · Passed: **17/17**

| Script | Turns | Pass | Description |
|--------|-------|------|-------------|
| `villa_buyer_en` | 3 | 3/3 | WhatsApp replay — villa request then inventory/location follow-up |
| `project_faq_ru` | 3 | 3/3 | Russian project FAQ — price, FET, installment |
| `settlement_en` | 2 | 2/2 | Settlement — payee mismatch, no deposit approval |
| `mixed_ru_en` | 2 | 2/2 | Language switch — RU greeting then EN price question |
| `follow_up_context` | 2 | 2/2 | Session follow-up — unit types after price question |
| `mixed_project_settlement` | 2 | 2/2 | Project price question then settlement deposit — bridge KB + bank tools |
| `usdt_buyer_ru` | 1 | 1/1 | USDT purchase pitch — no prompt leak |
| `cash_buyer_ru` | 1 | 1/1 | Cash buyer — red route, no deposit encouragement |
| `mixed_capital_en` | 1 | 1/1 | Mixed SWIFT + USDT — conditional route |

## `villa_buyer_en`

_WhatsApp replay — villa request then inventory/location follow-up_

### Turn 1 — PASS
- User: 'привет'
- Intent: `greeting` · mode: `greeting_template`
- Tools: `[]`
- Reply: Здравствуйте! Я консультант Bankable Property Network (демо). Могу ответить по проекту Landmark Sukhumvit Tower (цены, FET, рассрочка) или по банковскому маршруту сделки (payee, escrow, SWIFT/USDT). Платежи не одобряю — решение за банком на bankable rails.

### Turn 2 — PASS
- User: 'i want buy villa'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «Step 3 — Bankable handoff (settlement layer)» (Buyer_Settlement_Bridge.md): 1. Capital classification — SWIFT (green), USDT mix (amber), cash/P2P (red).
2. Payee verification — Developer Knowledge Hub (anchor demo may show agent vs authorized mismatch on *other* deals).
3. Route decision — Scenario Simulator outcomes.
4. Escrow + Closing Passport — evidence hash before release.

### How to buy Landmark → bank rails (WhatsApp pitch)

When a buyer asks *«... This demo 

### Turn 3 — PASS
- User: 'what do you have and where?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «Villas vs condos» (FAQ.md): Q: Do you sell standalone villas?  
A: This demo inventory is Landmark Sukhumvit Tower luxury condominiums in Bangkok — not Phuket villas or land plots. «Step 3 — Bankable handoff (settlement layer)» (Buyer_Settlement_Bridge.md): 1. Capital classification — SWIFT (green), USDT mix (amber), cash/P2P (red).
2. Payee verification — Developer Knowledge Hub (anchor demo may show agent vs authorized mismatch on *other* deals).
3. Route decision 


## `project_faq_ru`

_Russian project FAQ — price, FET, installment_

### Turn 1 — PASS
- User: 'сколько стоит квартира?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: По базе знаний (демо): «Russian summary (demo)» (FAQ.md): В: Сколько стоит квартира?  
A: 2BR от 18,5 млн бат, 3BR от 24,8 млн бат (Landmark Sukhumvit Tower, Bangkok). Платежи не одобряю — решение за банком.

### Turn 2 — PASS
- User: 'что такое FET?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: По базе знаний (демо): «Russian summary (demo)» (FAQ.md): В: Сколько стоит квартира?  
A: 2BR от 18,5 млн бат, 3BR от 24,8 млн бат (Landmark Sukhumvit Tower, Bangkok). «Buyer_Settlement_Bridge.md (intro)» (Buyer_Settlement_Bridge.md): ---
title: "Buyer Journey — Landmark Sales to Bank Settlement"
type: "bridge"
last_updated: "2026-05-20"
keywords: ["escrow", "SWIFT", "FET", "deposit", "bankable", "Landmark Sukhumvit", "Closing Passport"]
related_docs: ["FAQ.md", "Sales_Process.md", "Project_Over

### Turn 3 — PASS
- User: 'есть рассрочка?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: По базе знаний (демо): «Buyer_Settlement_Bridge.md (intro)» (Buyer_Settlement_Bridge.md): ---
title: "Buyer Journey — Landmark Sales to Bank Settlement"
type: "bridge"
last_updated: "2026-05-20"
keywords: ["escrow", "SWIFT", "FET", "deposit", "bankable", "Landmark Sukhumvit", "Closing Passport"]
related_docs: ["FAQ.md", "Sales_Process.md", "Project_Overview.md"]
---

# Buyer Journey: Landmark Sukhumvit → Bankable Settlement

Synthetic demo narrative linking tier-1 project sales ... «Step 3 — Ban


## `settlement_en`

_Settlement — payee mismatch, no deposit approval_

### Turn 1 — PASS
- User: 'What is the payee mismatch on escrow?'
- Intent: `settlement` · mode: `keyword_template`
- Tools: `['consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:developer-suspicious-route']`
- Reply: Developer Hub: agent payee «SRL Holding 2026 Co., Ltd.» vs authorized «Siam Riverside Living Co., Ltd.». Scenario developer-suspicious-route: bank action escalate, Closing Passport generated_after_corrected_instructions. I do not approve payments — banks decide.

### Turn 2 — PASS
- User: 'Can I deposit cash today?'
- Intent: `settlement` · mode: `keyword_template`
- Tools: `['consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:cash-red-route']`
- Reply: Developer Hub: agent payee «SRL Holding 2026 Co., Ltd.» vs authorized «Siam Riverside Living Co., Ltd.». Scenario cash-red-route: bank action reject, Closing Passport not_generated. Do not deposit to an unverified payee — use bankable escrow only. I do not approve payments — banks decide. This route is rejected in the synthetic demo — no deposit guidance.


## `mixed_ru_en`

_Language switch — RU greeting then EN price question_

### Turn 1 — PASS
- User: 'Привет'
- Intent: `greeting` · mode: `greeting_template`
- Tools: `[]`
- Reply: Здравствуйте! Я консультант Bankable Property Network (демо). Могу ответить по проекту Landmark Sukhumvit Tower (цены, FET, рассрочка) или по банковскому маршруту сделки (payee, escrow, SWIFT/USDT). Платежи не одобряю — решение за банком на bankable rails.

### Turn 2 — PASS
- User: 'What is the price for a 2BR unit?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «Prices» (FAQ.md): Q: How much is a 2-bedroom unit?  
A: From 18,500,000 THB (floors 28–35), subject to availability on the developer feed.

Q: How much is a 3-bedroom unit?  
A: From 24,800,000 THB (floors 36–42). «Available inventory (demo)» (Project_Overview.md): | Unit | Floors | Price (THB) | Status |
|------|--------|-------------|--------|
| 2BR | 28–35 | 18,500,000 | available |
| 3BR | 36–42 | 24,800,000 | available | I do not approve payments — banks decide.


## `follow_up_context`

_Session follow-up — unit types after price question_

### Turn 1 — PASS
- User: 'How much does a 2BR cost?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «Prices» (FAQ.md): Q: How much is a 2-bedroom unit?  
A: From 18,500,000 THB (floors 28–35), subject to availability on the developer feed.

Q: How much is a 3-bedroom unit?  
A: From 24,800,000 THB (floors 36–42). «Step 3 — Bankable handoff (settlement layer)» (Buyer_Settlement_Bridge.md): 1. Capital classification — SWIFT (green), USDT mix (amber), cash/P2P (red).
2. Payee verification — Developer Knowledge Hub (anchor demo may show agent vs authorized mismatch on *

### Turn 2 — PASS
- User: 'what unit types do you have?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «Prices» (FAQ.md): Q: How much is a 2-bedroom unit?  
A: From 18,500,000 THB (floors 28–35), subject to availability on the developer feed.

Q: How much is a 3-bedroom unit?  
A: From 24,800,000 THB (floors 36–42). «Available inventory (demo)» (Project_Overview.md): | Unit | Floors | Price (THB) | Status |
|------|--------|-------------|--------|
| 2BR | 28–35 | 18,500,000 | available |
| 3BR | 36–42 | 24,800,000 | available | I do not approve payments — banks decide.


## `mixed_project_settlement`

_Project price question then settlement deposit — bridge KB + bank tools_

### Turn 1 — PASS
- User: 'How much is a 2BR at Landmark Sukhumvit Tower?'
- Intent: `project_faq` · mode: `keyword_template`
- Tools: `['consult_knowledge_search']`
- Reply: From knowledge base (demo): «FAQ.md (intro)» (FAQ.md): ---
title: "FAQ — Landmark Sukhumvit Tower"
type: "faq"
last_updated: "2026-05-20"
keywords: ["price", "2BR", "3BR", "FET", "installment", "Bangkok Landmark", "Sukhumvit", "escrow"]
related_docs: ["Project_Overview.md", "Sales_Process.md", "Legal_and_Terms.md"]
---

# FAQ — Landmark Sukhumvit Tower

> Synthetic demo data — not a sales offer. «Villas vs condos» (FAQ.md): Q: Do you sell standalone villas?  
A: This demo inventory is Landmark S

### Turn 2 — PASS
- User: 'Can I wire the deposit to the agent account?'
- Intent: `settlement` · mode: `keyword_template`
- Tools: `['consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:agent-risk-route']`
- Reply: Developer Hub: agent payee «SRL Holding 2026 Co., Ltd.» vs authorized «Siam Riverside Living Co., Ltd.». Scenario agent-risk-route: bank action escalate, Closing Passport generated_with_agent_risk_evidence. Do not deposit to an unverified payee — use bankable escrow only. I do not approve payments — banks decide.


## `usdt_buyer_ru`

_USDT purchase pitch — no prompt leak_

### Turn 1 — PASS
- User: 'а как покупать? у меня usdt'
- Intent: `mixed` · mode: `purchase_pitch_template`
- Tools: `['consult_knowledge_search', 'consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:usdt-mixed-route']`
- Reply: Landmark Sukhumvit Tower (демо): бронирование у Bangkok Landmark Group, оплата только на уполномоченного получателя из фида застройщика. USDT — «янтарный» капитал: не переводите криптовалюту агенту. Нужны conversion evidence, bank review, затем FET-ready escrow. Зачем через банк: проверка застройщика (Developer Hub), верифицированный payee, escrow, FET для freehold, регистрация в Land Department, Closing Passport до release. Payee gap: агент «SRL Holding 2026 Co., Ltd.» vs authorized «Siam River


## `cash_buyer_ru`

_Cash buyer — red route, no deposit encouragement_

### Turn 1 — PASS
- User: 'хочу купить за наличные'
- Intent: `mixed` · mode: `purchase_pitch_template`
- Tools: `['consult_knowledge_search', 'consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:cash-red-route']`
- Reply: Landmark Sukhumvit Tower (демо): бронирование у Bangkok Landmark Group, оплата только на уполномоченного получателя из фида застройщика. Наличные / P2P — «красный» маршрут в демо: банк отклоняет или эскалирует, Closing Passport не формируется без bankable trail. Зачем через банк: проверка застройщика (Developer Hub), верифицированный payee, escrow, FET для freehold, регистрация в Land Department, Closing Passport до release. Payee gap: агент «SRL Holding 2026 Co., Ltd.» vs authorized «Siam River


## `mixed_capital_en`

_Mixed SWIFT + USDT — conditional route_

### Turn 1 — PASS
- User: 'I have SWIFT and USDT mixed'
- Intent: `mixed` · mode: `purchase_pitch_template`
- Tools: `['consult_knowledge_search', 'consult_knowledge_search', 'developer_hub_snapshot', 'supplier_contrast_snapshot', 'scenario_hint:mixed-capital-route']`
- Reply: Landmark Sukhumvit Tower (demo): reserve with Bangkok Landmark Group; pay only the developer-authorized payee on the verified feed. USDT is amber capital — do not send crypto to an agent wallet. Bank review, conversion evidence, then FET-ready escrow. Why bank rails: verified developer feed, authorized payee, escrow, FET for freehold, Land Department registration, Closing Passport before release. Payee gap: agent «SRL Holding 2026 Co., Ltd.» vs authorized «Siam Riverside Living Co., Ltd.». Demo 

## Recommended tuning

- Prefer `consult_kb` RAG filter for project_faq (no synthetic project JSON in replies).
- Villa requests → honest Bangkok luxury condo inventory (Landmark Sukhumvit), not Phuket villas.
- Session-aware retrieval query for follow-ups («what do you have and where?»).
- WhatsApp: `_sanitize_reply()` max 1200 chars, no JSON leak.

## Related

- [`CONSULT_KNOWLEDGE_DEMO.md`](CONSULT_KNOWLEDGE_DEMO.md)
- [`WHATSAPP_CONSULT_DEMO.md`](WHATSAPP_CONSULT_DEMO.md)
