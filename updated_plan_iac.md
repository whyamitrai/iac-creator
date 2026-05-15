# PATH B — Real Multi-Agent Rebuild

> **AI INSTRUCTIONS:** This is the build plan for upgrading IaC Creator from RAG demo to a true multi-agent system that backs the resume claims.
> 1. Read this file FIRST when working on Path B
> 2. Then read iac-creator/CONTEXT.md for current state
> 3. Compare current date with "Last Updated" in LIVE STATE
> 4. **NEVER write code for the user. Guide, review, correct — user types every line.**
> 5. **No AI-vomit allowed.** If user can't explain a line in interview, the line shouldn't exist.
> 6. Update LIVE STATE after every session.

---

## LIVE STATE

```
Last Updated     : 2026-05-16
Phase Status     : Not started — planning complete
Current Phase    : Phase 1 (Diagram parsing)
Hours Logged     : 0 / ~70 estimated
Target Finish    : 2026-06-21 (5 weekends from May 16)
Blockers         : None
Next Action      : Pick a Saturday. Start Phase 1, Step 1.
```

---


## What "True Multi-Agent IaC" Means

```
            ┌─────────────────────────────┐
            │  Architecture Diagram (PNG) │
            └──────────────┬──────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Vision Parser      │
                │ (Claude Sonnet/Llava)│
                │  → JSON of           │
                │    components +      │
                │    relationships     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Supervisor Agent   │
                │ Routes by component  │
                │ type to specialists  │
                └──────────┬───────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌────────────┐ ┌────────────┐ ┌────────────┐
    │  Compute   │ │  Storage   │ │ Networking │
    │ Specialist │ │ Specialist │ │ Specialist │
    │ (EC2,ECS,  │ │ (S3,RDS,   │ │ (VPC,SG,   │
    │  Lambda)   │ │  DDB)      │ │  Subnets)  │
    │ Own RAG    │ │ Own RAG    │ │ Own RAG    │
    └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                ┌──────────────────────┐
                │   Composer Agent     │
                │ Stitches into single │
                │ Terraform module set │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Validator Agent    │
                │ terraform validate   │
                │ terraform plan       │
                │ ↻ loops back on fail │
                └──────────┬───────────┘
                           │
                           ▼
                  Deployable Terraform
```

---

## Phase 1 — Diagram Input Layer (Weekend 1)

### Goal
Take an architecture diagram image, return structured JSON of components.

### Decisions To Make
1. **Vision model.** Two options:
   - **AWS Bedrock Claude Sonnet** (anthropic.claude-3-sonnet) — strong vision, but costs money per call.
   - **Ollama Llava 1.6** — free, local, weaker accuracy.
   - **Recommendation:** Build with Llava for dev (free), add Bedrock toggle in config. This proves multi-LLM architecture in the resume.

2. **Component schema.** Decide before coding. Suggested:
   ```python
   {
     "components": [
       {"id": "c1", "type": "ec2", "name": "web_server", "specs": {"instance_type": "t3.medium"}},
       {"id": "c2", "type": "rds", "name": "users_db", "specs": {"engine": "postgres"}},
     ],
     "relationships": [
       {"from": "c1", "to": "c2", "type": "connects_to"},
     ]
   }
   ```

### What To Build
- `backend/vision/parser.py` — single function that takes image path, calls vision LLM with structured output prompt, returns parsed JSON.
- Pydantic models for the schema (validation matters).
- 3 test diagrams in `test_data/diagrams/` (you draw these yourself in draw.io or excalidraw — keep it simple: 3-tier web app, microservices with queue, serverless API).
- `tests/test_parser.py` — at minimum, asserts each test diagram returns expected components.

### Definition of Done
- [ ] Image goes in, JSON comes out for all 3 test diagrams.
- [ ] Llava local works.
- [ ] Bedrock toggle works (even if Bedrock untested due to no payment method — code path exists).
- [ ] Tests pass.
- [ ] You can explain in interview: prompt engineering choices, why structured output matters, where this would fail in production.

### Common Failure Modes (Watch For These)
- Vision model hallucinates components that aren't in diagram. Mitigate with strict JSON schema enforcement.
- LLM returns malformed JSON. Use `json_repair` library or retry-with-feedback pattern.
- Same diagram returns different JSON each call. Set temperature=0.

---

## Phase 2 — Multi-Agent Skeleton with Supervisor (Weekend 2)

### Goal
Supervisor routes components to specialists. Each specialist has its own RAG corpus.

