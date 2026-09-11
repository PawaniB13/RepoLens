export const mockRepositories = [
  {
    repositoryId: "repolens-backend",
    repositoryName: "RepoLens Backend",
    repositoryUrl: "https://github.com/example/repolens-backend",
    defaultBranch: "main",

    description:
      "Spring Boot backend responsible for GitHub integration, business logic, and repository analysis orchestration.",

    mainTechnologies: ["Java", "Spring Boot", "PostgreSQL"],

    architectureType: "Layered Architecture",

    syncStatus: "SYNCHRONIZED",

    lastAnalyzedCommit: "a8f42c1",
    lastAnalysisTimestamp: "2026-09-07T08:42:00Z",

    dashboard: {
      engineeringTruthScore: 94,

      documentation: {
        score: 96,
        status: "Healthy",
        description:
          "README and project documentation are aligned with the current repository."
      },

      architecture: {
        score: 91,
        status: "Strong",
        description:
          "Repository structure and documented architecture are largely synchronized."
      },

      apiKnowledge: {
        score: 88,
        status: "Good",
        description:
          "Most API contracts are documented, with a few areas that could use additional context."
      },

      lastAnalysis: "8 min ago",

      activity: {
        eventsTracked: 128,
        changesToday: 24,
        syncStatus: "Synchronized",

        timeline: [
          {
            title: "Documentation updated",
            time: "8 minutes ago",
            description:
              "README.md was synchronized with the latest repository structure.",
            reference: "README.md"
          },
          {
            title: "Architecture changed",
            time: "32 minutes ago",
            description:
              "A new service component was detected in the backend architecture.",
            reference: "src/services/"
          },
          {
            title: "API endpoint detected",
            time: "1 hour ago",
            description:
              "A new repository analysis endpoint was identified and added to the engineering knowledge.",
            reference: "/api/v1/analyze"
          },
          {
            title: "Repository analyzed",
            time: "2 hours ago",
            description:
              "RepoLens completed a full repository synchronization and recalculated the engineering truth score.",
            reference: "RepoLens Backend"
          }
        ]
      }
    }
  },

  {
    repositoryId: "repolens-ai-service",
    repositoryName: "RepoLens AI Service",
    repositoryUrl: "https://github.com/example/repolens-ai-service",
    defaultBranch: "main",

    description:
      "FastAPI AI service responsible for code parsing, context construction, semantic reasoning, and knowledge drift detection.",

    mainTechnologies: ["Python", "FastAPI", "Tree-sitter"],

    architectureType: "AI Service",

    syncStatus: "DRIFT_DETECTED",

    lastAnalyzedCommit: "f31d92a",
    lastAnalysisTimestamp: "2026-09-07T07:18:00Z",

    dashboard: {
      engineeringTruthScore: 82,

      documentation: {
        score: 78,
        status: "Needs Attention",
        description:
          "Some AI-service documentation does not fully reflect the current implementation."
      },

      architecture: {
        score: 84,
        status: "Moderate",
        description:
          "The documented AI-service architecture has drift in a few implementation areas."
      },

      apiKnowledge: {
        score: 86,
        status: "Good",
        description:
          "The analysis API is well documented, with some recently changed behavior requiring review."
      },

      lastAnalysis: "1 hour ago",

      activity: {
        eventsTracked: 96,
        changesToday: 17,
        syncStatus: "Drift detected",

        timeline: [
          {
            title: "Knowledge drift detected",
            time: "12 minutes ago",
            description:
              "Repository implementation differs from the documented AI-service behavior.",
            reference: "Drift Analysis"
          },
          {
            title: "Context builder changed",
            time: "28 minutes ago",
            description:
              "Changes were detected in repository context construction.",
            reference: "context/context_builder.py"
          },
          {
            title: "Tree-sitter parser updated",
            time: "52 minutes ago",
            description:
              "Repository parsing behavior changed and requires documentation verification.",
            reference: "parsers/"
          },
          {
            title: "Repository analyzed",
            time: "1 hour ago",
            description:
              "RepoLens completed analysis of the AI service and detected knowledge drift.",
            reference: "RepoLens AI Service"
          }
        ]
      }
    }
  },

  {
    repositoryId: "repolens-frontend",
    repositoryName: "RepoLens Frontend",
    repositoryUrl: "https://github.com/example/repolens-frontend",
    defaultBranch: "main",

    description:
      "React frontend for repository intelligence, knowledge health, drift review, and documentation updates.",

    mainTechnologies: ["React", "Vite", "Tailwind CSS"],

    architectureType: "Component-Based Architecture",

    syncStatus: "SYNCHRONIZED",

    lastAnalyzedCommit: "c72b11e",
    lastAnalysisTimestamp: "2026-09-07T06:55:00Z",

    dashboard: {
      engineeringTruthScore: 89,

      documentation: {
        score: 92,
        status: "Healthy",
        description:
          "Frontend documentation is largely aligned with the current component structure."
      },

      architecture: {
        score: 87,
        status: "Strong",
        description:
          "The documented component architecture closely matches the current frontend implementation."
      },

      apiKnowledge: {
        score: 83,
        status: "Good",
        description:
          "Most frontend API integrations are documented, with some areas requiring additional detail."
      },

      lastAnalysis: "2 hours ago",

      activity: {
        eventsTracked: 114,
        changesToday: 21,
        syncStatus: "Synchronized",

        timeline: [
          {
            title: "Dashboard updated",
            time: "18 minutes ago",
            description:
              "Repository selection functionality was added to the dashboard.",
            reference: "src/pages/Dashboard.jsx"
          },
          {
            title: "Layout component changed",
            time: "42 minutes ago",
            description:
              "Frontend layout structure was updated.",
            reference: "src/layouts/"
          },
          {
            title: "API integration detected",
            time: "1 hour ago",
            description:
              "Repository service integration was detected in the frontend.",
            reference: "src/services/"
          },
          {
            title: "Repository analyzed",
            time: "2 hours ago",
            description:
              "RepoLens completed analysis of the frontend repository.",
            reference: "RepoLens Frontend"
          }
        ]
      }
    }
  }
];