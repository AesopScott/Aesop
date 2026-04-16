import { useState } from "react";

// Sample course data from the actual site
const categories = [
  { name: "AI Models", icon: "📡", count: 8, courses: ["The Alignment Problem", "GPT vs. Claude vs. Gemini", "How Large Language Models Work", "Image Generation Models", "Model Evaluation & Benchmarks", "Multimodal Models", "Reinforcement Learning", "Running Models Locally"] },
  { name: "AI Progress", icon: "🔭", count: 9, courses: ["AI Agents in the Wild", "AI in Science", "The Context Window Race", "The Hardware Race", "Multimodal Breakthroughs", "The Reasoning Revolution", "Synthetic Data", "Voice & Real-Time AI", "What's Coming Next"] },
  { name: "Art", icon: "🎨", count: 12, courses: ["AI & Architecture", "AI & the Writer's Voice", "AI for Graphic Design", "AI in Game Design I", "AI in Game Design II", "AI in Game Design III", "AI Music Composition", "AI Video Production", "Performing Arts & AI", "Photography & AI", "Prompt Craft for Visual Art", "Storytelling with AI"] },
  { name: "Business", icon: "💼", count: 10, courses: ["AI & the Future of Work", "AI for Finance & Ops", "AI for Marketing & Growth", "AI for Product Dev", "AI in Customer Service", "AI Risk for Leaders", "AI Tools for Solo Founders", "Building AI-First Business", "Funding AI Ventures", "Procurement & Vendor Eval"] },
  { name: "Development", icon: "⚙️", count: 13, courses: ["AI App Architecture", "AI Security & Red-Teaming", "Building AI Agents I", "Building AI Agents II", "Building AI Agents III", "Building AI Agents IV", "Building AI Agents V", "Building AI Pipelines", "Coding with AI Assistants", "Data Engineering for AI", "Fine-Tuning Models", "Prompt Engineering", "Testing AI Systems"] },
  { name: "Core Courses", icon: "📚", count: 21, courses: ["AI & Climate", "AI & Creativity", "AI & Education", "AI & Finance", "AI & Media", "AI & National Security", "AI Careers & Research", "AI Consciousness", "AI Ethics", "AI Governance", "AI in Healthcare", "AI in Society", "AI Leadership", "AI Privacy & Security", "AI Psychology", "AI Safety & Alignment", "Future of Work", "Applied AI Dev", "Building with AI", "Future of Intelligence", "AI Bias & Fairness"] },
];

const liveStatus = (name) => {
  const live = ["AI Governance", "AI in Society", "AI Ethics", "AI & Education", "AI in Healthcare", "AI Leadership", "Building with AI", "Building AI Agents I", "Building AI Agents II", "Building AI Agents III", "Building AI Agents IV", "Building AI Agents V"];
  return live.some(l => name.includes(l.substring(0, 10)));
};

const gold = "#c9a05a";
const navy = "#0d1b2a";
const darkBg = "#112236";

