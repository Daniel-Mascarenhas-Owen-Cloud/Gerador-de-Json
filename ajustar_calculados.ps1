$ErrorActionPreference = 'Stop'
$source = 'C:\Users\OWEN CLOUD 02\Downloads\helio_filtrado_por_texto.json'
$destination = Join-Path $PSScriptRoot 'helio_calculados_ajustados.json'
$raw = [IO.File]::ReadAllText($source)
$doc = $raw | ConvertFrom-Json
$affected = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
$known = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($point in $doc.dataPoints) {
    [void]$known.Add($point.xid)
    if ($point.dataSourceXid -eq 'PBO_ETM_D') { [void]$affected.Add($point.xid) }
}
do {
    $added = 0
    foreach ($point in $doc.dataPoints) {
        foreach ($dependency in $point.pointLocator.context) {
            if ($affected.Contains($dependency.dataPointXid)) {
                if ($affected.Add($point.xid)) { $added++ }
                break
            }
        }
    }
} while ($added -gt 0)
$blocks = [regex]::Matches($raw, '(?ms)^      \{\r?\n.*?^      \}')
if ($blocks.Count -ne $doc.dataPoints.Count) { throw 'Quantidade de blocos inesperada.' }
$result = $raw
$changed = 0
for ($i = $blocks.Count - 1; $i -ge 0; $i--) {
    $point = $doc.dataPoints[$i]
    if ($point.dataSourceXid -ne 'PBO_Dados Calculados') { continue }
    $block = $blocks[$i]
    $expected = if ($affected.Contains($point.xid)) { 'false' } else { 'true' }
    $updated = [regex]::Replace($block.Value, '("enabled"\s*:\s*)(true|false)', "`${1}$expected")
    if ($updated -ne $block.Value) { $changed++ }
    $result = $result.Remove($block.Index, $block.Length).Insert($block.Index, $updated)
}
$verified = $result | ConvertFrom-Json
for ($i = 0; $i -lt $doc.dataPoints.Count; $i++) {
    $before = $doc.dataPoints[$i]
    $after = $verified.dataPoints[$i]
    if ($before.dataSourceXid -eq 'PBO_Dados Calculados') {
        if ($after.enabled -ne (-not $affected.Contains($before.xid))) { throw 'Estado incorreto.' }
        $after.enabled = $before.enabled
    }
    if (($before | ConvertTo-Json -Depth 100 -Compress) -cne ($after | ConvertTo-Json -Depth 100 -Compress)) { throw 'Alteracao inesperada.' }
}
[IO.File]::WriteAllText($destination, $result, [Text.UTF8Encoding]::new($false))
$calculated = @($doc.dataPoints | Where-Object dataSourceXid -eq 'PBO_Dados Calculados')
$disabled = @($calculated | Where-Object { $affected.Contains($_.xid) })
$missing = @($calculated | ForEach-Object { $_.pointLocator.context } | Where-Object { -not $known.Contains($_.dataPointXid) } | Select-Object -ExpandProperty dataPointXid -Unique)
"Ativos: $($calculated.Count - $disabled.Count); desativos: $($disabled.Count); alterados: $changed"
"Referencias ausentes: $($missing.Count)"
$missing
"Arquivo: $destination"
$disabled | Select-Object -ExpandProperty xid
