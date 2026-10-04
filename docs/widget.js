(() => {
  const script = document.currentScript;
  if (!script || script.dataset.webring !== "~ring") return;

  const endpoint = new URL("members.json", script.src).href;
  const baseUrl = new URL(".", script.src).href;
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

  const link = (href, text, className = "") => {
    const a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    a.rel = "noopener";
    if (className) {
      a.className = className;
      if (className === "webring-button") {
        a.style.display = "inline-block";
        a.style.padding = "0.35rem 0.7rem";
        a.style.border = "1px solid currentColor";
        a.style.borderRadius = "0.35rem";
        a.style.textDecoration = "none";
      }
    }
    return a;
  };

  const logo = () => {
    const img = document.createElement("img");
    img.src = new URL("ring.svg", baseUrl).href;
    img.alt = "~ring";
    img.className = "webring-logo";
    img.style.display = "block";
    img.style.width = "96px";
    img.style.height = "auto";
    img.style.margin = "0 0 0.75rem";
    const a = document.createElement("a");
    a.href = "https://tildering.pages.dev/";
    a.append(img);
    a.setAttribute("aria-label", "~ring");
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

      const current = new URL(location.href);
      const memberRoot = (value) => {
        const u = new URL(value, location.href);
        return { origin: u.origin, path: u.pathname.replace(/\/$/, "") };
      };
      const isWithinMember = (member) => {
        const root = memberRoot(member.url);
        if (root.origin !== current.origin) return false;
        return current.pathname === root.path || current.pathname.startsWith(root.path + "/");
      };
      let index = members.findIndex(isWithinMember);

      if (index < 0) return;

      const previous = members[(index - 1 + members.length) % members.length];
      const next = members[(index + 1) % members.length];

      const style = script.dataset.webringStyle || "text";
      const showLogo = script.dataset.webringLogo === "true";

      container.replaceChildren();

      if (showLogo) {
        container.append(logo());
      }

      const nav = document.createElement("span");
      nav.className = "webring-nav";

      if (style === "buttons") {
        nav.append(
          link(previous.url, "← Prev", "webring-button"),
          document.createTextNode(" "),
          link(members[Math.floor(Math.random() * members.length)].url, "Random", "webring-button"),
          document.createTextNode(" "),
          link(next.url, "Next →", "webring-button")
        );
      } else if (style === "stacked") {
        nav.append(
          link(previous.url, "← Prev"),
          document.createElement("br"),
          link(members[Math.floor(Math.random() * members.length)].url, "Random"),
          document.createElement("br"),
          link(next.url, "Next →")
        );
      } else {
        nav.append(
          link(previous.url, "← Prev"),
          document.createTextNode(" · "),
          link(members[Math.floor(Math.random() * members.length)].url, "Random"),
          document.createTextNode(" · "),
          link(next.url, "Next →")
        );
      }

      container.append(nav);
      container.dataset.webringReady = "true";
    })
    .catch(() => {});
})();
