import { useEffect, useRef } from 'react'
import COAST_RAW from './coastline.js'

/*
 * GlobeDispatch
 * -------------
 * A ballistic dispatch board: dotted great-circle arcs, lifted off the surface,
 * fanning from Buenos Aires to cities across the United States. Drawn on a 2D
 * canvas with a hand-rolled 3D projection, so arcs are properly hidden when
 * they pass behind the globe.
 *
 * No dependencies beyond React, no network calls, no image assets. Everything
 * it needs is in this file and coastline.js.
 *
 * Props
 *   cities     how many US destinations, subsampled evenly across the list
 *   tempo      seconds between launches
 *   lift       arc apex height, in globe radii (0 skims the surface)
 *   size       globe radius in drawing units, where 1080 units is the canvas width
 *   distance   camera distance in globe radii; lower means stronger perspective
 *   offsetX    framing offset, fraction of canvas width
 *   offsetY    framing offset, fraction of canvas height
 *   globe      { spin, tilt, roll }   rotations of the earth about its own axes
 *   camera     { yaw, pitch, roll }   rotations of the camera about its own axes
 *   loop       seconds per cycle
 *   aspect     CSS aspect ratio of the canvas
 *   palette    colour overrides, see PALETTE below
 *   paused     freeze the animation (it keeps the last frame)
 *   className, style   forwarded to the canvas
 */

const US_CITIES = [
  [-122.3321, 47.6062], [-122.6765, 45.5231], [-122.4194, 37.7749],
  [-118.2437, 34.0522], [-117.1611, 32.7157], [-112.0740, 33.4484],
  [-111.8910, 40.7608], [-104.9903, 39.7392], [-106.6504, 35.0844],
  [-97.7431, 30.2672], [-96.7970, 32.7767], [-95.3698, 29.7604],
  [-94.5786, 39.0997], [-93.2650, 44.9778], [-87.6298, 41.8781],
  [-90.1994, 38.6270], [-86.7816, 36.1627], [-90.0715, 29.9511],
  [-83.0458, 42.3314], [-84.3880, 33.7490], [-80.1918, 25.7617],
  [-77.0369, 38.9072], [-74.0060, 40.7128], [-71.0589, 42.3601],
]

const BUENOS_AIRES = [-58.3816, -34.6037]

// colour tokens, matching the rest of the site
const PALETTE = {
  ocean: '#050a0e',   // background behind and inside the globe
  sphere: '#0b1119',  // globe fill, a hair lighter than the ocean
  coast: '#10b981',   // continent outlines
  route: '#34d399',   // arcs
  pin: '#6ee7b7',     // launch pad and destination markers
  glow: '#10b981',    // halo and bloom
  limb: 'rgba(255,255,255,0.10)',
}

const RAD = Math.PI / 180
const LOGICAL_WIDTH = 1080 // the drawing space the constants are tuned for
const SAMPLES = 220        // points per arc
const DRAW_SECONDS = 0.8   // time an arc takes to travel
const FLARE_SECONDS = 0.55 // how long the arrival flare lasts

/* ------------------------------------------------------------ vector math */
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
const mul = (a, s) => [a[0] * s, a[1] * s, a[2] * s]
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
const len = (a) => Math.sqrt(dot(a, a))
const norm = (a) => {
  const l = len(a) || 1
  return [a[0] / l, a[1] / l, a[2] / l]
}
const cross = (a, b) => [
  a[1] * b[2] - a[2] * b[1],
  a[2] * b[0] - a[0] * b[2],
  a[0] * b[1] - a[1] * b[0],
]
const clamp = (v, lo, hi) => (v < lo ? lo : v > hi ? hi : v)

function lonLatToVector(lon, lat) {
  const la = lat * RAD
  const lo = lon * RAD
  const c = Math.cos(la)
  return [c * Math.cos(lo), c * Math.sin(lo), Math.sin(la)]
}