### Decisions To Make
1. **Supervisor pattern.** LangGraph supports this natively. Use `langgraph.prebuilt.create_supervisor` OR build manually with conditional edges. **Recommendation:** Build manually. You'll understand it deeper, and `create_supervisor` is too magical for an interview where you'll be asked "show me where routing happens."

2. **Specialist communication.** Two patterns:
   - **Shared state** (all agents read/write to same TypedDict). Simpler, less isolation.
   - **Message passing** (each specialist returns its piece, supervisor aggregates). More realistic, harder.
   - **Recommendation:** Shared state for v1. Note the tradeoff in your README.

3. **RAG corpus per specialist.** Each specialist needs its own ChromaDB collection. Compute specialist gets EC2/ECS/Lambda docs only — not networking. Reduces noise, improves retrieval.

### What To Build
- `backend/agents/supervisor.py` — routing logic. Inspects parsed JSON, determines which specialists to invoke, in what order.
- `backend/agents/compute_specialist.py` — handles EC2, ECS, Lambda. Has its own retriever pointing to compute-specific Chroma collection.
- `backend/agents/storage_specialist.py` — S3, RDS, DynamoDB.
- `backend/agents/networking_specialist.py` — VPC, subnets, security groups, IGW.
- `backend/rag/corpora/` — separate folders, separate ingest commands. Add `make ingest-all` or a script.
- `backend/rag/sources/` — actual HashiCorp Terraform docs (clone from `hashicorp/terraform-provider-aws` docs/, or scrape `registry.terraform.io/providers/hashicorp/aws/latest/docs`). Replace your single `naming_conventions.md`.
- Update `graph.py` — supervisor as entry, specialists as parallel nodes, fan-in for composer.

### Definition of Done
- [ ] Parsed JSON for "3-tier web app" diagram routes to compute + storage + networking specialists.
- [ ] Each specialist returns Terraform code for its own components (just code blocks, not yet composed).
- [ ] Each specialist actually retrieves from its own RAG (verify with print/log).
- [ ] You can draw the LangGraph DAG on a whiteboard from memory.
- [ ] You can answer: "Why didn't you make storage and compute one agent?"

### Common Failure Modes
- Supervisor tries to route everything to one specialist. Test routing logic in isolation first.
- Specialists hallucinate components not in their input. Strict input filtering — supervisor passes only relevant components.
- Token bloat from large RAG retrievals. Set `k=3` not `k=10`.

---

## Phase 3 — Composer + Validator with Self-Heal (Weekend 3)

### Goal
Stitch specialist outputs into single deployable Terraform. Validate. Loop back on failure.

### Decisions To Make
1. **Validation method.** Options:
   - `terraform validate` only — catches syntax + basic schema.
   - `terraform plan` — catches more (requires AWS creds, can fail on missing creds even if code is right).
   - **Recommendation:** Validate primary, plan optional with try/except.

2. **Self-heal loop limit.** Infinite loop = death. Cap at 3 retries.

3. **Composer scope.** Does the composer just concatenate? Or does it create a `modules/` structure with `main.tf`, `variables.tf`, `outputs.tf` per module? Latter is harder but matches what real Terraform looks like. **Recommendation:** Modules structure. Yes it's more work. It's also what makes the resume claim "with proper modules" actually true.

### What To Build
- `backend/agents/composer.py` — takes specialist outputs, organizes into module structure, generates root `main.tf` that calls modules.
- `backend/agents/validator.py` — runs `terraform init && terraform validate` in subprocess, parses errors.
- `backend/agents/healer.py` (or extend supervisor) — on validation failure, sends error back to relevant specialist with context "this is what you produced, this is what failed, fix it."
- Update graph: add validator node, add conditional edge `validate_passed → END`, `validate_failed → router_to_specialist`.
- Retry counter in state. Hard cap.

### Definition of Done
- [ ] Generated Terraform actually parses and `terraform validate` passes.
- [ ] Output has proper module structure: `modules/compute/`, `modules/storage/`, `modules/networking/`, root `main.tf`.
- [ ] Intentionally break something in a specialist prompt — verify validator catches it, healer fixes it within 3 retries, or fails gracefully.
- [ ] You can answer in interview: "What if your healer creates an infinite loop of incorrect fixes?"

---

## Phase 4 — Polish for Portfolio (Weekend 4-5)

### Goal
Make this look like a real project, not a homework assignment. This is the weekend that actually generates calls.

