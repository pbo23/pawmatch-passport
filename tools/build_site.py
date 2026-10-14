#!/usr/bin/env python3
"""Собирает сайт PaWow для GitHub Pages.

    python3 tools/build_site.py

Пишет лендинг на трёх языках (index.html по-нидерландски: аудитория в NL и
проверка партнёрки bol; en/ и ru/), гид на тех же трёх языках (gids/,
en/guides/, ru/guides/; статьи лежат в site_guides.py), 404.html и картинки
в assets/ (нужен Pillow). Тексты правятся здесь и в site_guides.py,
сгенерированные html руками не трогать. Длинных тире в текстах нет.

passport.html (рендерер QR-ветпаспорта) и privacy/terms скрипт не трогает.
"""
import html
import json
import random
import re
from pathlib import Path

from site_guides import GIDS, GUIDE_DIR, GUIDES

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://pbo23.github.io/pawmatch-passport/"
EMAIL = "support@pawmatch.app"
UPDATED = "2026-10-14"
LANGS = ("nl", "en", "ru")
LANG_PATH = {"nl": "", "en": "en/", "ru": "ru/"}
OG_LOCALE = {"nl": "nl_NL", "en": "en_GB", "ru": "ru_RU"}
NBSP = " "


def esc(s):
    return html.escape(s, quote=True)


def on(selected):
    return ' class="on"' if selected else ""


CURRENT = ' aria-current="true"'


# ── Иконки ────────────────────────────────────────────────────────────────────

SVG_SIGNAL = ('<svg viewBox="0 0 18 12" fill="currentColor"><rect y="8" width="3" height="4" rx="1"/>'
              '<rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/>'
              '<rect x="15" width="3" height="12" rx="1"/></svg>')
SVG_WIFI = ('<svg viewBox="0 0 16 12" fill="currentColor"><path d="M8 2.2c2.4 0 4.6.9 6.3 2.5l1.2-1.3A10.6 10.6 0 0 0 8 '
            '.4C5.2.4 2.5 1.4.5 3.4l1.2 1.3A8.8 8.8 0 0 1 8 2.2zm0 3.6c1.4 0 2.7.5 3.7 1.4l1.2-1.3A7.4 7.4 0 0 0 8 4c-1.9 '
            '0-3.6.7-4.9 1.9l1.2 1.3c1-.9 2.3-1.4 3.7-1.4zm0 3.5c-.6 0-1.2.2-1.6.6L8 11.6l1.6-1.7c-.4-.4-1-.6-1.6-.6z"/></svg>')
SVG_BATT = ('<svg viewBox="0 0 27 12" fill="none"><rect x=".5" y=".5" width="23" height="11" rx="3.5" stroke="currentColor" '
            'opacity=".4"/><rect x="2" y="2" width="20" height="8" rx="2" fill="currentColor"/><path d="M25 4v4c.8-.3 '
            '1.4-1.1 1.4-2S25.8 4.3 25 4z" fill="currentColor" opacity=".45"/></svg>')
SVG_HEART = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.3l-1.5-1.3C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 '
             '3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.5 11.5z"/></svg>')
TAB_ICONS = [
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.3 2.6a1 1 0 0 1 1.4 0l8.6 7.9a1 1 0 0 1-.7 1.7H19v8a1.8 '
    '1.8 0 0 1-1.8 1.8h-2.7v-6h-5v6H6.8A1.8 1.8 0 0 1 5 20.2v-8H3.4a1 1 0 0 1-.7-1.7z"/></svg>',
    SVG_HEART,
    '<svg viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd"><path d="M5 4h14a3 3 0 0 1 3 3v10a3 3 0 0 1-3 3H5a3 '
    '3 0 0 1-3-3V7a3 3 0 0 1 3-3zm3.5 3.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM4 17.5V18h16v-2.6l-4.6-4.6-5.4 5.4-2.3-2.3z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.2 3h15.6l1.9 5.4A3 3 0 0 1 19 12.2V20a1 1 0 0 1-1 1h-4v-5h-4v5H6a1 '
    '1 0 0 1-1-1v-7.8A3 3 0 0 1 2.3 8.4z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd"><path d="M6 2h12a3 3 0 0 1 3 3v14a3 3 0 0 1-3 3H6a3 3 '
    '0 0 1-3-3V5a3 3 0 0 1 3-3zm6 13.6l.6-.5c2.2-2 3.6-3.2 3.6-4.8A2.1 2.1 0 0 0 14 8.2c-.8 0-1.5.4-2 1-.5-.6-1.2-1-2-1a2.1 '
    '2.1 0 0 0-2.2 2.1c0 1.6 1.4 2.8 3.6 4.8z"/></svg>',
]
SVG_X = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round">'
         '<path d="M6 6l12 12M18 6L6 18"/></svg>')
SVG_I = '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2.4"/><rect x="9.8" y="9" width="4.4" height="12" rx="2.2"/></svg>'
SVG_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/>'
            '<path d="M4 7.5l8 6 8-6"/></svg>')
SVG_CHEVRON = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
               'stroke-linejoin="round"><path d="M2.5 4.5L6 8l3.5-3.5"/></svg>')


def fake_qr(seed=11, n=25):
    """Узор «как QR» для макета. Не настоящий код: сканировать нечего."""
    rnd = random.Random(seed)
    cells = [[rnd.random() < .5 for _ in range(n)] for _ in range(n)]
    for r0, c0 in ((0, 0), (0, n - 7), (n - 7, 0)):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = r0 + r, c0 + c
                if 0 <= rr < n and 0 <= cc < n:
                    ring = max(abs(r - 3), abs(c - 3))
                    cells[rr][cc] = 0 <= r < 7 and 0 <= c < 7 and ring in (0, 1, 3)
    d = []
    for r in range(n):
        c = 0
        while c < n:
            if cells[r][c]:
                start = c
                while c < n and cells[r][c]:
                    c += 1
                d.append(f"M{start} {r}h{c - start}v1h-{c - start}z")
            else:
                c += 1
    return (f'<svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
            f'<path fill="currentColor" d="{"".join(d)}"/></svg>')


def eur(cents, lang):
    s = f"{cents / 100:.2f}"
    if lang == "en":
        return "€" + s
    s = s.replace(".", ",")
    return f"€{NBSP}{s}" if lang == "nl" else f"{s}{NBSP}€"


# ── Тексты ────────────────────────────────────────────────────────────────────

