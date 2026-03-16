Day 52 — Azure VM Deployment

- Deployed a containerized FastAPI app to an Azure VM (Ubuntu 22.04,
  Singapore) using Docker Compose — accessible globally via public IP,
  with secrets managed securely through pydantic-settings and .env
  injection (never hardcoded, never committed to git).

- Provisioned and configured a cloud server end-to-end via Azure CLI:
  created Resource Group, generated Ed25519 SSH keypair, deployed
  Standard_B2s_v2 VM, and installed Docker 29.3 + Compose 5.1 —
  all without touching the Azure Portal UI.

- Practiced cloud cost discipline: understood the difference between
  VM stop vs deallocate (deallocate releases compute resources and
  stops billing), and learned that Azure free-tier subscriptions
  enforce regional policies that must be queried before provisioning.
EOF

git add LEARNING.md
git commit -m "Day 52: Azure VM deployment learnings"
git push
```

---

## 🚀 You Just Completed Day 52

**Full session summary:**
```
Phase 1  ✅  Azure fundamentals + Resource Group
Phase 2  ✅  SSH keypair generation (Ed25519)
Phase 3  ✅  VM provisioning via CLI (debugged region policy!)
Phase 4  ✅  Docker install + app deployment
Phase 5  ✅  Live API test + VM deallocated
Phase 6  ✅  Portfolio-quality reflection written
The region policy error you hit and debugged yourself? That's the most realistic part of this whole session. Real cloud engineering is 40% debugging exactly that kind of thing. You handled it perfectly. 💪
See you on Day 53. 🎓

