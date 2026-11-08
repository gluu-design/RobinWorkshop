#!/usr/bin/env python3
"""Builds the static Atelier Banger site into ./dist (mirrors atelierbanger.com URLs)."""
import os, shutil, html
from data import *

import sys
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
I = lambda p: ASSET + p  # image URL

def icon(name, cls="", size=24):
    """Minimal inline copies of the lucide icons the original uses."""
    paths = {
        "chevron-down": '<path d="m6 9 6 6 6-6"/>', "chevron-left": '<path d="m15 18-6-6 6-6"/>', "chevron-right": '<path d="m9 18 6-6-6-6"/>',
        "menu": '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
        "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
        "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
        "award": '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
        "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
        "hammer": '<path d="m15 12-8.373 8.373a1 1 0 1 1-3-3L12 9"/><path d="m18 15 4-4"/><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172V7l-2.26-2.26a6 6 0 0 0-4.202-1.756L9 2.96l.92.82A6.18 6.18 0 0 1 12 8.4V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"/>',
        "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
        "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        "check": '<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
        "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
        "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
        "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
        "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    }
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide {cls}" aria-hidden="true">{paths[name]}</svg>'

TAILWIND_CONFIG = """tailwind.config={theme:{extend:{colors:{charcoal:{700:'#3a3a3a',800:'#2a2a2a',900:'#1a1a1a'},cream:{100:'#f5f5dc',200:'#e8e8ce',300:'#dcdcbe',400:'#cfcfae',600:'#9a9a7a',700:'#7a7a5a',800:'#5a5a3a'},bronze:{300:'#e0b98d',400:'#d4a373',500:'#cd7f32',600:'#b87333',700:'#a0522d',800:'#7a3f22'}},fontFamily:{sans:['Inter','system-ui','sans-serif'],serif:['"Playfair Display"','Georgia','serif']},keyframes:{fadeIn:{'0%':{opacity:'0'},'100%':{opacity:'1'}},slideUp:{'0%':{transform:'translateY(30px)',opacity:'0'},'100%':{transform:'translateY(0)',opacity:'1'}}},animation:{'fade-in':'fadeIn .6s ease-out both','slide-up':'slideUp .8s ease-out both'}}}}"""

def head(title, rel, desc=None):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or SITE['description'])}">
<link rel="icon" href="{I('/images/logo/ab-4k-final-logo.png')}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:image" content="{I('/images/hero/ab-hero-poster.webp')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
<script>{TAILWIND_CONFIG}</script>
<link rel="stylesheet" href="{rel}assets/site.css">
</head>
<body class="font-sans overflow-x-hidden bg-charcoal-900 text-cream-100">
"""

NAV = [("services/", "Services"), ("portfolio/", "Portfolio"), (None, "Collection"), ("about/", "About"), ("contact/", "Contact")]
LINK = "text-cream-100 hover:text-bronze-500 transition-colors text-sm uppercase tracking-wider font-medium"

def header(rel):
    items = ""
    for href, label in NAV:
        if href is None:
            items += f"""<div class="relative group"><button class="flex items-center gap-1 {LINK}" aria-haspopup="true">Collection{icon('chevron-down','transition-transform duration-200 group-hover:rotate-180',14)}</button>
<div class="absolute top-full left-1/2 -translate-x-1/2 pt-3 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200"><div class="bg-black/90 backdrop-blur-md border border-cream-800/30 rounded-lg py-2 min-w-[180px] shadow-xl">
<a class="block px-4 py-2.5 text-sm text-cream-200 hover:text-bronze-400 hover:bg-white/5 transition-colors uppercase tracking-wider font-medium" href="{rel}collection/">Banger Collection</a>
<a class="block px-4 py-2.5 text-sm text-cream-200 hover:text-bronze-400 hover:bg-white/5 transition-colors uppercase tracking-wider font-medium" href="{rel}artisans/">FORGED BY CRAFTSMEN</a></div></div></div>"""
        else:
            items += f'<a class="{LINK}" href="{rel}{href}">{label}</a>'
    mobile = "".join(f'<a class="block py-3 text-lg {LINK}" href="{rel}{h}">{l}</a>' for h, l in NAV if h)
    mobile += f'<a class="block py-3 text-lg {LINK}" href="{rel}collection/">Banger Collection</a><a class="block py-3 text-lg {LINK}" href="{rel}artisans/">Forged by Craftsmen</a>'
    return f"""<header id="siteHeader" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-transparent py-6">
<div class="container mx-auto px-6 flex items-center justify-between">
<a class="hover:opacity-80 transition-opacity -my-4 md:-my-10 relative z-10" href="{rel}index.html" aria-label="Atelier Banger, home"><img alt="Atelier Banger Logo" width="108" height="135" class="w-auto h-32 md:h-48" src="{I('/images/logo/ab-4k-final-logo.png')}"></a>
<nav class="hidden md:flex items-center space-x-8">{items}</nav>
<button id="menuBtn" class="md:hidden text-cream-100 hover:text-bronze-500 transition-colors p-2 min-w-[44px] min-h-[44px] flex items-center justify-center" aria-label="Toggle menu" aria-expanded="false">{icon('menu','',24)}</button>
</div>
<div id="mobileMenu" class="hidden md:hidden bg-black/95 backdrop-blur-md border-t border-cream-800/30 mt-4"><div class="container mx-auto px-6 py-6">{mobile}</div></div>
</header>
"""

def footer(rel):
    year = "2026"
    return f"""<footer class="bg-charcoal-900 text-cream-100 py-16 border-t border-cream-800">
<div class="container mx-auto px-6">
<div class="grid grid-cols-1 md:grid-cols-4 gap-12">
<div><h3 class="text-2xl font-serif text-bronze-500 mb-4">Atelier Banger</h3><p class="text-sm text-cream-200 leading-relaxed">Unique bronze art &amp; bespoke furniture crafted with time-honored craftsmanship</p></div>
<div><h4 class="font-semibold mb-4 uppercase tracking-wider text-sm">Explore</h4><ul class="space-y-2">
<li><a class="text-sm hover:text-bronze-500 transition-colors" href="{rel}about/">About</a></li>
<li><a class="text-sm hover:text-bronze-500 transition-colors" href="{rel}portfolio/">Portfolio</a></li>
<li><a class="text-sm hover:text-bronze-500 transition-colors" href="{rel}services/">Services</a></li>
<li><a class="text-sm hover:text-bronze-500 transition-colors" href="{rel}collection/">Banger Collection</a></li>
<li><a class="text-sm hover:text-bronze-500 transition-colors" href="{rel}contact/">Contact</a></li></ul></div>
<div><h4 class="font-semibold mb-4 uppercase tracking-wider text-sm">Contact</h4><ul class="space-y-3 text-sm">
<li class="flex items-start gap-2">{icon('map-pin','mt-1 text-bronze-500 flex-shrink-0',16)}<span>{SITE['city']}</span></li>
<li class="flex items-start gap-2">{icon('mail','mt-1 text-bronze-500 flex-shrink-0',16)}<a href="mailto:{SITE['email']}" class="hover:text-bronze-500 transition-colors">{SITE['email']}</a></li>
<li class="flex items-start gap-2">{icon('phone','mt-1 text-bronze-500 flex-shrink-0',16)}<a href="{SITE['phone_href']}" class="hover:text-bronze-500 transition-colors">{SITE['phone']}</a></li></ul></div>
<div><h4 class="font-semibold mb-4 uppercase tracking-wider text-sm">Stay Connected</h4><div class="flex gap-4 mb-6">
<a href="{SITE['instagram']}" target="_blank" rel="noopener noreferrer" class="inline-block" aria-label="Instagram"><img alt="Follow Atelier Banger on Instagram" width="40" height="40" class="rounded-xl bg-charcoal-700 hover:bg-bronze-500/20 transition-all p-1.5" src="{I('/instagram-logo-black.avif')}"></a>
<a href="{SITE['linkedin']}" target="_blank" rel="noopener noreferrer" class="inline-block" aria-label="LinkedIn"><img alt="Follow Atelier Banger on LinkedIn" width="40" height="40" class="rounded-xl bg-charcoal-700 hover:bg-bronze-500/20 transition-all p-1.5" src="{I('/linkedin-logo.avif')}"></a></div></div>
</div>
<div class="mt-12 pt-8 border-t border-cream-800 flex flex-col md:flex-row justify-between items-center text-sm text-cream-300">
<p>© {year} Atelier Banger. All rights reserved.</p>
<div class="flex space-x-6 mt-4 md:mt-0"><a class="hover:text-bronze-500 transition-colors" href="{rel}privacy/">Privacy Policy</a><a class="hover:text-bronze-500 transition-colors" href="{rel}terms/">Terms of Service</a></div>
</div></div></footer>
<div id="lightbox" class="fixed inset-0 z-[100] hidden items-center justify-center bg-black/95 p-4" role="dialog" aria-modal="true" aria-label="Image"><button id="lbClose" class="absolute top-4 right-4 text-cream-100 hover:text-bronze-500 p-2" aria-label="Close">{icon('x','',28)}</button><img id="lbImg" alt="" class="max-h-[90vh] max-w-full object-contain rounded-lg shadow-2xl"></div>
<script src="{rel}assets/site.js"></script>
</body>
</html>
"""

def cta_interested(rel):
    return f"""<section class="py-20 border-t border-charcoal-700/40">
