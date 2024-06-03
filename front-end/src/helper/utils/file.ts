export default {
  exportCSV: (jsonData: any, fileName: string = 'exportCSV.csv') => {
    if (!jsonData || jsonData.length == 0) {
      return
    }
    const header = [
      'title',
      'url',
      'authors',
      'abstract',
      'code',
      'citation',
      'conf',
      'year'
    ]
    let csvText = ''
    csvText = `${header.join(',')}\n`

    jsonData.forEach((v: any) => {
      let row = ''
      header.map(key => {
        if (v[key] instanceof Array) {
          row += `"${v[key].join(',')}\t",`
        } else {
          row += `"${String(v[key]).replaceAll('"', '"')}\t",`
        }
      })
      row = row.substring(0, row.length - 1) + '\n'
      csvText += row
    })
    const uri =
      'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(csvText)
    const link = document.createElement('a')
    link.href = uri
    link.download = fileName
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  },
  exportTxt(jsonData: any, fileName: string = 'exportTXT.txt') {
    let text = ''
    jsonData.forEach((v: any) => {
      text += `[${v.conf + v.year}]\t${v.title}\r\n`
    })
    const uri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(text)
    const link = document.createElement('a')
    link.setAttribute('href', uri)
    link.setAttribute('download', fileName)
    link.click()
  }
}