T = {
    "nl": {
        "title": "PaWow: alles voor je huisdier in één app",
        "desc": ("PaWow is een iPhone-app voor huisdiereigenaren in Nederland: vind speelmaatjes in de buurt, houd "
                 "vaccinaties en dierenartsbezoeken bij, deel een QR-dierenpaspoort met je dierenarts en vind "
                 "dierenartsen en trimsalons om de hoek."),
        "skip": "Naar de inhoud",
        "nav": [("features", "Functies"), ("how", "Hoe het werkt"), ("partners", "Partnerlinks"), ("contact", "Contact")],
        "nav_guide": "Gids",
        "eyebrow": "Nu in bèta voor iPhone",
        "h1": 'Alles voor je huisdier, <span class="g">in één app</span>',
        "lead": ("Vind speelmaatjes in de buurt, houd vaccinaties en dierenartsbezoeken bij en deel het dierenpaspoort "
                 "met één QR-code. PaWow is gemaakt voor honden- en kattenbaasjes in Nederland."),
        "cta": "Bekijk wat PaWow kan",
        "cta_guide": "Lees de gids",
        "soon": "<b>Binnenkort in de App Store</b> · nu in bèta via TestFlight",
        "features_kicker": "Functies",
        "features_h2": "Wat je met PaWow kunt",
        "features_lead": "Van de eerste ontmoeting in het park tot de jaarlijkse controle: alles rond je huisdier op één plek.",
        "features": [
            ("💞", "Matchen", "Vind speelmaatjes of een partner voor je hond of kat bij jou in de buurt. Filter op ras "
                             "en afstand, en chat met de eigenaar zodra het klikt."),
            ("🩺", "Gezondheidsdossier", "Vaccinaties, medicijnen en bezoeken aan de dierenarts op één plek, met "
                                        "herinneringen op je telefoon."),
            ("🔳", "QR-dierenpaspoort", "De dierenarts scant een QR-code en ziet meteen vaccinaties, chipnummer en eerdere "
                                       "bezoeken. De kliniek kan via dezelfde link de factuur terugsturen."),
            ("🐕", "Samen wandelen", "Zie welke honden er nu bij jou in de buurt lopen en ga samen een rondje. Je plek deel "
                                    "je alleen als je zelf een wandeling start."),
            ("📸", "Feed", "Deel foto's van je huisdier en zie wat andere baasjes delen. Leuk profiel gezien? Geef direct "
                          "een like."),
            ("📍", "Diensten in de buurt", "Dierenartsen, trimsalons en dierenwinkels bij jou in de buurt, op de kaart."),
            ("🛍️", "Productcatalogus", "Voer, speelgoed en verzorging van webwinkels als bol en Zooplus, afgestemd op "
                                      "jouw dier. Je bestelt gewoon bij de winkel."),
            ("🏠", "Adopteren", "Dieren uit asielen in de buurt die een nieuw thuis zoeken."),
        ],
        "health_kicker": "Gezondheid",
        "health_h2": "Het dierenpaspoort, altijd bij de hand",
        "health_text": ("Vaccinaties, medicijnen, chipnummer en bezoeken aan de dierenarts: in PaWow staat alles op één "
                        "plek, ook als het papieren paspoort thuis in een la ligt."),
        "health_points": [
            "Herinneringen voor de volgende vaccinatie, controle of medicijnen, gewoon op je telefoon.",
            "Een QR-link voor de dierenarts: 7 dagen geldig en op elk moment in te trekken.",
            "De kliniek stuurt de factuur via dezelfde link terug, zodat jij hem kunt doorsturen naar je verzekeraar.",
        ],
        "catalog_kicker": "Catalogus",
        "catalog_h2": "Spullen voor je dier, zonder eindeloos zoeken",
        "catalog_text": ("In de catalogus vind je voer, speelgoed, accessoires en verzorgingsproducten van webwinkels als bol "
                         "en Zooplus, afgestemd op het soort dier dat je hebt."),
        "catalog_points": [
            "Gefilterd op soort: voor honden, voor katten of alles.",
            "Prijs, korting en levertijd in één oogopslag. Prijzen werken we dagelijks bij.",
            "Je bestelt en betaalt bij de winkel zelf, met hun service en retourbeleid.",
        ],
        "catalog_link": "Zo werken onze partnerlinks →",
        "how_kicker": "Hoe het werkt",
        "how_h2": "In drie stappen op weg",
        "steps": [
            ("Maak een profiel", "Naam, soort, ras, geboortedatum en een foto. Meer dieren? Je wisselt met één tik."),
            ("Zet de gezondheid op een rij", "Voeg vaccinaties en bezoeken toe, en PaWow herinnert je eraan als er iets "
                                            "aankomt."),
            ("Ontdek de buurt", "Matches, wandelmaatjes, dierenartsen en trimsalons om de hoek."),
        ],
        "guides_kicker": "Gids",
        "guides_h2": "Gids voor baasjes",
        "guides_lead": ("Praktische artikelen die we zelf schrijven: over de eerste weken met een pup, op reis met je "
                        "huisdier en de regels voor het uitlaten."),
        "guides_all": "Alle artikelen in de gids →",
        "read": "Lees verder →",
        "min": "min lezen",
        "partners_kicker": "Partnerlinks",
        "partners_h2": "Transparant over partnerlinks",
        "partners_lead": "PaWow verdient aan partnerlinks, niet aan jouw gegevens. Zo werkt het:",
        "partners": [
            ("Commissie, geen meerprijs", "Koop je iets via een link in onze catalogus, dan krijgt PaWow een kleine "
                                          "commissie van de winkel. Jij betaalt niets extra."),
            ("Je koopt bij de winkel", "We verkopen zelf niets. Bestellen, betalen, bezorgen en retourneren regel je met "
                                       "de winkel, onder hun voorwaarden."),
            ("De winkel is leidend", "Prijzen werken we dagelijks bij, maar de prijs op de site van de winkel is altijd "
                                     "leidend."),
            ("Duidelijk gemarkeerd", "Partnerlinks zijn in de app als zodanig gemarkeerd, en we geven geen "
                                     "persoonsgegevens door aan de winkel."),
            ("Eerlijk advies", "Onze artikelen schrijven we zelf. Een commissie verandert niets aan wat we aanraden."),
        ],
        "privacy_kicker": "Privacy",
        "privacy_h2": "Je gegevens blijven van jou",
        "privacy_text": "We bewaren alleen wat nodig is om de app te laten werken, en jij houdt de regie.",
        "privacy_points": [
            "Opgeslagen in datacenters in de EU.",
            "Medische gegevens zie alleen jij, en de dierenarts als jij een QR-link deelt.",
            "Anderen zien de locatie van je huisdier alleen afgerond.",
            "We verkopen je gegevens niet en gebruiken ze niet voor advertenties.",
            "Account verwijderen? Dan wissen we alles, ook je dieren en berichten.",
        ],
        "privacy_link": "Lees het volledige privacybeleid (Engels)",
        "faq_kicker": "Vragen",
        "faq_h2": "Veelgestelde vragen",
        "faq": [
            ("Wanneer staat PaWow in de App Store?",
             "We testen de app nu via TestFlight met een kleine groep baasjes. Zodra PaWow in de App Store staat, vind "
             "je de link op deze pagina."),
            ("Is er een Android-versie?", "Nog niet: PaWow is er voorlopig alleen voor iPhone."),
            ("In welke talen is de app beschikbaar?", "In het Engels en het Russisch."),
            ("Voor welke dieren is PaWow?",
             "Voor honden, katten, vogels, konijnen en andere huisdieren. Samen wandelen is er alleen voor honden."),
            ("Wie kan de gegevens van mijn huisdier zien?",
             "Naam, ras en foto van je huisdier zien andere gebruikers bij het matchen, in de feed en op de wandelkaart. "
             "Medische gegevens, documenten en berichten zie alleen jij, plus degene met wie je chat of een QR-link deelt."),
            ("Verkoopt PaWow zelf producten?",
             'Nee. De catalogus verwijst naar webwinkels; daar bestel en betaal je. Lees <a href="#partners">hoe '
             'partnerlinks werken</a>.'),
        ],
        "about_kicker": "Over ons",
        "about_h2": "Over PaWow",
        "about": [
            "PaWow is een onafhankelijke app voor huisdiereigenaren in Nederland. We bouwen hem stap voor stap, samen met "
            "de eerste gebruikers. Elke reactie helpt.",
            "Ben je dierenarts, trimsalon of asiel en wil je in PaWow zichtbaar zijn? Laat het ons weten.",
        ],
        "contact_h3": "Contact",
        "contact_text": "Vragen, ideeën of samenwerken? We horen graag van je.",
        "contact_btn": "Mail ons",
        "legal_privacy": "Privacybeleid (Engels)",
        "legal_terms": "Gebruiksvoorwaarden (Engels)",
        "legal_lang": "en",
        "foot_tag": "Alles voor je huisdier, in één app.",
        "foot_cookies": "Deze website plaatst geen cookies en gebruikt geen trackers.",
        "m": {
            "pet": "Max", "chips": ["🐾 Jack Russell", "Dichtbij · 5 km"], "dist": "740 m",
            "name": "Luna", "age": "2 jaar", "meta": "Border Collie · Teef", "bio": "Rent het liefst achter een bal aan 🎾",
            "next": ("Bella", "3 jaar", "Poedel · Teef", "Dol op wandelingen in het bos 🌳", "1,2 km"),
            "tabs": ["Home", "Match", "Feed", "Diensten", "Gezondheid"],
            "health": "Gezondheid", "pets": ["Max", "Pip"], "qr_t": "QR-dierenpaspoort", "qr_s": "Laat de dierenarts scannen",
            "qr_v": "7 dagen geldig", "vacc": "VACCINATIES",
            "vaccs": [("Cocktailenting", "12 mrt 2026", "tot mrt 2027", "ok"),
                      ("Leptospirose", "12 mrt 2026", "tot mrt 2027", "ok"),
                      ("Rabiës", "4 nov 2025", "over 3 weken", "warn")],
            "visits": "AFSPRAKEN", "visit": ("Jaarlijkse controle", "Dierenkliniek · 10:30", "28 okt"),
            "services": "Diensten", "seg": ["Kaart", "Catalogus", "Afspraken"],
            "cats": [("🥩", "Voer"), ("🎾", "Speelgoed"), ("🦮", "Accessoires"), ("✂️", "Verzorging")],
            "species": ["Voor honden", "Voor katten", "Alle"],
            "products": [("🍖", "Hondenbrokken lam & rijst, 12 kg", "bol.com", 3999, 4799),
                         ("🥫", "Natvoer kip, 12 × 400 g", "zooplus", 1849, None),
                         ("🦴", "Kauwbotten rund, 3 stuks", "bol.com", 799, None),
                         ("🐟", "Puppybrokken zalm, 3 kg", "zooplus", 1699, 1999)],
        },
    },
    "en": {
        "title": "PaWow: everything for your pet in one app",
        "desc": ("PaWow is an iPhone app for pet owners in the Netherlands: find playmates nearby, keep track of "
                 "vaccinations and vet visits, share a QR vet passport with your clinic and find vets and groomers "
                 "around the corner."),
        "skip": "Skip to content",
        "nav": [("features", "Features"), ("how", "How it works"), ("partners", "Affiliate links"), ("contact", "Contact")],
        "nav_guide": "Guides",
        "eyebrow": "Now in beta for iPhone",
        "h1": 'Everything for your pet, <span class="g">in one app</span>',
        "lead": ("Find playmates nearby, keep vaccinations and vet visits in one place and share the vet passport with a "
                 "single QR code. PaWow is made for dog and cat owners in the Netherlands."),
        "cta": "See what PaWow does",
        "cta_guide": "Read the guides",
        "soon": "<b>Coming soon to the App Store</b> · now in beta on TestFlight",
        "features_kicker": "Features",
        "features_h2": "What you can do with PaWow",
        "features_lead": "From the first meeting in the park to the yearly check-up: everything about your pet in one place.",
        "features": [
            ("💞", "Matching", "Find playmates or a mate for your dog or cat nearby. Filter by breed and distance, and "
                              "chat with the owner once it clicks."),
            ("🩺", "Health record", "Vaccinations, medication and vet visits in one place, with reminders on your phone."),
            ("🔳", "QR vet passport", "Your vet scans a QR code and instantly sees vaccinations, the microchip number and "
                                     "past visits. The clinic can send the invoice back through the same link."),
            ("🐕", "Walk together", "See which dogs are out for a walk nearby and join them. Your location is only shared "
                                   "when you start a walk yourself."),
            ("📸", "Feed", "Share photos of your pet and see what other owners post. Like a profile? Send a like right "
                          "away."),
            ("📍", "Services nearby", "Vets, groomers and pet shops near you, on the map."),
            ("🛍️", "Product catalog", "Food, toys and care products from web shops such as bol and Zooplus, matched to "
                                     "your pet. You order from the shop as usual."),
            ("🏠", "Adoption", "Animals from nearby shelters looking for a new home."),
        ],
        "health_kicker": "Health",
        "health_h2": "The vet passport, always at hand",
        "health_text": ("Vaccinations, medication, the microchip number and vet visits: PaWow keeps it all in one place, "
                        "even when the paper passport is in a drawer at home."),
        "health_points": [
            "Reminders for the next vaccination, check-up or medication, right on your phone.",
            "A QR link for the vet: valid for 7 days and revocable at any time.",
            "The clinic sends the invoice back through the same link, so you can forward it to your insurer.",
        ],
        "catalog_kicker": "Catalog",
        "catalog_h2": "Supplies for your pet, without endless searching",
        "catalog_text": ("The catalog brings together food, toys, accessories and care products from web shops such as bol "
                         "and Zooplus, matched to the kind of pet you have."),
        "catalog_points": [
            "Filtered by species: for dogs, for cats or everything.",
            "Price, discount and delivery time at a glance. Prices are refreshed daily.",
            "You order and pay at the shop itself, with its service and return policy.",
        ],
        "catalog_link": "How our affiliate links work →",
        "how_kicker": "How it works",
        "how_h2": "Up and running in three steps",
        "steps": [
            ("Create a profile", "Name, species, breed, birth date and a photo. More pets? Switch with a single tap."),
            ("Get health in order", "Add vaccinations and visits, and PaWow reminds you when something is due."),
            ("Discover your area", "Matches, walking buddies, vets and groomers around the corner."),
        ],
        "guides_kicker": "Guides",
        "guides_h2": "Guides for pet owners",
        "guides_lead": ("Practical articles we write ourselves: about the first weeks with a puppy, travelling with your "
                        "pet and the rules for walking your dog."),
        "guides_all": "All guides →",
        "read": "Read more →",
        "min": "min read",
        "partners_kicker": "Affiliate links",
        "partners_h2": "Open about affiliate links",
        "partners_lead": "PaWow earns from affiliate links, not from your data. Here is how it works:",
        "partners": [
            ("Commission, no mark-up", "If you buy something through a link in our catalog, the shop pays PaWow a small "
                                       "commission. You pay nothing extra."),
            ("You buy from the shop", "We don't sell anything ourselves. Ordering, payment, delivery and returns are "
                                      "handled by the shop, under its terms."),
            ("The shop's price counts", "We refresh prices daily, but the price on the shop's website always prevails."),
            ("Clearly labelled", "Affiliate links are labelled as such in the app, and we don't pass your personal data "
                                 "to the shop."),
            ("Honest advice", "We write our articles ourselves. A commission doesn't change what we recommend."),
        ],
        "privacy_kicker": "Privacy",
        "privacy_h2": "Your data stays yours",
        "privacy_text": "We keep only what the app needs to work, and you stay in control.",
        "privacy_points": [
            "Stored in data centres in the EU.",
            "Medical records are visible only to you, and to your vet if you share a QR link.",
            "Other people only see your pet's location rounded.",
            "We never sell your data or use it for advertising.",
            "Delete your account and we erase everything, including your pets and messages.",
        ],
        "privacy_link": "Read the full privacy policy",
        "faq_kicker": "Questions",
        "faq_h2": "Frequently asked questions",
        "faq": [
            ("When will PaWow be in the App Store?",
             "We are testing the app on TestFlight with a small group of owners. As soon as PaWow is in the App Store, "
             "you'll find the link on this page."),
            ("Is there an Android version?", "Not yet: for now PaWow is iPhone-only."),
            ("Which languages is the app available in?", "English and Russian."),
            ("Which animals is PaWow for?",
             "Dogs, cats, birds, rabbits and other pets. Walking together is for dogs only."),
            ("Who can see my pet's data?",
             "Your pet's name, breed and photo are visible to other users in matching, in the feed and on the walks map. "
             "Medical records, documents and messages are visible only to you and to whoever you chat with or share a "
             "QR link with."),
            ("Does PaWow sell products itself?",
             'No. The catalog links to web shops, where you order and pay. Read <a href="#partners">how affiliate links '
             'work</a>.'),
        ],
        "about_kicker": "About",
        "about_h2": "About PaWow",
        "about": [
            "PaWow is an independent app for pet owners in the Netherlands. We are building it step by step, together with "
            "our first users. Every bit of feedback helps.",
            "Are you a vet, groomer or shelter and would you like to be visible in PaWow? Let us know.",
        ],
        "contact_h3": "Contact",
        "contact_text": "Questions, ideas or a partnership? We'd love to hear from you.",
        "contact_btn": "Email us",
        "legal_privacy": "Privacy policy",
        "legal_terms": "Terms of service",
        "legal_lang": "en",
        "foot_tag": "Everything for your pet, in one app.",
        "foot_cookies": "This website sets no cookies and uses no trackers.",
        "m": {
            "pet": "Max", "chips": ["🐾 Jack Russell", "Nearby · 5 km"], "dist": "740 m",
            "name": "Luna", "age": "2 years", "meta": "Border Collie · Female", "bio": "Would chase a ball all day 🎾",
            "next": ("Bella", "3 years", "Poodle · Female", "Loves walks in the woods 🌳", "1.2 km"),
            "tabs": ["Home", "Match", "Feed", "Services", "Health"],
            "health": "Health", "pets": ["Max", "Pip"], "qr_t": "QR vet passport", "qr_s": "Let your vet scan it",
            "qr_v": "Valid 7 days", "vacc": "VACCINATIONS",
            "vaccs": [("Core vaccine (DHP)", "12 Mar 2026", "until Mar 2027", "ok"),
                      ("Leptospirosis", "12 Mar 2026", "until Mar 2027", "ok"),
                      ("Rabies", "4 Nov 2025", "due in 3 weeks", "warn")],
            "visits": "APPOINTMENTS", "visit": ("Annual check-up", "Vet clinic · 10:30", "28 Oct"),
            "services": "Services", "seg": ["Map", "Catalog", "Bookings"],
            "cats": [("🥩", "Food"), ("🎾", "Toys"), ("🦮", "Accessories"), ("✂️", "Grooming")],
            "species": ["For dogs", "For cats", "All"],
            "products": [("🍖", "Dry dog food lamb & rice, 12 kg", "bol.com", 3999, 4799),
                         ("🥫", "Wet food chicken, 12 × 400 g", "zooplus", 1849, None),
                         ("🦴", "Beef chew bones, 3 pack", "bol.com", 799, None),
                         ("🐟", "Puppy food salmon, 3 kg", "zooplus", 1699, 1999)],
        },
    },
    "ru": {
        "title": "PaWow: всё для питомца в одном приложении",
        "desc": ("PaWow: приложение для iPhone для владельцев питомцев в Нидерландах. Друзья и пара для питомца рядом, "
                 "прививки и визиты к ветеринару, QR-ветпаспорт для клиники, ветклиники и груминг-салоны поблизости."),
        "skip": "К содержимому",
        "nav": [("features", "Возможности"), ("how", "Как это работает"), ("partners", "Партнёрские ссылки"),
                ("contact", "Контакты")],
        "nav_guide": "Гайды",
        "eyebrow": "Бета-версия для iPhone",
        "h1": 'Всё для питомца <span class="g">в одном приложении</span>',
        "lead": ("Находите друзей и пару для питомца рядом, храните прививки и визиты к ветеринару в одном месте и "
                 "показывайте ветпаспорт одним QR-кодом. PaWow сделан для владельцев собак и кошек в Нидерландах."),
        "cta": "Что умеет PaWow",
        "cta_guide": "Читать гайды",
        "soon": "<b>Скоро в App Store</b> · сейчас бета в TestFlight",
        "features_kicker": "Возможности",
        "features_h2": "Что можно делать в PaWow",
        "features_lead": "От первого знакомства в парке до ежегодного осмотра: всё о питомце в одном месте.",
        "features": [
            ("💞", "Матч", "Друзья для игр или пара для собаки или кошки рядом с вами. Фильтр по породе и расстоянию, а "
                          "когда симпатия взаимна, можно написать владельцу."),
            ("🩺", "Медкарта", "Прививки, препараты и визиты к ветеринару в одном месте, с напоминаниями на телефоне."),
            ("🔳", "QR-ветпаспорт", "Ветеринар сканирует QR-код и сразу видит прививки, номер чипа и прошлые визиты. По "
                                   "той же ссылке клиника может прислать счёт."),
            ("🐕", "Прогулки вместе", "Смотрите, какие собаки гуляют рядом прямо сейчас, и присоединяйтесь. Своё место "
                                     "вы показываете, только когда сами начинаете прогулку."),
            ("📸", "Лента", "Делитесь фото питомца и смотрите, что публикуют другие. Понравился профиль? Поставьте лайк "
                           "прямо из ленты."),
            ("📍", "Услуги рядом", "Ветклиники, груминг-салоны и зоомагазины поблизости, на карте."),
            ("🛍️", "Каталог товаров", "Корм, игрушки и средства ухода из интернет-магазинов bol и Zooplus с учётом "
                                     "вида питомца. Заказ как обычно, на сайте магазина."),
            ("🏠", "Усыновление", "Животные из приютов поблизости, которые ищут дом."),
        ],
        "health_kicker": "Здоровье",
        "health_h2": "Ветпаспорт всегда под рукой",
        "health_text": ("Прививки, препараты, номер чипа и визиты к ветеринару: в PaWow всё в одном месте, даже если "
                        "бумажный паспорт остался дома в ящике стола."),
        "health_points": [
            "Напоминания о следующей прививке, осмотре или приёме препарата, прямо на телефоне.",
            "QR-ссылка для ветеринара: действует 7 дней, отозвать можно в любой момент.",
            "По той же ссылке клиника присылает счёт, и вы пересылаете его в страховую.",
        ],
        "catalog_kicker": "Каталог",
        "catalog_h2": "Всё нужное для питомца без долгих поисков",
        "catalog_text": ("В каталоге собраны корм, игрушки, аксессуары и средства ухода из интернет-магазинов bol и "
                         "Zooplus, с учётом того, какой у вас питомец."),
        "catalog_points": [
            "Фильтр по виду: для собак, для кошек или всё.",
            "Цена, скидка и срок доставки сразу видны. Цены обновляются ежедневно.",
            "Заказ и оплата на сайте магазина, с его сервисом и условиями возврата.",
        ],
        "catalog_link": "Как работают партнёрские ссылки →",
        "how_kicker": "Как это работает",
        "how_h2": "Три шага, и готово",
        "steps": [
            ("Создайте анкету", "Кличка, вид, порода, дата рождения и фото. Несколько питомцев? Переключение одним "
                               "касанием."),
            ("Наведите порядок в здоровье", "Добавьте прививки и визиты, и PaWow напомнит, когда подойдёт срок."),
            ("Откройте свой район", "Матчи, компания для прогулок, ветклиники и груминг-салоны рядом."),
        ],
        "guides_kicker": "Гайды",
        "guides_h2": "Гайды для владельцев",
        "guides_lead": ("Практичные статьи, которые мы пишем сами: первые недели со щенком, поездки с питомцем и "
                        "правила выгула."),
        "guides_all": "Все гайды →",
        "read": "Читать →",
        "min": "мин чтения",
        "partners_kicker": "Партнёрские ссылки",
        "partners_h2": "Честно о партнёрских ссылках",
        "partners_lead": "PaWow зарабатывает на партнёрских ссылках, а не на ваших данных. Как это устроено:",
        "partners": [
            ("Комиссия без наценки", "Если вы покупаете что-то по ссылке из нашего каталога, магазин платит PaWow "
                                     "небольшую комиссию. Для вас цена не меняется."),
            ("Покупка в магазине", "Сами мы ничего не продаём. Заказ, оплата, доставка и возврат проходят через "
                                     "магазин, по его правилам."),
            ("Главная цена у магазина", "Цены мы обновляем ежедневно, но решает цена на сайте магазина."),
            ("Чёткая пометка", "Партнёрские ссылки в приложении помечены, а ваши личные данные магазину мы не "
                               "передаём."),
            ("Честные советы", "Статьи мы пишем сами. Комиссия не влияет на то, что мы советуем."),
        ],
        "privacy_kicker": "Приватность",
        "privacy_h2": "Ваши данные остаются вашими",
        "privacy_text": "Мы храним только то, что нужно для работы приложения, а управляете ими вы.",
        "privacy_points": [
            "Хранятся в дата-центрах в ЕС.",
            "Медицинские записи видите только вы и ветеринар, если вы поделились QR-ссылкой.",
            "Другим пользователям местоположение питомца показывается только округлённым.",
            "Мы не продаём данные и не используем их для рекламы.",
            "Если удалить аккаунт, мы сотрём всё, включая питомцев и переписку.",
        ],
        "privacy_link": "Полная политика конфиденциальности",
        "faq_kicker": "Вопросы",
        "faq_h2": "Частые вопросы",
        "faq": [
            ("Когда PaWow появится в App Store?",
             "Сейчас мы тестируем приложение в TestFlight с небольшой группой владельцев. Как только PaWow выйдет в App "
             "Store, ссылка появится на этой странице."),
            ("Есть ли версия для Android?", "Пока нет: PaWow сейчас только для iPhone."),
            ("На каких языках приложение?", "На английском и русском."),
            ("Для каких животных PaWow?",
             "Для собак, кошек, птиц, кроликов и других питомцев. Совместные прогулки есть только для собак."),
            ("Кто видит данные моего питомца?",
             "Кличку, породу и фото питомца видят другие пользователи: в подборе пар, в ленте и на карте прогулок. "
             "Медицинские записи, документы и переписку видите только вы и тот, с кем вы переписываетесь или кому "
             "отправили QR-ссылку."),
            ("PaWow сам продаёт товары?",
             'Нет. Каталог ведёт в интернет-магазины, заказ и оплата там. Подробнее: <a href="#partners">как работают '
             'партнёрские ссылки</a>.'),
        ],
        "about_kicker": "О нас",
        "about_h2": "О PaWow",
        "about": [
            "Мы делаем PaWow, независимое приложение для владельцев питомцев в Нидерландах, шаг за шагом и вместе с "
            "первыми пользователями. Любой отзыв помогает.",
            "Вы ветклиника, груминг-салон или приют и хотите появиться в PaWow? Напишите нам.",
        ],
        "contact_h3": "Контакты",
        "contact_text": "Вопросы, идеи или сотрудничество? Будем рады письму.",
        "contact_btn": "Написать",
        "legal_privacy": "Политика конфиденциальности",
        "legal_terms": "Условия использования",
        "legal_lang": "ru",
        "foot_tag": "Всё для питомца в одном приложении.",
        "foot_cookies": "Этот сайт не ставит cookies и не использует трекеры.",
        "m": {
            "pet": "Макс", "chips": ["🐾 Джек-рассел", "Рядом · 5 км"], "dist": "740 м",
            "name": "Луна", "age": "2 года", "meta": "Бордер-колли · девочка", "bio": "Готова гонять мяч весь день 🎾",
            "next": ("Белла", "3 года", "Пудель · девочка", "Обожает гулять в лесу 🌳", "1,2 км"),
            "tabs": ["Главная", "Матч", "Лента", "Услуги", "Здоровье"],
            "health": "Здоровье", "pets": ["Макс", "Пип"], "qr_t": "QR-ветпаспорт", "qr_s": "Покажите ветеринару",
            "qr_v": "7 дней", "vacc": "ПРИВИВКИ",
            "vaccs": [("Комплексная (DHP)", "12 мар 2026", "до мар 2027", "ok"),
                      ("Лептоспироз", "12 мар 2026", "до мар 2027", "ok"),
                      ("Бешенство", "4 ноя 2025", "через 3 нед", "warn")],
            "visits": "ВИЗИТЫ", "visit": ("Ежегодный осмотр", "Ветклиника · 10:30", "28 окт"),
            "services": "Услуги", "seg": ["Карта", "Каталог", "Записи"],
            "cats": [("🥩", "Корм"), ("🎾", "Игрушки"), ("🦮", "Аксессуары"), ("✂️", "Уход")],
            "species": ["Для собак", "Для кошек", "Все"],
            "products": [("🍖", "Сухой корм ягнёнок и рис, 12 кг", "bol.com", 3999, 4799),
                         ("🥫", "Влажный корм курица, 12 × 400 г", "zooplus", 1849, None),
                         ("🦴", "Жевательные кости, 3 шт.", "bol.com", 799, None),
                         ("🐟", "Корм для щенков лосось, 3 кг", "zooplus", 1699, 1999)],
        },
    },
}