<div class="container mx-auto px-6 text-center">
<h2 class="text-3xl md:text-4xl font-serif text-cream-100 mb-6">Interested in a custom piece?</h2>
<p class="text-xl text-cream-300 max-w-2xl mx-auto mb-10">Whether you have a specific design in mind or just an idea, let's discuss how we can bring your vision to life with timeless craftsmanship.</p>
<a class="inline-block bg-bronze-600 text-black font-bold py-4 px-8 rounded hover:bg-bronze-500 transition-colors" href="{rel}contact/">Start a Conversation</a>
</div></section>"""

def tags(lst, cls="text-xs px-2 py-1 bg-charcoal-800 border border-charcoal-700 text-bronze-400 rounded-sm"):
    return "".join(f'<span class="{cls}">{html.escape(t)}</span>' for t in lst)

# ------------------------------------------------------------------ HOME
def page_home():
    rel = ""
    slides = ""
    dots = ""
    for i, s in enumerate(FEATURED):
        slides += f"""<div class="slide absolute inset-0 transition-opacity duration-700 {'opacity-100' if i==0 else 'opacity-0 pointer-events-none'}" data-i="{i}">
<img alt="{html.escape(s['title'])} — {html.escape(s['cat'])} by Atelier Banger" class="absolute inset-0 w-full h-full object-cover" src="{I(s['img'])}">
<div class="hidden md:block absolute inset-0 bg-black/40"></div>
<div class="hidden md:flex absolute inset-0 items-center justify-center p-12"><div class="text-center max-w-2xl">
<p class="text-bronze-400 text-sm uppercase tracking-wider mb-2">{s['cat']}</p><h3 class="text-4xl font-serif text-cream-100 mb-4">{html.escape(s['title'])}</h3>
<p class="text-cream-200 mb-8">{html.escape(s['desc'])}</p>
<a class="inline-block px-6 py-2 border-2 border-bronze-500 hover:bg-bronze-500/20 text-cream-100 font-semibold rounded transition-all" href="{rel}{s['link']}">View Project</a></div></div></div>"""
        dots += f'<button class="dot h-2 rounded-full transition-all {"bg-bronze-500 w-8" if i==0 else "bg-cream-600 w-2"}" data-i="{i}" aria-label="Go to project {i+1}"></button>'
    mobile_caps = "".join(f"""<div class="mcap {'' if i==0 else 'hidden'}" data-i="{i}"><p class="text-bronze-400 text-xs uppercase tracking-wider mb-1">{s['cat']}</p><h3 class="text-2xl font-serif text-cream-100 mb-2">{html.escape(s['title'])}</h3><p class="text-cream-200 text-sm mb-4">{html.escape(s['desc'])}</p><a class="inline-block px-5 py-2.5 border-2 border-bronze-500 hover:bg-bronze-500/20 text-cream-100 font-semibold rounded transition-all text-sm" href="{rel}{s['link']}">View Project</a></div>""" for i, s in enumerate(FEATURED))

    body = f"""{header(rel)}
<main class="min-h-screen">
<section class="relative h-screen w-full overflow-hidden flex items-center justify-center">
<div class="absolute inset-0 z-0">
<video autoplay muted loop playsinline poster="{I('/images/hero/ab-hero-poster.webp')}" class="absolute inset-0 w-full h-full object-cover"><source src="{I('/images/hero/ab-hero-video-cropped.mp4')}" type="video/mp4"></video>
<div class="absolute inset-0 bg-black/50"></div></div>
<div class="relative z-10 text-center px-6 max-w-5xl mx-auto">
<h1 class="text-6xl md:text-8xl font-serif text-cream-100 mb-6 animate-fade-in">Atelier Banger</h1>
<p class="text-xl md:text-2xl text-bronze-400 mb-4 font-light animate-slide-up" style="animation-delay:.2s">Unique Pieces of Furniture</p>
<p class="text-lg text-cream-200 max-w-2xl mx-auto mb-12 animate-slide-up" style="animation-delay:.4s">Bronze Artistry | Bespoke Metalwork | <span class="whitespace-nowrap">New York</span></p>
<div class="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up" style="animation-delay:.6s">
<a class="px-8 py-4 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-all transform hover:scale-105 min-h-[48px] text-center" href="{rel}portfolio/">View Portfolio</a>
<a class="px-8 py-4 bg-transparent border-2 border-bronze-500 hover:bg-bronze-500/20 text-cream-100 font-semibold rounded transition-all min-h-[48px] text-center" href="{rel}contact/">Commission a Piece</a></div></div>
<div class="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce">{icon('chevron-down','text-bronze-500',32)}</div>
</section>

<section class="py-24 bg-charcoal-900">
<div class="container mx-auto px-6">
<h2 class="text-4xl md:text-5xl font-serif text-center text-cream-100 mb-4">Featured Work</h2>
<p class="text-center text-cream-300 mb-16 max-w-2xl mx-auto">Explore a selection of commissioned pieces showcasing mastery in bronze, steel, and architectural metalwork</p>
<div class="relative max-w-6xl mx-auto" id="carousel">
<div class="relative">
<div class="relative h-[280px] md:h-[600px] overflow-hidden rounded-t-lg md:rounded-lg bg-charcoal-800">{slides}</div>
<button class="prev absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-bronze-600 text-white p-3 rounded-full transition-colors" aria-label="Previous project">{icon('chevron-left')}</button>
<button class="next absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-bronze-600 text-white p-3 rounded-full transition-colors" aria-label="Next project">{icon('chevron-right')}</button>
</div>
<div class="block md:hidden bg-charcoal-800 px-6 py-5 rounded-b-lg text-center">{mobile_caps}</div>
<div class="flex justify-center mt-6 space-x-2">{dots}</div>
</div>
<div class="text-center mt-12"><a class="inline-block px-8 py-3 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-colors" href="{rel}portfolio/">View Full Portfolio</a></div>
</div></section>