// ─────────────────────────────────────────────
// OPTION 1: Horizontal pill filters + card grid
// ─────────────────────────────────────────────
const Option1 = () => {
  const [active, setActive] = useState("All");
  const allCats = ["All", ...categories.map(c => c.name)];
  const filtered = active === "All" ? categories : categories.filter(c => c.name === active);
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12, minHeight: 400 }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24 }}>
        {allCats.map(c => (
          <button key={c} onClick={() => setActive(c)} style={{
            padding: "6px 16px", borderRadius: 99, border: `1px solid ${active === c ? gold : "rgba(255,255,255,0.15)"}`,
            background: active === c ? "rgba(201,160,90,0.15)" : "transparent",
            color: active === c ? gold : "rgba(255,255,255,0.6)", fontSize: "0.8rem", fontWeight: 600, cursor: "pointer"
          }}>{c}</button>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 12 }}>
        {filtered.flatMap(cat => cat.courses.map(course => (
          <div key={course} style={{
            background: darkBg, borderRadius: 8, padding: "14px 16px",
            border: `1px solid ${liveStatus(course) ? "rgba(201,160,90,0.3)" : "rgba(255,255,255,0.08)"}`,
            cursor: "pointer", transition: "border-color 0.2s"
          }}>
            <div style={{ fontSize: "0.65rem", color: "rgba(255,255,255,0.35)", marginBottom: 4 }}>{cat.icon} {cat.name}</div>
            <div style={{ fontSize: "0.85rem", color: "#fff", fontWeight: 600 }}>{course}</div>
            {liveStatus(course) && <span style={{ fontSize: "0.6rem", color: "#3dd6c0", marginTop: 6, display: "inline-block" }}>● Live</span>}
            {!liveStatus(course) && <span style={{ fontSize: "0.6rem", color: "rgba(255,255,255,0.25)", marginTop: 6, display: "inline-block" }}>Coming Soon</span>}
          </div>
        )))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 2: Accordion sections
// ─────────────────────────────────────────────
const Option2 = () => {
  const [open, setOpen] = useState("Core Courses");
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12, maxWidth: 700, margin: "0 auto" }}>
      {categories.map(cat => (
        <div key={cat.name} style={{ marginBottom: 2 }}>
          <button onClick={() => setOpen(open === cat.name ? null : cat.name)} style={{
            width: "100%", textAlign: "left", padding: "14px 20px",
            background: open === cat.name ? darkBg : "rgba(255,255,255,0.03)",
            border: "none", borderBottom: "1px solid rgba(255,255,255,0.06)",
            color: open === cat.name ? gold : "rgba(255,255,255,0.7)",
            fontSize: "0.95rem", fontWeight: 700, cursor: "pointer",
            display: "flex", justifyContent: "space-between", alignItems: "center"
          }}>
            <span>{cat.icon} {cat.name}</span>
            <span style={{ fontSize: "0.7rem", opacity: 0.4 }}>{cat.count} courses {open === cat.name ? "▲" : "▼"}</span>
          </button>
          {open === cat.name && (
            <div style={{ background: darkBg, padding: "8px 0" }}>
              {cat.courses.map(c => (
                <div key={c} style={{
                  padding: "8px 24px 8px 40px", fontSize: "0.82rem",
                  color: liveStatus(c) ? "#fff" : "rgba(255,255,255,0.4)",
                  cursor: "pointer", display: "flex", justifyContent: "space-between", alignItems: "center"
                }}>
                  <span>{c}</span>
                  {liveStatus(c) ? <span style={{ fontSize: "0.55rem", color: "#3dd6c0" }}>● LIVE</span> :
                    <span style={{ fontSize: "0.55rem", color: "rgba(255,255,255,0.2)" }}>SOON</span>}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 3: Search + flat list
// ─────────────────────────────────────────────
const Option3 = () => {
  const [q, setQ] = useState("");
  const all = categories.flatMap(cat => cat.courses.map(c => ({ name: c, cat: cat.name, icon: cat.icon })));
  const filtered = q ? all.filter(c => c.name.toLowerCase().includes(q.toLowerCase())) : all;
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
      <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search 73 elective courses..."
        style={{
          width: "100%", padding: "12px 16px", borderRadius: 8, border: `1px solid rgba(255,255,255,0.15)`,
          background: darkBg, color: "#fff", fontSize: "0.9rem", marginBottom: 20, boxSizing: "border-box",
          outline: "none"
        }} />
      <div style={{ maxHeight: 350, overflowY: "auto" }}>
        {filtered.map(c => (
          <div key={c.name + c.cat} style={{
            padding: "10px 16px", display: "flex", justifyContent: "space-between", alignItems: "center",
            borderBottom: "1px solid rgba(255,255,255,0.04)", cursor: "pointer"
          }}>
            <div>
              <div style={{ fontSize: "0.85rem", color: "#fff", fontWeight: 500 }}>{c.name}</div>
              <div style={{ fontSize: "0.65rem", color: "rgba(255,255,255,0.3)" }}>{c.icon} {c.cat}</div>
            </div>
            {liveStatus(c.name) ? <span style={{ fontSize: "0.6rem", color: "#3dd6c0", fontWeight: 700 }}>LIVE →</span> :
              <span style={{ fontSize: "0.6rem", color: "rgba(255,255,255,0.2)" }}>Soon</span>}
          </div>
        ))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 4: Category cards that expand
// ─────────────────────────────────────────────
const Option4 = () => {
  const [expanded, setExpanded] = useState(null);
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
        {categories.map(cat => (
          <div key={cat.name} onClick={() => setExpanded(expanded === cat.name ? null : cat.name)} style={{
            background: darkBg, borderRadius: 10, padding: 20, cursor: "pointer",
            border: `1px solid ${expanded === cat.name ? gold : "rgba(255,255,255,0.08)"}`,
            gridColumn: expanded === cat.name ? "1 / -1" : "auto",
            transition: "all 0.3s"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div style={{ fontSize: "1.5rem", marginBottom: 4 }}>{cat.icon}</div>
                <div style={{ color: gold, fontWeight: 700, fontSize: "0.95rem" }}>{cat.name}</div>
                <div style={{ color: "rgba(255,255,255,0.35)", fontSize: "0.7rem" }}>{cat.count} courses</div>
              </div>
            </div>
            {expanded === cat.name && (
              <div style={{ marginTop: 16, display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 8 }}>
                {cat.courses.map(c => (
                  <div key={c} style={{
                    padding: "8px 12px", background: "rgba(255,255,255,0.03)", borderRadius: 6,
                    fontSize: "0.8rem", color: liveStatus(c) ? "#fff" : "rgba(255,255,255,0.4)",
                    display: "flex", justifyContent: "space-between"
                  }}>
                    {c} {liveStatus(c) && <span style={{ color: "#3dd6c0", fontSize: "0.6rem" }}>●</span>}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 5: Horizontal tabs (top) + grid
// ─────────────────────────────────────────────
const Option5 = () => {
  const [tab, setTab] = useState("Core Courses");
  const cat = categories.find(c => c.name === tab);
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
      <div style={{ display: "flex", gap: 0, borderBottom: `1px solid rgba(255,255,255,0.1)`, marginBottom: 24, overflowX: "auto" }}>
        {categories.map(c => (
          <button key={c.name} onClick={() => setTab(c.name)} style={{
            padding: "10px 18px", border: "none", borderBottom: `2px solid ${tab === c.name ? gold : "transparent"}`,
            background: "transparent", color: tab === c.name ? gold : "rgba(255,255,255,0.5)",
            fontSize: "0.78rem", fontWeight: 600, cursor: "pointer", whiteSpace: "nowrap"
          }}>{c.icon} {c.name}</button>
        ))}
      </div>
      {cat && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: 12 }}>
          {cat.courses.map(c => (
            <div key={c} style={{
              background: darkBg, borderRadius: 8, padding: "16px",
              borderLeft: `3px solid ${liveStatus(c) ? gold : "rgba(255,255,255,0.08)"}`,
              cursor: "pointer"
            }}>
              <div style={{ fontSize: "0.85rem", color: "#fff", fontWeight: 600, marginBottom: 4 }}>{c}</div>
              <div style={{ fontSize: "0.6rem", color: liveStatus(c) ? "#3dd6c0" : "rgba(255,255,255,0.25)" }}>
                {liveStatus(c) ? "● Live — 8 Modules" : "Coming Soon"}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 6: Two-column catalog with sticky sidebar
// ─────────────────────────────────────────────
const Option6 = () => {
  const [active, setActive] = useState("Core Courses");
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12, display: "flex", gap: 24 }}>
      <div style={{ width: 180, flexShrink: 0 }}>
        {categories.map(c => (
          <button key={c.name} onClick={() => setActive(c.name)} style={{
            display: "block", width: "100%", textAlign: "left", padding: "10px 14px",
            background: active === c.name ? "rgba(201,160,90,0.1)" : "transparent",
            border: "none", borderLeft: `3px solid ${active === c.name ? gold : "transparent"}`,
            color: active === c.name ? gold : "rgba(255,255,255,0.5)",
            fontSize: "0.78rem", fontWeight: 600, cursor: "pointer", marginBottom: 2
          }}>{c.icon} {c.name} <span style={{ opacity: 0.4 }}>({c.count})</span></button>
        ))}
      </div>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6 }}>
        <div style={{ fontSize: "1.1rem", color: gold, fontWeight: 700, marginBottom: 8 }}>
          {categories.find(c => c.name === active)?.icon} {active}
        </div>
        {categories.find(c => c.name === active)?.courses.map(c => (
          <div key={c} style={{
            padding: "12px 16px", background: darkBg, borderRadius: 8,
            display: "flex", justifyContent: "space-between", alignItems: "center",
            border: "1px solid rgba(255,255,255,0.05)", cursor: "pointer"
          }}>
            <span style={{ color: "#fff", fontSize: "0.85rem", fontWeight: 500 }}>{c}</span>
            {liveStatus(c) ?
              <span style={{ fontSize: "0.65rem", background: "rgba(61,214,192,0.12)", color: "#3dd6c0", padding: "3px 10px", borderRadius: 99 }}>Live</span> :
              <span style={{ fontSize: "0.65rem", color: "rgba(255,255,255,0.2)" }}>Soon</span>}
          </div>
        ))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 7: Netflix-style horizontal rows
// ─────────────────────────────────────────────
const Option7 = () => (
  <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
    {categories.map(cat => (
      <div key={cat.name} style={{ marginBottom: 28 }}>
        <div style={{ color: "#fff", fontWeight: 700, fontSize: "0.95rem", marginBottom: 10 }}>
          {cat.icon} {cat.name} <span style={{ color: "rgba(255,255,255,0.3)", fontWeight: 400, fontSize: "0.7rem" }}>{cat.count} courses</span>
        </div>
        <div style={{ display: "flex", gap: 10, overflowX: "auto", paddingBottom: 8 }}>
          {cat.courses.map(c => (
            <div key={c} style={{
              minWidth: 180, maxWidth: 180, background: darkBg, borderRadius: 8, padding: "14px 16px",
              border: `1px solid ${liveStatus(c) ? "rgba(201,160,90,0.25)" : "rgba(255,255,255,0.06)"}`,
              cursor: "pointer", flexShrink: 0
            }}>
              <div style={{ fontSize: "0.82rem", color: "#fff", fontWeight: 600, marginBottom: 6 }}>{c}</div>
              {liveStatus(c) ? <span style={{ fontSize: "0.58rem", color: "#3dd6c0" }}>● Live</span> :
                <span style={{ fontSize: "0.58rem", color: "rgba(255,255,255,0.2)" }}>Soon</span>}
            </div>
          ))}
        </div>
      </div>
    ))}
  </div>
);

// ─────────────────────────────────────────────
// OPTION 8: Grouped chips with hover preview
// ─────────────────────────────────────────────
const Option8 = () => {
  const [hovered, setHovered] = useState(null);
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
      {categories.map(cat => (
        <div key={cat.name} style={{ marginBottom: 20 }}>
          <div style={{ color: gold, fontWeight: 700, fontSize: "0.75rem", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 8 }}>
            {cat.icon} {cat.name}
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {cat.courses.map(c => (
              <button key={c}
                onMouseEnter={() => setHovered(c)}
                onMouseLeave={() => setHovered(null)}
                style={{
                  padding: "6px 14px", borderRadius: 6, cursor: "pointer",
                  background: liveStatus(c) ? "rgba(201,160,90,0.12)" : "rgba(255,255,255,0.04)",
                  border: `1px solid ${hovered === c ? gold : liveStatus(c) ? "rgba(201,160,90,0.25)" : "rgba(255,255,255,0.08)"}`,
                  color: liveStatus(c) ? "#fff" : "rgba(255,255,255,0.4)",
                  fontSize: "0.76rem", fontWeight: 500,
                  transform: hovered === c ? "translateY(-2px)" : "none",
                  transition: "all 0.15s"
                }}>{c}</button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

// ─────────────────────────────────────────────
// OPTION 9: Compact table view
// ─────────────────────────────────────────────
const Option9 = () => (
  <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr style={{ borderBottom: `1px solid rgba(255,255,255,0.1)` }}>
          <th style={{ textAlign: "left", padding: "8px 12px", color: "rgba(255,255,255,0.4)", fontSize: "0.65rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" }}>Course</th>
          <th style={{ textAlign: "left", padding: "8px 12px", color: "rgba(255,255,255,0.4)", fontSize: "0.65rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" }}>Category</th>
          <th style={{ textAlign: "center", padding: "8px 12px", color: "rgba(255,255,255,0.4)", fontSize: "0.65rem", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" }}>Status</th>
        </tr>
      </thead>
      <tbody>
        {categories.flatMap(cat => cat.courses.slice(0, 4).map(c => (
          <tr key={c + cat.name} style={{ borderBottom: "1px solid rgba(255,255,255,0.03)", cursor: "pointer" }}>
            <td style={{ padding: "10px 12px", color: "#fff", fontSize: "0.82rem", fontWeight: 500 }}>{c}</td>
            <td style={{ padding: "10px 12px", color: "rgba(255,255,255,0.35)", fontSize: "0.75rem" }}>{cat.icon} {cat.name}</td>
            <td style={{ padding: "10px 12px", textAlign: "center" }}>
              {liveStatus(c) ?
                <span style={{ fontSize: "0.6rem", background: "rgba(61,214,192,0.12)", color: "#3dd6c0", padding: "2px 10px", borderRadius: 99 }}>Live</span> :
                <span style={{ fontSize: "0.6rem", color: "rgba(255,255,255,0.2)" }}>Soon</span>}
            </td>
          </tr>
        )))}
      </tbody>
    </table>
  </div>
);

// ─────────────────────────────────────────────
// OPTION 10: Visual tiles with category color coding
// ─────────────────────────────────────────────
const catColors = { "AI Models": "#6366f1", "AI Progress": "#3dd6c0", "Art": "#f472b6", "Business": "#c9a05a", "Development": "#60a5fa", "Core Courses": "#a78bfa" };
const Option10 = () => {
  const [filter, setFilter] = useState("All");
  const filtered = filter === "All" ? categories : categories.filter(c => c.name === filter);
  return (
    <div style={{ background: navy, padding: "2rem", borderRadius: 12 }}>
      <div style={{ display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
        {["All", ...categories.map(c => c.name)].map(f => (
          <button key={f} onClick={() => setFilter(f)} style={{
            padding: "8px 16px", borderRadius: 8, cursor: "pointer",
            background: filter === f ? (catColors[f] || gold) + "22" : "rgba(255,255,255,0.03)",
            border: `1px solid ${filter === f ? (catColors[f] || gold) : "rgba(255,255,255,0.08)"}`,
            color: filter === f ? (catColors[f] || gold) : "rgba(255,255,255,0.5)",
            fontSize: "0.78rem", fontWeight: 600
          }}>{categories.find(c => c.name === f)?.icon || "📋"} {f}</button>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 10 }}>
        {filtered.flatMap(cat => cat.courses.map(c => (
          <div key={c + cat.name} style={{
            background: darkBg, borderRadius: 10, padding: "16px", cursor: "pointer",
            borderTop: `3px solid ${catColors[cat.name] || gold}`,
            boxShadow: "0 2px 8px rgba(0,0,0,0.2)"
          }}>
            <div style={{ fontSize: "0.6rem", color: catColors[cat.name], fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 6 }}>{cat.name}</div>
            <div style={{ fontSize: "0.85rem", color: "#fff", fontWeight: 600, marginBottom: 8 }}>{c}</div>
            {liveStatus(c) ?
              <span style={{ fontSize: "0.6rem", color: "#3dd6c0" }}>● Live — Enter →</span> :
              <span style={{ fontSize: "0.6rem", color: "rgba(255,255,255,0.2)" }}>Coming Soon</span>}
          </div>
        )))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// MAIN: Preview all 10 options
// ─────────────────────────────────────────────
export default function App() {
  const [viewing, setViewing] = useState(1);
  const options = [
    { n: 1, label: "Pill Filters + Card Grid", desc: "Horizontal filter pills at top, flat card grid below", component: <Option1 /> },
    { n: 2, label: "Accordion Sections", desc: "One category open at a time, clean vertical list", component: <Option2 /> },
    { n: 3, label: "Search + Flat List", desc: "Searchable list of all courses with instant filtering", component: <Option3 /> },
    { n: 4, label: "Expanding Category Cards", desc: "Category cards that expand inline to show courses", component: <Option4 /> },
    { n: 5, label: "Horizontal Tab Bar + Grid", desc: "Tab row across the top, card grid per category", component: <Option5 /> },
    { n: 6, label: "Sidebar + List (Refined)", desc: "Clean left sidebar nav with list view, similar to current but better", component: <Option6 /> },
    { n: 7, label: "Netflix Rows", desc: "Horizontal scrollable rows grouped by category", component: <Option7 /> },
    { n: 8, label: "Grouped Chip Tags", desc: "Courses as clickable chips grouped under category headers", component: <Option8 /> },
    { n: 9, label: "Table View", desc: "Compact sortable table with status badges", component: <Option9 /> },
    { n: 10, label: "Color-Coded Tiles", desc: "Category filter + color-coded tile cards with top border accent", component: <Option10 /> },
  ];

  return (
    <div style={{ fontFamily: "'Inter', system-ui, sans-serif", background: "#0a1018", minHeight: "100vh", padding: 24 }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <h1 style={{ color: "#fff", fontSize: "1.3rem", fontWeight: 800, marginBottom: 4 }}>Course Selector Options</h1>
        <p style={{ color: "rgba(255,255,255,0.4)", fontSize: "0.85rem", marginBottom: 24 }}>Click any option to preview. All use your actual course data and site colors.</p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24 }}>
          {options.map(o => (
            <button key={o.n} onClick={() => setViewing(o.n)} style={{
              padding: "8px 16px", borderRadius: 8, cursor: "pointer",
              background: viewing === o.n ? "rgba(201,160,90,0.15)" : "rgba(255,255,255,0.04)",
              border: `1px solid ${viewing === o.n ? gold : "rgba(255,255,255,0.1)"}`,
              color: viewing === o.n ? gold : "rgba(255,255,255,0.6)",
              fontSize: "0.78rem", fontWeight: 600
            }}>#{o.n} {o.label}</button>
          ))}
        </div>
        <div style={{ marginBottom: 12, color: "rgba(255,255,255,0.5)", fontSize: "0.8rem" }}>
          <strong style={{ color: gold }}>Option {viewing}:</strong> {options[viewing - 1].desc}
        </div>
        {options[viewing - 1].component}
      </div>
    </div>
  );
}