# ── Макеты экранов ────────────────────────────────────────────────────────────

def status_bar():
    return f'<div class="island"></div><div class="sb"><span>9:41</span><span>{SVG_SIGNAL}{SVG_WIFI}{SVG_BATT}</span></div>'


def tabbar(m, active):
    items = "".join(
        f'<span{on(i == active)}>{icon}{esc(label)}</span>'
        for i, (icon, label) in enumerate(zip(TAB_ICONS, m["tabs"]))
    )
    return f'<div class="tabbar">{items}</div>'


def phone_match(m):
    chips = "".join(f'<span{on(i == 0)}>{esc(c)}</span>' for i, c in enumerate(m["chips"]))
    nx_name, nx_age, nx_meta, nx_bio, nx_dist = m["next"]
    return f"""<div class="phone" aria-hidden="true"><div class="screen">{status_bar()}
<div class="scr"><div class="m-top"><span class="m-petchip"><span class="m-av">🐶</span>{esc(m["pet"])}{SVG_CHEVRON}</span></div>
<div class="m-chips">{chips}</div>
<div class="m-deck">
<div class="m-card c2"><span class="m-dist">➤ {esc(nx_dist)}</span><div class="m-photo">🐩</div>
<div class="m-info"><b>{esc(nx_name)}</b><span>{esc(nx_age)}</span><div>{esc(nx_meta)}</div><p>{esc(nx_bio)}</p></div></div>
<div class="m-card c1"><span class="m-dist">➤ {esc(m["dist"])}</span><div class="m-photo">🐕</div>
<div class="m-info"><b>{esc(m["name"])}</b><span>{esc(m["age"])}</span><div>{esc(m["meta"])}</div><p>{esc(m["bio"])}</p></div>
<span class="m-stamp">{SVG_HEART}</span></div>
</div>
<div class="m-actions"><span class="a-x">{SVG_X}</span><span class="a-i">{SVG_I}</span><span class="a-h">{SVG_HEART}</span></div></div>
{tabbar(m, 1)}</div></div>"""