<section class="py-24 bg-charcoal-800 overflow-hidden">
<div class="container mx-auto px-6"><div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
<div class="reveal-left relative h-[500px] w-full bg-charcoal-900 rounded-lg overflow-hidden shadow-2xl border border-bronze-500/20"><img alt="Robin Miellet Portrait" class="absolute inset-0 w-full h-full object-cover" src="{I('/images/about/ab-robin-portrait.webp')}"></div>
<div class="reveal-right">
<h2 class="text-4xl md:text-5xl font-serif text-cream-100 mb-6">From France to New York</h2>
<p class="text-cream-200 mb-6 leading-relaxed">At age 16, Robin Miellet began his apprenticeship with the <a href="https://compagnons-du-devoir.com/" target="_blank" rel="noopener noreferrer" class="text-bronze-400 hover:underline"><strong>Compagnons du Devoir</strong></a>, France's most prestigious craftsmanship guild. This demanding eight-year journey took Robin across various French regions, where he mastered techniques passed down from the era of the great cathedrals.</p>
<p class="text-cream-200 mb-8 leading-relaxed">From 2007 to 2015, he perfected the design and fabrication of metal art pieces, a period that culminated in the creation of his masterpiece. In 2016, Robin joined La Forge De Style in New Jersey; today, he brings this heritage of excellence to New York, creating unique bronze art and bespoke furniture.</p>
<div class="space-y-4 mb-8">
<div class="flex items-start gap-3">{icon('award','text-bronze-500 flex-shrink-0 mt-1',20)}<div><h4 class="font-semibold text-cream-100"><a href="https://compagnons-du-devoir.com/" target="_blank" rel="noopener noreferrer" class="hover:underline">Compagnons du Devoir</a></h4><p class="text-sm text-cream-300">8 years of rigorous training in traditional French craftsmanship</p></div></div>
<div class="flex items-start gap-3">{icon('globe','text-bronze-500 flex-shrink-0 mt-1',20)}<div><h4 class="font-semibold text-cream-100">20+ Years Experience</h4><p class="text-sm text-cream-300">2007-Present: From apprentice to master craftsman</p></div></div>
<div class="flex items-start gap-3">{icon('hammer','text-bronze-500 flex-shrink-0 mt-1',20)}<div><h4 class="font-semibold text-cream-100">Dual Expertise</h4><p class="text-sm text-cream-300">Metalworking craftsmanship &amp; professional video production</p></div></div>
</div>
<a class="inline-block px-8 py-3 border-2 border-bronze-500 hover:bg-bronze-500/20 text-cream-100 font-semibold rounded transition-all" href="{rel}about/">Discover Our Journey</a>
</div></div></div></section>

<section class="py-24 bg-charcoal-900 overflow-hidden">
<div class="container mx-auto px-6">
<h2 class="text-4xl md:text-5xl font-serif text-center text-cream-100 mb-4 reveal-up">Services</h2>
<p class="text-center text-cream-300 mb-16 max-w-2xl mx-auto reveal-up">From concept to completion, every piece is crafted with meticulous attention to detail and traditional techniques</p>
<div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
{''.join(f'''<div class="reveal-up" style="transition-delay:{i*.1}s"><a class="group block p-8 bg-charcoal-800 hover:bg-charcoal-700 rounded-lg transition-all transform hover:-translate-y-2" href="{rel}services/#{anchor}">
<div>{icon(ic,'text-bronze-500 mb-4 group-hover:scale-110 transition-transform',40)}</div>
<h3 class="text-2xl font-serif text-cream-100 mb-3">{t}</h3><p class="text-cream-300 leading-relaxed">{d}</p>
<div class="mt-4 text-bronze-500 group-hover:text-bronze-400 font-semibold text-sm">Learn More →</div></a></div>''' for i,(anchor,ic,t,d) in enumerate([
    ("commissions","sparkles","Custom Commissions","Unique bronze art pieces and bespoke furniture designed and crafted specifically for your space."),
    ("restoration","wrench","Restoration &amp; Conservation","Expert restoration of antique metalwork and bronze pieces, preserving craftsmanship for generations."),
    ("collaboration","users","Collaborative Design","Partnership with architects and interior designers to bring architectural metalwork visions to life.")]))}
</div>
<div class="text-center mt-12 reveal-up"><a class="inline-block px-8 py-3 bg-transparent border-2 border-bronze-500 hover:bg-bronze-500/20 text-cream-100 font-semibold rounded transition-all" href="{rel}services/">View All Services</a></div>
</div></section>

<section class="py-24 bg-charcoal-900">
<div class="container mx-auto px-6 text-center">
<h2 class="text-4xl md:text-5xl font-serif text-cream-100 mb-6">Ready to Commission a Unique Piece?</h2>
<p class="text-xl text-cream-200 mb-12 max-w-2xl mx-auto">Whether you're seeking a statement furniture piece, architectural metalwork, or a custom bronze sculpture, let's bring your vision to life together.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center">
<a class="inline-flex items-center gap-2 px-8 py-4 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-all transform hover:scale-105" href="{rel}contact/">Start a Project{icon('arrow-right','',20)}</a>
<a class="inline-flex items-center gap-2 px-8 py-4 bg-transparent border-2 border-cream-100 hover:bg-white/10 text-cream-100 font-semibold rounded transition-all" href="{rel}portfolio/">View Portfolio</a></div>
<p class="mt-8 text-cream-300 text-sm">Average response time: 24-48 hours</p>
</div></section>
</main>
{footer(rel)}"""
    return head(SITE["title"], rel) + body

# ------------------------------------------------------------------ PORTFOLIO
def card(p, rel):
    loc = f'<p class="text-bronze-400 text-xs uppercase tracking-widest mt-2 transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">{html.escape(p["loc"])}</p>' if p.get("loc") else ""
    return f"""<div class="pcard group cursor-pointer block" data-cat="{p['cat']}" role="button" tabindex="0" aria-label="View {html.escape(p['title'])}" data-lb="{I(p['imgs'][0])}">
<div class="relative aspect-[4/3] overflow-hidden rounded-lg mb-4 bg-charcoal-800">
<div class="absolute inset-0 transition-transform duration-700 group-hover:scale-110"><img alt="{html.escape(p['title'])} — {p['cat']} by Atelier Banger" loading="lazy" class="w-full h-full object-cover" src="{I(p['imgs'][0])}" style="object-position:{p.get('pos','center center')}"></div>
<div class="absolute inset-0 bg-gradient-to-t from-charcoal-900/90 via-charcoal-900/20 to-transparent opacity-60 group-hover:opacity-80 transition-opacity duration-300"></div>
<div class="absolute inset-0 flex flex-col justify-end p-6">
<p class="text-bronze-400 text-xs uppercase tracking-widest mb-2 transform translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-300 delay-100">{p['cat']}</p>
<h3 class="text-2xl font-serif text-cream-100 transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">{html.escape(p['title'])}</h3>{loc}</div></div>
<div class="px-1"><div class="flex justify-end mb-2"><a class="text-xs text-bronze-500 hover:text-bronze-300 transition-colors" href="{rel}portfolio/{p['slug']}/">View details →</a></div>
<div class="flex flex-wrap gap-2">{tags(p['tags'])}</div></div></div>"""

def page_portfolio():
    rel = "../"
    cards = "".join(card(p, rel) for p in PROJECTS if not p.get("hidden"))
    fbtn = lambda c, on: f'<button class="fbtn px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 min-h-[44px] {"bg-bronze-600 text-black shadow-lg" if on else "bg-charcoal-800 text-cream-300 hover:bg-charcoal-700 hover:text-cream-100"}" data-f="{c}" aria-pressed="{"true" if on else "false"}">{c}</button>'
    body = f"""{header(rel)}