function slerp(a, b, t) {
  const d = Math.acos(clamp(dot(a, b), -1, 1))
  if (d < 1e-9) return [a[0], a[1], a[2]]
  const s = Math.sin(d)
  const c1 = Math.sin((1 - t) * d) / s
  const c2 = Math.sin(t * d) / s
  return [a[0] * c1 + b[0] * c2, a[1] * c1 + b[1] * c2, a[2] * c1 + b[2] * c2]
}

// Rodrigues rotation of v about a unit axis
function rotate(v, axis, angle) {
  const c = Math.cos(angle)
  const s = Math.sin(angle)
  const kd = dot(axis, v)
  const kc = cross(axis, v)
  return [
    v[0] * c + kc[0] * s + axis[0] * kd * (1 - c),
    v[1] * c + kc[1] * s + axis[1] * kd * (1 - c),
    v[2] * c + kc[2] * s + axis[2] * kd * (1 - c),
  ]
}

const RGB_CACHE = new Map()
function hexToRgbTriplet(hex) {
  const cached = RGB_CACHE.get(hex)
  if (cached) return cached
  const h = hex.replace('#', '')
  const full = h.length === 3 ? h.split('').map((c) => c + c).join('') : h
  const n = parseInt(full, 16)
  const out = `${(n >> 16) & 255},${(n >> 8) & 255},${n & 255}`
  RGB_CACHE.set(hex, out)
  return out
}

// parse the coastline once per page load, not per mount
let COAST_POLYS = null
function coastlines() {
  if (COAST_POLYS) return COAST_POLYS
  const polys = []
  const chunks = COAST_RAW.split(';')
  for (let i = 0; i < chunks.length; i++) {
    const raw = chunks[i].split(' ')
    const pts = []
    for (let j = 0; j < raw.length; j++) {
      const c = raw[j].split(',')
      pts.push(lonLatToVector(parseFloat(c[0]), parseFloat(c[1])))
    }
    if (pts.length > 1) polys.push(pts)
  }
  COAST_POLYS = polys
  return polys
}

// pick n destinations spread across the list rather than slicing off the top
function selectCities(n) {
  const total = US_CITIES.length
  const count = Math.max(2, Math.min(total, Math.round(n)))
  if (count >= total) return US_CITIES.slice()
  const out = []
  for (let i = 0; i < count; i++) out.push(US_CITIES[Math.round((i * (total - 1)) / (count - 1))])
  return out
}

