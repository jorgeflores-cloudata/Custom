# Installs the global `awake` and `cursor` functions into the PowerShell profile.
# Usage:  powershell -ExecutionPolicy Bypass -File .\setup.ps1
# Idempotent: safe to run multiple times; replaces the previous block.

param(
    [string]$ProfilePath = $PROFILE.CurrentUserAllHosts
)

$dir   = $PSScriptRoot
$start = '# >>> Custom functions (awake, cursor) >>>'
$end   = '# <<< Custom functions (awake, cursor) <<<'

$block = @"
$start
function awake {
    python "$dir\keep_awake.py" --minutes 600 --display @args
}

function cursor {
    python "$dir\move_cursor_to.py" --points '[[100,100],[500,300],[900,600]]' --repeat 200 --duration 5 --pause 0.2 @args
}
$end
"@

New-Item -ItemType File -Force $ProfilePath | Out-Null
$content = Get-Content $ProfilePath -Raw
if ($null -eq $content) { $content = '' }

$pattern = '(?s)' + [regex]::Escape($start) + '.*?' + [regex]::Escape($end)
if ($content -match $pattern) {
    $content = [regex]::Replace($content, $pattern, { $block })
} else {
    $content = $content.TrimEnd() + "`r`n`r`n" + $block + "`r`n"
}
Set-Content -Path $ProfilePath -Value $content -Encoding utf8

Write-Host "Functions installed in: $ProfilePath"
Write-Host "Open a new terminal and type 'awake' or 'cursor'."
