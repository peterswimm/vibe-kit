# Event Agent Innovation Kit — Roadmap

**Last Updated**: November 21, 2025

## Vision
Enable event attendees to build personalized itineraries using AI-driven recommendation scoring with Graph/SharePoint integration, adaptive card UX, and Microsoft 365 Agents SDK hosting.

---

## Maturity Tiers

### ✅ **Foundation** (Completed)
**Goal**: Core logic + local CLI demo + SDK scaffold.

**Features**:
- ✅ Scoring engine (interest match, popularity, diversity)
- ✅ Conflict-aware itinerary builder
- ✅ Mock session data seed
- ✅ Adaptive Card output with Explain action buttons
- ✅ File + Blob profile storage fallback
- ✅ Structured telemetry (success/error/latency)
- ✅ CLI runner + SDK hosting scaffold
- ✅ Auth wrapper (MSAL client credentials)

**Exit Criteria**: Non-engineer runs recommend locally, saves profile, sees adaptive card with actions.

---

### 🎯 **MVP** (Current Sprint — Today)
**Goal**: Live Graph data + authoring + hosted agent ready for first users.

**Features**:
- [ ] Pydantic Settings config layer (env validation, feature flags)
- [ ] Real `fetch_sessions()` from SharePoint List or Graph Calendar
- [ ] Session cache layer (memory + TTL refresh)
- [ ] Auto-load user profile in explain card action handler
- [ ] Real `publish_itinerary()` with SharePoint Pages API + permalink
- [ ] Enhanced telemetry: Graph call duration, cache hit ratio, publish outcome
- [ ] Token scope refinement (Sites.Read.All, Calendars.Read)
- [ ] Error messages with remediation hints (missing scopes, expired tokens)

**Exit Criteria**: 
- Hosted agent responds with live event sessions from Graph.
- User clicks "Explain #1" → handler loads interests → returns explanation.
- Itinerary published to SharePoint page with returned URL.
- Telemetry tracks Graph latency & publish success.

**Timeline**: Complete today (6–8 hours focused work).

---

### 🚀 **Integrated** (Next 2 Weeks)
**Goal**: Production-ready reliability + observability.

**Features**:
- [ ] Multi-profile management (named profiles + weighting)
- [ ] Graph retry logic + circuit breaker
- [ ] Calendar free/busy conflict resolution (personal schedule check)
- [ ] Cosmos/Table storage for user history + sessions cache
- [ ] Centralized config validation (raise on missing required env vars)
- [ ] Unit + integration test suite (scoring, Graph mapping, hosted message)
- [ ] Adaptive Card follow-up for explain responses (not just JSON string)
- [ ] Telemetry correlation IDs for distributed tracing
- [ ] Token caching + refresh automation (MSAL cache persistence)

**Exit Criteria**:
- Agent handles Graph outages gracefully (fallback to cached sessions).
- Personalized recommendations show measurable improvement.
- Test suite >80% coverage on core logic.
- Telemetry exported to dashboard (e.g. Azure Monitor, Grafana).

---

### 🏢 **Advanced** (Month 2–3)
**Goal**: Scale, personalization, compliance.

**Features**:
- [ ] Semantic similarity scoring (embeddings for interests → sessions)
- [ ] Interest decay weighting (recent interests boost)
- [ ] Async itinerary batch generation (background task queue)
- [ ] Differential privacy for aggregate interest analytics
- [ ] Audit trail (recommendation decisions → blob storage)
- [ ] Performance profiling (memory, latency optimization)
- [ ] Multi-tenant config (per-organization Graph tenants)
- [ ] Progressive rollout via feature flags (canary deployment)

**Exit Criteria**:
- Agent operates as multi-tenant service with SLOs (p95 latency <500ms).
- Semantic matching shows 15%+ uplift in user satisfaction metrics.
- Governance controls meet enterprise compliance requirements.

---

### 🌍 **Enterprise** (Month 4+)
**Goal**: Global scale + full observability + security hardening.

**Features**:
- [ ] Horizontal scaling (container orchestration, load balancer)
- [ ] Distributed cache (Redis) for sessions + profiles
- [ ] OpenTelemetry integration (traces, metrics, logs)
- [ ] Role-based authoring restrictions (publish only for authorized users)
- [ ] Data retention policy automation
- [ ] Multi-region deployment for latency optimization
- [ ] Cost optimization (Graph call throttling, precompute caches)
- [ ] Security scan automation (SAST, dependency vulnerability checks)