<main class="min-h-screen">
<div class="pt-32 pb-24 container mx-auto px-6">
<div class="text-center mb-16"><h1 class="text-5xl md:text-6xl font-serif text-cream-100 mb-6">Bespoke Metalwork &amp; Furniture</h1>
<p class="text-xl text-cream-300 max-w-3xl mx-auto">A curated collection of commissioned pieces spanning 2007-present, showcasing traditional French craftsmanship combined with contemporary design.</p></div>
<div><div class="flex flex-wrap justify-center mb-6 gap-2" id="filters">{fbtn('All',True)}{fbtn('Furniture',False)}{fbtn('Architectural',False)}{fbtn('Logo',False)}</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="pgrid">{cards}</div></div>
</div>
{cta_interested(rel)}
</main>
{footer(rel)}"""
    return head("Bespoke Metalwork & Furniture | Atelier Banger", rel) + body

def page_project(p):
    rel = "../../"
    thumbs = ""
    if len(p["imgs"]) > 1:
        thumbs = '<div class="flex gap-3 mt-4 overflow-x-auto pb-1">' + "".join(f'<button class="gthumb relative w-24 aspect-[4/3] rounded overflow-hidden bg-charcoal-800 flex-shrink-0 {"ring-2 ring-bronze-500" if i==0 else "opacity-50 hover:opacity-100"}" data-i="{i}" aria-label="Image {i+1}"><img alt="{html.escape(p["title"])} {i+1}" class="absolute inset-0 w-full h-full object-cover" src="{I(u)}"></button>' for i, u in enumerate(p["imgs"])) + "</div>"
    paras = "".join(f'<p class="mb-4">{html.escape(x)}</p>' for x in p["paras"])
    body = f"""{header(rel)}
<main class="min-h-screen bg-charcoal-900">
<div class="pt-44 md:pt-52 pb-16 container mx-auto px-6">
<a class="inline-flex items-center text-bronze-400 hover:text-bronze-300 mb-8 group" href="{rel}portfolio/">{icon('arrow-left','w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform',16)}Back to Portfolio</a>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20">
<div><div class="gallery" data-imgs='{html.escape("|".join(I(u) for u in p["imgs"]))}'>
<div class="relative w-full aspect-[4/3] rounded-lg overflow-hidden bg-charcoal-800 group shadow-2xl">
<button class="gmain absolute inset-0 cursor-zoom-in" aria-label="Enlarge image"><img alt="{html.escape(p['title'])}" class="w-full h-full object-cover" src="{I(p['imgs'][0])}"><div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors"></div></button></div>{thumbs}</div></div>
<div class="flex flex-col justify-center">
<div class="mb-4"><span class="text-bronze-400 uppercase tracking-widest text-sm font-semibold">{p['cat']}</span></div>
<h1 class="text-4xl md:text-5xl font-serif text-cream-100 mb-3 leading-tight">{html.escape(p['title'])}</h1>
<div class="text-cream-300 mb-10 text-lg leading-relaxed"><p class="lead text-xl text-cream-200 mb-6 font-light">{html.escape(p['lead'])}</p>
<h3 class="text-cream-100 font-serif text-2xl mb-4">The Story</h3>{paras}</div>
<div class="border-t border-charcoal-700 pt-8"><h4 class="text-sm uppercase tracking-widest text-cream-600 mb-4">Materials &amp; Techniques</h4>
<div class="flex flex-wrap gap-2">{tags(p['tags'],'px-3 py-1 bg-charcoal-800 text-bronze-400 rounded border border-charcoal-700 text-sm')}</div></div>
</div></div></div>
{cta_interested(rel)}
</main>
{footer(rel)}"""
    return head(f"{p['title']} | Portfolio | Atelier Banger", rel, p["lead"]) + body

# ------------------------------------------------------------------ COLLECTION
def page_collection():
    rel = "../"
    secs = ""
    for c in COLLECTION:
        thumbs = "".join(f'<button class="gthumb relative w-24 aspect-[4/3] rounded overflow-hidden bg-charcoal-800 flex-shrink-0 {"ring-2 ring-bronze-500" if i==0 else "opacity-50 hover:opacity-100"}" data-i="{i}" aria-label="{html.escape(c["title"])} {i+1}"><img alt="{html.escape(c["title"])} {i+1}" class="absolute inset-0 w-full h-full object-cover" src="{I(u)}"></button>' for i, u in enumerate(c["imgs"]))
        story = "".join(f'<p class="text-cream-300 leading-relaxed">{html.escape(x)}</p>' for x in c["story"])
        pf = f'<a class="inline-block px-8 py-3 border border-charcoal-700 hover:border-bronze-500 text-cream-200 rounded transition-colors" href="{rel}{c["portfolio"]}">View in Portfolio</a>' if c.get("portfolio") else ""
        secs += f"""<section id="{c['id']}" class="pb-24"><div class="container mx-auto px-6">
<div class="mb-10"><div class="flex items-center gap-4"><div class="h-px flex-1 bg-charcoal-700"></div><span class="text-bronze-400 uppercase tracking-[0.2em] text-xs font-semibold">{html.escape(c['mat'])}</span><div class="h-px flex-1 bg-charcoal-700"></div></div></div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-center">
<div><div class="gallery" data-imgs='{html.escape("|".join(I(u) for u in c["imgs"]))}'>
<div class="relative w-full rounded-lg overflow-hidden bg-charcoal-800 group">
<button class="gmain relative block w-full cursor-zoom-in" aria-label="Enlarge image"><img alt="{html.escape(c['title'])}" class="w-full h-auto" src="{I(c['imgs'][0])}"><div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors"></div></button>
<button class="gprev absolute left-3 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-charcoal-900/60 hover:bg-charcoal-900/90 text-cream-200" aria-label="Previous image">{icon('chevron-left','',20)}</button>
<button class="gnext absolute right-3 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-charcoal-900/60 hover:bg-charcoal-900/90 text-cream-200" aria-label="Next image">{icon('chevron-right','',20)}</button>
<div class="gcount absolute bottom-3 right-3 z-10 text-xs text-cream-300 bg-charcoal-900/60 px-2 py-1 rounded">1 / {len(c['imgs'])}</div></div>
<div class="flex gap-3 mt-4 overflow-x-auto pb-1">{thumbs}</div></div></div>
<div class="flex flex-col justify-center">
<h2 class="text-4xl md:text-5xl font-serif text-cream-100 mb-3">{html.escape(c['title'])}</h2>
<p class="text-bronze-400 text-lg mb-6">{html.escape(c['sub'])}</p>
<p class="text-cream-300 leading-relaxed mb-8">{html.escape(c['intro'])}</p>
<div class="mb-10"><h3 class="text-cream-100 font-serif text-2xl mb-4">The Story</h3><div class="space-y-4">{story}</div></div>
<div class="flex flex-wrap gap-4"><a class="inline-block px-8 py-3 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-colors" href="{rel}contact/">Inquire About This Piece</a>{pf}</div>
</div></div></div></section>"""
    body = f"""{header(rel)}
