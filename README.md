## en-AI Prompt Orchestration App (Local Dev)

A production-grade SaaS foundation with a dense UI, visual pipeline editor, multi-tenant data model, and mocked orchestration/billing.

### Stack
- Next.js 14 (App Router, TS), Tailwind + shadcn-style UI, Lucide
- Prisma + PostgreSQL (local), NextAuth (credentials + magic link preview)
- React Query, Zustand (later), React Flow, Recharts
- SSE for run logs (stub), Stripe test mode (stub)

### Prereqs
- Node 18+ (or 20+)
- pnpm or npm
- PostgreSQL 15/16 (or Supabase local)

### Setup
```bash
pnpm install
cp .env.example .env
# Edit DATABASE_URL, NEXTAUTH_* and optional Stripe/Pusher

pnpm prisma migrate dev --name init
pnpm prisma db seed
pnpm dev
# open http://localhost:3000 and Sign in with:
# email: owner@enai.local, password: password
```

### Notes
- Magic link email provider logs links to the server console.
- Seed includes orgs, users, projects, pipelines, runs, prompts, datasets, integrations, credits.
- UI pages scaffolded; editor and orchestrator stubs to follow.
