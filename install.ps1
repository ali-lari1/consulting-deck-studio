# Consulting Deck Studio installer for Windows (PowerShell). Copies the skill into every detected agent's skills folder.
#   powershell -ExecutionPolicy Bypass -File install.ps1            # install
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall
param([switch]$Uninstall, [switch]$All)
$ErrorActionPreference = "Stop"
$Name = "consulting-deck-studio"
$Src = Join-Path $PSScriptRoot "skills\$Name"
if (-not (Test-Path "$Src\SKILL.md")) { Write-Error "Run this from the cloned repository folder."; exit 1 }
$H = $env:USERPROFILE
$Targets = @(
  @{ id="agents";   path=".agents\skills";            det=@() },
  @{ id="claude";   path=".claude\skills";            det=@("claude", ".claude") },
  @{ id="gemini";   path=".gemini\skills";            det=@("gemini", ".gemini") },
  @{ id="opencode"; path=".config\opencode\skills";   det=@("opencode", ".config\opencode") },
  @{ id="hermes";   path=".hermes\skills";            det=@("hermes", ".hermes") },
  @{ id="grok";     path=".grok\skills";              det=@("grok", ".grok") },
  @{ id="codex";    path=".codex\skills";             det=@(".codex") },
  @{ id="cursor";   path=".cursor\skills";            det=@("cursor", ".cursor") },
  @{ id="copilot";  path=".copilot\skills";           det=@("copilot", ".copilot") },
  @{ id="kiro";     path=".kiro\skills";              det=@("kiro", ".kiro") },
  @{ id="cline";    path=".cline\skills";             det=@("cline", ".cline") },
  @{ id="windsurf"; path=".codeium\windsurf\skills";  det=@(".codeium\windsurf") }
)
function Detected($dets) {
  if ($dets.Count -eq 0) { return $true }
  foreach ($d in $dets) {
    if ($d.StartsWith(".")) { if (Test-Path (Join-Path $H $d)) { return $true } }
    elseif (Get-Command $d -ErrorAction SilentlyContinue) { return $true }
  }
  return $false
}
$n = 0
foreach ($t in $Targets) {
  $dest = Join-Path (Join-Path $H $t.path) $Name
  if ($Uninstall) { if (Test-Path "$dest\.cds-installed") { Remove-Item -Recurse -Force $dest; "removed $dest"; $n++ }; continue }
  if (-not $All -and -not (Detected $t.det)) { continue }
  if ((Test-Path $dest) -and -not (Test-Path "$dest\.cds-installed")) { "skipped $dest (not installed by this script)"; continue }
  New-Item -ItemType Directory -Force -Path (Join-Path $H $t.path) | Out-Null
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  Copy-Item -Recurse $Src $dest
  New-Item -ItemType File -Path "$dest\.cds-installed" | Out-Null
  "$($t.id) -> $dest"; $n++
}
"Done ($n). Restart your agent, then ask: 'Build the October SteerCo pack from these files' or /consulting-deck-studio"
