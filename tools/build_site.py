#!/usr/bin/env python3
"""Собирает сайт PaWow для GitHub Pages.

    python3 tools/build_site.py

Пишет лендинг на трёх языках (index.html по-нидерландски: аудитория в NL и
проверка партнёрки bol; en/ и ru/), гид на тех же трёх языках (gids/,
en/guides/, ru/guides/; статьи лежат в site_guides.py), 404.html и картинки
в assets/ (нужен Pillow). Тексты правятся здесь и в site_guides.py,
сгенерированные html руками не трогать. Длинных тире в текстах нет.

passport.html (рендерер QR-ветпаспорта) и privacy/terms скрипт не трогает:
privacy и terms собирает docs/gen_legal.py в репозитории приложения.

Лендинг устроен как один день с собакой и кошкой (Houston и Appolon): у
каждой отметки времени фрагмент интерфейса приложения, собранный вёрсткой в
системе приложения (DESIGN.md приложения, «Тёплый спутник»).
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
NBSP = "\u00a0"   # неразрывный пробел; явной escape-последовательностью, чтобы не потерялся при правке

# Публичная ссылка TestFlight (testflight.apple.com/join/…). Пока её нет,
# кнопки беты на сайте нет вовсе, а честно сказано, что бета закрыта.
TESTFLIGHT_URL = None

# Подписка «сообщить о запуске» пишет прямо в Supabase (миграция 070).
# Ключ публикуемый: аноним с ним может только вставить строку в
# launch_signups и ничего не может прочитать.
SUPABASE_URL = "https://ltvgxpdcxejxhzemlamj.supabase.co"
SUPABASE_KEY = "sb_publishable_BkiC7nGdqI_XV7S3NWOWxA_hosVZRnN"


def esc(s):
    return html.escape(s, quote=True)


CURRENT = ' aria-current="true"'


# ── Иконки ────────────────────────────────────────────────────────────────────
# Простые символы в духе SF Symbols для плиток 44×44: один штрих, один вес.

def icon(paths, fill=False):
    attrs = 'fill="currentColor"' if fill else ('fill="none" stroke="currentColor" stroke-width="2" '
                                                 'stroke-linecap="round" stroke-linejoin="round"')
    return f'<svg viewBox="0 0 24 24" {attrs} aria-hidden="true">{paths}</svg>'


I_WALK = icon('<circle cx="13" cy="4.5" r="1.8"/><path d="M10 21l2.2-6.2L15 17v4"/><path d="M8 11.5l2.8-3.2 3.4 1 '
              '2.3 3.2"/><path d="M12.2 14.8l-1.4-6.5"/>')
I_BELL = icon('<path d="M6 16V11a6 6 0 1 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>')
I_SHIELD = icon('<path d="M12 3l7 3v5.5c0 4.4-3 8-7 9.5-4-1.5-7-5.1-7-9.5V6z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>')
I_DOC = icon('<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/><path d="M9.5 12h6M9.5 15.5h6"/>')
I_HEART = icon('<path d="M12 20.3l-1.4-1.3C5.6 14.6 3 12.2 3 8.9 3 6.2 5.1 4 7.7 4c1.6 0 3.2.8 4.3 2.1C13.1 4.8 '
               '14.7 4 16.3 4 18.9 4 21 6.2 21 8.9c0 3.3-2.6 5.7-7.6 10.1z"/>', fill=True)
I_HOUSE = icon('<path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>')
I_PIN = icon('<path d="M12 21s-6.5-6.2-6.5-11.3a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z"/><circle cx="12" cy="9.7" r="2.3"/>')
I_BAG = icon('<path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>')
I_SCISSORS = icon('<circle cx="6.5" cy="17" r="2.5"/><circle cx="17.5" cy="17" r="2.5"/><path d="M8.3 15.3L18 4M15.7 '
                  '15.3L6 4"/>')
I_PAW = icon('<circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="6" r="1.8"/><circle cx="15" cy="6.5" r="1.8"/>'
             '<circle cx="18" cy="10" r="1.8"/><path d="M12 12c-3 0-5.5 3.2-5.5 5.4 0 1.5 1.2 2.1 2.6 2.1 1.1 0 1.9-.6 '
             '2.9-.6s1.8.6 2.9.6c1.4 0 2.6-.6 2.6-2.1C17.5 15.2 15 12 12 12z"/>', fill=True)
I_CHEV_L = icon('<path d="M14.5 6l-6 6 6 6"/>')
I_CHEV_R = icon('<path d="M9.5 6l6 6-6 6"/>')
I_ARROW = icon('<path d="M5 12h13M13 6.5l5.5 5.5-5.5 5.5"/>')
I_LOCK = icon('<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>')
SVG_MAIL = icon('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7.5l8 6 8-6"/>')


def fake_qr(seed=11, n=25):
    """Узор «как QR» для иллюстрации. Не настоящий код: сканировать нечего.
    Настоящий QR владельца на сайт больше не попадает (в нём живая ссылка)."""
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
    return (f'<svg viewBox="0 0 {n} {n}" shape-rendering="crispEdges" aria-hidden="true">'
            f'<path fill="currentColor" d="{"".join(d)}"/></svg>')


# ── Тексты ────────────────────────────────────────────────────────────────────
#
# Главы дня: у каждой свой смысловой цвет приложения (мята здоровье,
# малиновый пары, синий клиники и места рядом). Отметки дня ссылаются на главу
# по ключу.

T = {
    "nl": {
        "title": "PaWow: het hele leven van je huisdier, in je broekzak",
        "desc": ("PaWow is een iPhone-app voor honden- en kattenbaasjes in Nederland: vaccinaties en een "
                 "QR-dierenpaspoort voor de dierenarts, facturen die declaraties worden, wandelmaatjes en matches, "
                 "asielen, rasverenigingen en diensten in de buurt."),
        "skip": "Naar de inhoud",
        "nav": [("gezondheid", "Gezondheid"), ("buren", "Buren"), ("buurt", "In de buurt")],
        "nav_guide": "Gids",
        "h1": "Het hele leven van je huisdier, in je broekzak",
        "lead": ("Gezondheid en papieren, buren en maatjes, asielen, trimsalons en voer om de hoek. Alles rond je hond "
                 "of kat, in één app."),
        "chapters": {"health": "Gezondheid en papieren", "buren": "Buren en maatjes", "buurt": "In de buurt"},
        "chapters_label": "Drie hoofdstukken",
        "beta_btn": "Probeer de bèta",
        "beta_hint": "Via TestFlight, de app van Apple voor testversies. Voor iPhone met iOS 17 of nieuwer.",
        "beta_closed": ("De bèta is nu besloten: we testen met een kleine groep baasjes. Laat je e-mailadres achter, dan "
                        "hoor je het als hij opengaat of als PaWow in de App Store staat."),
        "notify_h": "Laat het me weten bij de lancering",
        "notify_h_alt": "Liever wachten op de App Store?",
        "notify_label": "E-mailadres",
        "notify_ph": "jij@voorbeeld.nl",
        "notify_btn": "Aanmelden",
        "notify_consent": "Ik wil een e-mail als de bèta opengaat of PaWow in de App Store staat.",
        "notify_privacy": "Privacy",
        "notify_fine": "Alleen je e-mailadres en taal. Geen trackers.",
        "msg": {"sending": "Even geduld…", "ok": "Gelukt. We mailen je zodra het zover is.",
                "bad": "Dat e-mailadres lijkt niet te kloppen. Kijk het even na.",
                "busy": "Het is nu erg druk. Probeer het over een minuut opnieuw.",
                "offline": "Geen verbinding. Probeer het opnieuw als je weer online bent."},
        "day_h": "Een dinsdag met Houston en Appolon",
        "day_lead": ("Een voorbeelddag: dinsdag met jack russell Houston en maine coon Appolon. De schermen zijn "
                     "nagebouwd uit de app."),
        "weekday": "dinsdag",
        "moments": [
            {"id": "buren", "time": "07:30", "ch": "buren", "kind": "walk",
             "h": "Ochtendrondje met de buren",
             "p": ("Zie welke honden er nu in de buurt wandelen en loop samen een rondje. Je plek deel je alleen als "
                   "je zelf een wandeling start, en dan afgerond tot een huizenblok.")},
            {"id": "gezondheid", "time": "09:00", "ch": "health", "kind": "reminder",
             "h": "Een seintje voor Appolon",
             "p": "Ontwormen, vaccinaties, medicijnen: PaWow herinnert je op tijd, voor je kat net zo goed als voor je hond."},
            {"id": "", "time": "10:15", "ch": "health", "kind": "passport",
             "h": "De dierenarts scant het QR-paspoort",
             "p": ("Vaccinaties, chipnummer en eerdere bezoeken in de browser van de kliniek, zonder app. De link is "
                   "7 dagen geldig en je trekt hem in wanneer je wilt.")},
            {"id": "", "time": "14:00", "ch": "health", "kind": "invoice",
             "h": "Van factuur naar declaratie",
             "p": ("De kliniek stuurt de factuur via dezelfde link. Jij maakt er een concept-declaratie van voor je "
                   "verzekeraar, zonder overtypen.")},
            {"id": "buurt", "time": "17:30", "ch": "buurt", "kind": "nearby",
             "h": "Trimsalon, asiel of rasvereniging",
             "p": ("Dierenartsen en trimsalons op de kaart, met een aanvraag bij partnersalons. Asielen en "
                   "rasverenigingen met een link naar hun eigen pagina's, en voer en speelgoed van bol.")},
            {"id": "", "time": "21:00", "ch": "buren", "kind": "match",
             "h": "Een match voor Houston",
             "p": "Houston en Bonnie vinden elkaar leuk. Nu kunnen de baasjes chatten en een speelafspraak maken."},
        ],
        "m": {
            "walk_h": "3 honden wandelen nu", "walk_sub": "binnen 1 km",
            "walkers": [("molly", "Molly", "Samojeed", "400 m"), ("oscar", "Oscar", "Golden retriever", "650 m"),
                        ("toby", "Toby", "Beagle", "900 m")],
            "live": "Nu",
            "notif": [("Appolon: ontwormen vandaag", "Tik om af te vinken", "nu"),
                      ("Houston: herhaling Nobivac over 12 dagen", "Plan een afspraak bij je dierenarts", "8 min")],
            "pass_url": "pawmatch-passport/passport",
            "pass_h": "Dierenpaspoort van Houston", "pass_sub": "Jack Russell-terriër · Reu · Chip •••• 4127",
            "vacc": [("Cocktail (DHPPi)", "geldig tot mrt 2027"), ("Kennelhoest", "geldig tot jan 2027")],
            "badge_ok": "Geldig", "pass_until": "Link geldig tot ma 20 okt",
            "inv_h": "Factuur van de kliniek", "inv_sub": "Consult en vaccinatie · € 86,50",
            "claim_h": "Concept-declaratie", "claim_sub": "Klaar om naar je verzekeraar te sturen",
            "claim_badge": "Verzekerd",
            "near": [("79", "Asielen", "met een link naar hun eigen site"),
                     ("56", "Rasverenigingen", "van de Raad van Beheer"),
                     ("775", "Producten van bol", "ongeveer, elke 6 uur bijgewerkt")],
            "stats_note": "Partnerlinks: koop je via de catalogus, dan betaalt bol PaWow een kleine commissie.",
            "booking_h": "Aanvraag bij een trimsalon", "booking_sub": "do 10:30 · wassen en knippen",
            "booking_badge": "Bevestigd",
            "match_h": "Wederzijdse match", "match_sub": "Bonnie · Jack Russell-terriër",
            "chat": [("Zin in een rondje in het park morgen?", False), ("Graag! 18:00 bij de vijver?", True)],
        },
        "screens_h": "Zo ziet PaWow er echt uit",
        "prev": "Vorige schermen", "next": "Volgende schermen",
        "screens_lead": ("Echte schermen uit de bèta. Houston en Appolon zijn echte huisdieren; de profielen bij "
                         "Matchen zijn demoprofielen."),
        "shots": [("home", "Thuis: Houston in één oogopslag", "Homescherm van PaWow met Houston, een Jack Russell-terriër"),
                  ("health", "Gezondheid en verzekering, ook voor je kat",
                   "Gezondheid in PaWow voor Appolon, een Maine coon: vaccinaties, verzekering en het QR-dierenpaspoort"),
                  ("match", "Matchen in de buurt (demoprofiel)", "Matchen in PaWow: het demoprofiel van Bonnie"),
                  ("adopt", "Asielen bij jou in de buurt", "Lijst van asielen in PaWow met afstand en diersoorten")],
        "privacy_h": "Je gegevens blijven van jou",
        "privacy_points": [
            "Opgeslagen in datacenters in de EU.",
            "Medische gegevens zie alleen jij, en de dierenarts als jij een QR-link deelt.",
            "Anderen zien de locatie van je huisdier alleen afgerond.",
            "We verkopen je gegevens niet en gebruiken ze niet voor advertenties.",
            "Account verwijderen? Dan wissen we alles, ook je dieren en berichten.",
        ],
        "privacy_link": "Lees het volledige privacybeleid",
        "partners_h": "Hoe PaWow geld verdient",
        "partners_lead": ("Met partnerlinks, niet met jouw gegevens. Koop je iets via de catalogus, dan krijgt PaWow een "
                          "kleine commissie van bol. Jij betaalt niets extra."),
        "partners_more": "Meer over partnerlinks",
        "partners": [
            ("Partnerprogramma van bol", "PaWow neemt deel aan het partnerprogramma van bol. Producten en prijzen in de "
                                         "catalogus komen van bol, en ‘Kopen’ brengt je naar bol.com. PaWow is een "
                                         "onafhankelijke app en geen onderdeel van bol."),
            ("Je koopt bij de winkel", "We verkopen zelf niets. Bestellen, betalen, bezorgen en retourneren regel je met "
                                       "bol, onder hun voorwaarden."),
            ("De winkel is leidend", "Prijzen werken we elke 6 uur bij, maar de prijs op bol.com is altijd leidend."),
            ("Duidelijk gemarkeerd", "Partnerlinks zijn in de app als zodanig gemarkeerd, en we geven geen "
                                     "persoonsgegevens door aan de winkel."),
            ("Eerlijk advies", "Onze artikelen schrijven we zelf. Een commissie verandert niets aan wat we aanraden."),
        ],
        "guides_h": "Uit de gids",
        "guides_all": "Alle artikelen",
        "read": "Lees verder",
        "min": "min lezen",
        "faq_h": "Veelgestelde vragen",
        "faq": [
            ("Hoe kom ik in de bèta?",
             "De bèta loopt via TestFlight, de app van Apple voor testversies. Op dit moment is hij besloten. Meld je "
             "hierboven aan, dan mailen we je zodra je mee kunt doen of zodra PaWow in de App Store staat."),
            ("Is er een Android-versie?", "Nog niet: PaWow is er voorlopig alleen voor iPhone, met iOS 17 of nieuwer."),
            ("In welke talen is de app beschikbaar?", "In het Nederlands, Engels en Russisch. Je wisselt in de app zelf."),
            ("Voor welke dieren is PaWow?",
             "Voor honden, katten, vogels, konijnen en andere huisdieren. Samen wandelen is er alleen voor honden."),
            ("Wie kan de gegevens van mijn huisdier zien?",
             "Naam, ras en foto van je huisdier zien andere gebruikers bij het matchen, in de feed en op de wandelkaart. "
             "Medische gegevens, documenten en berichten zie alleen jij, plus degene met wie je chat of een QR-link deelt."),
            ("Verkoopt PaWow zelf producten?",
             'Nee. De catalogus verwijst naar bol; daar bestel en betaal je. Lees <a href="#partners">hoe '
             'partnerlinks werken</a>.'),
        ],
        "final_h": "Wees erbij als PaWow opengaat",
        "final_lead": "Eén e-mail als de bèta opengaat of PaWow in de App Store staat. Meer niet.",
        "legal_privacy": "Privacybeleid",
        "legal_terms": "Gebruiksvoorwaarden",
        "legal_lang": "nl",
        "foot_tag": "Het hele leven van je huisdier, in je broekzak",
        "foot_partner": "PaWow neemt deel aan het partnerprogramma van bol en is een onafhankelijke app.",
        "foot_cookies": "Deze website plaatst geen cookies en gebruikt geen trackers.",
        "foot_contact": "Vragen of samenwerken?",
        "cta_mini_h": "PaWow is in bèta",
        "cta_mini_p": "Alles van je hond of kat in één app. Laat je e-mailadres achter, dan hoor je het als je mee kunt doen.",
        "cta_mini_btn": "Laat het me weten",
    },
    "en": {
        "title": "PaWow: your pet's whole life, in your pocket",
        "desc": ("PaWow is an iPhone app for dog and cat owners in the Netherlands: vaccinations and a QR vet passport "
                 "for your vet, invoices that become insurance claims, walking buddies and matches, shelters, breed "
                 "clubs and services nearby."),
        "skip": "Skip to content",
        "nav": [("health", "Health"), ("neighbours", "Neighbours"), ("nearby", "Nearby")],
        "nav_guide": "Guides",
        "h1": "Your pet's whole life, in your pocket",
        "lead": ("Health and paperwork, neighbours and buddies, shelters, groomers and food nearby. Everything about "
                 "your dog or cat, in one app."),
        "chapters": {"health": "Health and paperwork", "buren": "Neighbours and buddies", "buurt": "Nearby"},
        "chapters_label": "Three chapters",
        "beta_btn": "Try the beta",
        "beta_hint": "Through TestFlight, Apple's app for test versions. For iPhone with iOS 17 or later.",
        "beta_closed": ("The beta is invite-only for now: we are testing with a small group of owners. Leave your email "
                        "and we will let you know when it opens or when PaWow is in the App Store."),
        "notify_h": "Tell me at launch",
        "notify_h_alt": "Rather wait for the App Store?",
        "notify_label": "Email address",
        "notify_ph": "you@example.com",
        "notify_btn": "Sign up",
        "notify_consent": "Email me when the beta opens or PaWow is in the App Store.",
        "notify_privacy": "Privacy",
        "notify_fine": "Only your email address and language. No trackers.",
        "msg": {"sending": "One moment…", "ok": "Done. We will email you when it is time.",
                "bad": "That email address does not look right. Please check it.",
                "busy": "It is very busy right now. Please try again in a minute.",
                "offline": "No connection. Please try again when you are back online."},
        "day_h": "A Tuesday with Houston and Appolon",
        "day_lead": ("An example day: a Tuesday with Houston the Jack Russell and Appolon the Maine Coon. The screens "
                     "are rebuilt from the app."),
        "weekday": "Tuesday",
        "moments": [
            {"id": "neighbours", "time": "07:30", "ch": "buren", "kind": "walk",
             "h": "A morning walk with the neighbours",
             "p": ("See which dogs are out walking nearby and join them. Your location is shared only when you start a "
                   "walk yourself, and then rounded to a city block.")},
            {"id": "health", "time": "09:00", "ch": "health", "kind": "reminder",
             "h": "A reminder for Appolon",
             "p": "Deworming, vaccinations, medication: PaWow reminds you in time, for your cat as much as your dog."},
            {"id": "", "time": "10:15", "ch": "health", "kind": "passport",
             "h": "The vet scans the QR passport",
             "p": ("Vaccinations, microchip number and past visits in the clinic's browser, no app needed. The link "
                   "works for 7 days and you can revoke it whenever you like.")},
            {"id": "", "time": "14:00", "ch": "health", "kind": "invoice",
             "h": "From invoice to claim",
             "p": ("The clinic sends the invoice through the same link. You turn it into a claim draft for your "
                   "insurer, without retyping anything.")},
            {"id": "nearby", "time": "17:30", "ch": "buurt", "kind": "nearby",
             "h": "Groomer, shelter or breed club",
             "p": ("Vets and groomers on the map, with booking requests to partner salons. Shelters and breed clubs "
                   "with a link to their own pages, plus food and toys from bol.")},
            {"id": "", "time": "21:00", "ch": "buren", "kind": "match",
             "h": "A match for Houston",
             "p": "Houston and Bonnie like each other. Now the owners can chat and set up a play date."},
        ],
        "m": {
            "walk_h": "3 dogs walking now", "walk_sub": "within 1 km",
            "walkers": [("molly", "Molly", "Samoyed", "400 m"), ("oscar", "Oscar", "Golden Retriever", "650 m"),
                        ("toby", "Toby", "Beagle", "900 m")],
            "live": "Now",
            "notif": [("Appolon: deworming today", "Tap to tick it off", "now"),
                      ("Houston: Nobivac booster in 12 days", "Book a vet appointment", "8 min")],
            "pass_url": "pawmatch-passport/passport",
            "pass_h": "Houston's pet passport", "pass_sub": "Jack Russell Terrier · Male · Chip •••• 4127",
            "vacc": [("DHPPi combination", "valid until Mar 2027"), ("Kennel cough", "valid until Jan 2027")],
            "badge_ok": "Valid", "pass_until": "Link valid until Mon 20 Oct",
            "inv_h": "Invoice from the clinic", "inv_sub": "Consultation and vaccination · €86.50",
            "claim_h": "Claim draft", "claim_sub": "Ready to send to your insurer",
            "claim_badge": "Insured",
            "near": [("79", "Shelters", "with a link to their own site"),
                     ("56", "Breed clubs", "from the Raad van Beheer"),
                     ("775", "Products from bol", "roughly, refreshed every 6 hours")],
            "stats_note": "Affiliate links: if you buy through the catalog, bol pays PaWow a small commission.",
            "booking_h": "Request at a groomer", "booking_sub": "Thu 10:30 · wash and trim",
            "booking_badge": "Confirmed",
            "match_h": "Mutual match", "match_sub": "Bonnie · Jack Russell Terrier",
            "chat": [("Fancy a walk in the park tomorrow?", False), ("Love to! 18:00 by the pond?", True)],
        },
        "screens_h": "What PaWow really looks like",
        "prev": "Previous screens", "next": "Next screens",
        "screens_lead": ("Real screens from the beta. Houston and Appolon are real pets; the profiles in Match are demo "
                         "profiles."),
        "shots": [("home", "Home: Houston at a glance", "PaWow home screen with Houston, a Jack Russell Terrier"),
                  ("health", "Health and insurance, for your cat too",
                   "Health in PaWow for Appolon, a Maine Coon: vaccinations, insurance and the QR vet passport"),
                  ("match", "Matching nearby (demo profile)", "Matching in PaWow: Bonnie's demo profile"),
                  ("adopt", "Shelters near you", "List of shelters in PaWow with distance and species")],
        "privacy_h": "Your data stays yours",
        "privacy_points": [
            "Stored in data centers in the EU.",
            "Medical records are visible only to you, and to the vet if you share a QR link.",
            "Others only see your pet's location rounded.",
            "We do not sell your data or use it for advertising.",
            "Delete your account and we erase everything, including your pets and messages.",
        ],
        "privacy_link": "Read the full privacy policy",
        "partners_h": "How PaWow makes money",
        "partners_lead": ("With affiliate links, not with your data. If you buy something through the catalog, bol pays "
                          "PaWow a small commission. You pay nothing extra."),
        "partners_more": "More about affiliate links",
        "partners": [
            ("bol affiliate program", "PaWow takes part in the bol affiliate program. Products and prices in the catalog "
                                      "come from bol, and ‘Buy’ takes you to bol.com. PaWow is an independent app and "
                                      "not part of bol."),
            ("You buy from the store", "We sell nothing ourselves. Ordering, paying, delivery and returns are between you "
                                       "and bol, under their terms."),
            ("The store's price counts", "We refresh prices every 6 hours, but the price on bol.com always applies."),
            ("Clearly labeled", "Affiliate links are labeled as such in the app, and we never pass personal data to the "
                                "store."),
            ("Honest advice", "We write our articles ourselves. A commission does not change what we recommend."),
        ],
        "guides_h": "From the guides",
        "guides_all": "All articles",
        "read": "Read more",
        "min": "min read",
        "faq_h": "Frequently asked questions",
        "faq": [
            ("How do I get into the beta?",
             "The beta runs on TestFlight, Apple's app for test versions. Right now it is invite-only. Sign up above and "
             "we will email you as soon as you can join or PaWow is in the App Store."),
            ("Is there an Android version?", "Not yet: for now PaWow is iPhone only, with iOS 17 or later."),
            ("Which languages does the app support?", "Dutch, English and Russian. You can switch inside the app."),
            ("Which animals is PaWow for?",
             "Dogs, cats, birds, rabbits and other pets. Walking together is for dogs only."),
            ("Who can see my pet's data?",
             "Other users see your pet's name, breed and photo in matching, the feed and on the walks map. Medical "
             "records, documents and messages are visible only to you, plus whoever you chat with or share a QR link with."),
            ("Does PaWow sell products itself?",
             'No. The catalog links to bol, where you order and pay. Read <a href="#partners">how affiliate links '
             'work</a>.'),
        ],
        "final_h": "Be there when PaWow opens",
        "final_lead": "One email when the beta opens or PaWow is in the App Store. Nothing more.",
        "legal_privacy": "Privacy policy",
        "legal_terms": "Terms of use",
        "legal_lang": "en",
        "foot_tag": "Your pet's whole life, in your pocket",
        "foot_partner": "PaWow takes part in the bol affiliate program and is an independent app.",
        "foot_cookies": "This website sets no cookies and uses no trackers.",
        "foot_contact": "Questions or partnerships?",
        "cta_mini_h": "PaWow is in beta",
        "cta_mini_p": "Everything about your dog or cat in one app. Leave your email and we will tell you when you can join.",
        "cta_mini_btn": "Tell me",
    },
    "ru": {
        "title": "PaWow: вся жизнь питомца в одном кармане",
        "desc": ("PaWow: приложение для iPhone для владельцев собак и кошек в Нидерландах. Прививки и QR-ветпаспорт "
                 "для врача, счета, которые становятся страховыми декларациями, соседи по прогулкам и пары, приюты, "
                 "клубы пород и услуги рядом."),
        "skip": "К содержимому",
        "nav": [("zdorovye", "Здоровье"), ("sosedi", "Соседи"), ("ryadom", "Рядом")],
        "nav_guide": "Гайды",
        "h1": "Вся жизнь питомца в одном кармане",
        "lead": ("Здоровье и бумаги, соседи и пары, приюты, груминг и корм рядом. Всё, что касается вашей собаки или "
                 "кошки, в одном приложении."),
        "chapters": {"health": "Здоровье и бумаги", "buren": "Соседи и пары", "buurt": "Рядом"},
        "chapters_label": "Три главы",
        "beta_btn": "Попробовать бету",
        "beta_hint": "Через TestFlight, приложение Apple для тестовых версий. Для iPhone с iOS 17 или новее.",
        "beta_closed": ("Бета сейчас закрытая: мы тестируем с небольшой группой владельцев. Оставьте email, и мы "
                        "напишем, когда она откроется или PaWow появится в App Store."),
        "notify_h": "Сообщить о запуске",
        "notify_h_alt": "Хотите дождаться App Store?",
        "notify_label": "Email",
        "notify_ph": "vy@primer.nl",
        "notify_btn": "Подписаться",
        "notify_consent": "Напишите мне, когда откроется бета или PaWow появится в App Store.",
        "notify_privacy": "Конфиденциальность",
        "notify_fine": "Только email и язык. Без трекеров.",
        "msg": {"sending": "Секунду…", "ok": "Готово. Напишем, когда придёт время.",
                "bad": "Похоже, в адресе ошибка. Проверьте его, пожалуйста.",
                "busy": "Сейчас слишком много подписок. Попробуйте через минуту.",
                "offline": "Нет соединения. Попробуйте ещё раз, когда появится интернет."},
        "day_h": "Вторник с Хьюстоном и Апполоном",
        "day_lead": ("Пример дня: вторник джек-рассела Хьюстона и мейн-куна Апполона. Экраны собраны по образцу "
                     "приложения."),
        "weekday": "вторник",
        "moments": [
            {"id": "sosedi", "time": "07:30", "ch": "buren", "kind": "walk",
             "h": "Утренняя прогулка с соседями",
             "p": ("Видно, какие собаки сейчас гуляют рядом, и можно пойти вместе. Ваше место видно, только если вы "
                   "сами начали прогулку, и то с точностью до квартала.")},
            {"id": "zdorovye", "time": "09:00", "ch": "health", "kind": "reminder",
             "h": "Напоминание для Апполона",
             "p": "Глистогонное, прививки, лекарства: PaWow напомнит вовремя, и про кошку, и про собаку."},
            {"id": "", "time": "10:15", "ch": "health", "kind": "passport",
             "h": "Врач сканирует QR-паспорт",
             "p": ("Прививки, номер чипа и прошлые визиты открываются в браузере клиники, без приложения. Ссылка "
                   "действует 7 дней, и её можно отозвать в любой момент.")},
            {"id": "", "time": "14:00", "ch": "health", "kind": "invoice",
             "h": "Счёт становится декларацией",
             "p": ("Клиника присылает счёт по той же ссылке. Вы делаете из него черновик декларации для страховой, "
                   "ничего не перепечатывая.")},
            {"id": "ryadom", "time": "17:30", "ch": "buurt", "kind": "nearby",
             "h": "Груминг, приют или клуб породы",
             "p": ("Ветклиники и салоны на карте, с заявкой в салоны-партнёры. Приюты и клубы пород со ссылками на "
                   "их сайты, а ещё корм и игрушки с bol.")},
            {"id": "", "time": "21:00", "ch": "buren", "kind": "match",
             "h": "Пара для Хьюстона",
             "p": "Хьюстон и Бонни понравились друг другу. Теперь хозяева могут списаться и договориться о встрече."},
        ],
        "m": {
            "walk_h": "3 собаки гуляют сейчас", "walk_sub": "в пределах 1 км",
            "walkers": [("molly", "Molly", "самоед", "400 м"), ("oscar", "Oscar", "золотистый ретривер", "650 м"),
                        ("toby", "Toby", "бигль", "900 м")],
            "live": "Сейчас",
            "notif": [("Апполон: глистогонное сегодня", "Нажмите, чтобы отметить", "сейчас"),
                      ("Хьюстон: ревакцинация Nobivac через 12 дней", "Запишитесь к ветеринару", "8 мин")],
            "pass_url": "pawmatch-passport/passport",
            "pass_h": "Ветпаспорт Хьюстона", "pass_sub": "Джек-рассел-терьер · Мальчик · Чип •••• 4127",
            "vacc": [("Комплексная (DHPPi)", "действует до мар. 2027"), ("Питомниковый кашель", "действует до янв. 2027")],
            "badge_ok": "Действует", "pass_until": "Ссылка до пн, 20 окт.",
            "inv_h": "Счёт от клиники", "inv_sub": "Приём и прививка · 86,50 €",
            "claim_h": "Черновик декларации", "claim_sub": "Можно отправить в страховую",
            "claim_badge": "Застрахован",
            "near": [("79", "Приютов", "со ссылкой на их сайт"),
                     ("56", "Клубов пород", "Raad van Beheer"),
                     ("775", "Товаров bol", "примерно, обновление каждые 6 часов")],
            "stats_note": "Ссылки партнёрские: если вы покупаете через каталог, bol платит PaWow небольшую комиссию.",
            "booking_h": "Заявка в салон", "booking_sub": "чт 10:30 · мытьё и стрижка",
            "booking_badge": "Подтверждено",
            "match_h": "Взаимное совпадение", "match_sub": "Bonnie · джек-рассел-терьер",
            "chat": [("Погуляем завтра в парке?", False), ("С удовольствием! В 18:00 у пруда?", True)],
        },
        "screens_h": "Как PaWow выглядит на самом деле",
        "prev": "Предыдущие экраны", "next": "Следующие экраны",
        "screens_lead": ("Настоящие экраны из беты. Хьюстон и Апполон настоящие питомцы; анкеты в «Матче» "
                         "демонстрационные."),
        "shots": [("home", "Главная: Хьюстон с одного взгляда", "Главный экран PaWow с Хьюстоном, джек-рассел-терьером"),
                  ("health", "Здоровье и страховка, и для кошки тоже",
                   "Здоровье в PaWow для Апполона, мейн-куна: прививки, страховка и QR-ветпаспорт"),
                  ("match", "Пары рядом (демо-анкета)", "Матч в PaWow: демо-анкета Бонни"),
                  ("adopt", "Приюты рядом с вами", "Список приютов в PaWow с расстоянием и видами животных")],
        "privacy_h": "Ваши данные остаются вашими",
        "privacy_points": [
            "Хранятся в дата-центрах в ЕС.",
            "Медицинские записи видите только вы, и врач, если вы поделились QR-ссылкой.",
            "Другие видят местоположение питомца только округлённо.",
            "Мы не продаём ваши данные и не используем их для рекламы.",
            "Удалите аккаунт, и мы сотрём всё, включая питомцев и переписку.",
        ],
        "privacy_link": "Политика конфиденциальности целиком",
        "partners_h": "Как PaWow зарабатывает",
        "partners_lead": ("На партнёрских ссылках, а не на ваших данных. Если вы покупаете что-то через каталог, bol "
                          "платит PaWow небольшую комиссию. Для вас цена та же."),
        "partners_more": "Подробнее о партнёрских ссылках",
        "partners": [
            ("Партнёрская программа bol", "PaWow участвует в партнёрской программе bol. Товары и цены в каталоге берутся "
                                          "у bol, а кнопка «Купить» ведёт на bol.com. PaWow независимое приложение и не "
                                          "часть bol."),
            ("Покупка в магазине", "Сами мы ничего не продаём. Заказ, оплата, доставка и возврат идут через bol, по их "
                                   "условиям."),
            ("Главная цена у магазина", "Цены мы обновляем каждые 6 часов, но действует всегда цена на bol.com."),
            ("Явная пометка", "Партнёрские ссылки в приложении помечены, и личные данные магазину мы не передаём."),
            ("Честные советы", "Статьи мы пишем сами. Комиссия не меняет того, что мы советуем."),
        ],
        "guides_h": "Из гайдов",
        "guides_all": "Все статьи",
        "read": "Читать",
        "min": "мин чтения",
        "faq_h": "Частые вопросы",
        "faq": [
            ("Как попасть в бету?",
             "Бета идёт через TestFlight, приложение Apple для тестовых версий. Сейчас она закрытая. Оставьте email "
             "выше, и мы напишем, как только вы сможете присоединиться или PaWow появится в App Store."),
            ("Есть ли версия для Android?", "Пока нет: сейчас PaWow только для iPhone с iOS 17 или новее."),
            ("На каких языках приложение?", "На нидерландском, английском и русском. Язык меняется прямо в приложении."),
            ("Для каких животных PaWow?",
             "Для собак, кошек, птиц, кроликов и других питомцев. Совместные прогулки только для собак."),
            ("Кто видит данные моего питомца?",
             "Кличку, породу и фото питомца другие пользователи видят в подборе пар, в ленте и на карте прогулок. "
             "Медицинские записи, документы и переписку видите только вы и тот, с кем вы переписываетесь или кому "
             "отправили QR-ссылку."),
            ("PaWow сам продаёт товары?",
             'Нет. Каталог ведёт на bol, там вы заказываете и платите. Читайте, <a href="#partners">как устроены '
             'партнёрские ссылки</a>.'),
        ],
        "final_h": "Узнайте первыми, когда PaWow откроется",
        "final_lead": "Одно письмо, когда откроется бета или PaWow появится в App Store. Больше ничего.",
        "legal_privacy": "Политика конфиденциальности",
        "legal_terms": "Условия использования",
        "legal_lang": "ru",
        "foot_tag": "Вся жизнь питомца в одном кармане",
        "foot_partner": "PaWow участвует в партнёрской программе bol и является независимым приложением.",
        "foot_cookies": "Сайт не ставит cookies и не использует трекеры.",
        "foot_contact": "Вопросы или сотрудничество?",
        "cta_mini_h": "PaWow в бете",
        "cta_mini_p": "Всё о собаке или кошке в одном приложении. Оставьте email, и мы напишем, когда можно будет присоединиться.",
        "cta_mini_btn": "Сообщить мне",
    },
}

# Цвет главы: класс на чипах и метках времени, значения в site.css.
# Малиновый в DESIGN.md значит «нажми», поэтому у глав его нет: соседи и пары
# сиренью, как бейдж «Ищет пару» в приложении.
CH_CLASS = {"health": "c-health", "buren": "c-buren", "buurt": "c-buurt"}


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


# Класс js на <html> ставится до стилей: без него (JS выключен) ничего не
# прячется под анимацию, и страница видна сразу целиком.
JS_FLAG = "<script>document.documentElement.classList.add('js')</script>\n"

# Один скрипт на все страницы. Движение один раз на элемент и только
# transform/opacity; при «уменьшить движение» всё сразу на месте.
SITE_SCRIPT = """<script>
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // День: часы крутят цифры к времени текущей отметки, фон «сейчас»
  // переходит на неё (opacity), маркер едет по линейке (transform), а
  // фрагмент интерфейса собирается, когда отметка показалась на экране.
  var day = document.querySelector('.day');
  if (day) {
    var moments = [].slice.call(day.querySelectorAll('.moment'));
    var marker = day.querySelector('.marker');
    var cols = [].slice.call(day.querySelectorAll('.clock .col'));
    var current = null;
    var place = function (m) {
      if (!marker) return;
      var t = m.querySelector('.m-time');
      // offsetTop отметки считается от списка, а маркер стоит в дорожке.
      // Над меткой времени, чтобы не закрывать цифры.
      var y = m.offsetTop + m.offsetParent.offsetTop + t.offsetTop - 20;
      marker.style.transform = 'translateY(' + y + 'px)';
    };
    var see = function (m) { m.classList.add('seen'); };
    var activate = function (m) {
      if (m === current) return;
      current = m;
      // Всё, что выше текущей отметки, тоже собрано: при быстрой прокрутке
      // пролистанный фрагмент не должен остаться пустым.
      var before = true;
      moments.forEach(function (o) {
        o.classList.toggle('is-now', o === m);
        if (before) see(o);
        if (o === m) before = false;
      });
      var d = m.dataset.time.replace(':', '').split('');
      cols.forEach(function (c, i) { c.style.setProperty('--n', d[i]); });
      place(m);
    };
    if (reduce || !hasIO) { moments.forEach(see); }
    else {
      day.classList.add('live');
      var vis = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { see(e.target); vis.unobserve(e.target); } });
      }, { threshold: 0.2 });
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) activate(e.target); });
      }, { rootMargin: '-42% 0px -42% 0px' });
      moments.forEach(function (m) { vis.observe(m); io.observe(m); });
      activate(moments[0]);
      window.addEventListener('resize', function () { if (current) place(current); });
    }
  }

  // Галерея настоящих экранов: кнопки листают ленту на одну карточку.
  var strip = document.getElementById('shots');
  document.querySelectorAll('.shots-nav .round').forEach(function (b) {
    b.addEventListener('click', function () {
      var card = strip.querySelector('.shot');
      var step = card ? card.getBoundingClientRect().width + 20 : 320;
      strip.scrollBy({ left: step * +b.dataset.dir, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  // Подписка «сообщить о запуске»: прямо в Supabase (только вставка).
  document.querySelectorAll('form.notify').forEach(function (f) {
    var status = f.querySelector('.status');
    var btn = f.querySelector('button');
    var msg = JSON.parse(f.dataset.msg);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.website.value) { f.classList.add('done'); status.textContent = msg.ok; return; }
      if (!f.checkValidity()) { f.reportValidity(); return; }
      btn.disabled = true;
      status.textContent = msg.sending;
      fetch('__API__/rest/v1/launch_signups', {
        method: 'POST',
        headers: { apikey: '__KEY__', 'Content-Type': 'application/json', Prefer: 'return=minimal' },
        body: JSON.stringify({ email: f.email.value.trim(), lang: f.dataset.lang, consent: true })
      }).then(function (r) {
        // 409: адрес уже в списке. Отвечаем так же, как на новый: по ответу
        // нельзя узнать, подписан ли чужой адрес.
        if (r.ok || r.status === 409) { f.classList.add('done'); status.textContent = msg.ok; return; }
        return r.json().catch(function () { return {}; }).then(function (j) {
          status.textContent = j && j.code === 'P0001' ? msg.busy : msg.bad;
          btn.disabled = false;
        });
      }).catch(function () { status.textContent = msg.offline; btn.disabled = false; });
    });
  });

  // Меню языка: открыто только одно, закрывается по клику мимо и по Esc.
  var menus = [].slice.call(document.querySelectorAll('.lang-menu'));
  menus.forEach(function (m) {
    m.addEventListener('toggle', function () { if (m.open) menus.forEach(function (o) { if (o !== m) o.open = false; }); });
  });
  document.addEventListener('click', function (e) {
    menus.forEach(function (m) { if (m.open && !m.contains(e.target)) m.open = false; });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    menus.forEach(function (m) { if (m.open) { m.open = false; m.querySelector('summary').focus(); } });
  });
})();
</script>
""".replace("__API__", SUPABASE_URL).replace("__KEY__", SUPABASE_KEY)


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
{alt}<meta name="theme-color" content="#f2f2f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
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


# Языки названиями: флаг обозначает страну, а не язык, и русский под флагом
# России отталкивал часть русскоязычных экспатов.
LANG_NAMES = {"nl": "Nederlands", "en": "English", "ru": "Русский"}
LANG_MENU_LABEL = {"nl": "Taal kiezen", "en": "Choose language", "ru": "Выбрать язык"}
CHEVRON = ('<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3" fill="none" '
           'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def lang_menu(root, lang, paths, up=False):
    """Выпадающий список языков. Без JS работает как обычный <details>;
    скрипт только закрывает его по клику мимо и по Esc. В подвале список
    раскрывается вверх (`up`), иначе уходил бы за край страницы."""
    items = "".join(
        f'<li><a href="{rel(root, paths[code])}" hreflang="{code}" lang="{code}"{CURRENT if code == lang else ""}>'
        f'{LANG_NAMES[code]}</a></li>'
        for code in LANGS
    )
    return (f'<details class="lang-menu{" up" if up else ""}">'
            f'<summary aria-label="{LANG_MENU_LABEL[lang]}: {LANG_NAMES[lang]}">{lang.upper()}{CHEVRON}</summary>'
            f'<ul>{items}</ul></details>')


def header(*, t, root, lang, on_landing, paths):
    home = rel(root, LANG_PATH[lang])
    pre = "" if on_landing else home
    links = [f'<a href="{pre}#{anchor}">{esc(label)}</a>' for anchor, label in t["nav"]]
    links.append(f'<a class="keep" href="{rel(root, GUIDE_DIR[lang])}">{esc(t["nav_guide"])}</a>')
    return f"""<a class="skip" href="#main">{esc(t["skip"])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{home}"><img src="{root}assets/logo-128.png" alt="" width="32" height="32">PaWow</a>
<nav class="nav" aria-label="Menu">{"".join(links)}</nav>
{lang_menu(root, lang, paths)}
</div></header>
"""


def footer(*, t, root, lang, on_landing, paths):
    home = rel(root, LANG_PATH[lang])
    pre = "" if on_landing else home
    ll = t["legal_lang"]
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-main">
<a class="brand" href="{home}"><img src="{root}assets/logo-128.png" alt="" width="28" height="28">PaWow</a>
<p>{esc(t["foot_tag"])}</p>
<p>{esc(t["foot_contact"])} <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div>
<nav class="foot-nav" aria-label="Footer">
<a href="{rel(root, GUIDE_DIR[lang])}">{esc(t["nav_guide"])}</a>
<a href="{pre}#partners">{esc(t["partners_h"])}</a>
<a href="{root}privacy.html?lang={ll}">{esc(t["legal_privacy"])}</a>
<a href="{root}terms.html?lang={ll}">{esc(t["legal_terms"])}</a>
</nav>
<div class="foot-lang">{lang_menu(root, lang, paths, up=True)}</div>
<div class="foot-fine">
<p>{esc(t["foot_partner"])} {esc(t["foot_cookies"])}</p>
<p>© 2026 PaWow</p>
</div>
</div></footer>
{SITE_SCRIPT}</body>
</html>
"""


def guide_path(g, lang):
    return GUIDE_DIR[lang] + g["slug"][lang] + ".html"


def guide_card(g, lang, root, t, i=0, level="h3"):
    """`level`: в индексе гида карточки идут сразу под h1, там они h2."""
    return (f'<a class="guide" href="{root}{guide_path(g, lang)}">'
            f'<{level}>{esc(g["title"][lang])}</{level}><p>{esc(g["excerpt"][lang])}</p>'
            f'<span class="guide-foot"><span class="go">{esc(t["read"])}{I_ARROW}</span>'
            f'<span class="meta">{g["minutes"]} {esc(t["min"])}</span></span></a>')


# ── Форма подписки ────────────────────────────────────────────────────────────

def notify_form(t, root, lang, fid):
    """Форма «сообщить о запуске». Без JS отправить её некуда (сайт
    статический), поэтому без JS она честно ведёт на почту."""
    ll = t["legal_lang"]
    msg = esc(json.dumps(t["msg"], ensure_ascii=False))
    return f"""<form class="notify" id="{fid}" data-lang="{lang}" data-msg="{msg}" action="mailto:{EMAIL}" method="post" novalidate>
<label class="field-label" for="{fid}-email">{esc(t["notify_label"])}</label>
<div class="field-row">
<input id="{fid}-email" name="email" type="email" inputmode="email" autocomplete="email" required maxlength="254" placeholder="{esc(t["notify_ph"])}">
<button class="btn btn-primary" type="submit">{esc(t["notify_btn"])}</button>
</div>
<label class="consent"><input type="checkbox" name="consent" required><span>{esc(t["notify_consent"])} <a href="{root}privacy.html?lang={ll}">{esc(t["notify_privacy"])}</a></span></label>
<input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
<p class="status" role="status" aria-live="polite"></p>
</form>"""


def action_card(t, root, lang, fid, final=False):
    if final:
        # В конце страницы заголовок и объяснение уже стоят рядом с карточкой.
        top = (f'<a class="btn btn-primary btn-wide" href="{esc(TESTFLIGHT_URL)}">{esc(t["beta_btn"])}</a><hr>'
               if TESTFLIGHT_URL else "")
        return f'<div class="act-card">{top}{notify_form(t, root, lang, fid)}<p class="fine">{I_LOCK}{esc(t["notify_fine"])}</p></div>'
    if TESTFLIGHT_URL:
        top = (f'<a class="btn btn-primary btn-wide" href="{esc(TESTFLIGHT_URL)}">{esc(t["beta_btn"])}</a>'
               f'<p class="hint">{esc(t["beta_hint"])}</p><hr>'
               f'<h2 class="act-h">{esc(t["notify_h_alt"])}</h2>')
    else:
        top = f'<h2 class="act-h">{esc(t["notify_h"])}</h2><p class="hint">{esc(t["beta_closed"])}</p>'
    return (f'<div class="act-card" id="aanmelden">{top}{notify_form(t, root, lang, fid)}'
            f'<p class="fine">{I_LOCK}{esc(t["notify_fine"])}</p></div>')


# ── Фрагменты интерфейса для отметок дня ──────────────────────────────────────
#
# Это вёрстка по образцу экранов приложения, а не скриншоты: она резкая на
# любом экране, переводится вместе со страницей и умеет собираться по частям.
# Классы u-* в site.css повторяют компоненты DESIGN.md приложения.

def row(icon_svg, tone, title, sub, badge="", badge_tone="", extra=""):
    b = f'<span class="badge {badge_tone}">{esc(badge)}</span>' if badge else ""
    return (f'<div class="u-row a"{extra}><span class="tile {tone}">{icon_svg}</span>'
            f'<span class="u-txt"><b>{esc(title)}</b><span>{esc(sub)}</span></span>{b}</div>')


def ui_walk(m):
    # Без loading="lazy": карточка прогулки стоит в первом экране.
    rows = "".join(
        f'<div class="u-row a" style="--d:{i + 1}"><img class="ava" src="__ROOT__assets/avatars/{f}.webp" alt="" '
        f'width="40" height="40" decoding="async">'
        f'<span class="u-txt"><b>{esc(n)}</b><span>{esc(b)}</span></span><span class="dist">{esc(d)}</span></div>'
        for i, (f, n, b, d) in enumerate(m["walkers"]))
    return (f'<div class="u-card">'
            f'<div class="u-head a"><span class="tile c-buren">{I_WALK}</span><span class="u-txt"><b>{esc(m["walk_h"])}</b>'
            f'<span>{esc(m["walk_sub"])}</span></span><span class="badge c-health">{esc(m["live"])}</span></div>'
            f'{rows}</div>')


def ui_reminder(m):
    notes = "".join(
        f'<div class="u-notif a" style="--d:{i}"><img src="__ROOT__assets/logo-128.png" alt="" width="38" height="38">'
        f'<span class="u-txt"><span class="n-top"><b>PaWow</b><span>{esc(w)}</span></span>'
        f'<b>{esc(h)}</b><span>{esc(s)}</span></span></div>'
        for i, (h, s, w) in enumerate(m["notif"]))
    return f'<div class="u-stack">{notes}</div>'


def ui_passport(m):
    vacc = "".join(row(I_SHIELD, "c-health", n, v, m["badge_ok"], "c-health", f' style="--d:{i + 2}"')
                   for i, (n, v) in enumerate(m["vacc"]))
    return (f'<div class="u-browser">'
            f'<div class="u-bar a"><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            f'<span class="url">{I_LOCK}{esc(m["pass_url"])}</span></div>'
            f'<div class="u-page"><div class="u-head a" style="--d:1"><span class="qr">{fake_qr()}</span>'
            f'<span class="u-txt"><b>{esc(m["pass_h"])}</b><span>{esc(m["pass_sub"])}</span></span></div>'
            f'{vacc}<p class="u-foot a" style="--d:4">{esc(m["pass_until"])}</p></div></div>')


def ui_invoice(m):
    invoice = row(I_DOC, "c-attn", m["inv_h"], m["inv_sub"])
    claim = row(I_SHIELD, "c-lilac", m["claim_h"], m["claim_sub"], m["claim_badge"], "c-lilac", ' style="--d:2"')
    return (f'<div class="u-flow"><div class="u-card">{invoice}</div>'
            f'<span class="u-arrow a" style="--d:1">{I_ARROW}</span>'
            f'<div class="u-card">{claim}</div></div>')


def ui_nearby(m):
    """Цифры строками списка, как в приложении: плитка, подпись, значение."""
    tones = (("c-health", I_HOUSE), ("c-lilac", I_PAW), ("c-neutral", I_BAG))
    rows = "".join(
        f'<div class="u-row a" style="--d:{i}"><span class="tile {tone}">{ico}</span>'
        f'<span class="u-txt"><b>{esc(label)}</b><span>{esc(sub)}</span></span><span class="val">{n}</span></div>'
        for i, ((n, label, sub), (tone, ico)) in enumerate(zip(m["near"], tones)))
    booking = row(I_SCISSORS, "c-neutral", m["booking_h"], m["booking_sub"], m["booking_badge"], "c-health",
                  ' style="--d:3"')
    return (f'<div class="u-near"><div class="u-card">{rows}</div><div class="u-card">{booking}</div>'
            f'<p class="u-note a" style="--d:4">{esc(m["stats_note"])}</p></div>')


def ui_match(m):
    bubbles = "".join(f'<p class="bubble a{" me" if me else ""}" style="--d:{i + 2}">{esc(txt)}</p>'
                      for i, (txt, me) in enumerate(m["chat"]))
    # Взаимное совпадение: тот фирменный момент, ради которого в DESIGN.md
    # держат градиент малинового в сирень.
    return (f'<div class="u-card">{row(I_HEART, "t-brand", m["match_h"], m["match_sub"])}'
            f'<div class="u-chat">{bubbles}</div></div>')


UI = {"walk": ui_walk, "reminder": ui_reminder, "passport": ui_passport, "invoice": ui_invoice,
      "nearby": ui_nearby, "match": ui_match}


def clock(time):
    """Часы дня: каждая цифра стоит в своей колонке с лентой 0-9, скрипт
    прокручивает ленту. Без JS видно первое время."""
    cols = []
    for ch in time:
        if ch == ":":
            cols.append('<span class="sep">:</span>')
        else:
            strip = "".join(f"<span>{d}</span>" for d in range(10))
            cols.append(f'<span class="col" style="--n:{ch}"><span class="strip">{strip}</span></span>')
    return "".join(cols)


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
    ll = t["legal_lang"]
    ld = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "PaWow",
        "operatingSystem": "iOS 17", "applicationCategory": "LifestyleApplication",
        "description": t["desc"], "url": BASE + path, "inLanguage": lang,
        "image": BASE + "assets/logo-512.png",
        "publisher": {"@type": "Organization", "name": "PaWow", "email": EMAIL, "url": BASE},
    }
    chapters = "".join(f'<li><a class="chip {CH_CLASS[k]}" href="#{next(mm["id"] for mm in t["moments"] if mm["ch"] == k)}">'
                       f'<i aria-hidden="true"></i>{esc(v)}</a></li>' for k, v in t["chapters"].items())
    moments = []
    for i, mo in enumerate(t["moments"]):
        mid = f' id="{mo["id"]}"' if mo["id"] else ""
        ui = UI[mo["kind"]](m).replace("__ROOT__", root)
        now = " is-now" if i == 0 else ""
        moments.append(
            f'<li class="moment{now}" data-time="{mo["time"]}"{mid}>'
            f'<time class="m-time {CH_CLASS[mo["ch"]]}" datetime="{mo["time"]}">{mo["time"]}</time>'
            f'<div class="m-text"><h3><span class="vh">{esc(t["chapters"][mo["ch"]])}: </span>{esc(mo["h"])}</h3>'
            f'<p>{esc(mo["p"])}</p></div>'
            f'<div class="m-ui u-{mo["kind"]}">{ui}</div></li>')
    shots = "".join(
        f'<figure class="shot"><div class="frame"><img{" class=\"fit\"" if s == "adopt" else ""} src="{root}assets/shots/{lang}-{s}.webp" '
        f'alt="{esc(alt)}" width="600" height="840" loading="lazy" decoding="async"></div><figcaption>{esc(cap)}</figcaption></figure>'
        for s, cap, alt in t["shots"])
    privacy = "".join(f"<li>{esc(p)}</li>" for p in t["privacy_points"])
    partners = "".join(f"<li><b>{esc(h)}</b> {esc(p)}</li>" for h, p in t["partners"])
    guides = "".join(guide_card(g, lang, root, t, i) for i, g in enumerate(GUIDES))
    faq = "".join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in t["faq"])

    page = head(lang=lang, title=t["title"], desc=t["desc"], path=path, root=root, alternates=LANG_PATH,
                early=PASSPORT_REDIRECT if lang == "nl" else "",
                extra=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=True, paths=LANG_PATH)
    page += f"""<main id="main">

<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<h1>{esc(t["h1"])}</h1>
<p class="lead">{esc(t["lead"])}</p>
</div>
{action_card(t, root, lang, "notify-top")}
</div></section>

<section class="day" aria-labelledby="day-h"><div class="wrap">
<h2 id="day-h" class="vh">{esc(t["day_h"])}</h2>
<div class="day-top"><ul class="chapters" aria-label="{esc(t["chapters_label"])}">{chapters}</ul>
<p class="day-note">{esc(t["day_lead"])}</p></div>
<div class="day-grid">
<div class="clock-wrap" aria-hidden="true"><div class="clock"><span class="digits">{clock(t["moments"][0]["time"])}</span>
<span class="weekday">{esc(t["weekday"])}</span></div></div>
<div class="track">
<span class="marker" aria-hidden="true"></span>
<ol class="moments">{"".join(moments)}</ol>
</div>
</div>
</div></section>

<section class="screens" aria-labelledby="screens-h"><div class="wrap">
<div class="sec-head sec-split"><div><h2 id="screens-h">{esc(t["screens_h"])}</h2><p>{esc(t["screens_lead"])}</p></div>
<div class="shots-nav"><button type="button" class="round" data-dir="-1" aria-label="{esc(t["prev"])}" aria-controls="shots">{I_CHEV_L}</button>
<button type="button" class="round" data-dir="1" aria-label="{esc(t["next"])}" aria-controls="shots">{I_CHEV_R}</button></div></div>
</div>
<div class="shots" id="shots" tabindex="0" role="region" aria-labelledby="screens-h">{shots}</div>
</section>

<section class="trust" id="privacy"><div class="wrap trust-grid">
<div class="card"><h2>{esc(t["privacy_h"])}</h2><ul class="checks">{privacy}</ul>
<a class="more" href="{root}privacy.html?lang={ll}">{esc(t["privacy_link"])}{I_ARROW}</a></div>
<div class="card" id="partners"><h2>{esc(t["partners_h"])}</h2><p>{esc(t["partners_lead"])}</p>
<details class="more-details"><summary>{esc(t["partners_more"])}</summary><ul class="plain">{partners}</ul></details></div>
</div></section>

<section class="guides-sec" aria-labelledby="guides-h"><div class="wrap">
<div class="sec-row"><h2 id="guides-h">{esc(t["guides_h"])}</h2><a class="more" href="{guides_href}">{esc(t["guides_all"])}{I_ARROW}</a></div>
<div class="guides">{guides}</div>
</div></section>

<section class="faq-sec" id="faq" aria-labelledby="faq-h"><div class="wrap faq-grid">
<h2 id="faq-h">{esc(t["faq_h"])}</h2>
<div class="faq">{faq}</div>
</div></section>

<section class="final" aria-labelledby="final-h"><div class="wrap final-grid">
<div class="final-copy"><h2 id="final-h">{esc(t["final_h"])}</h2><p>{esc(t["final_lead"])}</p></div>
{action_card(t, root, lang, "notify-end", final=True)}
</div></section>

</main>
"""
    page += footer(t=t, root=root, lang=lang, on_landing=True, paths=LANG_PATH)
    return page