**Exit Criteria**:
- Agent handles 10K+ concurrent users with <1% error rate.
- Observability dashboard tracks SLOs in real time.
- Security posture validated via penetration testing.

---

## MVP Implementation Plan (Today)

### Phase 1: Config Foundation (45 min)
**Files**: `settings.py`, update `graph_sources.py`, `auth.py`, `run_agent.py`

1. Create Pydantic `Settings` class with Graph creds, storage options, feature flags.
2. Validate env vars on startup; fail fast with clear error messages.
3. Add `ENABLE_GRAPH_FETCH` and `ENABLE_SHAREPOINT_PUBLISH` flags.

### Phase 2: Graph Session Fetch (90 min)
**Files**: `graph_sources.py`, `activities.py`, new `session_cache.py`

1. Implement Graph Calendar API call (List Events endpoint).
2. Map JSON response → Session model (title, start, end, tags, popularity).
3. Add in-memory cache with 15-minute TTL.
4. Fallback to MOCK_SESSIONS if Graph call fails or flag disabled.
5. Log cache hit/miss + Graph call latency to telemetry.

### Phase 3: Explain Action Auto-Profile (30 min)
**Files**: `event_handler.py`, `storage.py`

1. Extract user ID from turn_context in card action handler.
2. Load last-saved profile for that user (or use empty interests).
3. Return explanation with profile context noted in telemetry.

### Phase 4: SharePoint Itinerary Publish (90 min)
**Files**: `graph_sources.py`, `activities.py`

1. Implement POST to SharePoint Pages API (create new page).
2. Format itinerary as markdown/HTML body.
3. Return permalink in result JSON.
4. Add publish latency + outcome to telemetry.
5. Feature flag guard: skip if `ENABLE_SHAREPOINT_PUBLISH=false`.

### Phase 5: Enhanced Telemetry (30 min)
**Files**: `integration_telemetry.py`, all callers

1. Add `graph_latency_ms`, `cache_hit`, `publish_url` fields.
2. Update handler + activities to populate new fields.

### Phase 6: End-to-End Test (45 min)
**Files**: new `test_mvp.py` smoke test script

1. Verify recommend with Graph sessions (mock Graph response).
2. Simulate card action explain with auto-loaded profile.
3. Validate publish returns URL.
4. Assert telemetry file contains expected fields.

**Total Estimate**: ~6 hours focused work.

---

## Success Metrics

### MVP
- [ ] Graph session fetch success rate >95%
- [ ] Recommend latency p95 <2s
- [ ] Profile auto-load works for card actions
- [ ] Publish success rate >90%
- [ ] Telemetry captures all key fields

### Integrated
- [ ] Cache hit ratio >70%
- [ ] Error rate <2%
- [ ] Interest match score uplift >10% vs random baseline
- [ ] Test coverage >80%

### Advanced
- [ ] Semantic similarity uplift >15%
- [ ] p95 latency <500ms
- [ ] Multi-tenant config validated across 3+ orgs

### Enterprise
- [ ] Concurrent users >10K
- [ ] SLO adherence >99.5%
- [ ] Security audit passed

---

## Open Questions
- **Session data source**: SharePoint List vs Graph Calendar vs custom API?
- **Authoring target**: SharePoint Pages vs OneNote vs Planner cards?
- **Profile persistence**: Per-user Blob JSON vs Cosmos entity per profile?
- **Telemetry sink**: JSONL files vs Azure Monitor vs OpenTelemetry collector?

**Decision Point**: Resolve after MVP validation with first 10 users.

---

## Team & Roles
- **MVP**: 1 backend engineer (full-stack Python + Graph)
- **Integrated**: +0.5 DevOps (hosting, observability)
- **Advanced**: +1 data engineer (embeddings, personalization)
- **Enterprise**: +1 security/compliance specialist

---

## Risk Mitigation
- **Graph API rate limits**: Implement cache + exponential backoff.
- **Token expiration mid-request**: Use MSAL cache + refresh logic.
- **SharePoint authoring permissions**: Validate scopes early; surface clear errors.
- **Scope creep**: Lock MVP features; defer embeddings and multi-tenant until post-MVP validation.

---

## Next Immediate Actions (Starting Now)
1. ✅ Create this roadmap doc
2. Implement `settings.py` config layer
3. Build real `fetch_sessions()` with Graph
4. Wire auto-profile loading in explain handler
5. Implement SharePoint publish
6. Test end-to-end MVP flow

**Let's ship the MVP today.** 🚀
