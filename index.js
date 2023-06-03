let totalMessages = [
  1000,
  10000,
  50000,
  100000,
  250000,
  500000,
  750000,
  1000000,
  2000000,
]

let totalClients = [
  1
]

function getLogsPath(baseName) {
  const logsPath = []
  totalClients.forEach(
    (totalClient) => {
      totalMessages.forEach(
        (totalMessage) => {
          for (let i = 1; i <= 4; i++)
            logsPath.push(`logs/${baseName}-${totalClient}-${totalMessage}-${i}.txt`)
        }
      )
    }
  )

  return logsPath
}

function getReportsPath(baseName) {
  const reportsPath = []

  for (let i = 1; i <= 4; i++)
    reportsPath.push(`reports/${baseName}/general-report-${i}.txt`)

  return reportsPath
}

const clientDiv1 = document.getElementById('clientLogs1')
const serverDiv1 = document.getElementById('serverLogs1')

const clientTeste1 = getLogsPath('client/teste1/client').map(
  (path) => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[3]

    return a
  }
)
const serverTeste1 = getLogsPath('server/teste1/server').map(
  (path) => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[3]

    return a
  }
)

clientTeste1.forEach(
  (a) => {
    clientDiv1.appendChild(a)
  }
)

serverTeste1.forEach(
  (a) => {
    serverDiv1.appendChild(a)
  }
)

totalMessages = [
  100
]

totalClients = [
  10,
  100,
  500,
  1000,
  2500,
  5000,
  7500,
  10000
]

const clientDiv2 = document.getElementById('clientLogs2')
const serverDiv2 = document.getElementById('serverLogs2')

const clientTeste2 = getLogsPath('client/teste2/client').map(
  path => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[3]

    return a
  }
)

const serverTeste2 = getLogsPath('server/teste2/server').map(
  path => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[3]

    return a
  }
)

clientTeste2.forEach(
  a => {
    clientDiv2.appendChild(a)
  }
)

serverTeste2.forEach(
  a => {
    serverDiv2.appendChild(a)
  }
)

const report1 = document.getElementById('report1')
const report1Links = getReportsPath('teste1').map(
  path => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[2]

    return a
  }
)

report1Links.forEach(
  a => {
    report1.appendChild(a)
  }
)

const report2 = document.getElementById('report2')
const report2Links = getReportsPath('teste2').map(
  path => {
    const a = document.createElement('a')
    a.href = path
    a.text = path.split('/')[2]

    return a
  }
)

report2Links.forEach(
  a => {
    report2.appendChild(a)
  }
)