# Requirements and verification traceability

| Requirement | Implemented component | Evidence | Remaining gap |
|---|---|---|---|
| REQ-01 local reproducibility | Dockerfile, compose, README | pytest and smoke | hashed lock and image digest |
| REQ-02 typed ticket intake | POST /v1/tickets | test_tenant_isolation_and_idempotency | signed upstream webhook |
| REQ-03 tenant-scoped reads | SQL WHERE tenant=? | test_tenant_isolation_and_idempotency | verified OIDC claims, RLS |
| REQ-04 deterministic safe abstention | route() | test_abstains | AI retrieval evaluation |
| REQ-05 approval segregation | /v1/actions/* | test_approval_and_denials | approval TTL and real identity |
| REQ-06 audit evidence | /v1/audit | test_approval_and_denials | immutable export, retention |
| REQ-07 safe startup | config() | explicit fail-closed check | prod auth implementation |
| REQ-08 release controls | GitHub Actions CI | CI after GitHub push | SAST, SBOM, image scanning |
| REQ-09 AI grounding | not implemented | no evidence | retrieval and model gateway |
| REQ-10 infrastructure rollout | not implemented | no evidence | Terraform, EKS, Argo CD |
