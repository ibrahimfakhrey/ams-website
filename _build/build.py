"""Builds the site's HTML pages from _build/pages/*.html.

Each page file starts with a front-matter block:
    ---
    title: Page title
    description: One sentence for search engines
    nav: about            (which menu item is current)
    ---
followed by the page's body. The shared header and footer below wrap it.

Run:  python3 _build/build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / '_build' / 'pages'
SITE = 'Al-Alamiya Modern School International'
APPLY = 'https://admissions.ams-benha.com'
PORTAL = 'https://eduflow.ams-benha.com'
JOBS = 'https://jobs.ams-benha.com'
WHATSAPP = 'https://wa.me/201010630640'

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
ICONS = {
    'facebook': '<svg viewBox="0 0 24 24"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>',
    'youtube': '<svg viewBox="0 0 24 24"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3L10 15z"/></svg>',
    'linkedin': '<svg viewBox="0 0 24 24"><path d="M6.9 8.9H3.6V20h3.3V8.9zM5.2 3.5a1.9 1.9 0 1 0 0 3.9 1.9 1.9 0 0 0 0-3.9zM20.4 13.6c0-3-1.6-4.9-4.2-4.9-1.5 0-2.4.8-2.8 1.5V8.9h-3.2V20h3.3v-5.5c0-1.4.3-2.8 2-2.8s1.7 1.6 1.7 2.9V20h3.2v-6.4z"/></svg>',
    'whatsapp': '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.5-.3z"/></svg>',
}

NAV = [
    ('home', 'Home', 'index.html'),
    ('about', 'About', [
        ('About AMS', 'about.html'),
        ('Vision & Mission', 'about.html#vision'),
        ('Academic Life', 'academic-life.html'),
        ('School Campus', 'campus.html'),
        ('Accreditation', 'accreditation.html'),
    ]),
    ('admission', 'Admission', [
        ('How to apply', 'admission.html'),
        ('Tuition Fees', 'tuition-fees.html'),
        ('G12 Score Calculator', 'g12-score-calculator.html'),
    ]),
    ('gallery', 'Gallery', 'gallery.html'),
    ('jobs', 'Jobs', 'jobs.html'),
    ('contact', 'Contact', 'contact.html'),
]


def nav_html(current):
    out = []
    for key, label, target in NAV:
        if isinstance(target, list):
            links = ''.join(f'<a href="{h}">{t}</a>' for t, h in target)
            active = ' active' if key == current else ''
            out.append(f'<div class="drop{active}"><button type="button" aria-haspopup="true">{label}</button>'
                       f'<div class="drop-menu">{links}</div></div>')
        else:
            cur = ' aria-current="page"' if key == current else ''
            out.append(f'<a href="{target}"{cur}>{label}</a>')
    out.append(f'<a href="{PORTAL}">Student Portal</a>')
    out.append(f'<a class="btn gold" href="{APPLY}">Apply Now</a>')
    return '\n        '.join(out)


LAYOUT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="assets/img/hero-poster.jpg">
<meta name="theme-color" content="#3b0a0e">
<link rel="icon" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Manrope:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="sr-only" href="#main">Skip to content</a>
<div class="notice">Follow us on <a href="https://www.facebook.com/AMS.Benha" target="_blank" rel="noopener">Facebook</a> for all our news</div>
<header class="site-head over">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="{site} — home">
      <img src="assets/img/logo.png" alt="" width="54" height="54">
      <span><b>Al-Alamiya</b><small>Modern School International</small></span>
    </a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="Main">
        {nav}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <img src="assets/img/logo.png" alt="AMS crest" width="84" height="84" loading="lazy">
        <p>Benha's first international school. Together we light the way.</p>
        <div class="socials">
          <a href="https://www.facebook.com/AMS.Benha" target="_blank" rel="noopener" aria-label="Facebook">{fb}</a>
          <a href="https://www.youtube.com/channel/UCiAs6psHsaIbhn38Uve6NGQ" target="_blank" rel="noopener" aria-label="YouTube">{yt}</a>
          <a href="https://www.linkedin.com/company/ams-benha" target="_blank" rel="noopener" aria-label="LinkedIn">{li}</a>
          <a href="{whatsapp}" target="_blank" rel="noopener" aria-label="WhatsApp">{wa}</a>
        </div>
      </div>
      <div>
        <h4>School</h4>
        <ul>
          <li><a href="about.html">About AMS</a></li>
          <li><a href="academic-life.html">Academic Life</a></li>
          <li><a href="campus.html">School Campus</a></li>
          <li><a href="accreditation.html">Accreditation</a></li>
          <li><a href="gallery.html">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4>Families</h4>
        <ul>
          <li><a href="admission.html">Admission</a></li>
          <li><a href="tuition-fees.html">Tuition Fees</a></li>
          <li><a href="g12-score-calculator.html">G12 Score Calculator</a></li>
          <li><a href="{portal}">Student Portal</a></li>
          <li><a href="jobs.html">Jobs</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li>Kafr Saad, Banha, Egypt</li>
          <li><a href="tel:+201010630640">+20 101 063 0640</a></li>
          <li><a href="tel:+201027224445">+20 102 722 4445</a></li>
          <li><a href="mailto:info@ams-benha.com">info@ams-benha.com</a></li>
          <li>Sun – Thu, 08:00 – 15:00</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span id="year">2026</span> {site}. All rights reserved.</span>
      <span>Accredited by Cognia · American Diploma</span>
    </div>
  </div>
</footer>
<a class="wa" href="{whatsapp}" target="_blank" rel="noopener" aria-label="Message us on WhatsApp">{wa}</a>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def build():
    count = 0
    for src in sorted(PAGES.glob('*.html')):
        text = src.read_text(encoding='utf-8')
        m = re.match(r'---\n(.*?)\n---\n', text, re.S)
        meta = dict(line.split(':', 1) for line in m.group(1).splitlines() if ':' in line)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        body = text[m.end():]
        for k, v in {'{{APPLY}}': APPLY, '{{PORTAL}}': PORTAL, '{{JOBS}}': JOBS,
                     '{{WHATSAPP}}': WHATSAPP, '{{ARROW}}': ARROW, '{{WA}}': ICONS['whatsapp']}.items():
            body = body.replace(k, v)
        title = meta['title'] if meta.get('nav') == 'home' else f"{meta['title']} — {SITE}"
        html = LAYOUT.format(
            title=title, description=meta.get('description', ''), site=SITE, nav=nav_html(meta.get('nav')),
            body=body.strip(), portal=PORTAL, whatsapp=WHATSAPP,
            fb=ICONS['facebook'], yt=ICONS['youtube'], li=ICONS['linkedin'], wa=ICONS['whatsapp'])
        (ROOT / src.name).write_text(html, encoding='utf-8')
        count += 1
    print(f'built {count} pages')


if __name__ == '__main__':
    build()
