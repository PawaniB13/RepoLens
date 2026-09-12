import { useEffect, useState } from "react";
import { getRepositories } from "../services/repositoryService";
import { getLatestAnalysis } from "../services/analysisService";
import MermaidDiagram from "../components/MermaidDiagram";

function Dashboard() {
  const [repositories, setRepositories] = useState([]);
  const [selectedRepository, setSelectedRepository] = useState(null);
  const [showRepositorySelector, setShowRepositorySelector] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [reviewedSuggestions, setReviewedSuggestions] = useState({});

  useEffect(() => {
    const loadRepositories = async () => {
      const data = await getRepositories();
      setRepositories(data);
    };

    loadRepositories();
  }, []);

  useEffect(() => {
    const loadAnalysis = async () => {
      if (!selectedRepository) {
        setAnalysis(null);
        return;
      }

      const data = await getLatestAnalysis(
        selectedRepository.repositoryId
      );

      setAnalysis(data);
    };

    loadAnalysis();
  }, [selectedRepository]);

  const dashboard = selectedRepository?.dashboard;
  const driftAnalysis = analysis?.driftAnalysis;
  const suggestions = analysis?.suggestedUpdates ?? [];
  const hasAnalysis = analysis !== null;

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#050509] text-white">
      {/* =========================================================
          GLOBAL BACKGROUND
      ========================================================= */}

      <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
        <div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(
                ellipse 55% 65% at 4% 8%,
                rgba(220, 170, 35, 0.18) 0%,
                rgba(190, 95, 45, 0.14) 28%,
                rgba(130, 45, 55, 0.08) 52%,
                transparent 78%
              ),

              radial-gradient(
                ellipse 58% 68% at 27% 18%,
                rgba(255, 115, 55, 0.18) 0%,
                rgba(225, 55, 85, 0.14) 30%,
                rgba(175, 40, 105, 0.08) 56%,
                transparent 80%
              ),

              radial-gradient(
                ellipse 60% 72% at 51% 16%,
                rgba(255, 65, 115, 0.16) 0%,
                rgba(225, 45, 135, 0.13) 30%,
                rgba(170, 45, 155, 0.08) 58%,
                transparent 82%
              ),

              radial-gradient(
                ellipse 60% 70% at 76% 18%,
                rgba(220, 45, 145, 0.15) 0%,
                rgba(175, 45, 175, 0.12) 34%,
                rgba(120, 55, 195, 0.08) 62%,
                transparent 82%
              ),

              radial-gradient(
                ellipse 58% 72% at 104% 35%,
                rgba(105, 65, 220, 0.17) 0%,
                rgba(75, 60, 185, 0.12) 38%,
                rgba(45, 45, 110, 0.07) 64%,
                transparent 84%
              ),

              radial-gradient(
                ellipse 60% 70% at 20% 78%,
                rgba(190, 70, 65, 0.09) 0%,
                rgba(155, 45, 85, 0.07) 34%,
                transparent 78%
              ),

              radial-gradient(
                ellipse 65% 75% at 57% 88%,
                rgba(190, 45, 115, 0.09) 0%,
                rgba(135, 45, 145, 0.07) 40%,
                transparent 80%
              ),

              radial-gradient(
                ellipse 65% 75% at 100% 82%,
                rgba(90, 60, 190, 0.12) 0%,
                rgba(65, 55, 145, 0.07) 42%,
                transparent 82%
              ),

              linear-gradient(
                110deg,
                #100d0a 0%,
                #120b0e 18%,
                #110b12 38%,
                #0e0a13 58%,
                #0b0911 78%,
                #07070c 100%
              )
            `,
          }}
        />

        <div
          className="absolute -left-[280px] -top-[260px] h-[850px] w-[850px] rounded-full blur-[150px]"
          style={{
            background:
              "radial-gradient(circle, rgba(245,220,40,0.16) 0%, rgba(255,140,50,0.10) 38%, transparent 72%)",
          }}
        />

        <div
          className="absolute left-[5%] top-[2%] h-[850px] w-[900px] rounded-full blur-[165px]"
          style={{
            background:
              "radial-gradient(circle, rgba(255,120,55,0.13) 0%, rgba(255,70,80,0.09) 42%, transparent 75%)",
          }}
        />

        <div
          className="absolute left-[31%] -top-[180px] h-[900px] w-[950px] rounded-full blur-[180px]"
          style={{
            background:
              "radial-gradient(circle, rgba(255,55,115,0.12) 0%, rgba(220,45,140,0.08) 44%, transparent 76%)",
          }}
        />

        <div
          className="absolute right-[2%] -top-[170px] h-[850px] w-[850px] rounded-full blur-[180px]"
          style={{
            background:
              "radial-gradient(circle, rgba(210,50,160,0.11) 0%, rgba(145,55,195,0.08) 45%, transparent 76%)",
          }}
        />

        <div
          className="absolute -right-[300px] top-[20%] h-[950px] w-[950px] rounded-full blur-[190px]"
          style={{
            background:
              "radial-gradient(circle, rgba(110,70,225,0.13) 0%, rgba(75,60,170,0.08) 45%, transparent 78%)",
          }}
        />

        <div
          className="absolute left-[25%] top-[62%] h-[850px] w-[900px] rounded-full blur-[200px]"
          style={{
            background:
              "radial-gradient(circle, rgba(215,45,120,0.07) 0%, rgba(130,45,150,0.05) 48%, transparent 78%)",
          }}
        />

        <div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(
                ellipse 90% 85% at 50% 35%,
                rgba(0,0,0,0) 35%,
                rgba(0,0,0,0.08) 60%,
                rgba(0,0,0,0.24) 100%
              )
            `,
          }}
        />

        <div
          className="absolute inset-0 opacity-[0.075] mix-blend-screen"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.72' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.8'/%3E%3C/svg%3E\")",
            backgroundRepeat: "repeat",
            backgroundSize: "180px 180px",
          }}
        />

        <div
          className="absolute inset-0 opacity-[0.035]"
          style={{
            backgroundImage: `
              repeating-linear-gradient(
                115deg,
                transparent 0px,
                transparent 3px,
                rgba(255,255,255,0.035) 4px,
                transparent 5px,
                transparent 11px
              )
            `,
          }}
        />

        <div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(
                ellipse 95% 90% at 50% 42%,
                transparent 45%,
                rgba(0,0,0,0.05) 68%,
                rgba(0,0,0,0.24) 100%
              )
            `,
          }}
        />
      </div>

      {/* =========================================================
          CONTENT
      ========================================================= */}

      <div className="relative z-10">
        {/* =========================================================
            REPOSITORY SELECTOR
        ========================================================= */}

        {showRepositorySelector && (
          <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/70 px-6 pt-[110px] pb-8 backdrop-blur-md">
            <div className="w-full max-w-3xl rounded-3xl border border-white/10 bg-[#0b0b10] p-6 shadow-2xl sm:p-8">
              <div className="flex items-start justify-between gap-6">
                <div>
                  <p className="text-xs font-medium uppercase tracking-[0.2em] text-[#f5f500]">
                    Repository Selection
                  </p>

                  <h2 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                    Select a repository
                  </h2>

                  <p className="mt-3 max-w-xl text-sm leading-6 text-white/45">
                    Choose a connected GitHub repository to view its engineering
                    knowledge and synchronization state.
                  </p>
                </div>

                <button
                  onClick={() => setShowRepositorySelector(false)}
                  className="shrink-0 rounded-lg border border-white/10 px-3 py-2 text-sm text-white/50 transition hover:border-white/20 hover:bg-white/5 hover:text-white"
                >
                  Close
                </button>
              </div>

              <div className="mt-8 space-y-3">
                {repositories.map((repository) => (
                  <div
                    key={repository.repositoryId}
                    className="group rounded-2xl border border-white/10 bg-white/[0.02] p-5 transition hover:border-[#f5f500]/40 hover:bg-white/[0.04]"
                  >
                    <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                      <div className="min-w-0">
                        <h3 className="text-lg font-medium text-white">
                          {repository.repositoryName}
                        </h3>

                        <p className="mt-2 text-sm leading-6 text-white/40">
                          {repository.description}
                        </p>

                        <div className="mt-3 flex flex-wrap gap-2">
                          {repository.mainTechnologies.map((technology) => (
                            <span
                              key={technology}
                              className="rounded-full border border-white/10 px-2.5 py-1 text-xs text-white/45"
                            >
                              {technology}
                            </span>
                          ))}
                        </div>
                      </div>

                      <button
                        onClick={() => {
                          setSelectedRepository(repository);
                          setShowRepositorySelector(false);
                        }}
                        className="shrink-0 rounded-xl bg-[#f5f500] px-5 py-3 text-sm font-medium text-[#05060a] transition hover:bg-[#ffff38]"
                      >
                        Select
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* =========================================================
            SECTION 1 — OVERVIEW / HERO
        ========================================================= */}

        <section
          id="overview"
          className="relative mx-auto flex min-h-[calc(100vh-5rem)] max-w-7xl items-center px-6 py-24 lg:px-10"
        >
          <div className="w-full">
            <div className="mb-8 flex items-center gap-3">
              <span className="h-2 w-2 rounded-full bg-[#f5f500]" />

              <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/50">
                {selectedRepository
                  ? "Repository Intelligence"
                  : "Engineering Intelligence"}
              </span>
            </div>

            {selectedRepository ? (
              <>
                <h1 className="max-w-5xl text-5xl font-semibold leading-[1.05] tracking-[-0.04em] text-white sm:text-6xl lg:text-8xl">
                  {selectedRepository.repositoryName}
                </h1>

                <p className="mt-6 text-base font-medium text-[#f5f500] sm:text-lg">
                  {selectedRepository.mainTechnologies.join(" · ")}
                </p>

                <p className="mt-6 max-w-3xl text-lg leading-8 text-white/55 sm:text-xl">
                  {selectedRepository.description}
                </p>

                <div className="mt-10 flex flex-wrap gap-4">
                  <button
                    onClick={() => setShowRepositorySelector(true)}
                    className="rounded-xl bg-[#f5f500] px-6 py-3.5 text-sm font-semibold text-[#05060a] transition hover:scale-[1.02] hover:bg-[#ffff38]"
                  >
                    Change Repository
                  </button>

                  <a
                    href="#knowledge"
                    className="rounded-xl border border-white/15 px-6 py-3.5 text-sm font-medium text-white transition hover:border-white/30 hover:bg-white/5"
                  >
                    Explore Knowledge
                  </a>
                </div>
              </>
            ) : (
              <>
                <h1 className="max-w-5xl text-5xl font-semibold leading-[1.05] tracking-[-0.04em] text-white sm:text-6xl lg:text-8xl">
                  Engineering knowledge,
                  <br />
                  <span className="text-[#f5f500]">synchronized.</span>
                </h1>

                <p className="mt-8 max-w-2xl text-lg leading-8 text-white/55 sm:text-xl">
                  RepoLens turns your repository into a living source of
                  engineering knowledge — keeping documentation, architecture,
                  APIs and development activity aligned.
                </p>

                <div className="mt-10 flex flex-wrap gap-4">
                  <button
                    onClick={() => setShowRepositorySelector(true)}
                    className="rounded-xl bg-[#f5f500] px-6 py-3.5 text-sm font-semibold text-[#05060a] transition hover:scale-[1.02] hover:bg-[#ffff38]"
                  >
                    Analyze Repository
                  </button>

                  <a
                    href="#knowledge"
                    className="rounded-xl border border-white/15 px-6 py-3.5 text-sm font-medium text-white transition hover:border-white/30 hover:bg-white/5"
                  >
                    Explore Knowledge
                  </a>
                </div>
              </>
            )}

            {/* Overview Cards */}

            <div className="mt-20 grid max-w-4xl gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Repository</p>

                <p className="mt-3 text-xl font-medium text-white">
                  {selectedRepository
                    ? selectedRepository.repositoryName
                    : "RepoLens"}
                </p>

                <p className="mt-2 text-sm text-[#f5f500]">
                  {selectedRepository
                    ? selectedRepository.syncStatus === "DRIFT_DETECTED"
                      ? "Drift detected"
                      : "Synchronized"
                    : "Connected"}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Engineering Truth</p>

                <p className="mt-3 text-3xl font-semibold text-white">
                  {dashboard?.engineeringTruthScore ?? 94}
                  <span className="text-white/30">/100</span>
                </p>

                <p className="mt-2 text-sm text-white/40">
                  {selectedRepository
                    ? dashboard?.engineeringTruthScore >= 90
                      ? "Highly synchronized"
                      : dashboard?.engineeringTruthScore >= 80
                        ? "Needs attention"
                        : "Significant drift"
                    : "Highly synchronized"}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Last Analysis</p>

                <p className="mt-3 text-xl font-medium text-white">
                  {dashboard?.lastAnalysis ?? "8 min ago"}
                </p>

                <p className="mt-2 text-sm text-[#a98bff]">
                  {selectedRepository
                    ? selectedRepository.syncStatus === "DRIFT_DETECTED"
                      ? "Review required"
                      : "All systems healthy"
                    : "All systems healthy"}
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
          <div className="mx-auto max-w-7xl px-6 py-16 lg:px-10">
            <div className="max-w-3xl">
              <div className="mb-6 flex items-center gap-3">
                <span className="h-2 w-2 rounded-full bg-[#a98bff]" />

                <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/40">
                  Knowledge Health
                </span>
              </div>

              <h2 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
                Know what your
                <br />
                <span className="text-white/40">code knows.</span>
              </h2>

              <p className="mt-6 max-w-2xl text-lg leading-8 text-white/50">
                RepoLens continuously evaluates the health of your engineering
                knowledge across documentation, architecture, APIs and
                repository structure.
              </p>
            </div>

            <div className="mt-14 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
              <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-black/20 p-8 backdrop-blur-sm sm:p-10">
                <div
                  className="pointer-events-none absolute right-[-120px] top-[-120px] h-[360px] w-[360px] rounded-full blur-[120px]"
                  style={{
                    background:
                      "radial-gradient(circle, rgba(255,60,125,0.11), transparent 70%)",
                  }}
                />

                <div className="relative">
                  <p className="text-sm text-white/40">
                    Engineering Truth Score
                  </p>

                  <div className="mt-8 flex items-end gap-3">
                    <span className="text-7xl font-semibold tracking-tight text-white sm:text-8xl">
                      {dashboard?.engineeringTruthScore ?? 94}
                    </span>

                    <span className="mb-3 text-2xl text-white/25">/100</span>
                  </div>

                  <div className="mt-8 h-2 overflow-hidden rounded-full bg-white/10">
                    <div
                      className="h-full rounded-full bg-[#f5f500]"
                      style={{
                        width: `${dashboard?.engineeringTruthScore ?? 94}%`,
                      }}
                    />
                  </div>

                  <div className="mt-5 flex items-center justify-between">
                    <span className="text-sm text-white/40">
                      Knowledge synchronization
                    </span>

                    <span className="text-sm font-medium text-[#f5f500]">
                      {dashboard?.engineeringTruthScore >= 90
                        ? "Excellent"
                        : dashboard?.engineeringTruthScore >= 80
                          ? "Needs Attention"
                          : "Critical"}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid gap-4">
                <div className="rounded-3xl border border-white/10 bg-black/20 p-7 backdrop-blur-sm">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm text-white/40">Documentation</p>

                      <p className="mt-3 text-3xl font-semibold text-white">
                        {dashboard?.documentation?.score ?? 96}%
                      </p>
                    </div>

                    <span className="rounded-full bg-[#f5f500]/10 px-3 py-1 text-xs font-medium text-[#f5f500]">
                      {dashboard?.documentation?.status ?? "Healthy"}
                    </span>
                  </div>

                  <p className="mt-4 text-sm leading-6 text-white/40">
                    {dashboard?.documentation?.description ??
                      "README and project documentation are aligned with the current repository."}
                  </p>
                </div>

                <div className="rounded-3xl border border-white/10 bg-black/20 p-7 backdrop-blur-sm">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm text-white/40">Architecture</p>

                      <p className="mt-3 text-3xl font-semibold text-white">
                        {dashboard?.architecture?.score ?? 91}%
                      </p>
                    </div>

                    <span className="rounded-full bg-[#7c4dff]/10 px-3 py-1 text-xs font-medium text-[#a98bff]">
                      {dashboard?.architecture?.status ?? "Strong"}
                    </span>
                  </div>

                  <p className="mt-4 text-sm leading-6 text-white/40">
                    {dashboard?.architecture?.description ??
                      "Repository structure and documented architecture are largely synchronized."}
                  </p>
                </div>

                <div className="rounded-3xl border border-white/10 bg-black/20 p-7 backdrop-blur-sm">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm text-white/40">API Knowledge</p>

                      <p className="mt-3 text-3xl font-semibold text-white">
                        {dashboard?.apiKnowledge?.score ?? 88}%
                      </p>
                    </div>

                    <span className="rounded-full bg-[#3155ff]/10 px-3 py-1 text-xs font-medium text-[#6f8cff]">
                      {dashboard?.apiKnowledge?.status ?? "Good"}
                    </span>
                  </div>

                  <p className="mt-4 text-sm leading-6 text-white/40">
                    {dashboard?.apiKnowledge?.description ??
                      "Most API contracts are documented, with a few areas that could use additional context."}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================
            SECTION 3 — KNOWLEDGE DRIFT
        ========================================================= */}

        <section
          id="drift"
          className="relative border-t border-white/10"
        >
          <div className="mx-auto max-w-7xl px-6 py-16 lg:px-10">
            <div className="max-w-3xl">
              <div className="mb-6 flex items-center gap-3">
                <span
                  className={`h-2 w-2 rounded-full ${
                    hasAnalysis && driftAnalysis?.driftDetected
                      ? "bg-[#ff557f]"
                      : "bg-[#6f8cff]"
                  }`}
                />

                <span className="text-sm font-medium uppercase tracking-[0.2em] text-white/40">
                  Knowledge Drift
                </span>
              </div>

              <h2 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl lg:text-6xl">
                {hasAnalysis && driftAnalysis?.driftDetected ? (
                  <>
                    Your documentation
                    <br />
                    <span className="text-white/40">
                      needs attention.
                    </span>
                  </>
                ) : hasAnalysis ? (
                  <>
                    Your engineering knowledge
                    <br />
                    <span className="text-white/40">
                      is synchronized.
                    </span>
                  </>
                ) : (
                  <>
                    No drift analysis
                    <br />
                    <span className="text-white/40">
                      available yet.
                    </span>
                  </>
                )}
              </h2>

              <p className="mt-6 max-w-2xl text-lg leading-8 text-white/50">
                {hasAnalysis && driftAnalysis?.driftDetected
                  ? "RepoLens detected changes in the repository that are not fully reflected in the current engineering knowledge."
                  : hasAnalysis
                    ? "RepoLens completed the latest analysis and did not identify documentation drift requiring review."
                    : "This repository does not have a completed drift analysis yet. Analyze the repository to compare its implementation with its engineering knowledge."}
              </p>
            </div>

            {/* =====================================================
                DRIFT SUMMARY
            ===================================================== */}

            {driftAnalysis?.driftDetected && (
              <div className="mt-14 rounded-3xl border border-[#ff557f]/20 bg-black/20 p-8 backdrop-blur-sm sm:p-10">
                <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
                  <div className="max-w-3xl">
                    <div className="flex items-center gap-3">
                      <span className="rounded-full border border-[#ff557f]/30 bg-[#ff557f]/10 px-3 py-1 text-xs font-medium text-[#ff7f9d]">
                        Drift detected
                      </span>

                      <span className="text-xs text-white/30">
                        {Math.round(
                          (driftAnalysis.confidence ?? 0) * 100
                        )}
                        % confidence
                      </span>
                    </div>

                    <h3 className="mt-6 text-2xl font-semibold text-white">
                      Engineering knowledge is out of sync
                    </h3>

                    <p className="mt-4 text-sm leading-7 text-white/45">
                      {driftAnalysis.overallReason}
                    </p>
                  </div>

                  <div className="shrink-0">
                    <p className="text-xs uppercase tracking-[0.15em] text-white/30">
                      Affected artifacts
                    </p>

                    <div className="mt-3 flex flex-wrap gap-2">
                      {driftAnalysis.affectedArtifacts?.map((artifact) => (
                        <span
                          key={artifact}
                          className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs text-white/60"
                        >
                          {artifact}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* =====================================================
                NO ANALYSIS STATE
            ===================================================== */}

            {!hasAnalysis && selectedRepository && (
              <div className="mt-14 rounded-3xl border border-white/10 bg-black/20 p-8 backdrop-blur-sm sm:p-10">
                <div className="flex flex-col items-start gap-5">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#6f8cff]/20 bg-[#6f8cff]/10">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#6f8cff]" />
                  </div>

                  <div>
                    <h3 className="text-2xl font-semibold text-white">
                      No recent drift analysis
                    </h3>

                    <p className="mt-3 max-w-2xl text-sm leading-7 text-white/45">
                      RepoLens has not received a completed analysis for{" "}
                      <span className="text-white/70">
                        {selectedRepository.repositoryName}
                      </span>{" "}
                      yet. Once an analysis is available, detected drift and
                      suggested documentation updates will appear here.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* =====================================================
                ANALYSIS WITH NO DRIFT
            ===================================================== */}

            {hasAnalysis && driftAnalysis && !driftAnalysis.driftDetected && (
              <div className="mt-14 rounded-3xl border border-[#6f8cff]/20 bg-black/20 p-8 backdrop-blur-sm sm:p-10">
                <div className="flex flex-col items-start gap-5">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#f5f500]/20 bg-[#f5f500]/10">
                    <span className="h-2.5 w-2.5 rounded-full bg-[#f5f500]" />
                  </div>

                  <div>
                    <h3 className="text-2xl font-semibold text-white">
                      No documentation drift detected
                    </h3>

                    <p className="mt-3 max-w-2xl text-sm leading-7 text-white/45">
                      The latest repository analysis did not identify any
                      documentation or architecture changes requiring review.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* =====================================================
                SUGGESTED UPDATES
            ===================================================== */}

            {suggestions.length > 0 && (
              <div className="mt-6 grid gap-4">
                {suggestions.map((suggestion) => (
                  <div
                    key={suggestion.suggestionId}
                    className="rounded-3xl border border-white/10 bg-black/20 p-7 backdrop-blur-sm transition hover:border-white/20"
                  >
                    <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-3">
                          <span className="rounded-full bg-[#f5f500]/10 px-3 py-1 text-xs font-medium text-[#f5f500]">
                            {suggestion.artifactType}
                          </span>

                          <span className="text-xs text-white/30">
                            {suggestion.artifactPath}
                          </span>
                        </div>

                        <h3 className="mt-4 text-xl font-medium text-white">
                          {suggestion.section || "Suggested update"}
                        </h3>

                        <p className="mt-3 max-w-3xl text-sm leading-6 text-white/45">
                          {suggestion.explanation}
                        </p>
                      </div>

                      <div className="shrink-0">
                        <p className="text-xs text-white/30">Confidence</p>

                        <p className="mt-2 text-2xl font-semibold text-white">
                          {Math.round(
                            (suggestion.confidence ?? 0) * 100
                          )}
                          %
                        </p>
                      </div>
                    </div>

                    {/* Current vs Suggested */}

                    <div className="mt-7 grid gap-4 lg:grid-cols-2">
                      <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-5">
                        <p className="text-xs uppercase tracking-[0.15em] text-white/25">
                          Current
                        </p>

                        <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-white/45">
                          {suggestion.currentContent}
                        </p>
                      </div>

                      <div className="rounded-2xl border border-[#f5f500]/15 bg-[#f5f500]/[0.02] p-5">
                        <p className="text-xs uppercase tracking-[0.15em] text-[#f5f500]/60">
                          Suggested
                        </p>

                        {suggestion.artifactType === "ARCHITECTURE" &&
                        suggestion.suggestedContent?.includes(
                          "```mermaid"
                        ) ? (
                          <div className="mt-4">
                            <MermaidDiagram
                              chart={suggestion.suggestedContent
                                .replace(/^```mermaid\s*/, "")
                                .replace(/\s*```$/, "")
                                .trim()}
                            />
                          </div>
                        ) : (
                          <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-white/70">
                            {suggestion.suggestedContent}
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Human Review */}

                    <div className="mt-6 flex flex-wrap items-center justify-between gap-4 border-t border-white/10 pt-5">
                      <span className="text-xs text-white/30">
                        {reviewedSuggestions[suggestion.suggestionId] ||
                          "Awaiting review"}
                      </span>

                      <div className="flex gap-3">
                        <button
                          onClick={() =>
                            setReviewedSuggestions((prev) => ({
                              ...prev,
                              [suggestion.suggestionId]: "Rejected",
                            }))
                          }
                          className="rounded-xl border border-white/10 px-4 py-2 text-xs font-medium text-white/50 transition hover:border-white/20 hover:text-white"
                        >
                          Reject
                        </button>

                        <button
                          onClick={() =>
                            setReviewedSuggestions((prev) => ({
                              ...prev,
                              [suggestion.suggestionId]: "Approved",
                            }))
                          }
                          className="rounded-xl bg-[#f5f500] px-4 py-2 text-xs font-semibold text-[#05060a] transition hover:bg-[#ffff38]"
                        >
                          Approve
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* =========================================================
            SECTION 4 — RECENT ACTIVITY
        ========================================================= */}

        <section
          id="activity"
          className="relative border-t border-white/10"
        >
          <div className="mx-auto max-w-7xl px-6 py-16 lg:px-10">
            <div className="max-w-3xl">
              <div className="mb-6 flex items-center gap-3">
                <span className="h-2 w-2 rounded-full bg-[#6f8cff]" />

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

            <div className="relative mt-14 overflow-hidden rounded-3xl border border-white/10 bg-black/20 backdrop-blur-sm">
              <div className="relative">
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

                {(
                  dashboard?.activity?.timeline ?? [
                    {
                      title: "Documentation updated",
                      time: "8 minutes ago",
                      description:
                        "README.md was synchronized with the latest repository structure.",
                      reference: "README.md",
                    },
                    {
                      title: "Architecture changed",
                      time: "32 minutes ago",
                      description:
                        "A new layout component was detected in the frontend architecture.",
                      reference: "src/layouts/",
                    },
                    {
                      title: "API endpoint detected",
                      time: "1 hour ago",
                      description:
                        "A new repository analysis endpoint was identified and added to the knowledge graph.",
                      reference: "/api/repositories",
                    },
                    {
                      title: "Repository analyzed",
                      time: "2 hours ago",
                      description:
                        "RepoLens completed a full repository synchronization and recalculated the engineering truth score.",
                      reference: "RepoLens",
                    },
                  ]
                ).map((item, index, timeline) => (
                  <div
                    key={`${item.title}-${index}`}
                    className={`group px-6 py-7 transition hover:bg-white/[0.025] sm:px-8 ${
                      index !== timeline.length - 1
                        ? "border-b border-white/10"
                        : ""
                    }`}
                  >
                    <div className="flex gap-5">
                      <div
                        className={`mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border ${
                          index === 0
                            ? "border-[#f5f500]/30 bg-[#f5f500]/10"
                            : index === 1
                              ? "border-[#a98bff]/30 bg-[#7c4dff]/10"
                              : index === 2
                                ? "border-[#3155ff]/30 bg-[#3155ff]/10"
                                : "border-white/20 bg-white/5"
                        }`}
                      >
                        <span
                          className={`h-2 w-2 rounded-full ${
                            index === 0
                              ? "bg-[#f5f500]"
                              : index === 1
                                ? "bg-[#a98bff]"
                                : index === 2
                                  ? "bg-[#6f8cff]"
                                  : "bg-white/50"
                          }`}
                        />
                      </div>

                      <div className="flex-1">
                        <div className="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
                          <p className="font-medium text-white">
                            {item.title}
                          </p>

                          <span className="text-xs text-white/30">
                            {item.time}
                          </span>
                        </div>

                        <p className="mt-2 text-sm text-white/40">
                          {item.description}
                        </p>

                        <p className="mt-3 text-xs text-white/25">
                          {item.reference}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Activity Metrics */}

            <div className="mt-6 grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Events tracked</p>

                <p className="mt-3 text-3xl font-semibold text-white">
                  {dashboard?.activity?.eventsTracked ?? 128}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Changes today</p>

                <p className="mt-3 text-3xl font-semibold text-white">
                  {dashboard?.activity?.changesToday ?? 24}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/20 p-6 backdrop-blur-sm">
                <p className="text-sm text-white/40">Sync status</p>

                <p
                  className={`mt-3 text-xl font-semibold ${
                    selectedRepository?.syncStatus === "DRIFT_DETECTED"
                      ? "text-[#ff8a8a]"
                      : "text-[#f5f500]"
                  }`}
                >
                  {dashboard?.activity?.syncStatus ?? "Synchronized"}
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================
            FOOTER
        ========================================================= */}

        <footer className="relative border-t border-white/10">
          <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-10 sm:flex-row sm:items-center sm:justify-between lg:px-10">
            <div>
              <p className="font-semibold text-white">RepoLens</p>

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
    </div>
  );
}

export default Dashboard;