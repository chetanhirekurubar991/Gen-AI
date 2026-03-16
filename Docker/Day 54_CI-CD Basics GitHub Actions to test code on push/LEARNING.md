# 🚀 Gen AI DevOps Learning Journal — Chetan Hirekurubar

---

## Day 54 — CI/CD with GitHub Actions
**Stack:** FastAPI · Docker · PostgreSQL · Azure VM · GitHub Actions

---

### ✅ What I Built Today

A **full CI/CD pipeline** that automatically tests, builds, and deploys my FastAPI app to Azure VM every time I push to `main`.

```
git push → pytest → docker build → SSH deploy to Azure VM
```

---

### 📚 3 Key Learnings

- **`needs: test` creates a dependency chain between jobs.**
  If pytest fails, the docker-build job is automatically skipped — saving compute minutes and preventing broken code from ever reaching the Docker build stage. This is how real pipelines protect production.

- **Secrets must never be hardcoded in `ci.yml`.**
  The `ci.yml` file is public — anyone on the internet can read it. Credentials like SSH keys and VM IPs must be stored in GitHub Secrets (encrypted) and referenced as `${{ secrets.SECRET_NAME }}`. Hardcoding secrets is a critical security vulnerability that can lead to data breaches.

- **CI and CD are two separate responsibilities in the same pipeline.**
  CI (Continuous Integration) continuously checks every code change — it installs dependencies, runs tests, and builds Docker images to verify nothing is broken. CD (Continuous Deployment) only runs after CI passes — it takes the verified code and automatically deploys it to the live Azure VM. This separation means broken code can never reach real users.

---

### 🔧 Debugging I Did Today

| Problem | Root Cause | Fix Applied |
|---------|-----------|-------------|
| Workflow failed on first run | `.env` file missing on GitHub's Ubuntu machine | Added default values to `config.py` |
| Tests passed locally but not in CI | GitHub machine is a blank slate — no `.env` | Used `pydantic-settings` defaults |
| Docker build path issue | Folder name has spaces | Added `working-directory` to workflow |

---

### 🔗 Connections to Previous Days

- **Day 51 (Env Vars):** GitHub Secrets are the CI/CD equivalent of `.env` — never committed, always injected at runtime.
- **Day 52 (Logging):** Tests verify app behavior; logs verify app health. Both are observability tools.
- **Day 53 (Azure VM):** The deployment target — CI/CD automates what we did manually on Day 53.

---

### 🎯 Interview Answer Drilled Today

**Q: Why is CI/CD critical for GenAI applications?**

> In GenAI apps, bugs aren't just crashes — they're subtle behavior changes like prompt regressions or model output drift. CI/CD pipelines can run automated evaluation tests that catch these silent failures before they reach users. This is why companies like Anthropic require CI/CD gates before any merge to main.

---

### 📁 Files Created Today

```
.github/
  workflows/
    ci.yml          ← Full pipeline: test → docker-build → deploy
test_main.py        ← Automated FastAPI tests with TestClient
```

---

### 💰 Cost Check

- GitHub Actions free tier: **2,000 mins/month**
- Used today: ~10 minutes
- Remaining: ~1,990 minutes ✅

---

*Next: Day 55 — Monitoring & Observability*