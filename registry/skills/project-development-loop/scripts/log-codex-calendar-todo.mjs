const args = process.argv.slice(2)

const readArgs = (items) => {
  const flags = new Map()
  for (let index = 0; index < items.length; index += 1) {
    const item = items[index]
    if (!item.startsWith('--')) {
      continue
    }

    const key = item.slice(2)
    const next = items[index + 1]
    if (next === undefined || next.startsWith('--')) {
      flags.set(key, 'true')
      continue
    }

    flags.set(key, next)
    index += 1
  }
  return flags
}

const parseDuration = (value) => {
  const match = /^(\d+)(m|h|d)$/.exec(value)
  if (!match) {
    throw new Error(`Unsupported duration: ${value}`)
  }

  const amount = Number(match[1])
  const unit = match[2]
  if (unit === 'm') {
    return amount * 60 * 1000
  }
  if (unit === 'h') {
    return amount * 60 * 60 * 1000
  }
  return amount * 24 * 60 * 60 * 1000
}

const parseStamp = (flags, absoluteKey, relativeKey) => {
  const absolute = flags.get(absoluteKey)
  if (absolute) {
    return new Date(absolute).toISOString()
  }

  const relative = flags.get(relativeKey)
  if (!relative) {
    return null
  }

  return new Date(Date.now() + parseDuration(relative)).toISOString()
}

const flags = readArgs(args)
const dryRun = flags.get('dry-run') === 'true'
const apiBase = flags.get('api-base') ?? 'http://127.0.0.1:4321'
const endpoint = `${apiBase}/api/agents/intake`
const kind = flags.get('kind') ?? 'stage'
const type = flags.get('type') ?? 'bundle'
const provider = flags.get('provider') ?? 'codex'
const priority = flags.get('priority') ?? 'focus'
const reminderMinutes = flags.get('reminder-minutes')
const title = flags.get('title')
const detail = flags.get('detail') ?? ''
const paths = (flags.get('paths') ?? '')
  .split('|')
  .map((item) => item.trim())
  .filter(Boolean)
const startAt = parseStamp(flags, 'start-at', 'start-in')
const endAt = parseStamp(flags, 'end-at', 'end-in')
const dueAt = parseStamp(flags, 'due-at', 'due-in')
const duration = flags.get('duration')

if (!title) {
  throw new Error('Missing required --title')
}

const resolvedEndAt =
  endAt ??
  (startAt && duration ? new Date(new Date(startAt).getTime() + parseDuration(duration)).toISOString() : null)

const detailWithPaths =
  paths.length === 0
    ? detail
    : `${detail}${detail ? '\n\n' : ''}Refs:\n${paths.map((item) => `- ${item}`).join('\n')}`

const prefixedTitle = title.startsWith('[') ? title : `[${kind}] ${title}`
const payload = {
  type,
  provider,
  title: prefixedTitle,
  detail: detailWithPaths,
  dueAt,
  startAt,
  endAt: resolvedEndAt,
  goalId: null,
  priority,
  reminderMinutes: reminderMinutes ? Number(reminderMinutes) : null,
}

if (dryRun) {
  console.log(JSON.stringify({ endpoint, payload }, null, 2))
  process.exit(0)
}

const health = await fetch(`${apiBase}/api/health`)
if (!health.ok) {
  throw new Error(`Health check failed with status ${health.status}`)
}

const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload),
})

if (!response.ok) {
  throw new Error(await response.text())
}

console.log(JSON.stringify(await response.json(), null, 2))
