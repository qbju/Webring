(() => {
  const script = document.currentScript;
  if (!script || script.dataset.webring !== "~ring") return;

  const endpoint = new URL("members.json", script.src).href;
  const containerId = script.dataset.container || "~ring";
  const container = document.getElementById(containerId);
  if (!container) return;

  const normalize = (value) => {
    try {
      const u = new URL(value, location.href);
      return (u.origin + u.pathname).replace(/\/$/, "");
    } catch {
      return value.replace(/\/$/, "");
    }
  };

  const link = (href, text) => {
    const a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    a.rel = "noopener";
    return a;
  };

  fetch(endpoint, { cache: "no-store" })
    .then((r) => {
      if (!r.ok) throw new Error("registry unavailable");
      return r.json();
    })
    .then((data) => {
      const members = (data.members || []).filter((m) => m.status === "active" && m.url);
      if (!members.length) return;

      const current = normalize(location.href);
      let index = members.findIndex((m) => normalize(m.url) === current);

      if (index < 0) {
        index = members.findIndex((m) => normalize(m.url) === normalize(location.origin));
      }
      if (index < 0) return;

      const previous = members[(index - 1 + members.length) % members.length];
      const next = members[(index + 1) % members.length];

      container.replaceChildren();
      container.append(
        link(previous.url, "← Prev"),
        document.createTextNode(" · "),
        link(members[Math.floor(Math.random() * members.length)].url, "Random"),
        document.createTextNode(" · "),
        link(next.url, "Next →")
      );
      container.dataset.webringReady = "true";
    })
    .catch(() => {});
})();
