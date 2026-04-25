# PLAN — Marketplace `hebstr`

> Reprise depuis nouvelle conversation. Objectif global : packager les skills perso en marketplace publishable, à la manière de `posit-dev-skills`.

## Contexte

- 8 skills perso actuellement standalone dans `~/.claude/skills/` (chacune son propre repo `.git`)
- Aucune skill perso n'est tagguée ni n'a de CHANGELOG (vérifié sur les 8)
- Modèle de référence : `~/.claude/plugins/marketplaces/posit-dev-skills/` — manifest minimal, multi-plugins, pas de tag, pas de CHANGELOG, juste `metadata.version`
- Publication envisagée à terme ("qualité pro") mais MVP fonctionnel d'abord

## Décisions actées

| Sujet | Décision |
|---|---|
| Marketplace name | `hebstr` (pas `hebstr-skills` — extensible : `litrev` MCP rejoindra plus tard sous `litrev@hebstr`) |
| Plugins MVP | 2 : `review` + `workflow` |
| `bookmarks-manager` | Reste standalone dans `~/.claude/skills/` (audience non-Claude) |
| `ref` | Reste standalone dans `~/.claude/skills/` (bibliothèque perso de notes, pas du tooling distribuable) |
| Composition `workflow` MVP | `sync-files` seul. Ajouts futurs possibles. |
| Versioning initial | Pas de tag git, pas de CHANGELOG.md, juste `metadata.version` (style posit-dev) |
| Historique git | Fresh — `cp -r` chaque skill, 1 commit `feat: import <name>` par skill (commits `.` actuels n'ont pas de valeur narrative à préserver) |
| Tag `v0.1.0` sur `review-walkthrough` | Abandonné — perd son sens dès la migration plugin |
| Emplacement repo | `~/Documents/pro/packages/claude/hebstr` (PAS `~/.claude/plugins/marketplaces/` qui est géré par le runtime — risque de collision lors de l'install via GitHub) |
| Emplacement fichiers Claude dans le repo | `.claude/` (PLAN.md, futurs handoffs, etc.) — convention globale CLAUDE.md |
| Workflow dev | Marketplace local + `plugin marketplace update <name>` à chaque modif. PAS de symlink (moins propre, ne reflète pas le comportement final côté users) |
| Gestion doublons pendant migration | Renommer `~/.claude/skills/<name>` en `<name>.bak.migration` après chaque `cp -r`+install, suppression définitive à l'Étape 4 |
| Migration future de `litrev` | À traiter à part — `litrev` est déjà publié comme marketplace standalone (`hebstr/litrev`). Fusion dans `hebstr` = déprécier l'ancienne marketplace + communication users. Décision reportée. |

## Composition cible

```
hebstr/
├── .claude-plugin/
│   └── marketplace.json
├── README.md
├── review/
│   ├── review-walkthrough/
│   ├── full-review/
│   ├── blindspot-review/
│   ├── skill-adversary/
│   └── mcp-adversary/
└── workflow/
    └── sync-files/
```

Skills restant standalone dans `~/.claude/skills/` :
- `bookmarks-manager`
- `ref`

## Étapes

### Étape 0 — Pré-migration ✅
- [x] Commit propre des 7 fichiers en attente dans `~/.claude/skills/review-walkthrough` (vrai message, pas `.`)
- [x] **Pas de tag** — migration en état clean

### Étape 1 — Skeleton marketplace
- [x] `mkdir ~/Documents/pro/packages/claude/hebstr` (+ sous-dossier `.claude/` créé, PLAN.md déplacé dedans)
- [ ] `git init` dans le repo
- [ ] Créer `.claude-plugin/marketplace.json` calqué sur posit-dev (cf. `~/.claude/plugins/marketplaces/posit-dev-skills/.claude-plugin/marketplace.json` pour le template exact). Marketplace name = `hebstr`. Pas de plugins déclarés à ce stade — juste le squelette.
- [ ] README.md minimal au niveau marketplace
- [ ] Commit initial `feat: marketplace skeleton`

**Reprise** : nouvelle session depuis `~/Documents/pro/packages/claude/hebstr`. Lire `.claude/PLAN.md` puis enchaîner sur `git init` + manifest.

### Étape 2 — Migration skills
Pour chaque skill (boucle) :
- [ ] `cp -r ~/.claude/skills/<name> ~/Documents/pro/packages/claude/hebstr/<plugin>/<name>` (review/ ou workflow/)
- [ ] Grep chemin absolu : `rg "~/.claude/skills/<name>" ~/Documents/pro/packages/claude/hebstr/<plugin>/<name>` — corriger si trouvé
- [ ] Ajouter le plugin au `marketplace.json` (à la première skill du plugin)
- [ ] Commit `feat: import <skill-name>`
- [ ] Renommer la version source : `mv ~/.claude/skills/<name> ~/.claude/skills/<name>.bak.migration` (évite doublons à l'install)

### Étape 3 — Test local
```bash
claude plugin marketplace add ~/Documents/pro/packages/claude/hebstr
claude plugin install review@hebstr
claude plugin install workflow@hebstr
```

À chaque modif post-install : `claude plugin marketplace update hebstr` pour rafraîchir le cache.

- [ ] Vérifier que les skills sont découvertes (Skill tool list)
- [ ] **Point critique** : tester que `review-walkthrough/scripts/scan-reviewers.py` trouve bien `skill-adversary` et `mcp-adversary` quand elles sont dans le contexte plugin et non plus dans `~/.claude/skills/`. Le mécanisme de découverte runtime peut casser silencieusement.
- [ ] Tester `full-review` et `blindspot-review` qui orchestrent `review-walkthrough`
- [ ] Vérifier que les `.bak.migration` ne causent pas de conflit (en théorie le nom du dossier change donc Claude ne devrait pas charger le `SKILL.md` dedans, mais à confirmer)

### Étape 4 — Bascule
- [ ] Supprimer les `~/.claude/skills/<name>.bak.migration`
- [ ] Garder `bookmarks-manager` et `ref` dans `~/.claude/skills/`
- [ ] Confirmer que tout fonctionne sans les `.bak`

## Différé pour publication "qualité pro"

À traiter après MVP fonctionnel, dans une session séparée :

- README marketplace soigné (description, install, liste plugins/skills)
- README par plugin
- LICENSE (MIT, comme posit-dev/ouroboros)
- Politique de versioning : si publication réelle et utilisateurs externes qui pinnent → introduire SemVer + CHANGELOG. Sinon rester sur le style minimal posit-dev.
- Repo public sur GitHub
- Annonce / discoverability
- **Décision fusion `litrev` → `hebstr`** : si oui, plan de migration users + dépréciation marketplace `hebstr/litrev` standalone

## Référents techniques

- Template manifest : `~/.claude/plugins/marketplaces/posit-dev-skills/.claude-plugin/marketplace.json`
- Layout multi-plugins de référence : `~/.claude/plugins/marketplaces/posit-dev-skills/` (7 plugins, 17 skills, certaines partagées entre plugins via path commun)
- Style versioning lourd (à éviter en MVP, à étudier pour version "pro") : `~/.claude/plugins/marketplaces/ouroboros/` — tags SemVer, CHANGELOG, version par plugin
- Cache des plugins installés : `~/.claude/plugins/cache/<marketplace>/<plugin>/<sha-or-id>/` (copie versionnée, pas un live link — d'où nécessité de `marketplace update`)