# ── Гид ───────────────────────────────────────────────────────────────────────

def cta_mini(t, lang, root):
    """Конец статьи гида: совет из приложения раньше ничем не заканчивался."""
    href = rel(root, LANG_PATH[lang]) + "#aanmelden"
    return (f'<aside class="cta-mini"><img src="{root}assets/logo-128.png" alt="" width="48" height="48">'
            f'<div><h2>{esc(t["cta_mini_h"])}</h2><p>{esc(t["cta_mini_p"])}</p></div>'
            f'<a class="btn btn-primary" href="{href}">{esc(t["cta_mini_btn"])}</a></aside>')


def gids_index(lang):
    t, gt = T[lang], GIDS[lang]
    path = GUIDE_DIR[lang]
    root = root_of(path)
    page = head(lang=lang, title=gt["title"], desc=gt["desc"], path=path, root=root, alternates=GUIDE_DIR)
    page += "<body>\n" + header(t=t, root=root, lang=lang, on_landing=False, paths=GUIDE_DIR)
    cards = "".join(guide_card(g, lang, root, t, i, level="h2") for i, g in enumerate(GUIDES))
    page += f"""<main id="main">
<div class="wrap page-head">
<nav class="crumbs" aria-label="{esc(gt["crumbs"])}"><a href="{rel(root, LANG_PATH[lang])}">{esc(gt["home"])}</a> / {esc(gt["kicker"])}</nav>
<h1>{esc(gt["h1"])}</h1>
<p>{esc(gt["lead"])}</p>
</div>
<section class="guides-sec" aria-label="{esc(gt["h1"])}"><div class="wrap"><div class="guides">{cards}</div>
{cta_mini(t, lang, root)}</div></section>
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
{cta_mini(t, lang, root)}
</article>
<aside class="related wrap"><h2>{esc(gt["more"])}</h2><div class="guides">{related}</div></aside>
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
<img src="{root}assets/logo-128.png" alt="" width="72" height="72">
<h1>Pagina niet gevonden</h1>
<p>Deze pagina bestaat niet (meer). <span lang="en">This page doesn't exist.</span></p>
<p><a class="btn btn-primary" href="{root}">Naar de homepage</a></p>
</div></div></main>
"""
    page += footer(t=t, root=root, lang="nl", on_landing=False, paths=LANG_PATH)
    return page


