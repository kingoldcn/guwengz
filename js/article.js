/* 古文观止 · 阅读页 */
(function () {
  "use strict";

  var params = new URLSearchParams(location.search);
  var id = params.get("id") || "v01-001";
  var meta = GW.findArticle(id);
  var content = null;
  var showPy = false;
  var synth = window.speechSynthesis ? window.speechSynthesis : null;

  function isCJK(ch) { return /[\u3400-\u9fff\uF900-\uFAFF]/.test(ch); }

  function sentHTML(s, withPy) {
    if (!withPy || !s.py) return '<span class="hanzi">' + GW.esc(s.zh) + "</span>";
    var syls = s.py.trim().split(/\s+/);
    var si = 0;
    var html = '<span class="hanzi">';
    for (var i = 0; i < s.zh.length; i++) {
      var ch = s.zh.charAt(i);
      if (isCJK(ch)) {
        var syl = syls[si] ? syls[si] : "";
        si++;
        if (syl) html += "<ruby>" + ch + "<rt>" + syl + "</rt></ruby>";
        else html += ch;
      } else {
        html += GW.esc(ch);
      }
    }
    return html + "</span>";
  }

  function readAloud(text) {
    if (!synth) return;
    synth.cancel();
    var u = new SpeechSynthesisUtterance(text.replace(/[“”《》]/g, ""));
    u.lang = "zh-CN";
    u.rate = 0.9;
    synth.speak(u);
  }

  function buildToolbar() {
    var favs = JSON.parse(localStorage.getItem("gw_fav") || "[]");
    var isFav = favs.indexOf(id) >= 0;
    var tbar = document.getElementById("gw-toolbar");
    tbar.innerHTML =
      '<button class="tool-btn' + (showPy ? " on" : "") + '" id="btn-py">注音</button>' +
      '<button class="tool-btn" id="btn-read">朗读本段</button>' +
      '<button class="tool-btn" id="btn-size-down">A−</button>' +
      '<button class="tool-btn" id="btn-size-up">A+</button>' +
      '<button class="tool-btn' + (isFav ? " on" : "") + '" id="btn-fav">' + (isFav ? "已收藏 ★" : "收藏") + "</button>";

    document.getElementById("btn-py").addEventListener("click", function () {
      showPy = !showPy;
      renderParagraphs();
      buildToolbar();
    });
    document.getElementById("btn-read").addEventListener("click", function () {
      var all = content.paragraphs.map(function (p) {
        return p.sentences.map(function (s) { return s.zh; }).join("");
      }).join("");
      readAloud(all);
    });
    document.getElementById("btn-size-down").addEventListener("click", function () {
      changeSize(-1);
    });
    document.getElementById("btn-size-up").addEventListener("click", function () {
      changeSize(1);
    });
    document.getElementById("btn-fav").addEventListener("click", function () {
      var fs = JSON.parse(localStorage.getItem("gw_fav") || "[]");
      var at = fs.indexOf(id);
      if (at >= 0) fs.splice(at, 1); else fs.push(id);
      localStorage.setItem("gw_fav", JSON.stringify(fs));
      buildToolbar();
    });
  }

  function changeSize(d) {
    var root = document.getElementById("gw-reader");
    var cur = parseFloat(root.getAttribute("data-size") || "18.5");
    var next = Math.max(14, Math.min(26, cur + d * 1.5));
    root.setAttribute("data-size", next);
    root.querySelectorAll(".sent .hanzi").forEach(function (el) {
      el.style.fontSize = next + "px";
    });
  }

  function renderParagraphs() {
    var box = document.getElementById("gw-sentences");
    box.innerHTML = content.paragraphs.map(function (p) {
      var label = p.label ? '<span class="para-label">' + GW.esc(p.label) + "</span>" : "";
      var sents = p.sentences.map(function (s) {
        return '<div class="sent" data-txt="' + GW.esc(s.zh) + '">' +
          sentHTML(s, showPy) +
          '<span class="yiyi">' + GW.esc(s.yi) + "</span></div>";
      }).join("");
      return '<div class="para">' + label + '<div class="sentences">' + sents + "</div></div>";
    }).join("");

    box.querySelectorAll(".sent").forEach(function (el) {
      el.addEventListener("click", function () {
        box.querySelectorAll(".sent").forEach(function (s) { s.classList.remove("reading"); });
        el.classList.add("reading");
        readAloud(el.getAttribute("data-txt"));
      });
    });
  }

  function renderTabs() {
    var notes = content.notes || [];
    var appre = content.appreciation || [];
    var html = '<div class="tabs">' +
      '<button class="tab-btn on" data-tab="notes">生词注释</button>' +
      '<button class="tab-btn" data-tab="appre">赏析导读</button>' +
      '<button class="tab-btn" data-tab="author">作者与背景</button>' +
      "</div>";

    html += '<div class="tab-panel on" id="tab-notes">';
    if (notes.length) {
      html += '<div class="notes-list">' + notes.map(function (n) {
        return '<div class="note"><span class="n-term">' + GW.esc(n.term) + "</span><span class=\"n-desc\">" + GW.esc(n.desc) + "</span></div>";
      }).join("") + "</div>";
    } else {
      html += '<p class="muted">注释整理中…</p>';
    }
    html += "</div>";

    html += '<div class="tab-panel" id="tab-appre"><div class="appreciation">';
    if (content.topic) html += '<div class="topic"><b>中心思想：</b>' + GW.esc(content.topic) + "</div>";
    if (appre.length) {
      html += appre.map(function (t) { return "<p>" + GW.esc(t) + "</p>"; }).join("");
    } else {
      html += '<p class="muted">赏析导读整理中…</p>';
    }
    html += "</div></div>";

    var author = GW.findAuthor(meta.authorId);
    var bio = content.authorBio || (author ? author.bio : "");
    html += '<div class="tab-panel" id="tab-author"><div class="author-box">' +
      '<div class="avatar" style="background:' + (author ? author.color : "#999") + '">' + (meta.author ? meta.author.charAt(0) : "?") + "</div>" +
      "<div>" +
        "<h3>" + GW.esc(meta.author) + "</h3>" +
        '<div class="a-era">' + GW.esc((author ? author.era : "") + " · " + meta.dynasty) + "</div>" +
        "<p>" + GW.esc(bio || "作者小传整理中…") + "</p>" +
        (content.background ? '<p style="margin-top:10px"><b>本篇背景：</b>' + GW.esc(content.background) + "</p>" : "") +
      "</div></div></div>";

    var box = document.getElementById("gw-tabs");
    box.innerHTML = html;
    box.querySelectorAll(".tab-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        box.querySelectorAll(".tab-btn").forEach(function (b) { b.classList.remove("on"); });
        box.querySelectorAll(".tab-panel").forEach(function (p) { p.classList.remove("on"); });
        btn.classList.add("on");
        document.getElementById("tab-" + btn.getAttribute("data-tab")).classList.add("on");
      });
    });
  }

  function render() {
    var v = GW.findVolume(meta.vol);
    var author = GW.findAuthor(meta.authorId);
    var prev = GW.prevArticle(id);
    var next = GW.nextArticle(id);

    document.title = meta.title + " · 古文观止";

    document.getElementById("gw-crumbs").innerHTML =
      '<a href="index.html">首页</a> / <a href="volume.html?vol=' + meta.vol + '">' + v.name + "</a> / " + GW.esc(meta.title);

    document.getElementById("gw-title-row").innerHTML =
      "<h1>" + GW.esc(meta.title) + "</h1>" +
      '<span class="tag ' + GW.diffClass(meta.difficulty) + '">' + GW.diffLabel(meta.difficulty) + "</span>";

    document.getElementById("gw-meta-line").innerHTML =
      GW.esc(meta.author + " · " + meta.dynasty + " · " + meta.source);

    document.getElementById("gw-cover").style.display = "block";
    document.getElementById("gw-cover").innerHTML =
      '<div class="cover-wrap">' +
        '<img src="assets/covers/' + id + '.png" alt="' + GW.esc(meta.title) + ' 绘本插画" onerror="this.parentNode.style.display=\'none\'">' +
        '<div class="cover-cap"><h2>' + GW.esc(meta.title) + "</h2>" +
        "<span>" + GW.esc(meta.author + " · " + meta.dynasty) + "</span></div>" +
      "</div>";

    var facts =
      '<div class="panel">' +
        "<h2>本篇速览</h2>" +
        '<div class="fact-list">' +
          fact("篇目来源", meta.source) +
          fact("作　者", meta.author + "（" + (author ? author.era : meta.dynasty) + "）") +
          fact("难度分级", GW.diffLabel(meta.difficulty) + " <span class=\"difficulty\">" + GW.stars(meta.difficulty) + "</span>") +
          fact("所属卷次", v.name + " · " + v.theme) +
        "</div>" +
        (meta.synopsis ? '<p class="synopsis">' + GW.esc(meta.synopsis) + "</p>" : "") +
      "</div>";
    document.getElementById("gw-facts").innerHTML = facts;

    var nav = "";
    if (prev) nav += '<a href="article.html?id=' + prev.id + '"><div class="dir">上一篇</div><div class="t">' + GW.esc(prev.title) + "</div></a>";
    if (next) nav += '<a href="article.html?id=' + next.id + '" style="text-align:right"><div class="dir">下一篇</div><div class="t">' + GW.esc(next.title) + " →</div></a>";
    document.getElementById("gw-nav").innerHTML = nav;

    renderParagraphs();
    renderTabs();
    buildToolbar();

    /* 记录阅读进度 */
    try {
      var done = JSON.parse(localStorage.getItem("gw_done") || "[]");
      if (done.indexOf(id) < 0) done.push(id);
      localStorage.setItem("gw_done", JSON.stringify(done));
    } catch (e) { /* ignore */ }
  }

  function fact(k, val) {
    return '<div class="fact"><span class="fk">' + k + "</span><span class=\"fv\">" + val + "</span></div>";
  }

  function showPlaceholder() {
    document.getElementById("gw-content").innerHTML =
      '<div class="panel text-center" style="padding:80px 20px">' +
        "<h2>本篇内容生产中</h2>" +
        '<p class="muted" style="margin:10px 0">《' + GW.esc(meta.title) + "》的注音、译文与赏析正在按卷制作，完成后即可阅读。</p>" +
        '<a class="btn ghost" href="volume.html?vol=' + meta.vol + '">返回第' + meta.vol + "卷</a></div>";
  }

  function loadContent() {
    if (window.CONTENT && CONTENT.id === id) {
      content = CONTENT;
      render();
      return;
    }
    var s = document.createElement("script");
    s.src = "articles/" + id + "/content.js";
    s.onload = function () {
      if (window.CONTENT && CONTENT.id === id) {
        content = CONTENT;
        render();
      } else {
        showPlaceholder();
      }
    };
    s.onerror = function () { showPlaceholder(); };
    document.body.appendChild(s);
  }

  GW.mount("");
  loadContent();
})();