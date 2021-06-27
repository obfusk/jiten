// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPLv3+

//  --                                                          ; {{{1
//
//  File        : static/script.js
//  Maintainer  : Felix C. Stegerman <flx@obfusk.net>
//  Date        : 2021-06-02
//
//  Copyright   : Copyright (C) 2021  Felix C. Stegerman
//  Version     : v1.0.0
//  License     : AGPLv3+
//
//  --                                                          ; }}}1

"use strict";
(() => {

// === kana conversion ===

const containsHiragana = t =>
  [...t].findIndex(c => HIRAGANA.indexOf(c) != -1) != -1

const convertKana = t =>
  (containsHiragana(t) ? hiraganaToKatakana : katakanaToHiragana)(t)

const hiraganaToKatakana = (t, long = false) => {
  let col = null
  return [...t].map(c => {
    const i = HIRAGANA.indexOf(c)
    const o = col === 4 && i === 2
    const k = long && (i === col || o) ? "ー" : KATAKANA[i] || c
    if (!o) col = i === -1 ? null : i % 5
    return k
  }).join("")
}

const katakanaToHiragana = t => {
  return [...t].map(c => HIRAGANA[KATAKANA.indexOf(c)] || c).join("")
}

// TODO: ヴャ, punctuation?!
const romajiToHiragana = t => {                               //  {{{1
  const r = [], rx = RegExp(RORX, "uy")
  let m
  while (m = rx.exec(t)) {
    if (m[1] || m[4]) {
      r.push(m[4] || ROSP[m[1] == "n" ? "nn" : m[1]])
    } else if (m[0].length == 1) {
      r.push(HIRAGANA[ROWS.indexOf(m[0])])
    } else {
      let s = "", x = m[2] ? ROMP[m[2]] : m[0]
      if (x[0] == x[1]) {
        s = "っ"; x = x.slice(1)
      }
      try {
        if (x.length == 3 && x[1] == "y" && x[0] != "x") {
          s += get(HIRAGANA, 5*indexOf(COLS, x[0])+1) +
               get(HIRAGANA, 5*(indexOf(COLS, "y")+1)
                              +indexOf(ROWS, x[2]))
        } else {
          s += get(HIRAGANA, 5*indexOf(COLS, x.slice(0, -1))
                              +indexOf(ROWS, x.slice(-1)))
        }
      } catch(e) {
        if (e instanceof LookupError) {
          r.push(m[0])                                        //  TODO
          continue
        } else {
          throw e
        }
      }
      r.push(s.includes("〇") ? m[0] : s)                     //  TODO
    }
  }
  return r.join("")
}                                                             //  }}}1

const romajiToKatakana = (t, long = false) =>
  hiraganaToKatakana(romajiToHiragana(t), long)

// KANA TABLES                                                //  {{{1
const HIRAGANA = `
  あ   い う   え   お
  ぁ   ぃ ぅ   ぇ   ぉ
ゔぁ ゔぃ ゔ ゔぇ ゔぉ
  か   き く   け   こ
  が   ぎ ぐ   げ   ご
  さ   し す   せ   そ
  ざ   じ ず   ぜ   ぞ
  た   ち つ   て   と
  だ   ぢ づ   で   ど
  〇   〇 っ   〇   〇
  な   に ぬ   ね   の
  は   ひ ふ   へ   ほ
  ば   び ぶ   べ   ぼ
  ぱ   ぴ ぷ   ぺ   ぽ
ふぁ ふぃ ふ ふぇ ふぉ
  ま   み む   め   も
  や   〇 ゆ   〇   よ
  ゃ   〇 ゅ   〇   ょ
  ら   り る   れ   ろ
  わ   ゐ 〇   ゑ   を
  ゎ   〇 〇   〇   〇
  ん   〇 〇   〇   〇
  ゝ   ゞ 〇   〇   〇
`.split(/\s+/).filter(x => x)

const KATAKANA = `
  ア   イ ウ   エ   オ
  ァ   ィ ゥ   ェ   ォ
ヴァ ヴィ ヴ ヴェ ヴォ
  カ   キ ク   ケ   コ
  ガ   ギ グ   ゲ   ゴ
  サ   シ ス   セ   ソ
  ザ   ジ ズ   ゼ   ゾ
  タ   チ ツ   テ   ト
  ダ   ヂ ヅ   デ   ド
  〇   〇 ッ   〇   〇
  ナ   ニ ヌ   ネ   ノ
  ハ   ヒ フ   ヘ   ホ
  バ   ビ ブ   ベ   ボ
  パ   ピ プ   ペ   ポ
ファ フィ フ フェ フォ
  マ   ミ ム   メ   モ
  ヤ   〇 ユ   〇   ヨ
  ャ   〇 ュ   〇   ョ
  ラ   リ ル   レ   ロ
  ワ   ヰ 〇   ヱ   ヲ
  ヮ   〇 〇   〇   〇
  ン   〇 〇   〇   〇
  ヽ   ヾ 〇   〇   〇
`.split(/\s+/).filter(x => x)
                                                              //  }}}1

const esc   = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

const ROWS  = "aiueo", COLS_ = "-xvkgsztdTnhbpfmyYrwW"
const COLS  = [...COLS_].map(c => "TYW".includes(c) ?
                                  "x" + c.toLowerCase() : c)

const ROMP  = {
  shi:  "si",  ji:  "zi", chi:  "ti", tsu: "tu", xtsu: "xtu",
  sha: "sya", sho: "syo", shu: "syu",
   ja: "zya",  jo: "zyo",  ju: "zyu",
  cha: "tya", cho: "tyo", chu: "tyu",
   fu:  "hu",
}
for (const k of Object.keys(ROMP)) {
  if (k[0] != "x") { ROMP[k[0]+k] = ROMP[k][0]+ROMP[k] }
}
const ROMPK = Object.keys(ROMP).sort().reverse()

const COLSX = COLS.slice(1).filter(x => x[0] != "x").map(x => x[0]+x)
const COLS2 = COLS.slice(1).concat(COLSX).sort().reverse()

const ROSP  = { nn:"ん", "-":"ー", "~":"〜", ",":"、", ".":"。",
                "?":"？", "!":"！", "(":"（", ")":"）" }      //  TODO

const RORX  = "(" + Object.keys(ROSP).map(esc).join("|")
                  + "|n(?![aiueoy]))|" +
              "(" + ROMPK.join("|") + ")|" +
              "(" + COLS2.join("|") + ")?y?"
                  + "[" + ROWS + "]|(.)"

// === miscellaneous ===

class LookupError extends Error {}

const get = (o, k) => {
  if (!(k in o)) { throw new LookupError() }
  return o[k]
}

const indexOf = (a, x) => {
  const i = a.indexOf(x)
  if (i == -1) { throw new LookupError() }
  return i
}

const uniq = (a, key = x => x) => a.filter((v, i, a) =>
  a.findIndex(x => key(x) == key(v)) === i
)

const selection = i => {
  const v = i.val(), a = i[0].selectionStart, b = i[0].selectionEnd
  return a == b ? ["", v, ""] : [v.slice(0, a), v.slice(a, b), v.slice(b)]
}

const playAudio = url =>
  new Audio(url).addEventListener("canplay", e => e.target.play())

// === history ===

const clearHistory = () => localStorage.removeItem("history")

const getHistory = () =>
  JSON.parse(localStorage.getItem("history") || "[]")

// NB: not atomic :(
const updateHistory = f =>
  localStorage.setItem("history", JSON.stringify(f(getHistory())))

// TODO
// NB: also sets document.title
const saveHistory = (max = 500) => {
  const params  = new URLSearchParams(location.search)
  let query     = (params.get("query") || "").trim()
  if (query) {
    if (query.startsWith("+#")) {
      const entry = $($(".entry")[0]).text().trim()
      if (entry) query += " (" + entry + ")"
      params.delete("noun"); params.delete("verb")
      params.delete("prio"); params.delete("jlpt")
    }
    const what = document.title.split(" - ").slice(-1)[0]
    const link = location.pathname + "?" + params.toString()
    document.title = `「${query}」 jiten - ${what}`
    updateHistory(hist =>
      uniq([[query, link], ...hist], x => x[1]).slice(0, max)
    )
  }
}

const populateHistoryList = () => {
  $("#history").empty()
  for (const [q, l] of getHistory()) {
    const li  = $('<li class="list-group-item p-2"></li>')
    const a   = $('<a class="link jap"></a>')
    a.text(l.split("?")[0].slice(1) + ": " + q); a.attr("href", l)
    li.append(a); $("#history").append(li)
  }
}

// === alert & confirm ===

const alert = msg => {
  const c = $("#alert-modal"), o = $(".modal:visible")
  return new Promise((resolve, reject) => {
    $(".modal-title", c).text(msg)
    o.modal("hide")
    c.on("hidden.bs.modal", () => {
      c.off(); o.modal("show"); resolve()
    }).modal()
  })
}

const confirm = msg => {
  const c = $("#confirm-modal"), o = $(".modal:visible")
  return new Promise((resolve, reject) => {
    $(".modal-title", c).text(msg)
    $("#confirm").off().click(() => {
      c.off().modal("hide"); o.modal("show"); resolve(true)
    })
    o.modal("hide")
    c.on("hidden.bs.modal", () => {
      c.off(); o.modal("show"); resolve(false)
    }).modal()
  })
}

// === node.js ===

if (typeof document === "undefined") {

console.log("Running tests...")

const assertEq = (a, b) => {
  if (a !== b) { throw new Error(`assertion failed: ${a} !== ${b}`) }
}

assertEq(romajiToHiragana("ikanakya")     , "いかなきゃ")
assertEq(romajiToKatakana("ferikkusu")    , "フェリックス")
assertEq(romajiToKatakana("vaiorinn")     , "ヴァイオリン")
assertEq(romajiToKatakana("uwisuki-")     , "ウヰスキー")
assertEq(romajiToKatakana("ko-su")        , "コース")

assertEq(romajiToHiragana("konnnichiha")  , "こんにちは")
assertEq(romajiToKatakana("uxirusu")      , "ウィルス")
assertEq(romajiToHiragana("koucha")       , "こうちゃ")

assertEq(romajiToHiragana("xya xwa xtsu") , "ゃ ゎ っ")
assertEq(romajiToHiragana("nacchau")      , "なっちゃう")

/* TODO */

console.log("OK")

} else {

// === browser ===

$(document).ready(() => {

// === fetch ===

const fetch_post = (info, path, data = "", json = false) => {
  const init = { method: "POST", body: data }
  if (json) init.headers = { "Content-Type": "application/json" }
  return fetch(path, init).then(r => {
    if (!r.ok) {
      throw new Error(`response (${r.status} ${r.statusText}) was not ok`)
    }
    return r
  }).catch(e => console.error(`${info} POST failed:`, e))
}

// === clipboard & webview & token ===

let webview_token   = localStorage.getItem("webview_token")
let copyToClipboard = null

if (document.location.hash.includes("webview_token")) {
  webview_token = document.location.hash.split("=")[1]
  localStorage.setItem("webview_token", webview_token)
}

if (webview_token) {
  $("#prefs-token").val(webview_token)
  copyToClipboard = t => fetch_post(
    "clipboard", `/__copy_to_clipboard__/${webview_token}`, t
  )
} else if (navigator.clipboard) {
  copyToClipboard = t => navigator.clipboard.writeText(t)
    .catch(e => console.error("clipboard.writeText() failed:", e))
}

// === event handlers ===

$(".play-audio").click(e => {
  playAudio(e.delegateTarget.href)
  return false
})

const convertModeToFunction = {
  r2h: t => romajiToHiragana(t.toLowerCase()),
  h2k: hiraganaToKatakana,
  k2h: katakanaToHiragana
}

const convertPart = t =>
  /^(\s*(?:\+(?:[=1ws]|r(?:andom)?)\s*)?)(.*?)(\s*)$/.exec(t)

// FIXME
const updateConvertMode = (e, i) => {
  const [b, v, a] = selection(i)
  const t = convertPart(v)[2]
  e.dataset.convertMode =
    e.dataset.r2h == "yes" && /[a-zA-Z]/.test(t) ? "r2h" :
    containsHiragana(t) ? "h2k" : "k2h"
}

const convertRomajiOrKana = (e, i) => {
  const [b, v, a] = selection(i)
  const f = convertModeToFunction[e.dataset.convertMode]
  const p = convertPart(v)
  i.val(b + p[1] + f(p[2]) + p[3] + a).focus()
  updateConvertMode(e, i)
}

$(".convert-kana").each((_i, e) => {
  const i = $(`#${e.dataset.convertInput}`)
  $(e).click(() => convertRomajiOrKana(e, i))
  i.on("input select focus", () => updateConvertMode(e, i))
  updateConvertMode(e, i)
})

$(".clear-input").click(evt => {
  const e = $(evt.delegateTarget), f = e.parents("form")
  $(".clear-input-checked"  , f).prop("checked", true)
  $(".clear-input-unchecked", f).prop("checked", false)
  $("input[type=text]", e.parents(".input-group")).val("").focus()
})

$(":checkbox[data-command]").change(evt => {
  const e = evt.delegateTarget, i = $("input[type=text]", $(e).parents("form"))
  const x = e.checked ? e.dataset.command + " " : "", v = i.val().trim()
  if (e.checked) {
    $(":checkbox", $(e).parents("fieldset"))
      .filter((i, x) => x != e).prop("checked", false)
  }
  if (!v || /^\+[^=1w]/.test(v)) return
  i.val(x + v.replace(/^\+[=1w]\s*/, ""))
})

if (copyToClipboard) {
  $(".copy-input").click(e => {
    const i = $("input[type=text]", $(e.delegateTarget).parents(".input-group"))
    copyToClipboard(selection(i)[1])
  }).show()
}

/*
$("#romaji-convert").click(() =>
  $("#romaji").val(romajiToHiragana($("#romaji").val()))
)

$("#romaji-modal").on("shown.bs.modal", () => $("#romaji").focus())
*/

const kanjiMatches = strokes => {
  const fuzzy   = $("#kanjidraw_chk_fuzzy" )[0].checked ? "yes" : "no",
        offby1  = $("#kanjidraw_chk_offby1")[0].checked ? "yes" : "no",
        url     = `/_kanji_matches?fuzzy=${fuzzy}&offby1=${offby1}`,
        done    = $("#kanjidraw_btn_done"), text = done.text()
  done.addClass("disabled").text("Loading...")
  return fetch_post(
    "kanji matches", url, JSON.stringify(strokes), true
  ).then(r => {
    done.removeClass("disabled").text(text)
    return r.text()
  })
}

let kanjiDrawCleanup = null

$("#kanjidraw-modal").on("shown.bs.modal", e => {
  const i = $("input[type=text]", $(e.relatedTarget).parents(".search-form"))
  $(".kanjidraw_chk").prop("checked", false)
  kanjiDrawCleanup = kanjiDraw({
    draw:         $("#kanjidraw_draw"),
    btn_undo:     $("#kanjidraw_btn_undo"),
    btn_clear:    $("#kanjidraw_btn_clear"),
    lbl_strokes:  $("#kanjidraw_lbl_strokes"),
    btn_done:     $("#kanjidraw_btn_done"),
    canvas:       $("#kanjidraw_canvas"),
    results:      $("#kanjidraw_results"),
    btn_back:     $("#kanjidraw_btn_back"),
    table:        $("#kanjidraw_table"),
    strokeStyle:  $("#kanjidraw_canvas").css("border-top-color"),
    buttonClass:  "jap btn btn-primary btn-lg m-1",
    gridColour:   $("#kanjidraw_canvas")[0].dataset.showGrid == "false" ?
                    $(".modal-content").css("background-color") : null,
    matches:      kanjiMatches,
    select: k => {
      const v = i.val(), p = i[0].selectionEnd
      i.val(v.slice(0, p) + k + v.slice(p))
      $("#kanjidraw-modal").modal("hide")
      setTimeout(() => {
        i.focus()
        i[0].selectionStart = i[0].selectionEnd = p + 1
      })
    },
  })
}).on("hidden.bs.modal", () => kanjiDrawCleanup())

const chooseRadicals = (elems, toggle = true) => {
  const q = $("#kanji-query"), v = q.val().trim().replace(/^\+r\s*/, "")
  let rs = [...v]
  elems.each((i, e) => {
    const r = e.innerText.trim(), inc = rs.includes(r)
    if (toggle) {
      if (inc) { rs = rs.filter(c => c != r) } else { rs.push(r) }
    }
    $(e)[((toggle ? !inc : inc) ? "add" : "remove") + "Class"]("chosen")
  })
  if (toggle) { q.val("+r " + rs.join("")) }
}

$(".radical").click(e => chooseRadicals($(e.delegateTarget)))

$("#radical-modal").on("shown.bs.modal", () =>
  chooseRadicals($(".radical"), false)
).on("hidden.bs.modal", () =>
  setTimeout(() => $("#kanji-query").focus())
)

$("#history-modal").on("shown.bs.modal", () => populateHistoryList())

$("#history-clear").click(async () => {
  if (await confirm("Clear search history?")) {
    $("#history").empty(); clearHistory()
  }
})

$(".lazy-iframe-modal").on("shown.bs.modal", evt => {
  const e = $(evt.delegateTarget).off("shown.bs.modal")
  $("iframe", e).each((i, x) => x.src = x.dataset.src)
})

$(".query-example").click(evt => {
  const e = $(evt.delegateTarget)
  const i = $("input[type=text]", e.parents("form"))
  i.val(e.text().trim()).focus()
  return false
})

$("#toggle-romaji").click(evt => {
  const e = evt.delegateTarget
  if (e.dataset.roma == "show") {
    e.dataset.roma = "hide"
    $(".romaji").addClass("d-none")
  } else {
    e.dataset.roma = "show"
    $(".romaji").removeClass("d-none")
  }
  return false
}).removeClass("disabled")

$("#expand-all").click(() => {
  $(".container .collapseall").collapse("show")
  return false
}).removeClass("disabled")

$("#collapse-all").click(() => {
  $(".container .collapseall").collapse("hide")
  return false
}).removeClass("disabled")

$(".collapsebtn").removeClass("disabled")

$("[data-toggle='tooltip']").tooltip().click(evt =>
  $(evt.delegateTarget).tooltip("hide")
)

const disableJLPT = () =>
  $("select[name=jlpt]").filter((i, x) => !x.value)
    .prop("disabled", true)
const enableJLPT = () =>
  $("select[name=jlpt]").prop("disabled", false)
$("#jmdict-query").parents("form").submit(disableJLPT)

const showLoading = () => {
  $("form.search-form .dropdown-toggle").addClass("disabled")
  $(".search-button").addClass("disabled").text("Loading...")
}
const undoLoading = () => {
  $("form.search-form .dropdown-toggle").removeClass("disabled")
  $(".search-button").removeClass("disabled")
    .each((i, x) => $(x).text(x.dataset.text))
}
$("form.search-form").submit(showLoading)

// TODO
$(".search-alt").click(evt => {
  const e = evt.delegateTarget, r = e.dataset.route
  const f = $(`<form action="/${r}">`)
  const i = $('<input type="hidden" name="query" />')
  let   v = $("input[type=text]", $(e).parents("form")).val()
  if (/sentences|stroke/.test(r)) { v = v.replace(/^\s*\+[=1w]\s*/, "") }
  $("body").append(f.append(i.val(v)))
  f.submit(showLoading).submit().remove()
  return false
})

// NB: undo modifications for firefox page cache
$(window).on("pageshow", () => { enableJLPT(); undoLoading() })

// === save history & pywebview & token ===

saveHistory()

$(window).on("pywebviewready", () => {
  $("#prefs-token").val(window.pywebview.token)
  if (localStorage.getItem("history_loaded") == "loaded") {
    fetch_post(
      "save history", `/__save_history__/${window.pywebview.token}`,
      localStorage.getItem("history")
    )
  } else {
    fetch_post(
      "load history", `/__load_history__/${window.pywebview.token}`,
    ).then(r => r.text()).then(data => {
      localStorage.setItem("history_loaded", "loaded")
      if (data) { localStorage.setItem("history", data) }
    })
  }
})

// === loaded ===

undoLoading()
$("#loading").modal("hide").remove()

})  // $(document).ready

}   // browser

})()

// vim: set tw=70 sw=2 sts=2 et fdm=marker :
// @license-end