### What To Build
- **Real demo video** — 90-second Loom. You drawing a diagram, uploading, watching it go through agents, showing the validated Terraform output. Embed in README.
- **Streamlit upgrade** — diagram upload (file picker), JSON preview, agent execution log streaming, generated Terraform with download button.
- **5 worked examples** in `examples/` folder. Each has: input diagram (PNG), parsed JSON, generated Terraform, validation log. Reference these in README.
- **Architecture diagram in README** — the box-and-arrow diagram from this file. Use Mermaid (renders on GitHub natively) or excalidraw export.
- **Bedrock path tested** — at minimum, code path. Ideally with one real Bedrock call (use AWS credits if you can, otherwise a friend's AWS account for one test).
- **Tests** — pytest covering each agent in isolation + 1 end-to-end test with a mocked LLM.
- **Proper README rewrite:**
  - Hero section: problem, solution, demo gif/video link.
  - "What makes this different" — explicitly call out: multi-agent, self-healing, vision input, separate RAG corpora.
  - Quickstart (≤5 commands).
  - Architecture deep dive (the diagram).
  - "How I built it" section — your design decisions, tradeoffs you considered, what you'd do differently. **This is what recruiters read.**
  - Roadmap (what's next: Bedrock production, more component types, drift detection).
- **GitHub polish** — pinned repo on profile, topics: `langgraph`, `multi-agent`, `terraform`, `aws-bedrock`, `rag`, `vision-llm`. Star count doesn't matter, presentation does.
- **LinkedIn post** the day you finish. Technical post, not "look at my project." Format: "Why I switched from a single-LLM IaC generator to a multi-agent supervisor pattern (and what broke when I did)." 4-5 paragraphs. Link the repo at the end.

### Definition of Done
- [ ] Stranger can clone repo, run `docker-compose up`, see it work in under 5 minutes.
- [ ] Stranger reading the README understands what makes this different in under 90 seconds.
- [ ] LinkedIn post live.
- [ ] Resume Stage 2 rewrite done with this repo as backing proof.

---

## Final Deliverables Checklist

After all phases complete, you should have:

- [ ] Public GitHub repo with green CI badge
- [ ] 90-second demo video linked in README
- [ ] Working Streamlit demo (locally, or deployed to Streamlit Cloud — free tier)
- [ ] 5 example diagrams + outputs committed to repo
- [ ] Mermaid architecture diagram in README
- [ ] Tests passing in CI
- [ ] Docker Compose works end-to-end
- [ ] At least one technical LinkedIn post about the build
- [ ] Resume updated with defensible claims that map to actual code in this repo
- [ ] You can give a 5-minute walkthrough of the architecture from memory

---

## Hard Rules

1. **You write every line.** AI assists with syntax errors, debugging, conceptual questions. AI does not generate functions, classes, or files for you. If a recruiter asks "walk me through `supervisor.py` line 47," you must have written line 47 yourself.

2. **No skipping definition of done.** Tempting to ship Phase 2 without proper testing because "it kinda works." Don't. Each phase must hit DoD before next phase starts.

3. **Commit small, commit often.** Green squares matter for recruiter optics. Daily commits during build weekends.

4. **One LinkedIn technical post per phase completed.** Document the build. People watch.

5. **Don't let Phase 4 slide.** 80% of candidates ship a half-broken project with no README. Phase 4 is what separates this from being just another GitHub repo. The polish is the entire point.

6. **If stuck for >2 hours**, ask AI for conceptual help, not code. "Explain how to handle parallel node execution in LangGraph" not "write the code for parallel execution."

---

## Time Reality Check

```
Phase 1 (Diagram parsing)         : ~12-15 hours
Phase 2 (Supervisor + specialists): ~18-22 hours
Phase 3 (Composer + validator)    : ~15-18 hours
Phase 4 (Polish + portfolio)      : ~12-15 hours
                                    ─────────────
Total                             : ~60-70 hours
```

5 weekends × 10-12 hours/weekend = 50-60 hours.
Plus weekday evenings: 30 min × 5 days × 5 weeks = 12.5 hours.
**Total available: ~62-72 hours. Matches estimate.**

This means: if you skip even one weekend, the build slides into July. Job hunt gets weaker for that month. Don't slide.

---

## Session Log

| Date | Phase | What Happened | Hours |
|------|-------|--------------|-------|
| 2026-05-16 | Planning | Path B plan written. Decisions deferred to start of each phase. | 0 |

---

## How To Resume

1. `git pull`
2. Tell AI: "read iac-creator/PATH_B_PLAN.md and continue from current phase"
3. AI checks LIVE STATE → knows current phase
4. Open the relevant Phase section, find next unchecked DoD item
5. Build → review → check off → update LIVE STATE → commit