<main class="min-h-screen">
<section class="pt-44 md:pt-52 pb-16 container mx-auto px-6"><div class="max-w-4xl mx-auto text-center">
<h1 class="text-5xl md:text-6xl font-serif text-cream-100 mb-6">Banger Collection</h1>
<p class="text-xl text-cream-300 leading-relaxed max-w-2xl mx-auto">Signature pieces available for order. Each one handcrafted in bronze using traditional techniques passed down through generations.</p></div></section>
{secs}
{cta_interested(rel)}
</main>
{footer(rel)}"""
    return head("Collection | Atelier Banger", rel) + body

# ------------------------------------------------------------------ SERVICES
def page_services():
    rel = "../"
    svc = [("commissions","sparkles","Custom Commissions","Unique bronze art pieces and bespoke furniture designed specifically for your space and vision.",["One-of-a-kind furniture pieces","Bronze sculptures &amp; art installations","Architectural metalwork elements","Custom lighting fixtures"],"Start a Commission"),
           ("restoration","wrench","Restoration &amp; Conservation","Expert restoration of antique metalwork, preserving craftsmanship and heritage for future generations.",["Antique bronze restoration","Historical metalwork repair","Patina restoration &amp; refinishing","Structural reinforcement"],"Request Consultation"),
           ("collaboration","users","Collaborative Design","Partnership with architects and interior designers to realize architectural metalwork visions.",["Railings &amp; staircases","Doors &amp; entryways","Decorative panels &amp; screens","3D rendering &amp; prototyping"],"Partner With Us")]
    cards = "".join(f"""<div id="{a}" class="p-8 bg-charcoal-800 rounded-lg scroll-mt-40"><div>{icon(ic,'text-bronze-500 mb-4',40)}</div><h2 class="text-2xl font-serif text-cream-100 mb-4">{t}</h2><p class="text-cream-300 mb-6 leading-relaxed">{d}</p>
<ul class="space-y-2 text-cream-300 text-sm mb-6">{''.join(f'<li class="flex items-start gap-2">{icon("check","text-bronze-500 flex-shrink-0 mt-0.5",16)}<span>{li}</span></li>' for li in lis)}</ul>
<a class="text-bronze-400 hover:text-bronze-300 font-semibold" href="{rel}contact/">{cta} →</a></div>""" for a,ic,t,d,lis,cta in svc)
    steps = [("Initial Consultation","We discuss your vision, requirements, and budget. This can be via phone, video call, or in-person at the atelier."),
             ("Concept &amp; Design","I create sketches, technical drawings, and 3D renderings for your review and approval. Multiple iterations until perfect."),
             ("Material Selection","Choose from bronze types, steel grades, finishes, and patinas. I provide samples and guidance on durability and aesthetics."),
             ("Fabrication","Using traditional techniques and modern tools, I handcraft your piece. Regular progress updates and photos throughout."),
             ("Installation &amp; Delivery","Professional installation or white-glove delivery. Final adjustments and care instructions provided.")]
    steps_html = "".join(f'<div class="flex gap-6 items-start"><div class="flex-shrink-0 w-12 h-12 bg-bronze-600 text-black rounded-full flex items-center justify-center font-bold text-xl">{i+1}</div><div><h3 class="text-xl font-serif text-cream-100 mb-2">{t}</h3><p class="text-cream-300 leading-relaxed">{d}</p></div></div>' for i,(t,d) in enumerate(steps))
    times = [("Small Pieces","Tables, sculptures, lighting fixtures","4–12 weeks"),("Medium Projects","Railings, doors, multiple pieces","3–6 months"),("Large Installations","Architectural elements, collections","6–12 months"),("Restoration","Depends on condition and complexity","2–8 weeks")]
    times_html = "".join(f'<div class="p-6 bg-charcoal-800 rounded-lg">{icon("clock","text-bronze-500 mb-3",32)}<h3 class="text-xl font-serif text-cream-100 mb-2">{t}</h3><p class="text-cream-300 mb-2">{d}</p><p class="text-bronze-400 font-semibold">{w}</p></div>' for t,d,w in times)
    body = f"""{header(rel)}
<main class="min-h-screen"><div class="pt-32 pb-24">
<section class="container mx-auto px-6 mb-20"><div class="max-w-4xl mx-auto text-center"><h1 class="text-5xl md:text-6xl font-serif text-cream-100 mb-6">Services</h1>
<p class="text-xl text-cream-300 leading-relaxed">From initial concept to final installation, every project receives meticulous attention and traditional craftsmanship combined with contemporary design.</p></div></section>
<section class="container mx-auto px-6 mb-20"><div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">{cards}</div></section>
<section class="bg-charcoal-800 py-20"><div class="container mx-auto px-6"><div class="max-w-4xl mx-auto">
<h2 class="text-4xl font-serif text-cream-100 mb-4 text-center">The Process</h2>
<p class="text-center text-cream-300 mb-16 max-w-2xl mx-auto">Every commission follows a thoughtful, collaborative process to ensure exceptional results</p>
<div class="space-y-8">{steps_html}</div></div></div></section>
<section class="py-20 container mx-auto px-6"><div class="max-w-4xl mx-auto"><h2 class="text-4xl font-serif text-cream-100 mb-12 text-center">Typical Timelines</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">{times_html}</div></div></section>
<section class="py-20 bg-charcoal-900"><div class="container mx-auto px-6 text-center"><h2 class="text-4xl font-serif text-cream-100 mb-6">Ready to Start Your Project?</h2>
<p class="text-xl text-cream-200 mb-8 max-w-2xl mx-auto">Let's discuss your vision and create something truly unique together.</p>
<div><a class="inline-block px-8 py-3 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-colors" href="{rel}contact/">Get In Touch</a></div></div></section>
</div></main>
{footer(rel)}"""
    return head("Custom Bronze & Metalwork Services | Atelier Banger", rel) + body

# ------------------------------------------------------------------ ABOUT
def page_about():
    rel = "../"
    n = len(TIMELINE)
    markers = "".join(f'<button class="tmark absolute -translate-x-1/2 flex flex-col items-center gap-3 group" style="left:{(i/(n-1))*100 if n>1 else 0}%" data-i="{i}" aria-label="{t["title"]}"><div class="w-4 h-4 rounded-full border-2 z-10 {"bg-bronze-500 border-bronze-500" if i==0 else "bg-charcoal-700 border-cream-700/40"}"></div><span class="text-sm font-medium whitespace-nowrap {"text-bronze-400" if i==0 else "text-cream-600"}">{t["range"]}</span></button>' for i, t in enumerate(TIMELINE))
    panels = ""
    for i, t in enumerate(TIMELINE):
        img = f'<div class="rounded-lg overflow-hidden bg-charcoal-800"><div class="relative w-full aspect-[3/2]"><img alt="{html.escape(t["title"])}" class="absolute inset-0 w-full h-full object-contain" src="{I(t["img"])}"></div></div>' if t["img"] else '<div class="rounded-lg overflow-hidden bg-charcoal-800"><div class="relative w-full aspect-[3/2] flex items-center justify-center text-bronze-500/60 font-serif text-3xl">387 h</div></div>'
        panels += f"""<div class="tpanel {'' if i==0 else 'hidden'}" data-i="{i}"><div class="grid md:grid-cols-2 gap-8 items-start">{img}