# ── Картинки ──────────────────────────────────────────────────────────────────

def images():
    from PIL import Image, ImageDraw, ImageFont
    from PIL.PngImagePlugin import PngInfo

    assets = ROOT / "assets"
    logo = Image.open(assets / "logo-512.png").convert("RGBA")

    def origin(text):
        """Происхождение картинки внутри файла (чанк impeccable:prompt): ни одна
        из них не сгенерирована, все собраны здесь из логотипа владельца."""
        info = PngInfo()
        info.add_text("impeccable:prompt", f"Origin: {text} Built by tools/build_site.py; not AI-generated.")
        return info

    def rounded(img, radius):
        mask = Image.new("L", img.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), radius=radius, fill=255)
        out = img.copy()
        out.putalpha(mask)
        return out

    from_logo = "resized from assets/logo-512.png, the PaWow app logo (owner asset)."
    logo.resize((180, 180), Image.LANCZOS).convert("RGB").save(assets / "icon-180.png", optimize=True,
                                                               pnginfo=origin(from_logo))
    logo.resize((128, 128), Image.LANCZOS).convert("RGB").save(assets / "logo-128.png", optimize=True,
                                                               pnginfo=origin(from_logo))
    rounded(logo.resize((64, 64), Image.LANCZOS), 14).save(assets / "favicon-64.png", optimize=True,
                                                           pnginfo=origin(from_logo))

    # Превью для ссылок (Open Graph), 1200×630: холст и карточки приложения,
    # без пятен света и градиентов.
    w, h = 1200, 630
    og = Image.new("RGB", (w, h), (242, 242, 247))
    d = ImageDraw.Draw(og)

    def font(size, weight):
        try:
            f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", size)
            f.set_variation_by_name(weight)
            return f
        except Exception:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)

    big = rounded(logo.resize((112, 112), Image.LANCZOS), 26)
    og.paste(big, (90, 70), big)
    for i, line in enumerate(("Het hele leven", "van je huisdier,", "in je broekzak")):
        d.text((90, 214 + i * 66), line, font=font(60, "Bold"), fill=(28, 28, 30))
    d.text((90, 438), "Vaccinaties, QR-paspoort, matches en asielen.", font=font(28, "Regular"),
           fill=(92, 92, 97))
    pill = "Bèta voor iPhone"
    pf = font(26, "Semibold")
    tw = d.textlength(pill, font=pf)
    d.rounded_rectangle((90, 500, 90 + tw + 44, 548), radius=24, fill=(253, 232, 239))
    d.text((112, 509), pill, font=pf, fill=(181, 23, 79))
    # Справа три карточки-главы.
    # Цвета глав как на странице: мята, сирень, синий (малиновый только у действий).
    cards = [((29, 158, 117), "Gezondheid en papieren"), ((123, 104, 238), "Buren en maatjes"),
             ((0, 122, 255), "In de buurt")]
    for i, (color, label) in enumerate(cards):
        x0, y0 = 770, 150 + i * 118
        d.rounded_rectangle((x0, y0, x0 + 370, y0 + 96), radius=16, fill=(255, 255, 255))
        tint = tuple(int(c * .14 + 255 * .86) for c in color)
        d.rounded_rectangle((x0 + 22, y0 + 26, x0 + 66, y0 + 70), radius=12, fill=tint)
        d.ellipse((x0 + 37, y0 + 41, x0 + 51, y0 + 55), fill=color)
        d.text((x0 + 84, y0 + 34), label, font=font(23, "Semibold"), fill=(28, 28, 30))
    og.save(assets / "og.png", optimize=True,
            pnginfo=origin("Open Graph card drawn with Pillow: system canvas, the PaWow logo, headline text and "
                           "three chapter cards."))


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
        text = text.replace("QR-", "QR‑")   # неразрывный дефис: «QR-» не отрывается от «кода»
        if lang == "ru":
            text = re.sub(RU_SHORT, lambda m: m.group(0)[:-1] + NBSP, text)
        parts[i] = text
    return "".join(parts)


def write(rel_path, content, lang="nl"):
    content = typo(content, lang)
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  {rel_path}  {len(content.encode()) // 1024} KB")


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