def phone_health(m):
    pets = "".join(f'<span{on(i == 0)}><b>{e}</b><i>{esc(n)}</i></span>'
                   for i, (e, n) in enumerate(zip(("🐶", "🐱"), m["pets"])))
    vaccs = "".join(
        f'<div class="h-row"><span class="ic">💉</span><div><b>{esc(name)}</b><span>{esc(date)}</span></div>'
        f'<span class="pill {kind}">{esc(pill)}</span></div>'
        for name, date, pill, kind in m["vaccs"]
    )
    title, sub, date = m["visit"]
    return f"""<div class="phone" aria-hidden="true"><div class="screen">{status_bar()}
<div class="scr"><div class="h-title">{esc(m["health"])}</div>
<div class="h-pets">{pets}</div>
<div class="h-qr"><div><b>{esc(m["qr_t"])}</b><span>{esc(m["qr_s"])}</span><em>{esc(m["qr_v"])}</em></div><span class="qrbox">{fake_qr()}<i class="scan"></i></span></div>
<div class="h-sec">{esc(m["vacc"])}</div><div class="h-list">{vaccs}</div>
<div class="h-sec">{esc(m["visits"])}</div>
<div class="h-list"><div class="h-row"><span class="ic v">🩺</span><div><b>{esc(title)}</b><span>{esc(sub)}</span></div><span class="date">{esc(date)}</span></div></div></div>
{tabbar(m, 4)}</div></div>"""