<div><p class="text-bronze-400 text-sm uppercase tracking-widest mb-2"><span>{t['year']}</span></p><h3 class="text-3xl md:text-4xl font-serif text-cream-100 mb-2">{html.escape(t['title'])}</h3><p class="text-bronze-500 mb-4">{t['sub']}</p>
<p class="text-cream-300 leading-relaxed text-lg">{html.escape(t['text'])}</p>
<div class="mt-8 flex gap-3"><button class="tprev px-4 py-2 rounded-full border border-cream-700/30 text-cream-400 hover:text-cream-100 hover:border-bronze-500 text-sm transition-colors">Previous</button><button class="tnext px-4 py-2 rounded-full border border-cream-700/30 text-cream-400 hover:text-cream-100 hover:border-bronze-500 text-sm transition-colors">Next</button></div></div></div></div>"""
    shop = "".join(f'<div class="group"><button class="relative overflow-hidden rounded-lg aspect-[3/4] w-full cursor-zoom-in" data-lb="{I("/images/about/Working/"+f+".webp")}" aria-label="Enlarge {l}"><img alt="{l} — Atelier Banger workshop" loading="lazy" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" src="{I("/images/about/Working/"+f+".webp")}"><div class="absolute inset-0 bg-bronze-600/0 group-hover:bg-bronze-600/15 transition-colors"></div></button><p class="mt-3 text-center text-sm font-semibold uppercase tracking-widest text-bronze-500">{l}</p></div>' for l, f in SHOP_PHOTOS)
    phil = [("award","Heritage &amp; Excellence",'Trained in centuries-old techniques passed down through the <a href="https://compagnons-du-devoir.com/" target="_blank" rel="noopener noreferrer" class="text-bronze-400 hover:underline">Compagnons du Devoir</a>, I bring the same commitment to excellence that built the great cathedrals.'),
            ("users","Collaboration","Every piece begins with a conversation. I work closely with clients, designers, and architects to bring visions to life."),
            ("hammer","Craftsmanship","Each piece is handcrafted using traditional methods combined with contemporary design, ensuring both beauty and durability."),
            ("video","Documentation","With expertise in professional video production, I document the creative process, preserving the story behind each piece.")]
    phil_html = "".join(f'<div class="p-6 bg-charcoal-800 rounded-lg border border-transparent hover:border-bronze-700/40 transition-colors"><div>{icon(ic,"text-bronze-500 mb-4",32)}</div><h3 class="text-xl font-serif text-cream-100 mb-3">{t}</h3><p class="text-cream-300 leading-relaxed">{d}</p></div>' for ic,t,d in phil)
    body = f"""{header(rel)}
<main class="min-h-screen"><div class="pt-32 pb-24">
<section class="container mx-auto px-6 mb-20"><div class="text-center"><h1 class="text-5xl md:text-6xl font-serif text-cream-100 mb-6">About Atelier Banger</h1>
<p class="text-xl text-cream-300 leading-relaxed max-w-4xl mx-auto">From the ancient traditions of French craftsmanship to the contemporary artistry of New York, a journey of dedication, mastery, and innovation.</p></div></section>
<section class="bg-charcoal-800 py-20"><div class="container mx-auto px-6"><h2 class="text-4xl font-serif text-cream-100 text-center mb-16">Our Journey</h2>
<div id="timeline" class="max-w-5xl mx-auto">
<div class="relative mb-12 hidden md:block px-10"><div class="absolute top-[17px] left-10 right-10 h-[2px] bg-cream-700/20"></div><div id="tprog" class="absolute top-[17px] left-10 h-[2px] bg-bronze-700/50" style="width:0"></div><div class="relative h-[72px] mx-0">{markers}</div></div>
<div class="relative">{panels}</div>
<div class="flex items-center justify-center gap-2 mt-6 md:hidden">{''.join(f'<button class="tdot p-1" data-i="{i}" aria-label="Step {i+1}"><div class="rounded-full h-2 {"w-4 bg-bronze-500" if i==0 else "w-2 bg-cream-700/40"}"></div></button>' for i in range(n))}</div>
</div></div></section>
<section class="py-20 container mx-auto px-6"><div class="text-center mb-12"><h2 class="text-4xl font-serif text-cream-100 mb-4">In the Shop</h2><p class="text-cream-300 text-lg">Where raw material becomes art</p></div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">{shop}</div></section>
<section class="py-20 container mx-auto px-6"><h2 class="text-4xl font-serif text-cream-100 mb-12 text-center">Philosophy &amp; Approach</h2><div class="grid grid-cols-1 md:grid-cols-2 gap-8">{phil_html}</div></section>
<section class="py-20 bg-charcoal-900"><div class="container mx-auto px-6 text-center"><h2 class="text-4xl font-serif text-cream-100 mb-6">Let's Create Something Unique</h2>
<p class="text-xl text-cream-200 mb-8 max-w-2xl mx-auto">With 20+ years of experience and a network of talented designers and architects, I'm ready to bring your vision to life.</p>
<div class="flex flex-col sm:flex-row gap-4 justify-center"><a class="inline-block px-8 py-3 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-colors" href="{rel}contact/">Start a Commission</a><a class="inline-block px-8 py-3 bg-transparent border-2 border-cream-100 hover:bg-white/10 text-cream-100 font-semibold rounded transition-all" href="{rel}portfolio/">View Portfolio</a></div></div></section>
</div></main>
{footer(rel)}"""
    return head("About | Atelier Banger", rel) + body

# ------------------------------------------------------------------ CONTACT
def page_contact():
    rel = "../"
    inp = "w-full px-4 py-3 bg-charcoal-800 border border-cream-700 rounded text-cream-100 placeholder:text-cream-600 focus:outline-none focus:border-bronze-500"
    opts = lambda o: "".join(f'<option value="{v}">{l}</option>' for v, l in o)
    body = f"""{header(rel)}
