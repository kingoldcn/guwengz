/* 古文观止 · 共用工具 */
(function () {
  "use strict";

  var DIFF_LABELS = { 1: "小学", 2: "初中", 3: "高中" };
  var DIFF_CLASS = { 1: "elementary", 2: "junior", 3: "senior" };

  window.GW = {
    navItems: [
      { href: "index.html", label: "首页" },
      { href: "volume.html?vol=1", label: "分卷阅读" },
      { href: "authors.html", label: "作者墙" },
      { href: "quotes.html", label: "名句金句" },
      { href: "progress.html", label: "我的进度" }
    ],

    diffLabel: function (d) { return DIFF_LABELS[d] || "初中"; },
    diffClass: function (d) { return DIFF_CLASS[d] || "junior"; },

    stars: function (d) {
      var s = "";
      for (var i = 1; i <= 3; i++) s += '<span class="star' + (i <= d ? "" : " off") + '">★</span>';
      return s;
    },

    findArticle: function (id) {
      for (var i = 0; i < ARTICLES.length; i++) if (ARTICLES[i].id === id) return ARTICLES[i];
      return null;
    },
    findVolume: function (id) {
      for (var i = 0; i < VOLUMES.length; i++) if (VOLUMES[i].id === id) return VOLUMES[i];
      return null;
    },
    articlesOfVolume: function (volId) {
      return ARTICLES.filter(function (a) { return a.vol === volId; });
    },
    findAuthor: function (id) {
      for (var i = 0; i < AUTHORS.length; i++) if (AUTHORS[i].id === id) return AUTHORS[i];
      return null;
    },
    nextArticle: function (id) {
      var a = this.findArticle(id);
      if (!a) return null;
      var list = this.articlesOfVolume(a.vol);
      var i = 0;
      for (; i < list.length; i++) if (list[i].id === id) break;
      return i + 1 < list.length ? list[i + 1] : null;
    },
    prevArticle: function (id) {
      var a = this.findArticle(id);
      if (!a) return null;
      var list = this.articlesOfVolume(a.vol);
      var i = 0;
      for (; i < list.length; i++) if (list[i].id === id) break;
      return i - 1 >= 0 ? list[i - 1] : null;
    },

    esc: function (s) {
      return String(s == null ? "" : s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    },

    header: function (active) {
      var nav = this.navItems.map(function (n) {
        return '<a href="' + n.href + '"' + (n.label === active ? ' class="active"' : "") + ">" + n.label + "</a>";
      }).join("");
      return '<header class="site-header"><div class="container bar">' +
        '<a class="brand" href="index.html"><span class="seal">观</span>' +
        '<span><span class="title">古文观止</span><span class="sub">青少年图文读本</span></span></a>' +
        '<nav class="top-nav">' + nav + "</nav>" +
        '<div class="search-box"><input id="gw-search" type="text" placeholder="搜索篇目…" autocomplete="off">' +
        '<span class="icon">⌕</span><div class="search-results" id="gw-search-results"></div></div>' +
        "</div></header>";
    },

    footer: function () {
      return '<footer class="site-footer"><div class="container">' +
        '<div class="brand-line">《古文观止》· 青少年图文读本</div>' +
        "清·吴楚材、吴调侯 编选 ｜ 全本 222 篇 · 12 卷 ｜ 图文阅读 / 注音 / 译文 / 赏析" +
        "</div></footer>";
    },

    mount: function (active) {
      var top = document.getElementById("gw-top");
      if (top) top.innerHTML = this.header(active);
      var bot = document.getElementById("gw-bottom");
      if (bot) bot.innerHTML = this.footer();
      this.initSearch();
    },

    initSearch: function () {
      var input = document.getElementById("gw-search");
      if (!input) return;
      var box = document.getElementById("gw-search-results");
      var timer = null;
      input.addEventListener("input", function () {
        clearTimeout(timer);
        var q = input.value.trim();
        if (!q) { box.classList.remove("open"); return; }
        timer = setTimeout(function () {
          var hits = [];
          var ql = q.toLowerCase();
          for (var i = 0; i < ARTICLES.length; i++) {
            var a = ARTICLES[i];
            if (a.title.indexOf(q) >= 0 || a.author.indexOf(q) >= 0 || a.source.indexOf(q) >= 0 || a.dynasty.indexOf(q) >= 0) {
              hits.push(a);
              if (hits.length >= 20) break;
            }
          }
          if (!hits.length) {
            box.innerHTML = '<a class="r-title" style="color:var(--ink-soft)">没有找到「' + GW.esc(q) + '」</a>';
          } else {
            box.innerHTML = hits.map(function (a) {
              var v = GW.findVolume(a.vol);
              return '<a href="article.html?id=' + a.id + '">' +
                '<div class="r-title">' + GW.esc(a.title) + "</div>" +
                '<div class="r-meta">' + GW.esc((v ? v.name : "") + " · " + a.author + " · " + a.dynasty) + "</div></a>";
            }).join("");
          }
          box.classList.add("open");
        }, 150);
      });
      document.addEventListener("click", function (e) {
        if (!e.target.closest(".search-box")) box.classList.remove("open");
      });
    },

    afterEachArticle: function () { /* 预留 */ }
  };
})();