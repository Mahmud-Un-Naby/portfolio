#!/usr/bin/env python3
"""Build the resume and shared portfolio sections from confirmed public profile data."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / 'data/profile.json').read_text())

def e(value):
    return html.escape(str(value), quote=True)

def link(url, label, extra=''):
    return f'<a href="{e(url)}"{extra}>{e(label)}</a>'

links = p['links']
email = link('mailto:' + p['email'], p['email'])
phone = link('tel:' + p['phone'], p['phone'])
social = ' · '.join(link(links[key], label) for key, label in [('linkedin','LinkedIn'),('github','GitHub'),('codeforces','Codeforces / Mahmud_Saikat'),('portfolio','Portfolio')])
skill_lines = ''.join(f'<p><strong>{e(group["category"])}:</strong> {e(", ".join(group["items"]))}</p>' for group in p['skills'])
project_lines = ''
for project in p['projects']:
    title = link(links['portfolio'] + '#' + project['id'] + '-title', project['name'])
    dates = f' · {e(project["dates"])}' if project.get('dates') else ''
    project_lines += f'<article class="resume-project"><h3>{title} <span>{e(project["role"])}{dates}</span></h3><p class="stack">{e(project["stack"])}</p><ul>'
    project_lines += ''.join(f'<li>{e(bullet)}</li>' for bullet in project['bullets'])
    project_lines += f'</ul><p class="project-note">{e(project["status"])} · {link(links["portfolio"] + "#" + project["id"] + "-title", "Project overview")}</p></article>'
contest_lines = ''
iupc_results = []
for result in p['achievements']:
    if result['contest'].endswith(' IUPC'):
        iupc_results.append(f'{e(result["place"])} — {e(result["contest"].removesuffix(" IUPC"))} {e(result["year"])}')
        continue
    name = f'{result.get("organizer", "")} {result["contest"]}'.strip()
    label = f'{name} {result["year"]}'
    title = link(result['url'], label) if result.get('url') else e(label)
    team = f' — Team {e(result["team"])}' if result.get('team') else ''
    contest_lines += f'<li><strong>{e(result["place"])} place</strong> — {title}{team}.</li>'
if iupc_results:
    contest_lines += f'<li><strong>{link(links["portfolio"] + "#contests", "IUPC team placements")}</strong>: {"; ".join(iupc_results)}.</li>'
experience = ''
experience_cards = []
if p.get('experience'):
    entries = []
    for item in p['experience']:
        organization = link(item['url'], item['organization']) if item.get('url') else e(item['organization'])
        timing = ' · '.join(e(value) for value in (item.get('dates'), item.get('duration')) if value)
        timing_html = f'<p class="experience-timing">{timing}</p>' if timing else ''
        bullets = '<ul>' + ''.join(f'<li>{e(b)}</li>' for b in item['bullets']) + '</ul>' if item.get('bullets') else ''
        entries.append(f'<article class="resume-experience"><h3>{e(item["role"])} · {organization}</h3>{timing_html}{bullets}</article>')
        paragraphs = ''.join(f'<p>{e(b)}</p>' for b in item.get('bullets', []))
        experience_cards.append(f'<article class="community-card"><p class="community-role">{e(item["role"])}</p><h3>{organization}</h3>{timing_html}{paragraphs}</article>')
    experience = '<section><h2>Teaching &amp; Leadership</h2>' + ''.join(entries) + '</section>'
ed = p['education']
resume = f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Résumé of {e(p['name'])}, competitive programmer and full-stack developer."><title>{e(p['name'])} — Résumé</title><link rel="icon" href="./favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="./resume.css"></head>
<body><nav class="resume-toolbar" aria-label="Résumé actions"><a href="./index.html">← Portfolio</a><a href="./assets/documents/Mahmud-Un-Naby-Resume.pdf" download>Download PDF ↓</a></nav>
<main class="resume"><header><h1>{e(p['name'])}</h1><p class="headline">{e(p['headline'])}</p><p class="contact-line">{email} · {phone}</p><p class="contact-line">{social}</p></header>
<section><h2>Profile</h2><p>{e(p['summary'])}</p></section>
<section><h2>Education</h2><h3>{e(ed['university'])}</h3><p>{e(ed['degree'])}<br>{e(ed['year'])} · Expected graduation: {e(ed['expected_graduation'])}</p></section>
<section class="resume-skills"><h2>Technical Skills</h2>{skill_lines}</section>
<section><h2>Projects</h2>{project_lines}</section>
{experience}
<section><h2>Competitive Programming &amp; Achievements</h2><p class="participation">{e(p['icpc_participations'])}-time ICPC Dhaka Regional participant · {link(links['codeforces'], 'Mahmud_Saikat on Codeforces')}</p><ul class="achievements">{contest_lines}</ul></section>
</main></body></html>
'''
(ROOT / 'resume.html').write_text(resume)

cards = ''.join(f'<article class="skill-group"><h3>{e(group["category"])}</h3><ul>' + ''.join(f'<li>{e(item)}</li>' for item in group['items']) + '</ul></article>' for group in p['skills'])
skills = f'''<section id="skills" class="skills wrap section-space" aria-labelledby="skills-title"><div class="section-heading"><div><p class="eyebrow">03 / SKILLS</p><h2 id="skills-title">From idea<br>to <em>working software.</em></h2></div><p>Full-stack web development, mobile apps,<br>and competitive problem solving.</p></div><div class="skill-groups">{cards}</div></section>'''
results = '<tbody>'
for result in p['achievements']:
    title = (result.get('organizer', '') + ' ' + result['contest']).strip()
    name = link(result['url'], title) if result.get('url') else e(title)
    results += f'<tr><th scope="row">{name}</th><td>{e(result["year"])}</td><td>{e(result.get("team") or "Individual")}</td><td><span class="placement">{e(result["place"])}</span></td></tr>'
results += '</tbody>'
community = f'''<section id="community" class="community wrap section-space" aria-labelledby="community-title"><div class="section-heading"><div><p class="eyebrow">05 / TEACHING &amp; LEADERSHIP</p><h2 id="community-title">Learning.<br>And <em>passing it on.</em></h2></div></div><div class="community-grid">{''.join(experience_cards)}</div></section>''' if experience_cards else ''
contact = f'''<section id="contact" class="contact wrap section-space" aria-labelledby="contact-title"><p class="eyebrow"><span class="status-dot"></span> 06 / GET IN TOUCH</p><h2 id="contact-title">Let’s build<br><em>something useful.</em><span class="contact-star" aria-hidden="true">✳</span></h2><div class="contact-bottom"><div><p>For software engineering opportunities and project conversations.</p><div class="contact-details">{email}{phone}{link(links['linkedin'], 'LinkedIn ↗', ' target="_blank" rel="noopener noreferrer"')}</div></div><div class="contact-actions">{link('mailto:' + p['email'], 'Send me an email ↗', ' class="button button-dark"')}{link('./assets/documents/Mahmud-Un-Naby-Resume.pdf', 'Download résumé ↓', ' class="text-link" download')}</div></div><p class="resume-browser-link">{link('./resume.html', 'Read my résumé online ↗')}</p></section>'''
portfolio = (ROOT / 'index.html').read_text()
for key, content in [('skills',skills),('results',results),('experience',community),('contact',contact)]:
    pattern = rf'(<!-- profile:{key}:start -->).*?(<!-- profile:{key}:end -->)'
    portfolio, count = re.subn(pattern, lambda m: m[1] + '\n' + content + '\n    ' + m[2], portfolio, flags=re.S)
    if count != 1:
        raise RuntimeError(f'Expected one {key} section, found {count}')
(ROOT / 'index.html').write_text(portfolio)
print('Built resume.html and shared portfolio skills, teaching/leadership, contacts, and contest results.')
