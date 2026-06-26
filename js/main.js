/* ============================================================
   West Coast Capital Mortgage — California
   Nav, mortgage calculator, Motion-powered animations.
   ============================================================ */
(function () {
  "use strict";

  const MOTION_CDN = "https://cdn.jsdelivr.net/npm/motion@12.42.0/+esm";
  const reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Sticky nav shadow ---- */
  const nav = document.getElementById("nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Mobile menu ---- */
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (toggle && links) {
    const close = () => {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    };
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    links.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  }

  /* ---- Mortgage calculator ---- */
  const $ = (id) => document.getElementById(id);
  const fmt = (n) => "$" + Math.round(n).toLocaleString("en-US");
  const inputs = { price: $("price"), down: $("down"), rate: $("rate"), term: $("term") };

  function calc() {
    const price = +inputs.price.value;
    const downPct = +inputs.down.value;
    const rate = +inputs.rate.value;
    const years = +inputs.term.value;

    const downAmt = price * (downPct / 100);
    const principal = price - downAmt;
    const monthlyRate = rate / 100 / 12;
    const n = years * 12;

    const payment =
      monthlyRate === 0
        ? principal / n
        : (principal * monthlyRate * Math.pow(1 + monthlyRate, n)) /
          (Math.pow(1 + monthlyRate, n) - 1);

    $("priceOut").textContent = fmt(price);
    $("downOut").textContent = `${fmt(downAmt)} (${downPct}%)`;
    $("rateOut").textContent =
      rate.toFixed(3).replace(/0+$/, "").replace(/\.$/, "") + "%";
    $("termOut").textContent = years + " years";
    $("payment").innerHTML = fmt(payment) + "<small>/mo</small>";
    $("loanAmount").textContent = `Loan amount ${fmt(principal)} · Principal & interest only`;
  }

  if (inputs.price && inputs.down && inputs.rate && inputs.term) {
    Object.values(inputs).forEach((el) => el.addEventListener("input", calc));
    calc();
  }

  /* ---- Footer year ---- */
  const yr = $("year");
  if (yr) yr.textContent = new Date().getFullYear();

  /* ---- Animated counters (stats) ---- */
  const counters = Array.from(document.querySelectorAll("[data-count-to]"));
  const renderCount = (el, value) => {
    const decimals = +(el.getAttribute("data-decimals") || 0);
    el.textContent = value
      .toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  };
  // Fallback: show final values immediately (overwritten by Motion if it loads).
  counters.forEach((el) => renderCount(el, +el.getAttribute("data-count-to")));

  /* ---- Scroll reveal + counters: enhanced with Motion, graceful fallback ----
     Motion (motion.dev) springs sections/cards in with a per-group stagger and
     counts the stats up. If the CDN is blocked/slow we fall back to a
     dependency-free CSS reveal so content is never hidden; reduced-motion shows
     everything instantly. */
  const revealTargets = document.querySelectorAll(".reveal");

  if (reduceMotion) {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  } else if (revealTargets.length || counters.length) {
    let handled = false;
    const showAll = () => revealTargets.forEach((el) => el.classList.add("is-visible"));

    const cssFallback = () => {
      if (handled) return;
      handled = true;
      if ("IntersectionObserver" in window) {
        const io = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                io.unobserve(entry.target);
              }
            });
          },
          { threshold: 0.12 }
        );
        revealTargets.forEach((el) => io.observe(el));
      } else {
        showAll();
      }
    };

    import(MOTION_CDN)
      .then(({ animate, inView, stagger, scroll }) => {
        if (handled) return;
        handled = true;

        // Subtle parallax on the hero background glows.
        const hero = document.querySelector(".hero");
        if (typeof scroll === "function" && hero) {
          const g1 = document.querySelector(".hero__glow--1");
          const g2 = document.querySelector(".hero__glow--2");
          if (g1) scroll(animate(g1, { y: [0, 140] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
          if (g2) scroll(animate(g2, { y: [0, -90] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
        }

        // Reveals — group siblings by parent so rows stagger together.
        const groups = new Map();
        revealTargets.forEach((el) => {
          const parent = el.parentElement;
          if (!groups.has(parent)) groups.set(parent, []);
          groups.get(parent).push(el);
        });
        groups.forEach((els) => {
          inView(
            els[0],
            () => {
              animate(
                els,
                { opacity: [0, 1], y: [28, 0] },
                { type: "spring", duration: 0.7, bounce: 0.26, delay: stagger(0.08) }
              );
              els.forEach((el) => el.classList.add("is-visible"));
            },
            { amount: 0.12 }
          );
        });

        // Counters — count up the first time the stat scrolls into view.
        counters.forEach((el) => {
          const target = +el.getAttribute("data-count-to");
          renderCount(el, 0);
          inView(
            el,
            () => {
              animate(0, target, {
                duration: 1.4,
                ease: [0.16, 1, 0.3, 1],
                onUpdate: (v) => renderCount(el, v),
              });
            },
            { amount: 0.6 }
          );
        });
      })
      .catch(cssFallback);

    // Safety net: never leave content hidden if Motion stalls.
    window.setTimeout(cssFallback, 2500);
    window.addEventListener("beforeprint", showAll);
  }
})();
