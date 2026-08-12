function Dashboard() {
  return (
    <div className="relative overflow-hidden">

      {/* =========================================================
    BACKGROUND ATMOSPHERE
    Yellow → Orange → Pink → Purple
========================================================= */}
<div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">

  {/* Yellow */}
  <div className="absolute left-[-15%] top-[-10%] h-[750px] w-[750px] rounded-full bg-[#f5f500]/25 blur-[120px]" />

  {/* Orange */}
  <div className="absolute left-[10%] top-[-8%] h-[700px] w-[800px] rounded-full bg-[#ff7a3d]/35 blur-[125px]" />

  {/* Pink */}
  <div className="absolute left-[35%] top-[-5%] h-[700px] w-[800px] rounded-full bg-[#ff3d81]/32 blur-[135px]" />

  {/* Magenta */}
  <div className="absolute right-[0%] top-[0%] h-[700px] w-[700px] rounded-full bg-[#e83eaa]/28 blur-[140px]" />

  {/* Purple */}
  <div className="absolute right-[-15%] top-[20%] h-[750px] w-[750px] rounded-full bg-[#7c4dff]/25 blur-[150px]" />

  {/* Orange / pink lower left */}
  <div className="absolute left-[-15%] top-[45%] h-[650px] w-[700px] rounded-full bg-[#ff5c35]/18 blur-[150px]" />

  {/* Pink lower right */}
  <div className="absolute right-[-5%] top-[55%] h-[700px] w-[700px] rounded-full bg-[#ff4d6d]/20 blur-[160px]" />

</div>

      {/* =========================================================
          SECTION 1 — OVERVIEW / HERO
      ========================================================= */}
      <section
        id="overview"
        className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-7xl items-center px-6 py-24 lg:px-10"
      >
        <div className="w-full">

          <div className="mb-8 flex items-center gap-3">
            <span className="h-2 w-2 rounded-full bg-[#f5f500]" />

            <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/50">
              Engineering Intelligence
            </span>
          </div>


          <h1 className="max-w-5xl text-5xl font-semibold leading-[1.05] tracking-[-0.04em] text-white sm:text-6xl lg:text-8xl">
            Engineering knowledge,
            <br />
            <span className="text-[#f5f500]">
              synchronized.
            </span>
          </h1>


          <p className="mt-8 max-w-2xl text-lg leading-8 text-white/55 sm:text-xl">
            RepoLens turns your repository into a living source of
            engineering knowledge — keeping documentation, architecture,
            APIs and development activity aligned.
          </p>


          <div className="mt-10 flex flex-wrap gap-4">

            <button className="rounded-xl bg-[#f5f500] px-6 py-3.5 text-sm font-semibold text-[#05060a] transition hover:scale-[1.02] hover:bg-[#ffff38]">
              Analyze Repository
            </button>

            <a
              href="#knowledge"
              className="rounded-xl border border-white/15 px-6 py-3.5 text-sm font-medium text-white transition hover:border-white/30 hover:bg-white/5"
            >
              Explore Knowledge
            </a>

          </div>


          <div className="mt-20 grid max-w-4xl gap-4 sm:grid-cols-3">

            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-sm">
              <p className="text-sm text-white/40">
                Repository
              </p>

              <p className="mt-3 text-xl font-medium text-white">
                RepoLens
              </p>

              <p className="mt-2 text-sm text-[#f5f500]">
                Connected
              </p>
            </div>


            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-sm">
              <p className="text-sm text-white/40">
                Engineering Truth
              </p>

              <p className="mt-3 text-3xl font-semibold text-white">
                94<span className="text-white/30">/100</span>
              </p>

              <p className="mt-2 text-sm text-white/40">
                Highly synchronized
              </p>
            </div>


            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-sm">
              <p className="text-sm text-white/40">
                Last Analysis
              </p>

              <p className="mt-3 text-xl font-medium text-white">
                8 min ago
              </p>

              <p className="mt-2 text-sm text-[#7c4dff]">
                All systems healthy
              </p>
            </div>

          </div>

        </div>
      </section>


      {/* =========================================================
          SECTION 2 — KNOWLEDGE HEALTH
      ========================================================= */}
      <section
        id="knowledge"
        className="relative border-t border-white/10"
      >
        <div className="mx-auto max-w-7xl px-6 py-12 lg:px-10">

          <div className="max-w-3xl">

            <div className="mb-6 flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-[#7c4dff]" />

              <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/40">
                Knowledge Health
              </span>
            </div>

            <h2 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Know what your
              <br />
              <span className="text-white/40">
                code knows.
              </span>
            </h2>

            <p className="mt-6 max-w-2xl text-lg leading-8 text-white/50">
              RepoLens continuously evaluates the health of your engineering
              knowledge across documentation, architecture, APIs and
              repository structure.
            </p>

          </div>


          <div className="mt-12 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">

            <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-8 sm:p-10">

              <div className="pointer-events-none absolute right-[-100px] top-[-100px] h-[300px] w-[300px] rounded-full bg-[#ff3d81]/15 blur-[100px]" />

              <div className="relative">

                <p className="text-sm text-white/40">
                  Engineering Truth Score
                </p>

                <div className="mt-8 flex items-end gap-3">
                  <span className="text-7xl font-semibold tracking-tight text-white sm:text-8xl">
                    94
                  </span>

                  <span className="mb-3 text-2xl text-white/25">
                    /100
                  </span>
                </div>

                <div className="mt-8 h-2 overflow-hidden rounded-full bg-white/10">
                  <div className="h-full w-[94%] rounded-full bg-[#f5f500]" />
                </div>

                <div className="mt-5 flex items-center justify-between">
                  <span className="text-sm text-white/40">
                    Knowledge synchronization
                  </span>

                  <span className="text-sm font-medium text-[#f5f500]">
                    Excellent
                  </span>
                </div>

              </div>
            </div>


            <div className="grid gap-4">

              <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-7">
                <div className="flex items-start justify-between">

                  <div>
                    <p className="text-sm text-white/40">
                      Documentation
                    </p>

                    <p className="mt-3 text-3xl font-semibold text-white">
                      96%
                    </p>
                  </div>

                  <span className="rounded-full bg-[#f5f500]/10 px-3 py-1 text-xs font-medium text-[#f5f500]">
                    Healthy
                  </span>

                </div>

                <p className="mt-4 text-sm leading-6 text-white/40">
                  README and project documentation are aligned with the
                  current repository.
                </p>
              </div>


              <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-7">
                <div className="flex items-start justify-between">

                  <div>
                    <p className="text-sm text-white/40">
                      Architecture
                    </p>

                    <p className="mt-3 text-3xl font-semibold text-white">
                      91%
                    </p>
                  </div>

                  <span className="rounded-full bg-[#7c4dff]/10 px-3 py-1 text-xs font-medium text-[#a98bff]">
                    Strong
                  </span>

                </div>

                <p className="mt-4 text-sm leading-6 text-white/40">
                  Repository structure and documented architecture are
                  largely synchronized.
                </p>
              </div>


              <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-7">
                <div className="flex items-start justify-between">

                  <div>
                    <p className="text-sm text-white/40">
                      API Knowledge
                    </p>

                    <p className="mt-3 text-3xl font-semibold text-white">
                      88%
                    </p>
                  </div>

                  <span className="rounded-full bg-[#3155ff]/10 px-3 py-1 text-xs font-medium text-[#6f8cff]">
                    Good
                  </span>

                </div>

                <p className="mt-4 text-sm leading-6 text-white/40">
                  Most API contracts are documented, with a few areas that
                  could use additional context.
                </p>
              </div>

            </div>

          </div>

        </div>
      </section>


      {/* =========================================================
          SECTION 3 — ACTIVITY
      ========================================================= */}
      {/* =========================================================
    SECTION 3 — ACTIVITY
========================================================= */}
<section
  id="activity"
  className="relative border-t border-white/10"
>
  {/* Activity glow */}
  <div className="pointer-events-none absolute right-[-200px] top-[100px] h-[600px] w-[600px] rounded-full bg-[#3155ff]/10 blur-[150px]" />

  <div className="mx-auto max-w-7xl px-6 py-12 lg:px-10">

    {/* Section heading */}
    <div className="max-w-3xl">

      <div className="mb-6 flex items-center gap-3">
        <span className="h-2 w-2 rounded-full bg-[#3155ff]" />

        <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/40">
          Recent Activity
        </span>
      </div>

      <h2 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
        See how your
        <br />
        <span className="text-white/40">
          repository evolves.
        </span>
      </h2>

      <p className="mt-6 max-w-2xl text-lg leading-8 text-white/50">
        Follow the changes that shape your engineering knowledge.
        RepoLens keeps repository activity connected to the context
        your team depends on.
      </p>

    </div>


    {/* Activity panel */}
    <div className="relative mt-12 overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">

      {/* Panel glow */}
      <div className="pointer-events-none absolute left-[-150px] top-[-150px] h-[400px] w-[400px] rounded-full bg-[#7c4dff]/10 blur-[120px]" />

      <div className="relative">

        {/* Panel header */}
        <div className="flex items-center justify-between border-b border-white/10 px-6 py-5 sm:px-8">

          <div>
            <p className="text-sm font-medium text-white">
              Repository Timeline
            </p>

            <p className="mt-1 text-xs text-white/35">
              Latest engineering events
            </p>
          </div>

          <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-white/40">
            Live
          </span>

        </div>


        {/* Activity items */}
        <div>

          {/* Item 1 */}
          <div className="group border-b border-white/10 px-6 py-7 transition hover:bg-white/[0.025] sm:px-8">

            <div className="flex gap-5">

              <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-[#f5f500]/30 bg-[#f5f500]/10">
                <span className="h-2 w-2 rounded-full bg-[#f5f500]" />
              </div>

              <div className="flex-1">

                <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">

                  <p className="font-medium text-white">
                    Documentation updated
                  </p>

                  <span className="text-xs text-white/30">
                    8 minutes ago
                  </span>

                </div>

                <p className="mt-2 text-sm text-white/40">
                  README.md was synchronized with the latest repository
                  structure.
                </p>

                <p className="mt-3 text-xs text-white/25">
                  README.md
                </p>

              </div>

            </div>

          </div>


          {/* Item 2 */}
          <div className="group border-b border-white/10 px-6 py-7 transition hover:bg-white/[0.025] sm:px-8">

            <div className="flex gap-5">

              <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-[#7c4dff]/30 bg-[#7c4dff]/10">
                <span className="h-2 w-2 rounded-full bg-[#7c4dff]" />
              </div>

              <div className="flex-1">

                <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">

                  <p className="font-medium text-white">
                    Architecture changed
                  </p>

                  <span className="text-xs text-white/30">
                    32 minutes ago
                  </span>

                </div>

                <p className="mt-2 text-sm text-white/40">
                  A new layout component was detected in the frontend
                  architecture.
                </p>

                <p className="mt-3 text-xs text-white/25">
                  src/layouts/
                </p>

              </div>

            </div>

          </div>


          {/* Item 3 */}
          <div className="group border-b border-white/10 px-6 py-7 transition hover:bg-white/[0.025] sm:px-8">

            <div className="flex gap-5">

              <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-[#3155ff]/30 bg-[#3155ff]/10">
                <span className="h-2 w-2 rounded-full bg-[#3155ff]" />
              </div>

              <div className="flex-1">

                <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">

                  <p className="font-medium text-white">
                    API endpoint detected
                  </p>

                  <span className="text-xs text-white/30">
                    1 hour ago
                  </span>

                </div>

                <p className="mt-2 text-sm text-white/40">
                  A new repository analysis endpoint was identified
                  and added to the knowledge graph.
                </p>

                <p className="mt-3 text-xs text-white/25">
                  /api/repositories
                </p>

              </div>

            </div>

          </div>


          {/* Item 4 */}
          <div className="group px-6 py-7 transition hover:bg-white/[0.025] sm:px-8">

            <div className="flex gap-5">

              <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-white/20 bg-white/5">
                <span className="h-2 w-2 rounded-full bg-white/50" />
              </div>

              <div className="flex-1">

                <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">

                  <p className="font-medium text-white">
                    Repository analyzed
                  </p>

                  <span className="text-xs text-white/30">
                    2 hours ago
                  </span>

                </div>

                <p className="mt-2 text-sm text-white/40">
                  RepoLens completed a full repository synchronization
                  and recalculated the engineering truth score.
                </p>

                <p className="mt-3 text-xs text-white/25">
                  RepoLens
                </p>

              </div>

            </div>

          </div>

        </div>

      </div>
    </div>


    {/* Bottom metric row */}
    <div className="mt-6 grid gap-4 sm:grid-cols-3">

      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <p className="text-sm text-white/40">
          Events tracked
        </p>

        <p className="mt-3 text-3xl font-semibold text-white">
          128
        </p>
      </div>


      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <p className="text-sm text-white/40">
          Changes today
        </p>

        <p className="mt-3 text-3xl font-semibold text-white">
          24
        </p>
      </div>


      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <p className="text-sm text-white/40">
          Sync status
        </p>

        <p className="mt-3 text-xl font-semibold text-[#f5f500]">
          Up to date
        </p>
      </div>

    </div>

  </div>
</section>

      {/* =========================================================
          FOOTER
      ========================================================= */}
      <footer className="border-t border-white/10">

        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-10 sm:flex-row sm:items-center sm:justify-between lg:px-10">

          <div>
            <p className="font-semibold text-white">
              RepoLens
            </p>

            <p className="mt-1 text-sm text-white/35">
              Engineering knowledge, synchronized.
            </p>
          </div>

          <p className="text-xs text-white/25">
            Repository intelligence platform
          </p>

        </div>

      </footer>

    </div>
  )
}

export default Dashboard