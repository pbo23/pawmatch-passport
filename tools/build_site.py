#!/usr/bin/env python3
"""Собирает сайт PaWow для GitHub Pages.

    python3 tools/build_site.py

Пишет index.html (нидерландский — основной язык сайта: аудитория в NL и
проверка партнёрки bol), en/index.html, ru/index.html, раздел gids/ (статьи
только по-нидерландски), 404.html и картинки в assets/ (нужен Pillow).
Тексты правятся здесь — сгенерированные html руками не трогать.

passport.html (рендерер QR-ветпаспорта) и privacy/terms скрипт не трогает.
"""
import html
import json
import random
from pathlib import Path

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
HREFLANG_NL = ' hreflang="nl"'


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
SVG_CHEVRON = ('<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
               'stroke-linejoin="round"><path d="M2.5 4.5L6 8l3.5-3.5"/></svg>')


def fake_qr(seed=11, n=25):
    """Узор «как QR» для макета. Не настоящий код — сканировать нечего."""
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
        "title": "PaWow – alles voor je huisdier, in één app",
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
            ("💞", "Matchen", "Vind speelmaatjes – of een partner – voor je hond of kat bij jou in de buurt. Filter op ras "
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
            "Herinneringen voor de volgende vaccinatie, controle of medicijnen – gewoon op je telefoon.",
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
            "Medische gegevens zie alleen jij – en de dierenarts, als jij een QR-link deelt.",
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
             "Medische gegevens, documenten en berichten zie alleen jij – en degene met wie je chat of een QR-link deelt."),
            ("Verkoopt PaWow zelf producten?",
             'Nee. De catalogus verwijst naar webwinkels; daar bestel en betaal je. Lees <a href="#partners">hoe '
             'partnerlinks werken</a>.'),
        ],
        "about_kicker": "Over ons",
        "about_h2": "Over PaWow",
        "about": [
            "PaWow is een onafhankelijke app voor huisdiereigenaren in Nederland. We bouwen hem stap voor stap, samen met "
            "de eerste gebruikers – elke reactie helpt.",
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
        "title": "PaWow – everything for your pet, in one app",
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
            ("💞", "Matching", "Find playmates – or a mate – for your dog or cat nearby. Filter by breed and distance, and "
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
            "Reminders for the next vaccination, check-up or medication – right on your phone.",
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
        "guides_lead": ("Practical articles we write ourselves – about the first weeks with a puppy, travelling with your "
                        "pet and the rules for walking your dog. The articles are in Dutch."),
        "guides_all": "All articles (in Dutch) →",
        "read": "Read (in Dutch) →",
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
            "Medical records are visible only to you – and to your vet, if you share a QR link.",
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
             "Medical records, documents and messages are visible only to you – and to whoever you chat with or share a "
             "QR link with."),
            ("Does PaWow sell products itself?",
             'No. The catalog links to web shops, where you order and pay. Read <a href="#partners">how affiliate links '
             'work</a>.'),
        ],
        "about_kicker": "About",
        "about_h2": "About PaWow",
        "about": [
            "PaWow is an independent app for pet owners in the Netherlands. We are building it step by step, together with "
            "our first users – every bit of feedback helps.",
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
        "title": "PaWow — всё для питомца в одном приложении",
        "desc": ("PaWow — приложение для iPhone для владельцев питомцев в Нидерландах: друзья и пара для питомца рядом, "
                 "прививки и визиты к ветеринару, QR-ветпаспорт для клиники, ветклиники и груминг-салоны поблизости."),
        "skip": "К содержимому",
        "nav": [("features", "Возможности"), ("how", "Как это работает"), ("partners", "Партнёрские ссылки"),
                ("contact", "Контакты")],
        "nav_guide": "Гайды",
        "eyebrow": "Бета-версия для iPhone",
        "h1": 'Всё для питомца — <span class="g">в одном приложении</span>',
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
                          "когда симпатия взаимна — чат с владельцем."),
            ("🩺", "Медкарта", "Прививки, препараты и визиты к ветеринару в одном месте, с напоминаниями на телефоне."),
            ("🔳", "QR-ветпаспорт", "Ветеринар сканирует QR-код и сразу видит прививки, номер чипа и прошлые визиты. По "
                                   "той же ссылке клиника может прислать счёт."),
            ("🐕", "Прогулки вместе", "Смотрите, какие собаки гуляют рядом прямо сейчас, и присоединяйтесь. Своё место "
                                     "вы показываете, только когда сами начинаете прогулку."),
            ("📸", "Лента", "Делитесь фото питомца и смотрите, что публикуют другие. Понравился профиль — поставьте лайк "
                           "прямо из ленты."),
            ("📍", "Услуги рядом", "Ветклиники, груминг-салоны и зоомагазины поблизости — на карте."),
            ("🛍️", "Каталог товаров", "Корм, игрушки и средства ухода из интернет-магазинов bol и Zooplus — с учётом "
                                     "вида питомца. Заказ — как обычно, на сайте магазина."),
            ("🏠", "Усыновление", "Животные из приютов поблизости, которые ищут дом."),
        ],
        "health_kicker": "Здоровье",
        "health_h2": "Ветпаспорт всегда под рукой",
        "health_text": ("Прививки, препараты, номер чипа и визиты к ветеринару: в PaWow всё в одном месте, даже если "
                        "бумажный паспорт остался дома в ящике стола."),
        "health_points": [
            "Напоминания о следующей прививке, осмотре или приёме препарата — прямо на телефоне.",
            "QR-ссылка для ветеринара: действует 7 дней, отозвать можно в любой момент.",
            "По той же ссылке клиника присылает счёт, и вы пересылаете его в страховую.",
        ],
        "catalog_kicker": "Каталог",
        "catalog_h2": "Всё нужное для питомца — без долгих поисков",
        "catalog_text": ("В каталоге собраны корм, игрушки, аксессуары и средства ухода из интернет-магазинов bol и "
                         "Zooplus — с учётом того, какой у вас питомец."),
        "catalog_points": [
            "Фильтр по виду: для собак, для кошек или всё.",
            "Цена, скидка и срок доставки сразу видны. Цены обновляются ежедневно.",
            "Заказ и оплата — на сайте магазина, с его сервисом и условиями возврата.",
        ],
        "catalog_link": "Как работают партнёрские ссылки →",
        "how_kicker": "Как это работает",
        "how_h2": "Три шага — и готово",
        "steps": [
            ("Создайте анкету", "Кличка, вид, порода, дата рождения и фото. Несколько питомцев? Переключение одним "
                               "касанием."),
            ("Наведите порядок в здоровье", "Добавьте прививки и визиты — PaWow напомнит, когда подойдёт срок."),
            ("Откройте свой район", "Матчи, компания для прогулок, ветклиники и груминг-салоны рядом."),
        ],
        "guides_kicker": "Гайды",
        "guides_h2": "Гайды для владельцев",
        "guides_lead": ("Практичные статьи, которые мы пишем сами: первые недели со щенком, поездки с питомцем и "
                        "правила выгула. Статьи на нидерландском."),
        "guides_all": "Все статьи (на нидерландском) →",
        "read": "Читать (на нидерландском) →",
        "min": "мин чтения",
        "partners_kicker": "Партнёрские ссылки",
        "partners_h2": "Честно о партнёрских ссылках",
        "partners_lead": "PaWow зарабатывает на партнёрских ссылках, а не на ваших данных. Как это устроено:",
        "partners": [
            ("Комиссия без наценки", "Если вы покупаете что-то по ссылке из нашего каталога, магазин платит PaWow "
                                     "небольшую комиссию. Для вас цена не меняется."),
            ("Покупка — в магазине", "Сами мы ничего не продаём. Заказ, оплата, доставка и возврат — у магазина, по "
                                     "его правилам."),
            ("Главная цена — у магазина", "Цены мы обновляем ежедневно, но решающая — цена на сайте магазина."),
            ("Чёткая пометка", "Партнёрские ссылки в приложении помечены, а ваши личные данные магазину мы не "
                               "передаём."),
            ("Честные советы", "Статьи мы пишем сами. Комиссия не влияет на то, что мы советуем."),
        ],
        "privacy_kicker": "Приватность",
        "privacy_h2": "Ваши данные остаются вашими",
        "privacy_text": "Мы храним только то, что нужно для работы приложения, а управляете ими вы.",
        "privacy_points": [
            "Хранятся в дата-центрах в ЕС.",
            "Медицинские записи видите только вы — и ветеринар, если вы поделились QR-ссылкой.",
            "Другим пользователям местоположение питомца показывается только округлённым.",
            "Мы не продаём данные и не используем их для рекламы.",
            "Удалите аккаунт — и мы сотрём всё, включая питомцев и переписку.",
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
             "Для собак, кошек, птиц, кроликов и других питомцев. Совместные прогулки — только для собак."),
            ("Кто видит данные моего питомца?",
             "Кличку, породу и фото питомца видят другие пользователи — в подборе пар, в ленте и на карте прогулок. "
             "Медицинские записи, документы и переписку видите только вы — и тот, с кем вы переписываетесь или кому "
             "отправили QR-ссылку."),
            ("PaWow сам продаёт товары?",
             'Нет. Каталог ведёт в интернет-магазины — заказ и оплата там. Подробнее — <a href="#partners">как работают '
             'партнёрские ссылки</a>.'),
        ],
        "about_kicker": "О нас",
        "about_h2": "О PaWow",
        "about": [
            "PaWow — независимое приложение для владельцев питомцев в Нидерландах. Мы делаем его шаг за шагом, вместе с "
            "первыми пользователями, — любой отзыв помогает.",
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


# ── Статьи (только нидерландский) ─────────────────────────────────────────────

RIJKSOVERHEID_CHIP = ("https://www.rijksoverheid.nl/onderwerpen/dierenwelzijn/vraag-en-antwoord/"
                      "moet-ik-mijn-hond-laten-chippen-en-registreren")
RIJKSOVERHEID_TRAVEL = ("https://www.rijksoverheid.nl/onderwerpen/dierenwelzijn/vraag-en-antwoord/"
                        "mag-mijn-kat-of-hond-mee-op-vakantie")
NVWA_EU = "https://www.nvwa.nl/onderwerpen/op-reis-met-mijn-huisdier/dier-mee-binnen-eu/hond-of-kat"
NVWA_ALL = "https://www.nvwa.nl/onderwerpen/op-reis-met-mijn-huisdier"

GUIDES = [
    {
        "slug": "puppy-in-huis", "emoji": "🐶", "minutes": 6,
        "title": {"nl": "Een pup in huis: de checklist voor de eerste weken",
                  "en": "A puppy at home: the checklist for the first weeks",
                  "ru": "Щенок дома: чек-лист на первые недели"},
        "excerpt": {"nl": "Welke spullen heb je nodig voordat je pup komt, en wat regel je in de eerste weken? Van bench "
                          "tot chipregistratie.",
                    "en": "What to get before your puppy arrives and what to arrange in the first weeks – from crate to "
                          "microchip registration.",
                    "ru": "Что купить до приезда щенка и что оформить в первые недели — от клетки-домика до регистрации "
                          "чипа."},
        "body": f"""
<p class="intro">Een pup ophalen is spannend, en de eerste dagen vliegen voorbij. Met deze lijst heb je de spullen klaar
voordat hij er is, en weet je wat je in de eerste weken moet regelen.</p>

<h2>Vóór de pup komt: de spullen</h2>
<h3>Een eigen plek: bench of mand</h3>
<p>Een bench geeft je pup een veilige plek om te slapen en tot rust te komen, en helpt bij de zindelijkheidstraining: een
hond plast niet graag waar hij slaapt. Kies een bench waarin je hond als volwassene kan staan, draaien en liggen; met een
tussenschot maak je hem kleiner zolang de pup nog klein is. Leg er een kussen of kleed in en zet hem op een rustige plek
waar je pup jullie wel kan zien.</p>
<h3>Voer- en drinkbak</h3>
<p>Kies bakken van rvs of keramiek: ze zijn stevig, kantelen minder snel en zijn makkelijk schoon te houden. Zet altijd
vers water klaar.</p>
<h3>Puppyvoer</h3>
<p>Vraag de fokker of het asiel welk voer je pup nu krijgt en houd dat de eerste weken aan: de verhuizing is al spannend
genoeg. Wil je overstappen, doe dat dan geleidelijk in ongeveer een week, door steeds iets meer nieuw voer door het oude
te mengen. Kies voer dat geschikt is voor pups en past bij het formaat dat je hond later krijgt.</p>
<h3>Halsband of tuigje, riem en penning</h3>
<p>Je pup groeit de eerste maanden hard, dus een licht en verstelbaar tuigje of halsbandje is handig. Een riem van 1,5 tot
2 meter werkt goed voor de dagelijkse rondjes. Hang een penning met je telefoonnummer aan de halsband.</p>
<h3>Speelgoed en kauwmateriaal</h3>
<p>Pups wisselen tussen ongeveer drie en zeven maanden hun tanden en willen dan op alles kauwen. Stevig kauwspeelgoed dat
bij hun formaat past, spaart je schoenen en stoelpoten. Wissel het speelgoed af, dan blijft het interessant.</p>
<h3>Handig om in huis te hebben</h3>
<ul>
<li>Poepzakjes, voor elk rondje.</li>
<li>Een reiniger met enzymen: die breekt de geur van een ongelukje echt af, zodat je pup niet terugkomt naar dezelfde
plek.</li>
<li>Kleine, zachte beloningssnoepjes voor de training.</li>
<li>Een borstel of kam die past bij de vacht van het ras.</li>
<li>Een kauwartikel of likmat voor de momenten dat je pup even alleen moet zijn.</li>
</ul>

<h2>Maak je huis puppy-proof</h2>
<p>Een pup ontdekt de wereld met zijn bek. Berg snoeren, schoenen, medicijnen en schoonmaakmiddelen op, en zet een hekje
voor de trap. Let ook op wat er binnen handbereik ligt: chocolade, druiven en rozijnen, ui en xylitol (een zoetstof in
onder meer suikervrije kauwgom) zijn giftig voor honden. Ook sommige kamer- en tuinplanten zijn giftig; zoek het op als je
twijfelt.</p>

<h2>De eerste weken: dit regel je</h2>
<h3>Chip en registratie op jouw naam</h3>
<p>In Nederland moet elke hond binnen 7 weken na de geboorte gechipt en geregistreerd zijn, dus je pup heeft al een chip
als je hem ophaalt. Hij hoort ook een Europees dierenpaspoort te hebben. Controleer bij het ophalen of het chipnummer in
het paspoort klopt. Daarna geef je online door dat jij de nieuwe eigenaar bent.</p>
<h3>Kennismaken met de dierenarts</h3>
<p>Plan in de eerste week of twee een eerste bezoek. De dierenarts controleert de gezondheid van je pup en bespreekt het
vaccinatieschema en het ontwormen. Vaak heeft je pup bij de fokker of het asiel al een eerste vaccinatie gehad; die staat
dan in het paspoort.</p>
<h3>Hondenbelasting</h3>
<p>Veel gemeenten heffen hondenbelasting. Hoeveel het is en hoe je je hond aanmeldt, verschilt per gemeente; je vindt het
op de site van je gemeente.</p>
<h3>Een verzekering overwegen</h3>
<p>Een behandeling bij de dierenarts kan flink in de papieren lopen. Bekijk of een dierenverzekering bij je past, en let
goed op wat er wel en niet onder valt, zoals erfelijke aandoeningen en het eigen risico.</p>
<h3>Puppycursus en socialisatie</h3>
<p>In de eerste levensmaanden went je pup het makkelijkst aan nieuwe mensen, dieren, geluiden en plekken. Laat hem rustig
en in kleine stapjes veel verschillende dingen meemaken. Een puppycursus helpt daarbij, en je leert er de basis: zit, af,
hier en netjes aan de lijn lopen.</p>
<h3>Zindelijk worden</h3>
<p>Breng je pup naar buiten na het wakker worden, na het eten, na het spelen en verder om de paar uur. Beloon hem meteen
als hij buiten plast. Gaat het binnen mis, ruim het dan op zonder boos te worden: straffen werkt averechts.</p>

<div class="tip"><p><b>Tip:</b> zet het chipnummer, de vaccinaties en de afspraken bij de dierenarts in PaWow. Dan heb je
alles bij de hand, ook als het paspoort thuis ligt, en krijg je een herinnering als de volgende vaccinatie eraan
komt.</p></div>

<p class="disclaimer">Dit artikel geeft algemene informatie en vervangt geen advies van je dierenarts. Regels rond chippen
en registreren: <a href="{RIJKSOVERHEID_CHIP}">Rijksoverheid</a>.</p>
""",
    },
    {
        "slug": "op-reis-met-huisdier", "emoji": "🧳", "minutes": 5,
        "title": {"nl": "Op reis met je hond of kat binnen de EU",
                  "en": "Travelling with your dog or cat in the EU",
                  "ru": "Поездка с собакой или кошкой по ЕС"},
        "excerpt": {"nl": "Chip, rabiësvaccinatie en dierenpaspoort: wat je nodig hebt, hoe lang van tevoren je begint en "
                          "welke landen extra eisen stellen.",
                    "en": "Microchip, rabies vaccination and pet passport: what you need, how early to start and which "
                          "countries ask for more.",
                    "ru": "Чип, прививка от бешенства и ветпаспорт: что нужно, за сколько начинать и какие страны "
                          "требуют больше."},
        "body": f"""
<p class="intro">Ga je met je hond of kat op vakantie in Europa? Binnen de EU gelden dezelfde basisregels voor huisdieren.
Begin wel op tijd: sommige stappen kosten minstens drie weken.</p>

<h2>De drie basisvoorwaarden</h2>
<h3>1. Een chip</h3>
<p>Je dier moet gechipt zijn vóór of op hetzelfde moment als de vaccinatie tegen rabiës (hondsdolheid). Een
rabiësvaccinatie die vóór het chippen is gegeven, telt voor reizen niet mee.</p>
<h3>2. Een geldige rabiësvaccinatie</h3>
<p>De eerste vaccinatie tegen rabiës mag vanaf een leeftijd van 12 weken. Daarna wacht je minstens 21 dagen voordat je met
je dier de grens over mag. Laat de vaccinatie op tijd herhalen: is hij eenmaal verlopen, dan telt de nieuwe prik weer als
eerste vaccinatie en begint de wachttijd opnieuw.</p>
<h3>3. Een Europees dierenpaspoort</h3>
<p>In het paspoort staan onder meer het chipnummer en de rabiësvaccinatie, ingevuld door de dierenarts. Neem het altijd mee
op reis: bij een controle moet je het kunnen laten zien.</p>

<h2>Extra eisen per land</h2>
<p>Reis je met je hond naar Ierland, Finland, Malta, Noorwegen of Noord-Ierland? Dan moet hij 1 tot 5 dagen (24 tot 120
uur) vóór aankomst door een dierenarts behandeld zijn tegen de lintworm <i>Echinococcus multilocularis</i>. De dierenarts
noteert de behandeling in het paspoort.</p>
<p>Voor landen buiten de EU gelden vaak andere regels, en ook voor de terugreis naar Nederland kunnen strengere eisen
gelden dan voor de heenreis. Kijk voor je bestemming op de site van de <a href="{NVWA_ALL}">NVWA</a>.</p>

<h2>Zo plan je het</h2>
<ol class="timeline">
<li><b>Een paar maanden vooraf</b>Check of de chip leesbaar is, of het paspoort compleet is en tot wanneer de
rabiësvaccinatie geldig is.</li>
<li><b>Minstens 21 dagen vooraf</b>De eerste rabiësvaccinatie, als je dier die nog niet heeft.</li>
<li><b>1 tot 5 dagen vóór aankomst</b>De lintwormbehandeling, als je bestemming die vraagt.</li>
<li><b>Bij vertrek</b>Paspoort, riem, water, voer- en drinkbak, poepzakjes, eventuele medicijnen en iets dat naar huis
ruikt.</li>
</ol>

<h2>Onderweg met de auto</h2>
<p>Vervoer je dier vastgezet: in een bench of met een autogordel voor honden. Plan elke twee tot drie uur een pauze om te
drinken, te plassen en de poten te strekken. Laat je dier nooit achter in een geparkeerde auto als het warm is: binnen een
paar minuten kan het daar levensgevaarlijk heet worden.</p>

<h2>Naar de dierenarts in het buitenland</h2>
<p>Moet je onderweg naar een dierenarts? Dan scheelt het veel als je de medische geschiedenis van je dier bij de hand
hebt.</p>
<div class="tip"><p><b>Tip:</b> met het QR-dierenpaspoort in PaWow laat je een dierenarts in het buitenland in een paar
seconden de vaccinaties, het chipnummer en eerdere bezoeken zien, in het Engels. Het officiële Europese dierenpaspoort
blijft wel verplicht.</p></div>

<p class="disclaimer">Dit artikel geeft algemene informatie; regels kunnen veranderen. Check vlak voor vertrek de actuele
eisen bij de <a href="{NVWA_EU}">NVWA</a> en de <a href="{RIJKSOVERHEID_TRAVEL}">Rijksoverheid</a>.</p>
""",
    },
    {
        "slug": "uitlaten-regels", "emoji": "🦮", "minutes": 4,
        "title": {"nl": "Uitlaten in Nederland: aanlijnen, opruimen en losloopgebieden",
                  "en": "Walking your dog in the Netherlands: leash rules, clean-up and off-leash areas",
                  "ru": "Прогулки с собакой в Нидерландах: поводок, уборка и зоны без поводка"},
        "excerpt": {"nl": "Waar mag je hond los en waar niet? Dat verschilt per gemeente. De belangrijkste regels, plus "
                          "tips voor warme dagen en donkere avonden.",
                    "en": "Where can your dog run free? Rules differ per municipality. The key ones, plus tips for hot "
                          "days and dark evenings.",
                    "ru": "Где собаке можно без поводка? Правила зависят от муниципалитета. Главное — и советы для жары "
                          "и тёмных вечеров."},
        "body": """
<p class="intro">Waar mag je hond los, en waar moet hij aan de lijn? In Nederland bepaalt vooral je gemeente dat. Dit zijn
de regels waar je in de praktijk mee te maken krijgt.</p>

<h2>Elke gemeente heeft eigen regels</h2>
<p>Gemeenten leggen hun hondenregels vast in de Algemene Plaatselijke Verordening (APV), vaak met een kaart van
uitlaatzones. Een veelvoorkomende regel is dat honden binnen de bebouwde kom aan de lijn moeten, behalve in aangewezen
losloopgebieden. Zoek op de site van je gemeente naar ‘honden’ of ‘hondenkaart’ voor wat er bij jou geldt.</p>

<h2>Opruimplicht</h2>
<p>In de meeste gemeenten moet je de poep van je hond opruimen, en vaak moet je ook een poepzakje bij je hebben. Wie dat
niet doet, riskeert een boete.</p>

<h2>Losloopgebieden</h2>
<p>In een losloopgebied mag je hond vrij rennen, zolang je hem onder appel hebt. Roep je hond bij je als er kinderen,
fietsers of andere honden aankomen, en ruim ook hier de poep op.</p>

<h2>Natuurgebieden en het broedseizoen</h2>
<p>In veel bossen en natuurgebieden moeten honden aan de lijn, vaak met aparte losloopgebieden. In het broedseizoen,
grofweg van half maart tot half juli, gelden op veel plekken strengere regels om vogels te beschermen die op de grond
broeden. Kijk op de borden bij de ingang of op de site van de beheerder, zoals Staatsbosbeheer of Natuurmonumenten.</p>

<h2>Op het strand</h2>
<p>Op veel stranden zijn honden in het zomerseizoen overdag niet of alleen aangelijnd welkom; buiten het seizoen mag vaak
meer. Ook dit verschilt per gemeente, en soms per strandopgang.</p>

<h2>Hondenbelasting</h2>
<p>Veel gemeenten heffen hondenbelasting, maar niet allemaal: een deel heeft hem afgeschaft. Meld je hond aan als jouw
gemeente die belasting heft.</p>

<h2>Wat neem je mee?</h2>
<ul>
<li>Een riem, ook in een losloopgebied: je weet nooit wanneer je hem nodig hebt.</li>
<li>Poepzakjes, genoeg voor het hele rondje.</li>
<li>Water en een opvouwbare drinkbak op warme dagen.</li>
<li>Beloningssnoepjes, om het terugkomen te oefenen.</li>
<li>In het donker: een lichtgevende halsband of een lampje, zodat je hond goed zichtbaar is.</li>
</ul>

<h2>Warm weer</h2>
<p>Asfalt en tegels kunnen in de zon zo heet worden dat je hond zijn voetzolen verbrandt. Leg je hand vijf seconden op de
grond: is het voor jou te heet, dan ook voor je hond. Wandel op warme dagen vroeg in de ochtend of ’s avonds, en kies
schaduw en gras.</p>

<div class="tip"><p><b>Tip:</b> met Wandelen in PaWow zie je welke honden er nu bij jou in de buurt lopen, zodat je samen
een rondje kunt doen. Je plek wordt alleen gedeeld als je zelf een wandeling start, afgerond tot ongeveer een huizenblok,
en verdwijnt na een uur vanzelf.</p></div>

<p class="disclaimer">Dit artikel geeft algemene informatie. De regels verschillen per gemeente en per natuurgebied; kijk
voor wat bij jou geldt op de site van je gemeente of van de terreinbeheerder.</p>
""",
    },
]

GIDS = {
    "title": "Gids voor baasjes – PaWow",
    "h1": "Gids voor baasjes",
    "lead": ("Praktische artikelen over het leven met je hond of kat in Nederland. We schrijven ze zelf en houden ze "
             "actueel."),
    "desc": ("Praktische artikelen voor hondenbaasjes en kattenmensen in Nederland: een pup in huis, op reis binnen de EU "
             "en de regels voor het uitlaten."),
    "updated": "Bijgewerkt op 14 oktober 2026",
    "by": "Door de redactie van PaWow",
    "more": "Meer uit de gids",
    "crumb_home": "Home",
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
    return f"""<div class="phone" aria-hidden="true"><div class="screen">{status_bar()}
<div class="scr"><div class="m-top"><span class="m-petchip"><span class="m-av">🐶</span>{esc(m["pet"])}{SVG_CHEVRON}</span></div>
<div class="m-chips">{chips}</div>
<div class="m-card"><span class="m-dist">➤ {esc(m["dist"])}</span><div class="m-photo">🐕</div>
<div class="m-info"><b>{esc(m["name"])}</b><span>{esc(m["age"])}</span><div>{esc(m["meta"])}</div><p>{esc(m["bio"])}</p></div></div>
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
<div class="h-qr"><div><b>{esc(m["qr_t"])}</b><span>{esc(m["qr_s"])}</span><em>{esc(m["qr_v"])}</em></div>{fake_qr()}</div>
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

def lang_href(lang, root):
    return (root + LANG_PATH[lang]) or "./"


def head(*, lang, title, desc, path, root, alternates=False, early="", extra=""):
    canonical = BASE + path
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{BASE + LANG_PATH[l]}">\n' for l in LANGS)
        alt += f'<link rel="alternate" hreflang="x-default" href="{BASE}">\n'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
{early}<meta name="viewport" content="width=device-width, initial-scale=1">
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


def header(*, t, root, lang, on_landing, langs):
    home = lang_href(lang, root)
    pre = "" if on_landing else home
    links = [f'<a href="{pre}#{anchor}">{esc(label)}</a>' for anchor, label in t["nav"][:2]]
    links.append(f'<a class="keep" href="{root}gids/">{esc(t["nav_guide"])}</a>')
    links += [f'<a href="{pre}#{anchor}">{esc(label)}</a>' for anchor, label in t["nav"][2:]]
    switch = "".join(
        f'<a href="{href}" hreflang="{code}" lang="{code}"{CURRENT if code == lang else ""}>'
        f'{code.upper()}</a>'
        for code, href in langs.items()
    )
    return f"""<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{home}"><img src="{root}assets/logo-128.png" alt="" width="34" height="34">PaWow</a>
<nav class="nav" aria-label="Menu">{"".join(links)}</nav>
<div class="langs" aria-label="Language">{switch}</div>
</div></header>
"""


def footer(*, t, root, lang, on_landing, langs):
    home = lang_href(lang, root)
    pre = "" if on_landing else home
    ll = t["legal_lang"]
    switch = "".join(
        f'<a href="{href}" hreflang="{code}" lang="{code}"{CURRENT if code == lang else ""}>'
        f'{code.upper()}</a>'
        for code, href in langs.items()
    )
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
<a href="{root}gids/">{esc(t["nav_guide"])}</a>
<a href="{pre}#partners">{esc(t["nav"][2][1])}</a>
<a href="{root}privacy.html?lang={ll}">{esc(t["legal_privacy"])}</a>
<a href="{root}terms.html?lang={ll}">{esc(t["legal_terms"])}</a>
</nav>
<div class="langs" style="margin-top:16px;display:inline-flex">{switch}</div>
</div>
</div></footer>
</body>
</html>
"""


def guide_card(g, lang, root, t):
    tag = '<span class="tag">NL</span>' if lang != "nl" else ""
    return (f'<a class="guide" href="{root}gids/{g["slug"]}.html"{HREFLANG_NL if lang != "nl" else ""}>'
            f'<div class="thumb" aria-hidden="true">{g["emoji"]}</div>'
            f'<div class="body"><div class="meta">{tag}<span>{g["minutes"]} {esc(t["min"])}</span></div>'
            f'<h3>{esc(g["title"][lang])}</h3><p>{esc(g["excerpt"][lang])}</p>'
            f'<span class="go">{esc(t["read"])}</span></div></a>')


# ── Лендинг ───────────────────────────────────────────────────────────────────

# Ссылки QR-ветпаспорта из приложения ведут на корень (`?id=…&lang=…`), и такие
# QR уже распечатаны и разосланы. Сама страница паспорта теперь passport.html —
# переадресация стоит первой в <head>, до загрузки стилей, чтобы врач не видел
# мелькнувший лендинг.
PASSPORT_REDIRECT = ("<script>if(new URLSearchParams(location.search).has('id'))"
                     "location.replace('passport.html'+location.search);</script>\n")


def landing(lang):
    t = T[lang]
    m = t["m"]
    root = "" if lang == "nl" else "../"
    langs = {code: lang_href(code, root) for code in LANGS}
    ld = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "PaWow",
        "operatingSystem": "iOS", "applicationCategory": "LifestyleApplication",
        "description": t["desc"], "url": BASE + LANG_PATH[lang], "inLanguage": lang,
        "image": BASE + "assets/logo-512.png",
        "publisher": {"@type": "Organization", "name": "PaWow", "email": EMAIL, "url": BASE},
    }
    features = "".join(f'<article class="card"><div class="ico" aria-hidden="true">{e}</div><h3>{esc(h)}</h3>'
                       f'<p>{esc(p)}</p></article>' for e, h, p in t["features"])
    health_points = "".join(f"<li>{esc(p)}</li>" for p in t["health_points"])
    catalog_points = "".join(f"<li>{esc(p)}</li>" for p in t["catalog_points"])
    steps = "".join(f'<li class="card"><h3>{esc(h)}</h3><p>{esc(p)}</p></li>' for h, p in t["steps"])
    guides = "".join(guide_card(g, lang, root, t) for g in GUIDES)
    partners = "".join(f"<li><b>{esc(h)}</b>{esc(p)}</li>" for h, p in t["partners"])
    privacy_points = "".join(f"<li>{esc(p)}</li>" for p in t["privacy_points"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in t["faq"])
    about = "".join(f"<p>{esc(p)}</p>" for p in t["about"])
    ll = t["legal_lang"]

    page = head(lang=lang, title=t["title"], desc=t["desc"], path=LANG_PATH[lang], root=root, alternates=True,
                early=PASSPORT_REDIRECT if lang == "nl" else "",
                extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=True, langs=langs)
    page += f"""<main id="main">

<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">{esc(t["eyebrow"])}</span>
<h1>{t["h1"]}</h1>
<p class="lead">{esc(t["lead"])}</p>
<div class="ctas"><a class="btn btn-primary" href="#features">{esc(t["cta"])}</a>
<a class="btn btn-ghost" href="{root}gids/">{esc(t["cta_guide"])}</a></div>
<p class="soon"><span class="dot" aria-hidden="true"></span><span>{t["soon"]}</span></p>
</div>
{phone_match(m)}
</div></section>

<section id="features"><div class="wrap">
<div class="sec-head"><span class="kicker">{esc(t["features_kicker"])}</span><h2>{esc(t["features_h2"])}</h2>
<p>{esc(t["features_lead"])}</p></div>
<div class="features">{features}</div>
</div></section>

<section><div class="wrap spot">
<div class="spot-media">{phone_health(m)}</div>
<div><span class="kicker">{esc(t["health_kicker"])}</span><h2>{esc(t["health_h2"])}</h2>
<p>{esc(t["health_text"])}</p><ul class="checks">{health_points}</ul></div>
</div></section>

<section><div class="wrap spot rev">
<div class="spot-media">{phone_catalog(m, lang)}</div>
<div><span class="kicker">{esc(t["catalog_kicker"])}</span><h2>{esc(t["catalog_h2"])}</h2>
<p>{esc(t["catalog_text"])}</p><ul class="checks">{catalog_points}</ul>
<a class="more-link" href="#partners">{esc(t["catalog_link"])}</a></div>
</div></section>

<section id="how"><div class="wrap">
<div class="sec-head"><span class="kicker">{esc(t["how_kicker"])}</span><h2>{esc(t["how_h2"])}</h2></div>
<ol class="steps">{steps}</ol>
</div></section>

<section id="guides"><div class="wrap">
<div class="sec-head"><span class="kicker">{esc(t["guides_kicker"])}</span><h2>{esc(t["guides_h2"])}</h2>
<p>{esc(t["guides_lead"])}</p></div>
<div class="guides">{guides}</div>
<p class="after"><a class="more-link" href="{root}gids/">{esc(t["guides_all"])}</a></p>
</div></section>

<section id="partners"><div class="wrap"><div class="panel">
<div class="sec-head"><span class="kicker">{esc(t["partners_kicker"])}</span><h2>{esc(t["partners_h2"])}</h2>
<p>{esc(t["partners_lead"])}</p></div>
<ul class="points">{partners}</ul>
</div></div></section>

<section id="privacy"><div class="wrap split">
<div><span class="kicker">{esc(t["privacy_kicker"])}</span><h2>{esc(t["privacy_h2"])}</h2>
<p class="lead" style="font-size:17px">{esc(t["privacy_text"])}</p>
<a class="more-link" href="{root}privacy.html?lang={ll}">{esc(t["privacy_link"])} →</a></div>
<ul class="checks">{privacy_points}</ul>
</div></section>

<section id="faq"><div class="wrap">
<div class="sec-head"><span class="kicker">{esc(t["faq_kicker"])}</span><h2>{esc(t["faq_h2"])}</h2></div>
<div class="faq">{faq}</div>
</div></section>

<section id="contact"><div class="wrap">
<div class="sec-head"><span class="kicker">{esc(t["about_kicker"])}</span><h2>{esc(t["about_h2"])}</h2></div>
<div class="about">
<div class="card">{about}</div>
<div class="card contact"><h3>{esc(t["contact_h3"])}</h3><p>{esc(t["contact_text"])}</p>
<a class="btn" href="mailto:{EMAIL}">{esc(t["contact_btn"])} · {EMAIL}</a></div>
</div>
</div></section>

</main>
"""
    page += footer(t=t, root=root, lang=lang, on_landing=True, langs=langs)
    return page


# ── Гид ───────────────────────────────────────────────────────────────────────

def gids_langs(root):
    # Статьи только на нидерландском: EN/RU ведут на лендинг своего языка.
    return {"nl": "./", "en": root + "en/", "ru": root + "ru/"}


def gids_index():
    t = T["nl"]
    root = "../"
    page = head(lang="nl", title=GIDS["title"], desc=GIDS["desc"], path="gids/", root=root)
    page += "<body>\n" + header(t=t, root=root, lang="nl", on_landing=False, langs=gids_langs(root))
    cards = "".join(guide_card(g, "nl", root, t) for g in GUIDES)
    page += f"""<main id="main">
<div class="wrap page-head">
<nav class="crumbs" aria-label="Kruimelpad"><a href="../">{GIDS["crumb_home"]}</a> / Gids</nav>
<span class="kicker">Gids</span>
<h1>{esc(GIDS["h1"])}</h1>
<p>{esc(GIDS["lead"])}</p>
</div>
<section style="padding-top:32px"><div class="wrap"><div class="guides">{cards}</div></div></section>
</main>
"""
    page += footer(t=t, root=root, lang="nl", on_landing=False, langs=gids_langs(root))
    return page


def article(g):
    t = T["nl"]
    root = "../"
    title = g["title"]["nl"]
    ld = {
        "@context": "https://schema.org", "@type": "Article", "headline": title,
        "description": g["excerpt"]["nl"], "inLanguage": "nl", "datePublished": UPDATED, "dateModified": UPDATED,
        "author": {"@type": "Organization", "name": "PaWow", "url": BASE},
        "publisher": {"@type": "Organization", "name": "PaWow",
                      "logo": {"@type": "ImageObject", "url": BASE + "assets/logo-512.png"}},
        "mainEntityOfPage": BASE + f"gids/{g['slug']}.html",
    }
    page = head(lang="nl", title=f"{title} – PaWow", desc=g["excerpt"]["nl"], path=f"gids/{g['slug']}.html", root=root,
                extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    page += "<body>\n" + header(t=t, root=root, lang="nl", on_landing=False, langs=gids_langs(root))
    related = "".join(guide_card(o, "nl", root, t) for o in GUIDES if o is not g)
    page += f"""<main id="main">
<article class="article">
<nav class="crumbs" aria-label="Kruimelpad"><a href="../">{GIDS["crumb_home"]}</a> / <a href="./">Gids</a></nav>
<h1>{esc(title)}</h1>
<div class="meta"><span>{g["minutes"]} {esc(t["min"])}</span><span><time datetime="{UPDATED}">{GIDS["updated"]}</time></span>
<span>{GIDS["by"]}</span></div>
{g["body"]}
</article>
<aside class="related"><h2>{GIDS["more"]}</h2><div class="guides">{related}</div></aside>
</main>
"""
    page += footer(t=t, root=root, lang="nl", on_landing=False, langs=gids_langs(root))
    return page


def not_found():
    # 404 GitHub Pages отдаёт на любой глубине — поэтому пути абсолютные.
    root = "/pawmatch-passport/"
    t = T["nl"]
    page = head(lang="nl", title="Pagina niet gevonden – PaWow", desc=t["desc"], path="404.html", root=root,
                extra='<meta name="robots" content="noindex">\n')
    page += "<body>\n" + header(t=t, root=root, lang="nl", on_landing=False,
                                langs={code: root + LANG_PATH[code] for code in LANGS})
    page += f"""<main id="main"><div class="center-page"><div>
<div style="font-size:64px" aria-hidden="true">🐾</div>
<h1 style="font-size:40px">Pagina niet gevonden</h1>
<p>Deze pagina bestaat niet (meer). <span lang="en">This page doesn't exist.</span></p>
<p><a class="btn btn-primary" href="{root}">Naar de homepage</a></p>
</div></div></main>
"""
    page += footer(t=t, root=root, lang="nl", on_landing=False, langs={code: root + LANG_PATH[code] for code in LANGS})
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
    # Пятна света — размытые эллипсы: у маски нулевые края, и квадрат слоя не виден.
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

def write(rel, content):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  {rel}  {len(content.encode()) // 1024} KB")


def main():
    for lang in LANGS:
        write("index.html" if lang == "nl" else f"{lang}/index.html", landing(lang))
    write("gids/index.html", gids_index())
    for g in GUIDES:
        write(f"gids/{g['slug']}.html", article(g))
    write("404.html", not_found())
    images()
    print("  assets/*.png")


if __name__ == "__main__":
    main()