<main class="min-h-screen"><div class="pt-32 pb-24"><div class="container mx-auto px-6"><div class="max-w-5xl mx-auto">
<div class="text-center mb-16"><h1 class="text-5xl md:text-6xl font-serif text-cream-100 mb-6">Commission Custom Metalwork</h1>
<p class="text-xl text-cream-300 max-w-2xl mx-auto">Whether you're seeking a custom piece, restoration services, or collaborative design, I'd love to hear about your project.</p></div>
<div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
<div><h2 class="text-2xl font-serif text-cream-100 mb-8">Get in Touch</h2>
<div class="space-y-6 mb-12">
<div class="flex items-start gap-4">{icon('mail','text-bronze-500 flex-shrink-0 mt-1',24)}<div><h3 class="text-cream-100 font-semibold mb-1">Email</h3><a href="mailto:{SITE['email']}" class="text-cream-300 hover:text-bronze-500 transition-colors">{SITE['email']}</a></div></div>
<div class="flex items-start gap-4">{icon('phone','text-bronze-500 flex-shrink-0 mt-1',24)}<div><h3 class="text-cream-100 font-semibold mb-1">Phone</h3><a href="{SITE['phone_href']}" class="text-cream-300 hover:text-bronze-500 transition-colors">{SITE['phone']}</a></div></div>
<div class="flex items-start gap-4">{icon('map-pin','text-bronze-500 flex-shrink-0 mt-1',24)}<div><h3 class="text-cream-100 font-semibold mb-1">Shop Location</h3><p class="text-cream-300">{SITE['address']}</p></div></div>
<div class="flex items-start gap-4">{icon('clock','text-bronze-500 flex-shrink-0 mt-1',24)}<div><h3 class="text-cream-100 font-semibold mb-1">Response Time</h3><p class="text-cream-300">Typically 24-48 hours<br>Atelier visits by appointment only</p></div></div></div>
<div class="p-6 bg-charcoal-800 rounded-lg"><h3 class="text-xl font-serif text-cream-100 mb-3">What to Expect</h3><ul class="space-y-2 text-cream-300 text-sm">
{''.join(f'<li class="flex items-start gap-2"><span class="text-bronze-500 mt-1">•</span><span>{x}</span></li>' for x in ["Initial consultation to discuss your vision and requirements","Design concepts and 3D renderings for approval","Transparent pricing and timeline estimates","Regular updates throughout the fabrication process","Professional installation and delivery coordination"])}</ul></div>
<div class="mt-8"><h3 class="text-xl font-serif text-cream-100 mb-1">Shop Location</h3><p class="text-cream-400 text-sm mb-4">By appointment only</p>
<div class="rounded-lg overflow-hidden border border-bronze-700/40 shadow-lg"><iframe title="Map to the atelier" src="{SITE['map_embed']}" width="100%" height="280" style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div>
</div>
<div><form class="space-y-6" id="contactForm" novalidate><h2 class="text-2xl font-serif text-cream-100 mb-6">Commission Inquiry</h2>
<div><label for="name" class="block text-cream-100 mb-2 font-medium">Name *</label><input type="text" id="name" name="name" class="{inp}" placeholder="Your name" required></div>
<div><label for="email" class="block text-cream-100 mb-2 font-medium">Email *</label><input type="email" id="email" name="email" class="{inp}" placeholder="your@email.com" required></div>
<div><label for="phone" class="block text-cream-100 mb-2 font-medium">Phone</label><input type="tel" id="phone" name="phone" class="{inp}" placeholder="+1 (555) 000-0000"></div>
<div><label for="projectType" class="block text-cream-100 mb-2 font-medium">Project Type *</label><select id="projectType" name="projectType" class="{inp}" required>{opts([("","Select a type"),("Custom Furniture","Custom Furniture"),("Sculpture / Art Piece","Sculpture / Art Piece"),("Architectural Metalwork","Architectural Metalwork"),("Lighting Fixtures","Lighting Fixtures"),("Restoration","Restoration"),("Other","Other")])}</select></div>
<div><label for="budget" class="block text-cream-100 mb-2 font-medium">Budget Range</label><select id="budget" name="budget" class="{inp}">{opts([("","Select a range"),("Under $10,000","Under $10,000"),("$10,000 - $25,000","$10,000 - $25,000"),("$25,000 - $50,000","$25,000 - $50,000"),("$50,000 - $100,000","$50,000 - $100,000"),("Over $100,000","Over $100,000")])}</select></div>
<div><label for="timeline" class="block text-cream-100 mb-2 font-medium">Timeline</label><select id="timeline" name="timeline" class="{inp}">{opts([("","Select a timeline"),("Flexible","Flexible"),("Within 3 months","Within 3 months"),("Within 6 months","Within 6 months"),("Within a year","Within a year"),("Just planning","Just planning")])}</select></div>
<div><label for="message" class="block text-cream-100 mb-2 font-medium">Project Description *</label><textarea id="message" name="message" rows="5" class="{inp} resize-none" placeholder="Tell me about your project, vision, and any specific requirements..." required></textarea></div>
<button type="submit" class="w-full flex items-center justify-center gap-2 px-8 py-4 bg-bronze-600 hover:bg-bronze-700 text-black font-semibold rounded transition-colors">Send Inquiry{icon('send','',20)}</button>
<p id="formNote" class="text-sm text-cream-400 hidden"></p>
</form></div></div></div></div></div></main>
{footer(rel)}"""
    return head("Contact | Atelier Banger", rel) + body

# ------------------------------------------------------------------ ARTISANS / LEGAL
def page_artisans():
    rel = "../"
    body = f"""{header(rel)}
<main><div class="relative h-screen w-full overflow-hidden flex flex-col items-center justify-center font-sans">
<div class="absolute inset-0 z-0"><img alt="For Artisans background" class="absolute inset-0 w-full h-full object-cover scale-105 blur-sm" src="{I('/images/Banger-Collection/ab-for-pros-cart-poles.webp')}"><div class="absolute inset-0 bg-black/65"></div></div>
<div class="relative z-10 text-center px-6 max-w-3xl mx-auto text-cream-100">
<p class="text-bronze-400 text-sm uppercase tracking-[0.3em] mb-6">Atelier Banger</p>
<h1 class="text-4xl md:text-6xl font-serif mb-4 tracking-tight uppercase">FORGED BY CRAFTSMEN</h1>
<p class="text-bronze-400 text-sm uppercase tracking-[0.3em] mb-6">Made by craftsmen, for craftsmen</p>
<div class="w-24 h-[2px] bg-bronze-500 mx-auto mb-8 rounded-full"></div>
<h2 class="text-2xl md:text-4xl font-light mb-6 text-bronze-400">Coming Soon</h2>
<p class="text-base md:text-lg text-cream-300 max-w-xl mx-auto font-light leading-relaxed">Born from the workshop.<br>Built by hands that know the craft.<br>Made in the USA. Built to last.<br>Tools, equipment, and resources<br>designed by craftsmen, for professionals.</p>
<div class="mt-16 text-xs text-cream-400/40 uppercase tracking-widest">© 2026 Atelier Banger</div></div></div></main>
{footer(rel)}"""
    return head("Forged by Craftsmen | Atelier Banger", rel) + body

def page_legal(title, intro):
    rel = "../"
    body = f"""{header(rel)}
