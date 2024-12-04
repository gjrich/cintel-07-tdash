# gjrich | Dec 2024
# Re-deploys the shiny assets based on any changes to the app.py

# created with the help of Claude.ai
# https://claude.ai

# Remove existing docs directory
Remove-Item -Path ".\docs" -Recurse -Force -ErrorAction SilentlyContinue

# Export app using shinylive
shinylive export .\app .\docs

# Update index.html
$content = Get-Content .\docs\index.html -Raw
$newContent = $content -replace '<title>Shiny App</title>', '<title>gjrich mod vii</title>'
$newContent = $newContent -replace '(<title>.*</title>)', "`$1`n    <link rel=`"icon`" type=`"image/x-icon`" href=`"app/favicon.ico`">"
$newContent | Set-Content .\docs\index.html -NoNewline
