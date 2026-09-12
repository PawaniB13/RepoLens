import { useEffect, useRef } from "react";
import mermaid from "mermaid";

function MermaidDiagram({ chart }) {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!chart || !containerRef.current) {
      return;
    }

    const renderDiagram = async () => {
      try {
        mermaid.initialize({
          startOnLoad: false,
          theme: "dark",
          securityLevel: "strict",
        });

        containerRef.current.innerHTML = "";

        const id = `mermaid-${Date.now()}`;

        const { svg } = await mermaid.render(id, chart);

        containerRef.current.innerHTML = svg;
      } catch (error) {
        console.error("Failed to render Mermaid diagram:", error);

        containerRef.current.innerHTML = `
          <div class="rounded-xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-300">
            Unable to render architecture diagram.
          </div>
        `;
      }
    };

    renderDiagram();
  }, [chart]);

  return (
    <div
      ref={containerRef}
      className="flex min-h-[320px] items-center justify-center overflow-x-auto rounded-2xl border border-white/10 bg-black/20 p-6"
    />
  );
}

export default MermaidDiagram;