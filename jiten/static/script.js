$(document).ready(() => {
  $(".convert-kana").each((i, e) => $(e).click(() => {
    const i = $("input", $(e).parents(".input-group"))
    i.val(convertKana(i.val())).focus()
  }))
  $(".clear-input").each((i, e) => $(e).click(() => {
    $(".clear-input-checked", $(e).parents("form")).prop("checked", true)
    $("input", $(e).parents(".input-group")).val("").focus()
  }))
  $($("input")[0]).focus()
})

const convertKana = t => {
  for (const c of t) {
    if (HIRAGANA.indexOf(c) != -1) {
      return convertToKatakana(t)
    }
  }
  return convertToHiragana(t)
}

const convertToKatakana = t => {
  let col = null
  return [...t].map(c => {
    const i = HIRAGANA.indexOf(c)
    const o = col === 4 && i === 2
    const k = i === col || o ? "ー" : KATAKANA[i] || c
    if (!o) col = i === -1 ? null : i % 5
    return k
  }).join("")
}

const convertToHiragana = t => {
  return [...t].map(c => HIRAGANA[KATAKANA.indexOf(c)] || c).join("")
}

const HIRAGANA = `
あ い う え お
ぁ ぃ ぅ ぇ ぉ
-- -- ゔ -- --
か き く け こ
が ぎ ぐ げ ご
さ し す せ そ
ざ じ ず ぜ ぞ
た ち つ て と
だ ぢ づ で ど
-- -- っ -- --
な に ぬ ね の
は ひ ふ へ ほ
ば び ぶ べ ぼ
ぱ ぴ ぷ ぺ ぽ
ま み む め も
や -- ゆ -- よ
ゃ -- ゅ -- ょ
ら り る れ ろ
わ ゐ -- ゑ を
ゎ -- -- -- --
ん -- -- -- --
ゝ ゞ -- -- --
`.split(/\s+/).filter(x => x)

const KATAKANA = `
ア イ ウ エ オ
ァ ィ ゥ ェ ォ
-- -- ヴ -- --
カ キ ク ケ コ
ガ ギ グ ゲ ゴ
サ シ ス セ ソ
ザ ジ ズ ゼ ゾ
タ チ ツ テ ト
ダ ヂ ヅ デ ド
-- -- ッ -- --
ナ ニ ヌ ネ ノ
ハ ヒ フ ヘ ホ
バ ビ ブ ベ ボ
パ ピ プ ペ ポ
マ ミ ム メ モ
ヤ -- ユ -- ヨ
ャ -- ュ -- ョ
ラ リ ル レ ロ
ワ ヰ -- ヱ ヲ
ヮ -- -- -- --
ン -- -- -- --
ヽ ヾ -- -- --
`.split(/\s+/).filter(x => x)