def phone_catalog(m, lang):
    seg = "".join(f'<span{on(i == 1)}>{esc(s)}</span>' for i, s in enumerate(m["seg"]))
    cats = "".join(f'<span{on(i == 0)}><i>{e}</i>{esc(n)}</span>' for i, (e, n) in enumerate(m["cats"]))
    sp = "".join(f'<span{on(i == 0)}>{esc(s)}</span>' for i, s in enumerate(m["species"]))
    cards = []
    for emoji, title, store, price, old in m["products"]:
        badge = f'<em>-{round((old - price) / old * 100)}%</em>' if old else ""
        was = f"<s>{eur(old, lang)}</s>" if old else ""
        cards.append(f'<div class="pc"><div class="pc-img">{emoji}{badge}</div><b>{esc(title)}</b>'
                     f'<span>{store}</span><strong>{eur(price, lang)}{was}</strong></div>')
    return f"""<div class="phone" aria-hidden="true"><div class="screen">{status_bar()}
<div class="scr"><div class="c-title">{esc(m["services"])}</div>
<div class="seg">{seg}</div>
<div class="c-cats">{cats}</div>
<div class="c-sp">{sp}</div>
<div class="c-grid">{"".join(cards)}</div></div>
{tabbar(m, 3)}</div></div>"""


