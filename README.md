# Trendione Client — Compound Intelligence MVP

Local-first internal research catalogue for compounds and performance-enhancing substances. No login workflow is included; run on localhost only.

## Get the project bundle

The initial source bundle is stored as `compound-intelligence-mvp.zip.base64`. Decode it to a ZIP, then extract it:

**Windows PowerShell**
```powershell
[IO.File]::WriteAllBytes('compound-intelligence-mvp.zip', [Convert]::FromBase64String((Get-Content .\compound-intelligence-mvp.zip.base64 -Raw)))
Expand-Archive .\compound-intelligence-mvp.zip -DestinationPath .
```

**macOS / Linux**
```bash
base64 -d compound-intelligence-mvp.zip.base64 > compound-intelligence-mvp.zip
unzip compound-intelligence-mvp.zip
```

Then follow `compound-intelligence/README.md` for setup. The app uses Django and SQLite for straightforward local development, with PubChem identity lookup/import as the first external connector.

## Safety and scope

This is a research catalogue, not a clinical decision-support system. Imported chemical identities are provisional until reviewed. Do not expose the unauthenticated development server to a network or the public internet.