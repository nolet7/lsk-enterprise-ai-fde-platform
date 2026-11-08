# Senior FDE interview defense outline

1. **Mandate:** What was the CTO asking? Which metric mattered, and who owned it?
2. **Discovery:** How did stakeholder interviews change scope? What was explicitly excluded?
3. **Architecture:** Why use explicit trust boundaries, durable events, and access-aware retrieval?
4. **Reproducibility:** Demonstrate a clone, isolated installation, tests, deterministic API call and negative security tests.
5. **Security:** Explain why local fake headers are NOT an enterprise IAM solution; show the production mitigation backlog.
6. **Failure scenario:** Replay an identical event, attempt cross-tenant access, attempt self-approval and unapproved execution; show blocked responses.
7. **AI:** Explain why a deterministic baseline is tested before adding an LLM and why model outputs cannot directly authorize tools.
8. **Pilot:** Present a credible experiment plan with human-adjudicated labels and measured costs.
9. **Production:** Explain the hard gates and demonstrate architecture, rollback, recovery and incident workflows only when implemented.
10. **Handover:** Show how customers assume reliable ownership, including runbooks and API contract versioning.

Never claim that target-only features are implemented or that fictional KPIs were achieved.