# ── Каркас страницы ───────────────────────────────────────────────────────────
#
# У каждой страницы есть адреса на всех трёх языках (`paths`): по ним строятся
# переключатель языка и hreflang. Переключатель ведёт на ту же страницу в
# другом языке, а не на главную.

def root_of(path):
    """Путь от страницы до корня сайта: "" → "", "en/" → "../", "en/guides/a.html" → "../../"."""
    return "../" * path.count("/")


def rel(root, path):
    return (root + path) or "./"


# Класс js на <html> ставится до стилей: без него (JS выключен) блоки с
# классом reveal не прячутся и видны сразу.
JS_FLAG = "<script>document.documentElement.classList.add('js')</script>\n"

# Блоки проявляются, когда доходят до экрана. Наблюдатель отписывается от
# показанного блока: анимация срабатывает один раз.
REVEAL_SCRIPT = """<script>
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { items.forEach(function (el) { el.classList.add('in'); }); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
})();
</script>
"""


def head(*, lang, title, desc, path, root, alternates=None, early="", extra=""):
    canonical = BASE + path
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE + alternates[l]}">\n' for l in LANGS)
        alt += f'<link rel="alternate" hreflang="x-default" href="{BASE + alternates["nl"]}">\n'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
{JS_FLAG}{early}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{alt}<meta name="theme-color" content="#e84b7a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PaWow">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}assets/og.png">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/favicon-64.png" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/icon-180.png">
<link rel="stylesheet" href="{root}assets/site.css">
{extra}</head>
"""


def lang_switch(root, lang, paths):
    return "".join(
        f'<a href="{rel(root, paths[code])}" hreflang="{code}" lang="{code}"{CURRENT if code == lang else ""}>'
        f'{code.upper()}</a>'
        for code in LANGS
    )


def header(*, t, root, lang, on_landing, paths):
    home = rel(root, LANG_PATH[lang])
    pre = "" if on_landing else home
    links = [f'<a href="{pre}#{anchor}">{esc(label)}</a>' for anchor, label in t["nav"][:2]]
    links.append(f'<a class="keep" href="{rel(root, GUIDE_DIR[lang])}">{esc(t["nav_guide"])}</a>')
    links += [f'<a href="{pre}#{anchor}">{esc(label)}</a>' for anchor, label in t["nav"][2:]]
    return f"""<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{home}"><img src="{root}assets/logo-128.png" alt="" width="34" height="34">PaWow</a>
<nav class="nav" aria-label="Menu">{"".join(links)}</nav>
<div class="langs" aria-label="Language">{lang_switch(root, lang, paths)}</div>
</div></header>
"""


def footer(*, t, root, lang, on_landing, paths):
    home = rel(root, LANG_PATH[lang])
    pre = "" if on_landing else home
    ll = t["legal_lang"]
    return f"""<footer class="foot"><div class="wrap">
