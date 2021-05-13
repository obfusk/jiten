// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPLv3+

//  --                                                          ; {{{1
//
//  File        : kanjidraw.js
//  Maintainer  : Felix C. Stegerman <flx@obfusk.net>
//  Date        : 2021-05-13
//
//  Copyright   : Copyright (C) 2021  Felix C. Stegerman
//  Version     : v0.2.0
//  License     : AGPLv3+
//
//  --                                                          ; }}}1

"use strict";

const kanjiDraw = config => {                                 //  {{{1
  const { draw, btn_undo, btn_clear, lbl_strokes, btn_done, canvas,
          results, btn_back, table } = config
  const buttonClass = config.buttonClass  || "",
        strokeStyle = config.strokeStyle  || "black",
        lineWidth   = config.lineWidth    || 5,
        columns     = config.columns      || 5,
        maxStrokes  = config.maxStrokes   || 30
  const ctx = canvas[0].getContext("2d")
  let drawing = false, x = 0, y = 0, strokes = [], lines = []

  const onPointerdown = e => {
    if (strokes.length >= maxStrokes) return
    drawing = true; x = e.offsetX; y = e.offsetY
    strokes.push([x * 255.0 / canvas[0].width,
                  y * 255.0 / canvas[0].height])
    lines.push([])
    enableButtons()
  }

  const onPointermove = e => {
    if (drawing) addLine(e.offsetX, e.offsetY)
  }

  const onPointerup = e => {
    if (!drawing) return
    drawing = false
    if (e.target === canvas[0]) addLine(e.offsetX, e.offsetY)
    strokes.slice(-1)[0].push(x * 255.0 / canvas[0].width,
                              y * 255.0 / canvas[0].height)
    updateStrokes()
  }

  const onUndo = () => {
    if (!strokes.length) return
    strokes.pop(); lines.pop()
    redrawLines(); updateStrokes()
    if (!strokes.length) disableButtons()
  }

  const onClear = () => {
    strokes = []; lines = []
    clearCanvas(); updateStrokes(); disableButtons()
  }

  const onDone = async () => {
    const matches = await config.matches(strokes),
          rows = Math.ceil(matches.length / columns)
    table.empty()
    for (let i = 0; i < rows; ++i) {
      const tr = $("<tr>")
      for (let j = 0; j < columns; ++j) {
        const p = i * columns + j
        if (p >= matches.length) break
        tr.append($("<td>").append(
          $("<button>").addClass(buttonClass)
            .text(matches[p]).click(onSelectKanji)
        ))
      }
      table.append(tr)
    }
    draw.hide(); results.show()
  }

  const onBack = () => { results.hide(); draw.show() }

  const onSelectKanji = e => {
    config.select($(e.delegateTarget).text())
    onClear(); onBack()
  }

  const addLine = (x2, y2) => {
    if (!(0 <= x2 && x2 <= canvas[0].width &&
          0 <= y2 && y2 <= canvas[0].height)) return
    drawLine(x, y, x2, y2)
    lines.slice(-1)[0].push([x, y, x2, y2])
    x = x2; y = y2
  }

  const drawLine = (x1, y1, x2, y2) => {
    ctx.beginPath()
    ctx.strokeStyle = strokeStyle
    ctx.lineWidth   = lineWidth
    ctx.lineCap     = ctx.lineJoin = "round"
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
    ctx.closePath()
  }

  const disableButtons = () => {
    for (const w of [btn_undo, btn_clear, btn_done])
      w.addClass("disabled").prop("disabled", true)
  }

  const enableButtons = () => {
    for (const w of [btn_undo, btn_clear, btn_done])
      w.removeClass("disabled").prop("disabled", false)
  }

  const updateStrokes = () =>
    lbl_strokes.text(`Strokes: ${strokes.length}`)

  const redrawLines = () => {
    clearCanvas()
    for (const stroke of lines)
      for (const line of stroke)
        drawLine(...line)
  }

  const clearCanvas = () =>
    ctx.clearRect(0, 0, canvas[0].width, canvas[0].height)

  const cleanup = () => {
    btn_undo  .off("click", onUndo)
    btn_clear .off("click", onClear)
    btn_done  .off("click", onDone)
    btn_back  .off("click", onBack)
    canvas    .off("pointerdown", onPointerdown)
    canvas    .off("pointermove", onPointermove)
    $(window) .off("pointerup"  , onPointerup)
  }

  onClear(); onBack()

  btn_undo  .on("click", onUndo)
  btn_clear .on("click", onClear)
  btn_done  .on("click", onDone)
  btn_back  .on("click", onBack)
  canvas    .on("pointerdown", onPointerdown)
  canvas    .on("pointermove", onPointermove)
  $(window) .on("pointerup"  , onPointerup)

  return cleanup
}                                                             //  }}}1

// vim: set tw=70 sw=2 sts=2 et fdm=marker :
// @license-end
