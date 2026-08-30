import { Bell, ChevronDown } from 'lucide-react'

function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-[#05060a] text-[#f5f5f5] bg-[radial-gradient(circle_at_70%_20%,rgba(88,28,135,0.16),transparent_35%),radial-gradient(circle_at_85%_55%,rgba(30,64,175,0.12),transparent_35%)]">

      {/* Navigation */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-[#05060a]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-10">

          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-[#f5f500] font-black text-[#05060a]">
              R
            </div>

            <span className="text-xl font-semibold tracking-tight">
              RepoLens
            </span>
          </div>

          {/* Navigation */}
          <nav className="hidden items-center gap-8 md:flex">
            <a
              href="#overview"
              className="text-sm text-white transition hover:text-[#f5f500]"
            >
              Overview
            </a>

            <a
              href="#knowledge"
              className="text-sm text-white/60 transition hover:text-[#f5f500]"
            >
              Knowledge
            </a>

            <a
              href="#activity"
              className="text-sm text-white/60 transition hover:text-[#f5f500]"
            >
              Activity
            </a>
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-3">

            {/* Notifications */}
            <button
              className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 text-white/60 transition hover:border-[#f5f500]/50 hover:text-[#f5f500]"
              aria-label="Notifications"
            >
              <Bell size={18} />
            </button>

            {/* GitHub */}
            <button className="hidden items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-sm transition hover:border-white/20 sm:flex">
              <span>GitHub</span>
              <ChevronDown size={15} />
            </button>

          </div>
        </div>
      </header>

      {/* Page Content */}
      <main>{children}</main>

    </div>
  )
}

export default DashboardLayout