<div>
<a class="brand" href="{home}"><img src="{root}assets/logo-128.png" alt="" width="28" height="28">PaWow</a>
<p>{esc(t["foot_tag"])}</p>
<p>{esc(t["foot_cookies"])}</p>
<p>© 2026 PaWow · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<div>
<nav aria-label="Footer">
<a href="{pre}#features">{esc(t["nav"][0][1])}</a>
<a href="{rel(root, GUIDE_DIR[lang])}">{esc(t["nav_guide"])}</a>
<a href="{pre}#partners">{esc(t["nav"][2][1])}</a>
<a href="{root}privacy.html?lang={ll}">{esc(t["legal_privacy"])}</a>
<a href="{root}terms.html?lang={ll}">{esc(t["legal_terms"])}</a>
</nav>
<div class="langs" style="margin-top:16px;display:inline-flex">{lang_switch(root, lang, paths)}</div>
</div>
</div></footer>
{REVEAL_SCRIPT}</body>
</html>
"""


def guide_path(g, lang):
    return GUIDE_DIR[lang] + g["slug"][lang] + ".html"


def guide_card(g, lang, root, t, i=0):
    return (f'<a class="guide reveal" style="--i:{i}" href="{root}{guide_path(g, lang)}">'
            f'<div class="thumb" aria-hidden="true"><span>{g["emoji"]}</span></div>'
            f'<div class="body"><div class="meta"><span>{g["minutes"]} {esc(t["min"])}</span></div>'
            f'<h3>{esc(g["title"][lang])}</h3><p>{esc(g["excerpt"][lang])}</p>'
            f'<span class="go">{esc(t["read"])}</span></div></a>')


# ── Лендинг ───────────────────────────────────────────────────────────────────

# Ссылки QR-ветпаспорта из приложения ведут на корень (`?id=…&lang=…`), и такие
# QR уже распечатаны и разосланы. Сама страница паспорта теперь passport.html:
# переадресация стоит первой в <head>, до загрузки стилей, чтобы врач не видел
# мелькнувший лендинг.
PASSPORT_REDIRECT = ("<script>if(new URLSearchParams(location.search).has('id'))"
                     "location.replace('passport.html'+location.search);</script>\n")


def landing(lang):
    t = T[lang]
    m = t["m"]
    path = LANG_PATH[lang]
    root = root_of(path)
    guides_href = rel(root, GUIDE_DIR[lang])
    ld = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "PaWow",
        "operatingSystem": "iOS", "applicationCategory": "LifestyleApplication",
        "description": t["desc"], "url": BASE + path, "inLanguage": lang,
        "image": BASE + "assets/logo-512.png",
        "publisher": {"@type": "Organization", "name": "PaWow", "email": EMAIL, "url": BASE},
    }
    features = "".join(f'<article class="card reveal" style="--i:{i % 4}"><div class="ico" aria-hidden="true">{e}</div>'
                       f'<h3>{esc(h)}</h3><p>{esc(p)}</p></article>' for i, (e, h, p) in enumerate(t["features"]))
    health_points = "".join(f"<li>{esc(p)}</li>" for p in t["health_points"])
    catalog_points = "".join(f"<li>{esc(p)}</li>" for p in t["catalog_points"])
    steps = "".join(f'<li class="card reveal" style="--i:{i}"><h3>{esc(h)}</h3><p>{esc(p)}</p></li>'
                    for i, (h, p) in enumerate(t["steps"]))
    guides = "".join(guide_card(g, lang, root, t, i) for i, g in enumerate(GUIDES))
    partners = "".join(f'<li class="reveal" style="--i:{i}"><b>{esc(h)}</b>{esc(p)}</li>'
                       for i, (h, p) in enumerate(t["partners"]))
    privacy_points = "".join(f"<li>{esc(p)}</li>" for p in t["privacy_points"])
    faq = "".join(f'<details class="reveal" style="--i:{i}"><summary>{esc(q)}</summary><p>{a}</p></details>'
                  for i, (q, a) in enumerate(t["faq"]))
    about = "".join(f"<p>{esc(p)}</p>" for p in t["about"])
    ll = t["legal_lang"]

    page = head(lang=lang, title=t["title"], desc=t["desc"], path=path, root=root, alternates=LANG_PATH,
                early=PASSPORT_REDIRECT if lang == "nl" else "",
                extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=True, paths=LANG_PATH)
    page += f"""<main id="main">

<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">{esc(t["eyebrow"])}</span>
<h1>{t["h1"]}</h1>
<p class="lead">{esc(t["lead"])}</p>
<div class="ctas"><a class="btn btn-primary" href="#features">{esc(t["cta"])}</a>
<a class="btn btn-ghost" href="{guides_href}">{esc(t["cta_guide"])}</a></div>
<p class="soon"><span class="dot" aria-hidden="true"></span><span>{t["soon"]}</span></p>
</div>
<div class="hero-phone">{phone_match(m)}</div>
</div></section>

<section id="features"><div class="wrap">
<div class="sec-head reveal"><span class="kicker">{esc(t["features_kicker"])}</span><h2>{esc(t["features_h2"])}</h2>
<p>{esc(t["features_lead"])}</p></div>
<div class="features">{features}</div>
</div></section>

<section><div class="wrap spot">
<div class="spot-media reveal">{phone_health(m)}</div>
<div class="reveal" style="--i:1"><span class="kicker">{esc(t["health_kicker"])}</span><h2>{esc(t["health_h2"])}</h2>
<p>{esc(t["health_text"])}</p><ul class="checks">{health_points}</ul></div>
</div></section>

<section><div class="wrap spot rev">
<div class="spot-media reveal">{phone_catalog(m, lang)}</div>
<div class="reveal" style="--i:1"><span class="kicker">{esc(t["catalog_kicker"])}</span><h2>{esc(t["catalog_h2"])}</h2>
<p>{esc(t["catalog_text"])}</p><ul class="checks">{catalog_points}</ul>
<a class="more-link" href="#partners">{esc(t["catalog_link"])}</a></div>
</div></section>

<section id="how"><div class="wrap">
<div class="sec-head reveal"><span class="kicker">{esc(t["how_kicker"])}</span><h2>{esc(t["how_h2"])}</h2></div>
<ol class="steps">{steps}</ol>
</div></section>

<section id="guides"><div class="wrap">
<div class="sec-head reveal"><span class="kicker">{esc(t["guides_kicker"])}</span><h2>{esc(t["guides_h2"])}</h2>
<p>{esc(t["guides_lead"])}</p></div>
<div class="guides">{guides}</div>
<p class="after"><a class="more-link" href="{guides_href}">{esc(t["guides_all"])}</a></p>
</div></section>

<section id="partners"><div class="wrap"><div class="panel">
<div class="sec-head reveal"><span class="kicker">{esc(t["partners_kicker"])}</span><h2>{esc(t["partners_h2"])}</h2>
<p>{esc(t["partners_lead"])}</p></div>
<ul class="points">{partners}</ul>
</div></div></section>

<section id="privacy"><div class="wrap split">
<div class="reveal"><span class="kicker">{esc(t["privacy_kicker"])}</span><h2>{esc(t["privacy_h2"])}</h2>
<p class="lead" style="font-size:17px">{esc(t["privacy_text"])}</p>
<a class="more-link" href="{root}privacy.html?lang={ll}">{esc(t["privacy_link"])} →</a></div>
<ul class="checks reveal" style="--i:1">{privacy_points}</ul>
</div></section>

<section id="faq"><div class="wrap">
<div class="sec-head reveal"><span class="kicker">{esc(t["faq_kicker"])}</span><h2>{esc(t["faq_h2"])}</h2></div>
<div class="faq">{faq}</div>
</div></section>

<section id="contact"><div class="wrap">
<div class="sec-head reveal"><span class="kicker">{esc(t["about_kicker"])}</span><h2>{esc(t["about_h2"])}</h2></div>
<div class="about">
<div class="card reveal">{about}</div>
<div class="card contact reveal" style="--i:1"><h3>{esc(t["contact_h3"])}</h3><p>{esc(t["contact_text"])}</p>
<a class="btn" href="mailto:{EMAIL}" aria-label="{esc(t["contact_btn"])}: {EMAIL}">{SVG_MAIL}<span>{EMAIL}</span></a></div>
</div>
</div></section>

</main>
"""
    page += footer(t=t, root=root, lang=lang, on_landing=True, paths=LANG_PATH)
    return page


# ── Гид ───────────────────────────────────────────────────────────────────────

def gids_index(lang):
    t, gt = T[lang], GIDS[lang]
    path = GUIDE_DIR[lang]
    root = root_of(path)
    page = head(lang=lang, title=gt["title"], desc=gt["desc"], path=path, root=root, alternates=GUIDE_DIR)
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=False, paths=GUIDE_DIR)
    cards = "".join(guide_card(g, lang, root, t, i) for i, g in enumerate(GUIDES))
    page += f"""<main id="main">
