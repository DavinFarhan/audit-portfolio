import subprocess
import fitz

with open('reports/PasswordStore-Security-Audit-Report.md', 'r', encoding='utf-8') as f:
    orig = f.read()

def compile_full_report(slug, bg_hex, logo_name, title_color, sub_color, accent_color, muted_color):
    clean_bg = bg_hex.replace('#', '')
    clean_accent = accent_color.replace('#', '')
    clean_muted = muted_color.replace('#', '')
    clean_title = title_color.replace('#', '')
    clean_sub = sub_color.replace('#', '')

    frontmatter = f"""---
title: PasswordStore Security Audit Report
author: Farhan Davin
date: \\today
header-includes:
  - \\usepackage{{titling}}
  - \\usepackage{{graphicx}}
  - \\usepackage{{pagecolor}}
---

\\definecolor{{cBg}}{{HTML}}{{{clean_bg}}}
\\definecolor{{cAccent}}{{HTML}}{{{clean_accent}}}
\\definecolor{{cMuted}}{{HTML}}{{{clean_muted}}}
\\definecolor{{cTitle}}{{HTML}}{{{clean_title}}}
\\definecolor{{cSub}}{{HTML}}{{{clean_sub}}}

\\begin{{titlepage}}
    \\newpagecolor{{cBg}}
    \\centering
    \\vspace*{{1.2cm}}
    \\begin{{figure}}[h]
        \\centering
        \\includegraphics[width=0.38\\textwidth]{{{logo_name}}}
    \\end{{figure}}
    \\vspace*{{1.2cm}}
    {{\\fontsize{{26}}{{32}}\\selectfont\\bfseries\\color{{cTitle}} PASSWORDSTORE PROTOCOL\\par}}
    \\vspace{{0.4cm}}
    {{\\fontsize{{14}}{{18}}\\selectfont\\bfseries\\color{{cSub}} SMART CONTRACT SECURITY AUDIT REPORT\\par}}
    \\vspace{{0.8cm}}
    {{\\color{{cAccent}}\\rule{{0.25\\textwidth}}{{1.5pt}}\\par}}
    \\vspace{{0.8cm}}
    {{\\large\\color{{cMuted}} Version 1.0 $\\cdot$ Comprehensive Security Assessment\\par}}
    \\vspace{{2.0cm}}
    {{\\small\\scshape\\color{{cMuted}} PREPARED BY\\par}}
    \\vspace{{0.25cm}}
    {{\\Large\\bfseries\\color{{cTitle}} FARHAN DAVIN\\par}}
    \\vspace{{0.15cm}}
    {{\\normalsize\\color{{cAccent}} Smart Contract Security Auditor\\par}}
    \\vfill
    {{\\small\\color{{cMuted}} October 2026 $\\cdot$ Independent Security Review\\par}}
    \\vspace*{{0.8cm}}
\\end{{titlepage}}

\\restorepagecolor
\\color{{black}}
"""
    parts = orig.split('<!-- Report Content Begins -->')
    md_content = frontmatter + '\n<!-- Report Content Begins -->' + parts[1]

    md_file = f"reports/PasswordStore-{slug}.md"
    pdf_file = f"reports/PasswordStore-{slug}.pdf"

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    cmd = f'cd "/mnt/d/project farhan/BlockChain/Smart Contract Security Auditor/audit-portfolio/reports" && pandoc "PasswordStore-{slug}.md" -o "PasswordStore-{slug}.pdf" --from markdown --template=eisvogel --listings -V fontfamily=lmodern'
    res = subprocess.run(['wsl', '-d', 'Ubuntu-26.04', '-u', 'root', '--', 'bash', '-c', cmd], capture_output=True, text=True)
    if res.returncode == 0:
        doc = fitz.open(pdf_file)
        print(f"[{slug}] Compiled {len(doc)} pages successfully!")
        doc[0].get_pixmap(dpi=150).save(f"reports/preview_{slug}_p0.png")
        doc[1].get_pixmap(dpi=150).save(f"reports/preview_{slug}_p1.png")
    else:
        print(f"[{slug}] Error:", res.stderr)

# 1. Dark Midnight Navy
compile_full_report("Dark-Navy", "070E18", "logo_navy.pdf", "FFFFFF", "F59E0B", "F59E0B", "94A3B8")

# 2. Dark OLED Black
compile_full_report("Dark-OLED", "000000", "logo_black.pdf", "FFFFFF", "F59E0B", "F59E0B", "94A3B8")

# 3. Light Executive
compile_full_report("Light-Executive", "FFFFFF", "logo_white.pdf", "0B192C", "0B192C", "F59E0B", "64748B")

print("All full reports compiled!")