/* ---------------------------------------------------------------- engine */
function createEngine(canvas) {
  const ctx = canvas.getContext('2d')
  const polys = coastlines()

  let cfg = null
  let raf = null
  let startTime = null
  let pausedAt = null
  let stillMode = false // reduced motion: draw one frame and stay put

  // canvas size in device pixels, plus the logical drawing space
  let dpr = 1
  let W = LOGICAL_WIDTH
  let H = LOGICAL_WIDTH
  let scale = 1

  // camera state
  let eye = [0, 0, 0]
  let rc = [1, 0, 0]
  let uc = [0, 1, 0]
  let fc = [0, 0, -1]
  let focal = 1
  let rsil = 1
  let origin = [0, 0]
  let aVec = [0, 0, 0]
  let view0 = [0, 0, 1]
  let right0 = [1, 0, 0]

  // projected scene
  let coastRuns = []
  let arcs = []
  let cityVecs = []
  let arcPoints = []

  function buildCities() {
    if (!cfg) return
    const list = selectCities(cfg.cities)
    cityVecs = list.map(([lon, lat]) => lonLatToVector(lon, lat))
    aVec = lonLatToVector(BUENOS_AIRES[0], BUENOS_AIRES[1])

    let sum = [0, 0, 0]
    for (let i = 0; i < cityVecs.length; i++) sum = add(sum, cityVecs[i])
    sum = norm(sum)
    // home frame: centred on the Buenos Aires / US axis, rolled so the United
    // States sits left and Argentina right
    view0 = norm(add(aVec, sum))
    right0 = norm(sub(aVec, mul(view0, dot(aVec, view0))))
    buildArcs()
  }

  function buildArcs() {
    if (!cfg) return
    const lift = cfg.lift
    arcPoints = cityVecs.map((b) => {
      const pts = []
      for (let j = 0; j < SAMPLES; j++) {
        const u = j / (SAMPLES - 1)
        const h = 1 + lift * 4 * u * (1 - u)
        pts.push(mul(norm(slerp(aVec, b, u)), h))
      }
      return pts
    })
  }

  // globe rotations run first, about the earth's own axes: z is the polar axis,
  // x and y are equatorial
  function globeRotate(p) {
    if (!cfg) return p
    let q = p
    if (cfg.globe.spin) q = rotate(q, [0, 0, 1], cfg.globe.spin * RAD)
    if (cfg.globe.tilt) q = rotate(q, [1, 0, 0], cfg.globe.tilt * RAD)
    if (cfg.globe.roll) q = rotate(q, [0, 1, 0], cfg.globe.roll * RAD)
    return q
  }

  // camera rotations run on the rig: yaw about its own up, pitch about its own
  // right, roll about its own forward. The eye sits on the forward axis, so yaw
  // and pitch orbit the globe while roll spins the image.
  function setCamera() {
    if (!cfg) return
    fc = mul(view0, -1)
    rc = right0
    uc = cross(view0, right0)
    const { yaw, pitch, roll } = cfg.camera
    if (yaw) {
      const a = rotate(rc, uc, yaw * RAD)
      const b = rotate(fc, uc, yaw * RAD)
      rc = a
      fc = b
    }
    if (pitch) {
      const c = rotate(uc, rc, pitch * RAD)
      const d = rotate(fc, rc, pitch * RAD)
      uc = c
      fc = d
    }
    if (roll) {
      const e = rotate(rc, fc, roll * RAD)
      const f = rotate(uc, fc, roll * RAD)
      rc = e
      uc = f
    }
    const D = cfg.distance
    const h = 1 / D
    eye = mul(fc, -D)
    focal = (cfg.size * (D - h)) / Math.sqrt(1 - h * h)
    rsil = cfg.size
    origin = project(aVec)
  }

  function project(p) {
    if (!cfg) return [0, 0]
    const rel = sub(p, eye)
    const z = dot(rel, fc)
    return [
      W / 2 + cfg.offsetX * W + (focal * dot(rel, rc)) / z,
      H / 2 + cfg.offsetY * H - (focal * dot(rel, uc)) / z,
    ]
  }

  // hidden by the globe: tangent test on the surface, ray test above it
  function occluded(p) {
    if (len(p) < 1.0005) return dot(p, eye) <= 1
    const d = sub(p, eye)
    const L = len(d)
    const u = mul(d, 1 / L)
    const t0 = -dot(eye, u)
    if (t0 <= 0) return false
    const d2 = dot(eye, eye) - t0 * t0
    if (d2 >= 1) return false
    return t0 - Math.sqrt(1 - d2) < L - 1e-9
  }

  function rebuild() {
    const aRot = globeRotate(aVec)
    const cityRot = cityVecs.map(globeRotate)
    const spawn = dot(aRot, eye) > 1

    coastRuns = []
    for (let i = 0; i < polys.length; i++) {
      let run = null
      for (let j = 0; j < polys[i].length; j++) {
        const q = globeRotate(polys[i][j])
        if (occluded(q)) {
          run = null
          continue
        }
        if (!run) {
          run = [[], []]
          coastRuns.push(run)
        }
        const s = project(q)
        run[0].push(s[0])
        run[1].push(s[1])
      }
    }
    coastRuns = coastRuns.filter((r) => r[0].length > 1)

    arcs = arcPoints.map((pts, i) => {
      const sc = []
      const runs = []
      let runStart = -1
      for (let j = 0; j < SAMPLES; j++) {
        const q = globeRotate(pts[j])
        const s = project(q)
        sc.push(s[0], s[1])
        if (!occluded(q)) {
          if (runStart < 0) runStart = j
        } else if (runStart >= 0) {
          runs.push([runStart, j - 1])
          runStart = -1
        }
      }
      if (runStart >= 0) runs.push([runStart, SAMPLES - 1])
      return {
        sc,
        runs,
        dest: project(cityRot[i]),
        destVisible: !occluded(cityRot[i]),
        spawnVisible: spawn,
        launch: i * (cfg ? cfg.tempo : 0),
      }
    })
  }

  /* ------------------------------------------------------------ drawing */
  function glowDot(x, y, r, alpha) {
    if (!cfg) return
    const g = ctx.createRadialGradient(x, y, 0, x, y, r)
    g.addColorStop(0, `rgba(${cfg.rgb.glow},${0.95 * alpha})`)
    g.addColorStop(0.35, `rgba(${cfg.rgb.glow},${0.35 * alpha})`)
    g.addColorStop(1, `rgba(${cfg.rgb.glow},0)`)
    ctx.fillStyle = g
    ctx.beginPath()
    ctx.arc(x, y, r, 0, 6.2832)
    ctx.fill()
  }

  function inRun(arc, idx) {
    for (let i = 0; i < arc.runs.length; i++) {
      if (idx >= arc.runs[i][0] && idx <= arc.runs[i][1]) return true
    }
    return false
  }

  function strokeArc(arc, head) {
    for (let i = 0; i < arc.runs.length; i++) {
      const s = arc.runs[i][0]
      const e = Math.min(arc.runs[i][1], head - 1)
      if (e <= s) continue
      ctx.beginPath()
      ctx.moveTo(arc.sc[2 * s], arc.sc[2 * s + 1])
      for (let j = s + 1; j <= e; j++) ctx.lineTo(arc.sc[2 * j], arc.sc[2 * j + 1])
      ctx.stroke()
    }
  }

  function render(t) {
    if (!cfg) return
    const loop = cfg.loop
    const fadeStart = loop - 0.55
    const fadeEnd = loop - 0.05
    const a = t < fadeStart ? 1 : Math.max(0, (fadeEnd - t) / (fadeEnd - fadeStart))

    ctx.setTransform(scale, 0, 0, scale, 0, 0)
    ctx.globalAlpha = 1
    ctx.fillStyle = cfg.palette.ocean
    ctx.fillRect(0, 0, W, H)

    // halo. The globe itself never fades, only the launches do.
    const cx = W / 2 + cfg.offsetX * W
    const cy = H / 2 + cfg.offsetY * H
    const halo = ctx.createRadialGradient(cx, cy, rsil * 0.97, cx, cy, rsil * 1.3)
    halo.addColorStop(0, `rgba(${cfg.rgb.glow},0.20)`)
    halo.addColorStop(0.4, `rgba(${cfg.rgb.glow},0.06)`)
    halo.addColorStop(1, `rgba(${cfg.rgb.glow},0)`)
    ctx.fillStyle = halo
    ctx.beginPath()
    ctx.arc(cx, cy, rsil * 1.3, 0, 6.2832)
    ctx.fill()

    // the globe
    ctx.fillStyle = cfg.palette.sphere
    ctx.beginPath()
    ctx.arc(cx, cy, rsil, 0, 6.2832)
    ctx.fill()
    ctx.strokeStyle = cfg.palette.limb
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.arc(cx, cy, rsil, 0, 6.2832)
    ctx.stroke()

    // continents
    ctx.strokeStyle = cfg.palette.coast
    ctx.lineWidth = 2
    ctx.lineJoin = 'round'
    ctx.lineCap = 'round'
    for (let i = 0; i < coastRuns.length; i++) {
      const run = coastRuns[i]
      ctx.beginPath()
      for (let j = 0; j < run[0].length; j++) {
        if (j) ctx.lineTo(run[0][j], run[1][j])
        else ctx.moveTo(run[0][j], run[1][j])
      }
      ctx.stroke()
    }

    // arcs
    for (let i = 0; i < arcs.length; i++) {
      const arc = arcs[i]
      const p = clamp((t - arc.launch) / DRAW_SECONDS, 0, 1)
      if (p <= 0) continue
      const head = 1 + Math.floor(p * (SAMPLES - 1))

      ctx.strokeStyle = cfg.palette.route
      ctx.globalAlpha = 0.14 * a
      ctx.lineWidth = 9
      strokeArc(arc, head)
      ctx.globalAlpha = 0.92 * a
      ctx.lineWidth = 2.4
      strokeArc(arc, head)
      ctx.globalAlpha = 1

      if (p < 1 && inRun(arc, head - 1)) {
        // warhead in flight
        const hx = arc.sc[2 * (head - 1)]
        const hy = arc.sc[2 * (head - 1) + 1]
        glowDot(hx, hy, 26, a)
        ctx.fillStyle = cfg.palette.pin
        ctx.beginPath()
        ctx.arc(hx, hy, 5.5, 0, 6.2832)
        ctx.fill()
      }

      const dt = t - arc.launch
      if (dt < 0.28 && arc.spawnVisible) {
        // ignition at the pad
        const f = dt / 0.28
        ctx.strokeStyle = cfg.palette.pin
        ctx.globalAlpha = 0.3 * a * (1 - f)
        ctx.lineWidth = 2.6
        ctx.beginPath()
        ctx.arc(origin[0], origin[1], 14 + 26 * f, 0, 6.2832)
        ctx.stroke()
        ctx.globalAlpha = 1
      }

      const fa = (t - (arc.launch + DRAW_SECONDS)) / FLARE_SECONDS
      if (fa > 0 && arc.destVisible) {
        // arrival
        const f = Math.min(fa, 1)
        const dx = arc.dest[0]
        const dy = arc.dest[1]
        if (f < 1) {
          ctx.strokeStyle = cfg.palette.pin
          ctx.globalAlpha = 0.55 * a * (1 - f)
          ctx.lineWidth = 2.4
          ctx.beginPath()
          ctx.arc(dx, dy, 6 + 30 * f, 0, 6.2832)
          ctx.stroke()
          ctx.globalAlpha = 1
        }
        const s2 = 1 + 0.9 * Math.sin(Math.PI * f)
        glowDot(dx, dy, 22 * s2, 0.5 * a)
        ctx.globalAlpha = a
        ctx.fillStyle = cfg.palette.pin
        ctx.beginPath()
        ctx.arc(dx, dy, 5.2 * s2, 0, 6.2832)
        ctx.fill()
        ctx.globalAlpha = 1
      }
    }

    // launch pad. Part of the map, so it stays lit through the fade.
    if (arcs.length && arcs[0].spawnVisible) {
      glowDot(origin[0], origin[1], 30, 0.75)
      ctx.fillStyle = cfg.palette.pin
      ctx.beginPath()
      ctx.arc(origin[0], origin[1], 8.5, 0, 6.2832)
      ctx.fill()
      ctx.fillStyle = cfg.palette.ocean
      ctx.beginPath()
      ctx.arc(origin[0], origin[1], 3.4, 0, 6.2832)
      ctx.fill()
    }
  }

  /* ------------------------------------------------------------- sizing */
  function resize() {
    const rect = canvas.getBoundingClientRect()
    dpr = Math.min(window.devicePixelRatio || 1, 2)
    const cw = Math.max(1, Math.round(rect.width * dpr))
    const ch = Math.max(1, Math.round(rect.height * dpr))
    if (canvas.width !== cw || canvas.height !== ch) {
      canvas.width = cw
      canvas.height = ch
    }
    scale = cw / LOGICAL_WIDTH
    W = LOGICAL_WIDTH
    H = ch / scale
    setCamera()
    rebuild()
    render(currentTime())
  }

  function currentTime() {
    if (!cfg) return 0
    if (pausedAt !== null) return pausedAt
    if (startTime === null) return 0
    return ((performance.now() - startTime) / 1000) % cfg.loop
  }

  function tick() {
    render(currentTime())
    raf = requestAnimationFrame(tick)
  }

  function start() {
    if (!cfg) return
    if (stillMode) {
      // never resume out of a still
      if (pausedAt !== null) render(pausedAt)
      return
    }
    if (raf !== null) return
    if (startTime === null) startTime = performance.now()
    if (pausedAt !== null) {
      render(pausedAt)
      return
    }
    raf = requestAnimationFrame(tick)
  }

  function stop() {
    if (raf !== null) {
      cancelAnimationFrame(raf)
      raf = null
    }
  }

  return {
    // settings changed: rebuild what depends on them, keep the clock
    update(next) {
      if (!cfg) {
        cfg = next
        buildCities()
        setCamera()
        rebuild()
        start()
        return
      }
      const citiesChanged = next.cities !== cfg.cities
      const liftChanged = next.lift !== cfg.lift
      const structural =
        citiesChanged ||
        liftChanged ||
        next.size !== cfg.size ||
        next.distance !== cfg.distance ||
        next.offsetX !== cfg.offsetX ||
        next.offsetY !== cfg.offsetY ||
        next.globe.spin !== cfg.globe.spin ||
        next.globe.tilt !== cfg.globe.tilt ||
        next.globe.roll !== cfg.globe.roll ||
        next.camera.yaw !== cfg.camera.yaw ||
        next.camera.pitch !== cfg.camera.pitch ||
        next.camera.roll !== cfg.camera.roll

      cfg = next
      if (citiesChanged) buildCities()
      else if (liftChanged) buildArcs()
      if (structural) {
        setCamera()
        rebuild()
      } else {
        render(currentTime())
      }
      start()
    },
    resize,
    setPaused(value) {
      if (stillMode) {
        render(pausedAt ?? 0)
        return
      }
      if (value) {
        stop()
        pausedAt = currentTime()
        render(pausedAt)
      } else {
        pausedAt = null
        start()
      }
    },
    showStill(t) {
      stillMode = true
      stop()
      pausedAt = t
      render(t)
    },
    dispose() {
      stop()
    },
  }
}