<div class="wrap page-head">
<nav class="crumbs" aria-label="{esc(gt["crumbs"])}"><a href="{rel(root, LANG_PATH[lang])}">{esc(gt["home"])}</a> / {esc(gt["kicker"])}</nav>
<span class="kicker">{esc(gt["kicker"])}</span>
<h1>{esc(gt["h1"])}</h1>
<p>{esc(gt["lead"])}</p>
</div>
<section style="padding-top:32px"><div class="wrap"><div class="guides">{cards}</div></div></section>
</main>
"""
    page += footer(t=t, root=root, lang=lang, on_landing=False, paths=GUIDE_DIR)
    return page


def article(g, lang):
    t, gt = T[lang], GIDS[lang]
    path = guide_path(g, lang)
    root = root_of(path)
    paths = {code: guide_path(g, code) for code in LANGS}
    title = g["title"][lang]
    ld = {
        "@context": "https://schema.org", "@type": "Article", "headline": title,
        "description": g["excerpt"][lang], "inLanguage": lang, "datePublished": UPDATED, "dateModified": UPDATED,
        "author": {"@type": "Organization", "name": "PaWow", "url": BASE},
        "publisher": {"@type": "Organization", "name": "PaWow",
                      "logo": {"@type": "ImageObject", "url": BASE + "assets/logo-512.png"}},
        "mainEntityOfPage": BASE + path,
    }
    page = head(lang=lang, title=f"{title} | PaWow", desc=g["excerpt"][lang], path=path, root=root, alternates=paths,
                extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=False, paths=paths)
    related = "".join(guide_card(o, lang, root, t, i) for i, o in enumerate(o for o in GUIDES if o is not g))
    page += f"""<main id="main">
<article class="article">
<nav class="crumbs" aria-label="{esc(gt["crumbs"])}"><a href="{rel(root, LANG_PATH[lang])}">{esc(gt["home"])}</a> / <a href="./">{esc(gt["kicker"])}</a></nav>
<h1>{esc(title)}</h1>
<div class="meta"><span>{g["minutes"]} {esc(t["min"])}</span><span><time datetime="{UPDATED}">{esc(gt["updated"])}</time></span>
<span>{esc(gt["by"])}</span></div>
{g["body"][lang]}
</article>
<aside class="related"><h2>{esc(gt["more"])}</h2><div class="guides">{related}</div></aside>
</main>
"""
    page += footer(t=t, root=root, lang=lang, on_landing=False, paths=paths)
    return page


def not_found():
    # 404 GitHub Pages отдаёт на любой глубине, поэтому пути абсолютные.
    root = "/pawmatch-passport/"
    t = T["nl"]
    page = head(lang="nl", title="Pagina niet gevonden | PaWow", desc=t["desc"], path="404.html", root=root,
                extra='<meta name="robots" content="noindex">\n')
    page += "<body>\n" + header(t=t, root=root, lang="nl", on_landing=False, paths=LANG_PATH)
    page += f"""<main id="main"><div class="center-page"><div>
<div style="font-size:64px" aria-hidden="true">🐾</div>
<h1 style="font-size:40px">Pagina niet gevonden</h1>
<p>Deze pagina bestaat niet (meer). <span lang="en">This page doesn't exist.</span></p>
<p><a class="btn btn-primary" href="{root}">Naar de homepage</a></p>
</div></div></main>
"""
    page += footer(t=t, root=root, lang="nl", on_landing=False, paths=LANG_PATH)
    return page


# ── Картинки ──────────────────────────────────────────────────────────────────

def images():
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    assets = ROOT / "assets"
    logo = Image.open(assets / "logo-512.png").convert("RGBA")

    def rounded(img, radius):
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), radius=radius, fill=255)
        out = img.copy()
        out.putalpha(mask)
        return out

    logo.resize((180, 180), Image.LANCZOS).convert("RGB").save(assets / "icon-180.png", optimize=True)
    logo.resize((128, 128), Image.LANCZOS).convert("RGB").save(assets / "logo-128.png", optimize=True)
    rounded(logo.resize((64, 64), Image.LANCZOS), 14).save(assets / "favicon-64.png", optimize=True)

    # Превью для ссылок (Open Graph), 1200×630.
    w, h = 1200, 630
    og = Image.new("RGB", (w, h), (251, 248, 250))
    # Пятна света: размытые эллипсы: у маски нулевые края, и квадрат слоя не виден.
    for (cx, cy, color) in ((260, 180, (255, 79, 139)), (1000, 140, (168, 85, 247)), (900, 620, (255, 79, 139))):
        glow = Image.new("L", (900, 900), 0)
        ImageDraw.Draw(glow).ellipse((200, 200, 700, 700), fill=70)
        glow = glow.filter(ImageFilter.GaussianBlur(110))
        layer = Image.new("RGB", (900, 900), color)
        og.paste(layer, (cx - 450, cy - 450), glow)
    big = rounded(logo.resize((240, 240), Image.LANCZOS), 56)
    og.paste(big, (110, (h - 240) // 2), big)

    def font(size, weight):
        try:
            f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
            f.set_variation_by_name(weight)
            return f
        except Exception:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)

    d = ImageDraw.Draw(og)
    x = 400
    d.text((x, 190), "PaWow", font=font(112, "Bold"), fill=(28, 28, 30))
    d.text((x, 330), "Alles voor je huisdier,", font=font(46, "Semibold"), fill=(93, 89, 101))
    d.text((x, 388), "in één app", font=font(46, "Semibold"), fill=(181, 23, 79))
    pill = "Nu in bèta voor iPhone"
    pf = font(26, "Semibold")
    tw = d.textlength(pill, font=pf)
    d.rounded_rectangle((x, 470, x + tw + 44, 470 + 48), radius=24, fill=(253, 232, 239))
    d.text((x + 22, 479), pill, font=pf, fill=(181, 23, 79))
    og.save(assets / "og.png", optimize=True)


# ── Сборка ────────────────────────────────────────────────────────────────────

# Неразрывный пробел после числа («7 дней») и, по-русски, после коротких
# предлогов и союзов («по ЕС», «в одном»): иначе они повисают в конце строки,
# особенно на узком экране. Теги, <script> и <style> не трогаем.
RU_SHORT = (r"(?<![\w-])(?:[вВкКсСуУоОиИаАяЯ]|на|На|не|Не|по|По|за|За|от|От|до|До|из|Из|во|Во|со|Со|"
            r"ко|Ко|об|Об|но|Но) (?=\S)")


def typo(page, lang):
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", page, flags=re.S)
    for i in range(0, len(parts), 2):
        text = re.sub(r"(\d) (?=\S)", "\\1" + NBSP, parts[i])
        text = text.replace("QR-", "QR\u2011")   # неразрывный дефис: «QR-» не отрывается от «кода»
        if lang == "ru":
            text = re.sub(RU_SHORT, lambda m: m.group(0)[:-1] + NBSP, text)
        parts[i] = text
    return "".join(parts)


def write(rel, content, lang="nl"):
    content = typo(content, lang)
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  {rel}  {len(content.encode()) // 1024} KB")


def main():
    for lang in LANGS:
        write(LANG_PATH[lang] + "index.html", landing(lang), lang)
        write(GUIDE_DIR[lang] + "index.html", gids_index(lang), lang)
        for g in GUIDES:
            write(guide_path(g, lang), article(g, lang), lang)
    write("404.html", not_found())
    images()
    print("  assets/*.png")


if __name__ == "__main__":
    main()