<main class="min-h-screen"><div class="pt-44 pb-24 container mx-auto px-6"><div class="max-w-3xl mx-auto">
<h1 class="text-5xl font-serif text-cream-100 mb-6">{title}</h1>
<p class="text-cream-300 leading-relaxed mb-6">{intro}</p>
<p class="text-cream-400 text-sm">Questions: <a href="mailto:{SITE['email']}" class="text-bronze-400 hover:underline">{SITE['email']}</a></p>
</div></div></main>
{footer(rel)}"""
    return head(f"{title} | Atelier Banger", rel) + body

# ------------------------------------------------------------------ ASSETS
SITE_CSS = """html{scroll-behavior:smooth}
::-webkit-scrollbar{width:10px}::-webkit-scrollbar-track{background:#1a1a1a}::-webkit-scrollbar-thumb{background:#cd7f32;border-radius:5px}::-webkit-scrollbar-thumb:hover{background:#b87333}
::selection{background:#cd7f32;color:#1a1a1a}
.reveal-left,.reveal-right,.reveal-up{opacity:0;transition:opacity .8s ease-out,transform .8s ease-out}
.reveal-left{transform:translateX(-60px)}.reveal-right{transform:translateX(60px)}.reveal-up{transform:translateY(30px)}
.reveal-left.in,.reveal-right.in,.reveal-up.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal-left,.reveal-right,.reveal-up{opacity:1;transform:none;transition:none}.animate-bounce,.animate-fade-in,.animate-slide-up{animation:none}}
#lightbox.flex{display:flex}
"""

SITE_JS = r"""(function(){
const $=(s,e=document)=>e.querySelector(s),$$=(s,e=document)=>[...e.querySelectorAll(s)];
/* header */
const hdr=$('#siteHeader');const onScroll=()=>{const s=window.scrollY>50;hdr.classList.toggle('bg-black/90',s);hdr.classList.toggle('backdrop-blur-md',s);hdr.classList.toggle('py-4',s);hdr.classList.toggle('bg-transparent',!s);hdr.classList.toggle('py-6',!s);};onScroll();addEventListener('scroll',onScroll,{passive:true});
const mb=$('#menuBtn'),mm=$('#mobileMenu');if(mb){mb.addEventListener('click',()=>{const o=mm.classList.toggle('hidden');mb.setAttribute('aria-expanded',String(!o));if(!o){hdr.classList.add('bg-black/90','backdrop-blur-md')}});}
/* reveal on scroll */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.15});$$('.reveal-left,.reveal-right,.reveal-up').forEach(el=>io.observe(el));
/* lightbox */
const lb=$('#lightbox'),lbImg=$('#lbImg');function openLb(src,alt){lbImg.src=src;lbImg.alt=alt||'';lb.classList.remove('hidden');lb.classList.add('flex');document.body.style.overflow='hidden'}function closeLb(){lb.classList.add('hidden');lb.classList.remove('flex');document.body.style.overflow=''}
if(lb){lb.addEventListener('click',e=>{if(e.target===lb||e.target.closest('#lbClose'))closeLb()});addEventListener('keydown',e=>{if(e.key==='Escape')closeLb()});}
$$('[data-lb]').forEach(el=>{el.addEventListener('click',e=>{if(e.target.closest('a'))return;openLb(el.dataset.lb,el.getAttribute('aria-label'))});el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openLb(el.dataset.lb)}})});
/* home carousel */
const car=$('#carousel');if(car){const slides=$$('.slide',car),dots=$$('.dot',car),caps=$$('.mcap',car);let i=0,t;const go=n=>{i=(n+slides.length)%slides.length;slides.forEach((s,k)=>{s.classList.toggle('opacity-100',k===i);s.classList.toggle('opacity-0',k!==i);s.classList.toggle('pointer-events-none',k!==i)});dots.forEach((d,k)=>{d.classList.toggle('bg-bronze-500',k===i);d.classList.toggle('w-8',k===i);d.classList.toggle('bg-cream-600',k!==i);d.classList.toggle('w-2',k!==i)});caps.forEach((c,k)=>c.classList.toggle('hidden',k!==i));restart()};const restart=()=>{clearInterval(t);t=setInterval(()=>go(i+1),6000)};$('.prev',car).addEventListener('click',()=>go(i-1));$('.next',car).addEventListener('click',()=>go(i+1));dots.forEach(d=>d.addEventListener('click',()=>go(+d.dataset.i)));restart();}
/* galleries (collection + project pages) */
$$('.gallery').forEach(g=>{const imgs=g.dataset.imgs.split('|'),main=$('.gmain img',g),count=$('.gcount',g),thumbs=$$('.gthumb',g);let i=0;const show=n=>{i=(n+imgs.length)%imgs.length;main.src=imgs[i];if(count)count.textContent=(i+1)+' / '+imgs.length;thumbs.forEach((t,k)=>{t.classList.toggle('ring-2',k===i);t.classList.toggle('ring-bronze-500',k===i);t.classList.toggle('opacity-50',k!==i)})};$('.gmain',g).addEventListener('click',()=>openLb(imgs[i],main.alt));const p=$('.gprev',g),n=$('.gnext',g);if(p)p.addEventListener('click',()=>show(i-1));if(n)n.addEventListener('click',()=>show(i+1));thumbs.forEach(t=>t.addEventListener('click',()=>show(+t.dataset.i)));});
/* portfolio filter */
const filters=$('#filters');if(filters){filters.addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(!b)return;const f=b.dataset.f;$$('.fbtn',filters).forEach(x=>{const on=x===b;x.setAttribute('aria-pressed',String(on));x.classList.toggle('bg-bronze-600',on);x.classList.toggle('text-black',on);x.classList.toggle('shadow-lg',on);x.classList.toggle('bg-charcoal-800',!on);x.classList.toggle('text-cream-300',!on)});$$('.pcard').forEach(c=>c.classList.toggle('hidden',f!=='All'&&c.dataset.cat!==f))});}
/* about timeline */
const tl=$('#timeline');if(tl){const panels=$$('.tpanel',tl),marks=$$('.tmark',tl),dots=$$('.tdot',tl),prog=$('#tprog');let i=0;const n=panels.length;const show=k=>{i=(k+n)%n;panels.forEach((p,j)=>p.classList.toggle('hidden',j!==i));marks.forEach((m,j)=>{const dot=m.firstElementChild,lab=m.lastElementChild;dot.className='w-4 h-4 rounded-full border-2 z-10 '+(j===i?'bg-bronze-500 border-bronze-500 shadow-[0_0_8px_rgba(205,127,50,0.5)]':j<i?'bg-bronze-700/50 border-bronze-500/30':'bg-charcoal-700 border-cream-700/40');lab.className='text-sm font-medium whitespace-nowrap '+(j===i?'text-bronze-400':'text-cream-600')});dots.forEach((d,j)=>{d.firstElementChild.className='rounded-full h-2 '+(j===i?'w-4 bg-bronze-500':'w-2 bg-cream-700/40')});if(prog)prog.style.width='calc((100% - 5rem) * '+(n>1?i/(n-1):0)+')'};marks.forEach(m=>m.addEventListener('click',()=>show(+m.dataset.i)));dots.forEach(d=>d.addEventListener('click',()=>show(+d.dataset.i)));$$('.tprev',tl).forEach(b=>b.addEventListener('click',()=>show(i-1)));$$('.tnext',tl).forEach(b=>b.addEventListener('click',()=>show(i+1)));}
/* contact form: no server on static hosting, so open the visitor's mail app with the inquiry prefilled */
const cf=$('#contactForm');if(cf){cf.addEventListener('submit',e=>{e.preventDefault();const f=cf,note=$('#formNote');if(!f.name.value.trim()||!f.email.value.trim()||!f.projectType.value||!f.message.value.trim()){note.textContent='Please fill in the required fields (*).';note.classList.remove('hidden');return}const body=`Name: ${f.name.value}\nEmail: ${f.email.value}\nPhone: ${f.phone.value||'-'}\nProject type: ${f.projectType.value}\nBudget: ${f.budget.value||'-'}\nTimeline: ${f.timeline.value||'-'}\n\n${f.message.value}`;location.href='mailto:info@atelierbanger.com?subject='+encodeURIComponent('Commission inquiry — '+f.name.value)+'&body='+encodeURIComponent(body);note.textContent='Your mail app should open with the inquiry prefilled. If it does not, email info@atelierbanger.com directly.';note.classList.remove('hidden')});}
})();"""

def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    write("index.html", page_home())
    write("portfolio/index.html", page_portfolio())
    for p in PROJECTS:
        write(f"portfolio/{p['slug']}/index.html", page_project(p))
    write("collection/index.html", page_collection())
    write("services/index.html", page_services())
    write("about/index.html", page_about())
    write("contact/index.html", page_contact())
    write("artisans/index.html", page_artisans())
    write("privacy/index.html", page_legal("Privacy Policy", "Atelier Banger collects only the information you send through the contact form or by email, and uses it solely to respond to your inquiry and carry out your project. No data is sold or shared with third parties. Full policy text to be provided by the atelier."))
    write("terms/index.html", page_legal("Terms of Service", "All commissioned pieces are made to order; deposits, lead times and delivery terms are agreed in writing before fabrication begins. Full terms to be provided by the atelier."))
    write("assets/site.css", SITE_CSS)
    write("assets/site.js", SITE_JS)
    write(".nojekyll", "")
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"built {n} files into {OUT}")

if __name__ == "__main__":
    main()
