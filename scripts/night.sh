#!/bin/bash
# scripts/night.sh   crontab: 0 2 * * * cd ~/second_brain && ./scripts/night.sh
set -e
day=$(date +%F)

# 02:00 free mechanical checks from Obsidian itself
obsidian orphans > reports/$day-mechanical.txt
obsidian unresolved >> reports/$day-mechanical.txt
obsidian deadends >> reports/$day-mechanical.txt
# 02:05 the scout lints every page changed since the last run
claude -p "Run the LINT rules in CLAUDE.md. Mechanical issues are in reports/$day-mechanical.txt." \
  --model haiku --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Write"
# 02:20 the librarian curates the day's sources
claude -p "Use the curate skill on everything logged today. Max 15 page edits per source." \
  --model opus --permission-mode acceptEdits
# 02:50 one summary for the morning
claude -p "Write reports/$day.md: what changed, conflicts found, fixes proposed but not applied." \
  --model haiku --permission-mode acceptEdits --allowedTools "Read,Write"