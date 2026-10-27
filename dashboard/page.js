(function () {
  const CFG = window.RT_CFG;
  const num = (v) => (Number.isInteger(v) ? String(v) : v.toFixed(1));
  const withUnit = (v, unit) => (unit === '%' ? num(v) + '%' : num(v) + ' years');

  // part chips scroll to their section
  document.querySelectorAll('.rt-chip').forEach((b) => {
    b.addEventListener('click', () => {
      const el = document.getElementById(b.dataset.target);
      if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); dash.setLink(el.id); }
    });
  });

  const parseWhere = (w) => Object.fromEntries(w.split('&').map((kv) => kv.split('=').map(decodeURIComponent)));

  function rowsOf(id) {
    const d = dash.data(id);
    if (d.status !== 'ok') return null;
    return d.data.map((r) => ({ year: String(r.year), series: String(r.series), value: Number(r.value) }));
  }

  function fillCells(id, rows, status) {
    document.querySelectorAll(`span[data-source="${id}"][data-field]`).forEach((el) => {
      if (!rows) {
        el.textContent = '—';
        if (status === 'error' || status === 'connect') el.classList.remove('dash-skeleton');
        return;
      }
      const w = parseWhere(el.dataset.where);
      const r = rows.find((x) => x.series === w.series && x.year === w.year);
      el.classList.remove('dash-skeleton');
      if (!r) { el.textContent = '—'; return; }
      el.textContent = el.dataset.field === 'year' ? r.year : withUnit(r.value, el.dataset.unit);
    });
  }

  function drawLegend(id, order) {
    const box = document.querySelector(`.rt-legend[data-source="${id}"]`);
    box.replaceChildren(...order.map((name, i) => {
      const s = document.createElement('span');
      const sw = document.createElement('span');
      sw.className = 'rt-sw';
      sw.style.background = dash.colors[i];
      s.append(sw, document.createTextNode(name));
      return s;
    }));
  }

  function segments(points, breaks) {
    // split a series where a break year falls between two points
    const segs = [];
    let cur = [];
    points.forEach((p, i) => {
      if (i > 0) {
        const prev = points[i - 1].x;
        if (breaks.some((b) => prev <= b && p.x > b)) { segs.push(cur); cur = []; }
      }
      cur.push(p);
    });
    if (cur.length) segs.push(cur);
    return segs;
  }

  function drawChart(id, rows, status) {
    const box = document.querySelector(`.rt-chart[data-id="${id}"]`);
    const cfg = CFG[id];
    if (!rows) {
      box.replaceChildren();
      if (status === 'error' || status === 'connect') {
        box.classList.remove('dash-skeleton');
        const f = document.createElement('div');
        f.className = 'rt-fail';
        f.textContent = 'Failed to load';
        box.append(f);
      }
      return;
    }
    box.classList.remove('dash-skeleton');
    const W = Math.max(240, box.clientWidth || 320), H = 180;
    const breaks = cfg.breaks.map(Number);
    const series = cfg.order.map((name, i) => ({
      name, color: dash.colors[i],
      pts: rows.filter((r) => r.series === name).map((r) => ({ x: Number(r.year), y: r.value, year: r.year }))
        .sort((a, b) => a.x - b.x),
    }));
    const years = Array.from(new Set(rows.map((r) => Number(r.year)))).sort((a, b) => a - b);
    const yMax = d3.max(rows, (r) => r.value) * 1.08;

    const svg = d3.create('svg').attr('width', '100%').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img');
    const y = d3.scaleLinear([0, yMax], [H - 22, 6]).nice();
    const yTicks = y.ticks(4);
    // measure widest y tick
    const probe = svg.append('text').attr('class', 'rt-tick');
    let lw = 0;
    box.appendChild(svg.node());
    yTicks.forEach((t) => { probe.text(withUnit(t, cfg.unit).replace(' years', '')); lw = Math.max(lw, probe.node().getComputedTextLength()); });
    probe.remove();
    svg.node().remove();
    const ml = Math.ceil(lw) + 8, mr = 10;
    const x = d3.scaleLinear([years[0], years[years.length - 1]], [ml, W - mr]);

    const g = svg.append('g');
    g.selectAll('line.grid').data(yTicks).join('line')
      .attr('x1', ml).attr('x2', W - mr).attr('y1', (d) => y(d)).attr('y2', (d) => y(d))
      .attr('stroke', 'var(--cds-chart-grid)').attr('stroke-width', 1);
    g.selectAll('text.yt').data(yTicks).join('text').attr('class', 'rt-tick')
      .attr('x', ml - 6).attr('y', (d) => y(d)).attr('dy', '0.32em').attr('text-anchor', 'end')
      .text((d) => withUnit(d, cfg.unit).replace(' years', ''));
    g.append('line').attr('x1', ml).attr('x2', W - mr).attr('y1', y(0)).attr('y2', y(0))
      .attr('stroke', 'var(--cds-chart-axis)');
    const nx = W < 360 ? 3 : 5;
    const xt = x.ticks(nx).filter((t) => Number.isInteger(t));
    g.selectAll('text.xt').data(xt).join('text').attr('class', 'rt-tick')
      .attr('x', (d) => x(d)).attr('y', H - 4).attr('text-anchor', 'middle').text((d) => String(d));

    // break markers
    breaks.forEach((b) => {
      const bx = x(b + 0.5);
      if (bx > ml && bx < W - mr) {
        g.append('line').attr('x1', bx).attr('x2', bx).attr('y1', 6).attr('y2', H - 22)
          .attr('stroke', 'var(--cds-chart-reference)').attr('stroke-dasharray', '3 3');
      }
    });

    const line = d3.line().x((p) => x(p.x)).y((p) => y(p.y));
    series.slice().reverse().forEach((s) => {
      segments(s.pts, breaks).forEach((seg) => {
        if (seg.length === 1) {
          g.append('circle').attr('cx', x(seg[0].x)).attr('cy', y(seg[0].y)).attr('r', 2.5).attr('fill', s.color);
        } else {
          g.append('path').attr('d', line(seg)).attr('fill', 'none').attr('stroke', s.color)
            .attr('stroke-width', 2).attr('stroke-linecap', 'round').attr('stroke-linejoin', 'round');
        }
      });
    });

    const rule = g.append('line').attr('y1', 6).attr('y2', H - 22).attr('stroke', 'var(--cds-chart-axis)').style('display', 'none');
    const dots = g.append('g');
    const tip = document.createElement('div');
    tip.className = 'rt-tip';
    tip.style.display = 'none';

    svg.append('rect').attr('x', ml).attr('y', 0).attr('width', W - ml - mr).attr('height', H - 20)
      .attr('fill', 'transparent')
      .on('mousemove', (event) => {
        const [mx] = d3.pointer(event);
        const yr = years[d3.minIndex(years, (v) => Math.abs(x(v) - mx))];
        const hits = series.map((s) => ({ s, p: s.pts.find((p) => p.x === yr) })).filter((h) => h.p);
        rule.style('display', null).attr('x1', x(yr)).attr('x2', x(yr));
        dots.selectAll('circle').data(hits).join('circle').attr('r', 3.5)
          .attr('cx', (h) => x(h.p.x)).attr('cy', (h) => y(h.p.y)).attr('fill', (h) => h.s.color);
        const head = document.createElement('div');
        head.className = 'rt-tip-h';
        head.textContent = String(yr);
        const lines = hits.map((h) => {
          const d = document.createElement('div');
          if (series.length > 1) {
            const sw = document.createElement('span');
            sw.className = 'rt-sw';
            sw.style.background = h.s.color;
            d.append(sw);
          }
          d.append(document.createTextNode(`${h.s.name}: ${withUnit(h.p.y, cfg.unit)}`));
          return d;
        });
        tip.replaceChildren(head, ...(lines.length ? lines : [document.createTextNode('No data this year')]));
        tip.style.display = 'block';
        const bw = box.clientWidth, scale = bw / W, px = x(yr) * scale;
        const tw = tip.offsetWidth;
        tip.style.left = Math.max(0, Math.min(bw - tw, px + 10 > bw - tw ? px - tw - 10 : px + 10)) + 'px';
        tip.style.top = '4px';
      })
      .on('mouseleave', () => { tip.style.display = 'none'; rule.style('display', 'none'); dots.selectAll('circle').remove(); });

    box.replaceChildren(svg.node(), tip);
  }

  dash.onData(() => {
    Object.keys(CFG).forEach((id) => {
      const d = dash.data(id);
      const rows = rowsOf(id);
      fillCells(id, rows, d.status);
      drawLegend(id, CFG[id].order);
      drawChart(id, rows, d.status);
    });
  });

  let jumped = false;
  dash.onData(() => {
    if (jumped) return;
    jumped = true;
    const named = document.getElementById(location.hash.slice(1));
    if (named) named.scrollIntoView();
  });
})();