/* ------------------------------------------------------------ component */
export default function GlobeDispatch({
  cities = 24,
  tempo = 0.075,
  lift = 0.24,
  size = 460,
  distance = 14,
  offsetX = -0.06,
  offsetY = 0.43,
  globe,
  camera,
  loop = 4,
  aspect = 16 / 9,
  palette,
  paused = false,
  className,
  style,
}) {
  const canvasRef = useRef(null)
  const engineRef = useRef(null)
  const reducedRef = useRef(false)

  const settings = {
    cities,
    tempo,
    loop,
    lift,
    size,
    distance,
    offsetX,
    offsetY,
    globe: { spin: 12, tilt: -22, roll: 17, ...globe },
    camera: { yaw: -22, pitch: 2, roll: 12, ...camera },
    palette: { ...PALETTE, ...palette },
  }
  const key = JSON.stringify(settings)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return undefined

    const engine = createEngine(canvas)
    engineRef.current = engine

    // honour prefers-reduced-motion with a single representative still
    reducedRef.current =
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const reduced = reducedRef.current

    const ro =
      typeof ResizeObserver !== 'undefined'
        ? new ResizeObserver(() => engine.resize())
        : null
    if (ro) ro.observe(canvas)
    window.addEventListener('resize', engine.resize)

    // stop burning frames while the canvas is off screen
    const io =
      typeof IntersectionObserver !== 'undefined'
        ? new IntersectionObserver(
            ([entry]) => {
              if (reduced) return
              if (entry.isIntersecting) engine.setPaused(false)
              else engine.setPaused(true)
            },
            { rootMargin: '120px' }
          )
        : null
    if (io) io.observe(canvas)

    return () => {
      if (ro) ro.disconnect()
      if (io) io.disconnect()
      window.removeEventListener('resize', engine.resize)
      engine.dispose()
      engineRef.current = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const engine = engineRef.current
    if (!engine) return
    const parsed = JSON.parse(key)
    engine.update({ ...parsed, rgb: { glow: hexToRgbTriplet(parsed.palette.glow) } })
    // drawn after the config lands, since render() reads it
    if (reducedRef.current) engine.showStill(loop * 0.65)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, loop])

  useEffect(() => {
    const engine = engineRef.current
    if (engine) engine.setPaused(paused)
  }, [paused])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      style={{
        display: 'block',
        width: '100%',
        aspectRatio: String(aspect),
        background: settings.palette.ocean,
        ...style,
      }}
    />
  )
}
