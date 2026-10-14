"""Статьи раздела «Гид» на трёх языках. Подключается из build_site.py.

Тексты пишутся без длинных тире (это правило сайта). Факты сверены с
rijksoverheid.nl и nvwa.nl (октябрь 2026); при правке сверять заново.
"""

# Где лежит гид в каждом языке. Нидерландские адреса не менять: они уже
# опубликованы и указаны в заявке bol.
GUIDE_DIR = {"nl": "gids/", "en": "en/guides/", "ru": "ru/guides/"}

RIJKSOVERHEID_CHIP = ("https://www.rijksoverheid.nl/onderwerpen/dierenwelzijn/vraag-en-antwoord/"
                      "moet-ik-mijn-hond-laten-chippen-en-registreren")
RIJKSOVERHEID_TRAVEL = ("https://www.rijksoverheid.nl/onderwerpen/dierenwelzijn/vraag-en-antwoord/"
                        "mag-mijn-kat-of-hond-mee-op-vakantie")
NVWA_EU = "https://www.nvwa.nl/onderwerpen/op-reis-met-mijn-huisdier/dier-mee-binnen-eu/hond-of-kat"
NVWA_ALL = "https://www.nvwa.nl/onderwerpen/op-reis-met-mijn-huisdier"

GIDS = {
    "nl": {
        "title": "Gids voor baasjes | PaWow",
        "h1": "Gids voor baasjes",
        "kicker": "Gids",
        "lead": ("Praktische artikelen over het leven met je hond of kat in Nederland. We schrijven ze zelf en houden "
                 "ze actueel."),
        "desc": ("Praktische artikelen voor hondenbaasjes en kattenmensen in Nederland: een pup in huis, op reis "
                 "binnen de EU en de regels voor het uitlaten."),
        "updated": "Bijgewerkt op 14 oktober 2026",
        "by": "Door de redactie van PaWow",
        "more": "Meer uit de gids",
        "home": "Home",
        "crumbs": "Kruimelpad",
    },
    "en": {
        "title": "Guides for pet owners | PaWow",
        "h1": "Guides for pet owners",
        "kicker": "Guides",
        "lead": ("Practical articles about life with your dog or cat in the Netherlands. We write them ourselves and "
                 "keep them up to date."),
        "desc": ("Practical articles for dog and cat owners in the Netherlands: a puppy at home, travelling in the EU "
                 "and the rules for walking your dog."),
        "updated": "Updated on 14 October 2026",
        "by": "By the PaWow editors",
        "more": "More guides",
        "home": "Home",
        "crumbs": "Breadcrumbs",
    },
    "ru": {
        "title": "Гайды для владельцев | PaWow",
        "h1": "Гайды для владельцев",
        "kicker": "Гайды",
        "lead": ("Практичные статьи о жизни с собакой или кошкой в Нидерландах. Мы пишем их сами и следим, чтобы они "
                 "оставались актуальными."),
        "desc": ("Практичные статьи для владельцев собак и кошек в Нидерландах: щенок дома, поездки по ЕС и правила "
                 "выгула."),
        "updated": "Обновлено 14 октября 2026",
        "by": "Редакция PaWow",
        "more": "Ещё гайды",
        "home": "Главная",
        "crumbs": "Навигация",
    },
}


# ── 1. Щенок дома ─────────────────────────────────────────────────────────────

PUPPY_NL = f"""
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
"""

PUPPY_EN = f"""
<p class="intro">Bringing a puppy home is exciting, and the first days fly by. With this list you will have everything
ready before your puppy arrives, and you will know what to arrange in the first weeks.</p>

<h2>Before your puppy arrives: the supplies</h2>
<h3>A place of their own: crate or bed</h3>
<p>A crate gives your puppy a safe place to sleep and settle down, and it helps with house training: dogs don't like to
pee where they sleep. Choose a crate in which your dog can stand, turn around and lie down as an adult; a divider makes it
smaller while your puppy is still small. Put a cushion or blanket inside and place it somewhere quiet where your puppy can
still see you.</p>
<h3>Food and water bowls</h3>
<p>Choose stainless steel or ceramic bowls: they are sturdy, don't tip over easily and are easy to keep clean. Always have
fresh water out.</p>
<h3>Puppy food</h3>
<p>Ask the breeder or shelter which food your puppy eats now and stick to it for the first weeks: the move is exciting
enough. If you want to switch, do it gradually over about a week, mixing a little more new food into the old each day.
Choose food made for puppies that suits the size your dog will grow to.</p>
<h3>Collar or harness, leash and ID tag</h3>
<p>Your puppy grows fast in the first months, so a light, adjustable harness or collar is handy. A leash of 1.5 to 2 metres
works well for daily walks. Attach a tag with your phone number to the collar.</p>
<h3>Toys and things to chew</h3>
<p>Puppies change their teeth between roughly three and seven months and then want to chew on everything. Sturdy chew toys
that suit their size will save your shoes and chair legs. Rotate the toys to keep them interesting.</p>
<h3>Handy to have at home</h3>
<ul>
<li>Poop bags, for every walk.</li>
<li>An enzyme cleaner: it really breaks down the smell of an accident, so your puppy doesn't return to the same spot.</li>
<li>Small, soft treats for training.</li>
<li>A brush or comb that suits the coat of the breed.</li>
<li>A chew or lick mat for the moments your puppy has to be alone for a while.</li>
</ul>

<h2>Puppy-proof your home</h2>
<p>A puppy explores the world with its mouth. Put away cables, shoes, medicines and cleaning products, and fit a gate at
the stairs. Also watch what is within reach: chocolate, grapes and raisins, onion and xylitol (a sweetener found in
sugar-free chewing gum, among other things) are toxic to dogs. Some house and garden plants are toxic too; look it up if
you are not sure.</p>

<h2>The first weeks: what to arrange</h2>
<h3>Microchip and registration in your name</h3>
<p>In the Netherlands every dog must be microchipped and registered within 7 weeks of birth, so your puppy will already
have a chip when you pick it up. It should also have a European pet passport. When you collect your puppy, check that the
chip number in the passport matches. Then report online that you are the new owner.</p>
<h3>Meet the vet</h3>
<p>Plan a first visit within the first week or two. The vet checks your puppy's health and discusses the vaccination
schedule and deworming. Often your puppy has already had a first vaccination at the breeder or shelter; it will then be
recorded in the passport.</p>
<h3>Dog tax</h3>
<p>Many municipalities charge a dog tax (hondenbelasting). How much it is and how you register your dog differs per
municipality; you will find it on your municipality's website.</p>
<h3>Consider insurance</h3>
<p>Vet treatment can get expensive. See whether pet insurance suits you, and check carefully what is and isn't covered,
such as hereditary conditions and the deductible.</p>
<h3>Puppy class and socialisation</h3>
<p>In the first months of life your puppy gets used to new people, animals, sounds and places most easily. Let it
experience lots of different things calmly and in small steps. A puppy class helps with this, and you will learn the
basics: sit, down, come and walking nicely on the leash.</p>
<h3>House training</h3>
<p>Take your puppy outside after waking up, after eating, after playing and otherwise every few hours. Reward it straight
away when it pees outside. If it goes wrong indoors, clean up without getting angry: punishment backfires.</p>

<div class="tip"><p><b>Tip:</b> add the chip number, vaccinations and vet appointments to PaWow. That way you have
everything at hand, even when the passport is at home, and you get a reminder when the next vaccination is due.</p></div>

<p class="disclaimer">This article gives general information and is not a substitute for advice from your vet. Rules on
microchipping and registration: <a href="{RIJKSOVERHEID_CHIP}" hreflang="nl">Rijksoverheid</a> (in Dutch).</p>
"""

PUPPY_RU = f"""
<p class="intro">Забрать щенка домой волнительно, а первые дни пролетают незаметно. С этим списком всё будет готово до
его приезда, и вы будете знать, что оформить в первые недели.</p>

<h2>До приезда щенка: что купить</h2>
<h3>Своё место: клетка-домик или лежанка</h3>
<p>Клетка-домик (бенч) даёт щенку безопасное место, где можно спать и успокоиться, и помогает приучить к туалету: собаки
не любят писать там, где спят. Выбирайте бенч, в котором взрослая собака сможет стоять, развернуться и лечь; перегородка
уменьшит его, пока щенок маленький. Положите внутрь подушку или плед и поставьте бенч в тихом месте, откуда щенку будет
видно вас.</p>
<h3>Миски для еды и воды</h3>
<p>Берите миски из нержавеющей стали или керамики: они устойчивые, реже опрокидываются и легко моются. Свежая вода должна
быть всегда.</p>
<h3>Корм для щенков</h3>
<p>Спросите у заводчика или в приюте, каким кормом щенка кормят сейчас, и не меняйте его первые недели: переезда и так
хватает. Если хотите перейти на другой корм, делайте это постепенно, примерно за неделю, каждый день подмешивая к старому
чуть больше нового. Выбирайте корм для щенков, подходящий под размер, до которого собака вырастет.</p>
<h3>Ошейник или шлейка, поводок и адресник</h3>
<p>В первые месяцы щенок быстро растёт, поэтому удобны лёгкие регулируемые шлейка или ошейник. Для ежедневных прогулок
хорошо подходит поводок длиной от 1,5 до 2 метров. Повесьте на ошейник адресник с вашим номером телефона.</p>
<h3>Игрушки и то, что можно грызть</h3>
<p>Примерно с трёх до семи месяцев у щенков меняются зубы, и в это время им хочется грызть всё подряд. Прочные жевательные
игрушки по размеру спасут ваши ботинки и ножки стульев. Чередуйте игрушки, чтобы они не надоедали.</p>
<h3>Что полезно иметь дома</h3>
<ul>
<li>Пакеты для уборки, на каждую прогулку.</li>
<li>Средство с ферментами: оно действительно разрушает запах после «происшествия», и щенок не возвращается на то же
место.</li>
<li>Маленькие мягкие лакомства для дрессировки.</li>
<li>Щётку или расчёску под шерсть вашей породы.</li>
<li>Жевательное лакомство или лизательный коврик на случай, когда щенку нужно побыть одному.</li>
</ul>

<h2>Подготовьте дом</h2>
<p>Щенок изучает мир ртом. Уберите провода, обувь, лекарства и бытовую химию, поставьте воротца на лестницу. Следите и за
тем, что лежит в зоне досягаемости: шоколад, виноград и изюм, лук и ксилит (подсластитель, который есть, например, в
жевательной резинке без сахара) ядовиты для собак. Некоторые комнатные и садовые растения тоже ядовиты; если сомневаетесь,
проверьте.</p>

<h2>Первые недели: что оформить</h2>
<h3>Чип и регистрация на ваше имя</h3>
<p>В Нидерландах каждую собаку нужно чипировать и зарегистрировать в течение 7 недель после рождения, так что чип у щенка
уже будет, когда вы его заберёте. У него также должен быть европейский ветпаспорт. Забирая щенка, проверьте, совпадает ли
номер чипа с паспортом. Затем сообщите онлайн, что теперь владелец вы.</p>
<h3>Знакомство с ветеринаром</h3>
<p>Запланируйте первый визит в течение первой или второй недели. Ветеринар осмотрит щенка и обсудит с вами график прививок
и обработку от глистов. Часто первую прививку щенку уже сделали у заводчика или в приюте; тогда она записана в
паспорте.</p>
<h3>Налог на собаку</h3>
<p>Во многих муниципалитетах есть налог на собаку (hondenbelasting). Сколько он стоит и как зарегистрировать собаку,
зависит от муниципалитета; это написано на его сайте.</p>
<h3>Подумайте о страховке</h3>
<p>Лечение у ветеринара может обойтись дорого. Посмотрите, нужна ли вам страховка для питомца, и внимательно проверьте, что
она покрывает, а что нет: например, наследственные заболевания и франшизу.</p>
<h3>Курсы для щенков и социализация</h3>
<p>В первые месяцы жизни щенок легче всего привыкает к новым людям, животным, звукам и местам. Давайте ему спокойно и
маленькими шагами знакомиться с самым разным. В этом помогут курсы для щенков, а заодно вы освоите основы: «сидеть»,
«лежать», «ко мне» и спокойная ходьба на поводке.</p>
<h3>Приучение к туалету</h3>
<p>Выводите щенка на улицу после сна, после еды, после игр и в остальное время каждые несколько часов. Сразу хвалите, когда
он сделал дела на улице. Если неудача случилась дома, уберите без ругани: наказание работает против вас.</p>

<div class="tip"><p><b>Совет:</b> внесите номер чипа, прививки и визиты к ветеринару в PaWow. Тогда всё будет под рукой,
даже если паспорт остался дома, а о следующей прививке придёт напоминание.</p></div>

<p class="disclaimer">Статья носит общий характер и не заменяет совет ветеринара. Правила чипирования и регистрации:
<a href="{RIJKSOVERHEID_CHIP}" hreflang="nl">Rijksoverheid</a> (на нидерландском).</p>
"""


# ── 2. Поездки по ЕС ──────────────────────────────────────────────────────────

TRAVEL_NL = f"""
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
"""

TRAVEL_EN = f"""
<p class="intro">Taking your dog or cat on holiday in Europe? Within the EU the same basic rules for pets apply. Do start in
time, though: some steps take at least three weeks.</p>

<h2>The three basic requirements</h2>
<h3>1. A microchip</h3>
<p>Your pet must be microchipped before or at the same time as the rabies vaccination. A rabies vaccination given before
the chip was implanted does not count for travel.</p>
<h3>2. A valid rabies vaccination</h3>
<p>The first rabies vaccination can be given from 12 weeks of age. After that you wait at least 21 days before you can
cross the border with your pet. Have the vaccination renewed in time: once it has expired, the new shot counts as a first
vaccination again and the waiting period starts over.</p>
<h3>3. A European pet passport</h3>
<p>The passport contains, among other things, the chip number and the rabies vaccination, filled in by the vet. Always take
it with you when you travel: you must be able to show it at a check.</p>

<h2>Extra requirements per country</h2>
<p>Travelling with your dog to Ireland, Finland, Malta, Norway or Northern Ireland? Then a vet must treat it against the
tapeworm <i>Echinococcus multilocularis</i> 1 to 5 days (24 to 120 hours) before arrival. The vet records the treatment
in the passport.</p>
<p>Countries outside the EU often have different rules, and the return trip to the Netherlands can have stricter
requirements than the outbound one. Check your destination on the website of the <a href="{NVWA_ALL}" hreflang="nl">NVWA</a>
(in Dutch).</p>

<h2>How to plan it</h2>
<ol class="timeline">
<li><b>A few months ahead</b>Check that the chip can be read, that the passport is complete and until when the rabies
vaccination is valid.</li>
<li><b>At least 21 days ahead</b>The first rabies vaccination, if your pet doesn't have one yet.</li>
<li><b>1 to 5 days before arrival</b>The tapeworm treatment, if your destination requires it.</li>
<li><b>When you leave</b>Passport, leash, water, food and water bowls, poop bags, any medication and something that
smells of home.</li>
</ol>

<h2>On the road by car</h2>
<p>Keep your pet secured: in a crate or with a dog seat belt. Plan a break every two to three hours to drink, pee and
stretch the legs. Never leave your pet in a parked car when it is warm: within minutes it can get dangerously hot
inside.</p>

<h2>Seeing a vet abroad</h2>
<p>Need a vet along the way? It helps a lot to have your pet's medical history at hand.</p>
<div class="tip"><p><b>Tip:</b> with the QR vet passport in PaWow you can show a vet abroad your pet's vaccinations, chip
number and past visits in seconds, in English. The official European pet passport is still required.</p></div>

<p class="disclaimer">This article gives general information; rules can change. Shortly before you leave, check the
current requirements with the <a href="{NVWA_EU}" hreflang="nl">NVWA</a> and the
<a href="{RIJKSOVERHEID_TRAVEL}" hreflang="nl">Rijksoverheid</a> (both in Dutch).</p>
"""

TRAVEL_RU = f"""
<p class="intro">Собираетесь в отпуск по Европе с собакой или кошкой? Внутри ЕС для питомцев действуют одни и те же
базовые правила. Но начинайте заранее: некоторые шаги занимают не меньше трёх недель.</p>

<h2>Три базовых условия</h2>
<h3>1. Чип</h3>
<p>Питомца нужно чипировать до прививки от бешенства или одновременно с ней. Прививка от бешенства, сделанная до
чипирования, для поездок не засчитывается.</p>
<h3>2. Действующая прививка от бешенства</h3>
<p>Первую прививку от бешенства можно делать с 12 недель. После неё нужно подождать не меньше 21 дня, прежде чем
пересекать границу с питомцем. Ревакцинируйте вовремя: если срок прививки истёк, новая снова считается первой, и
ожидание начинается заново.</p>
<h3>3. Европейский ветпаспорт</h3>
<p>В паспорте, среди прочего, указаны номер чипа и прививка от бешенства; их вписывает ветеринар. Всегда берите паспорт в
поездку: при проверке его нужно предъявить.</p>

<h2>Дополнительные требования стран</h2>
<p>Едете с собакой в Ирландию, Финляндию, на Мальту, в Норвегию или Северную Ирландию? Тогда за срок от 1 до 5 дней (от
24 до 120 часов) до прибытия ветеринар должен обработать её от ленточного червя <i>Echinococcus multilocularis</i>.
Обработку он отмечает в паспорте.</p>
<p>Для стран за пределами ЕС правила часто другие, а при возвращении в Нидерланды требования могут быть строже, чем при
выезде. Правила для своей страны назначения смотрите на сайте <a href="{NVWA_ALL}" hreflang="nl">NVWA</a> (на
нидерландском).</p>

<h2>Как спланировать</h2>
<ol class="timeline">
<li><b>За несколько месяцев</b>Проверьте, читается ли чип, заполнен ли паспорт и до какого числа действует прививка от
бешенства.</li>
<li><b>Минимум за 21 день</b>Первая прививка от бешенства, если её ещё нет.</li>
<li><b>За срок от 1 до 5 дней до прибытия</b>Обработка от ленточного червя, если её требует страна назначения.</li>
<li><b>Перед выездом</b>Паспорт, поводок, вода, миски, пакеты для уборки, лекарства, если нужны, и что-нибудь, что пахнет
домом.</li>
</ol>

<h2>В дороге на машине</h2>
<p>Перевозите питомца зафиксированным: в переноске или с автомобильным ремнём для собак. Делайте остановку каждые два-три
часа, чтобы попить, сходить в туалет и размять лапы. Никогда не оставляйте питомца в припаркованной машине в тёплую
погоду: за несколько минут там может стать смертельно жарко.</p>

<h2>Ветеринар за границей</h2>
<p>Понадобился ветеринар в пути? Очень помогает, если медицинская история питомца под рукой.</p>
<div class="tip"><p><b>Совет:</b> с QR-ветпаспортом в PaWow вы за пару секунд покажете ветеринару за границей прививки,
номер чипа и прошлые визиты, на английском. Официальный европейский ветпаспорт при этом всё равно обязателен.</p></div>

<p class="disclaimer">Статья носит общий характер; правила могут меняться. Незадолго до поездки проверьте актуальные
требования на сайтах <a href="{NVWA_EU}" hreflang="nl">NVWA</a> и <a href="{RIJKSOVERHEID_TRAVEL}" hreflang="nl">Rijksoverheid</a>
(на нидерландском).</p>
"""


# ── 3. Выгул ──────────────────────────────────────────────────────────────────

WALKS_NL = """
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
"""

WALKS_EN = """
<p class="intro">Where can your dog run free, and where does it have to be on a leash? In the Netherlands that is mostly up
to your municipality. These are the rules you will run into in practice.</p>

<h2>Every municipality has its own rules</h2>
<p>Municipalities set out their dog rules in the local by-laws (Algemene Plaatselijke Verordening, APV), often with a map
of dog zones. A common rule is that dogs must be on a leash in built-up areas, except in designated off-leash areas.
Search your municipality's website for ‘honden’ or ‘hondenkaart’ to see what applies where you live.</p>

<h2>Clean-up duty</h2>
<p>In most municipalities you have to pick up after your dog, and often you must also carry a poop bag. If you don't, you
risk a fine.</p>

<h2>Off-leash areas</h2>
<p>In an off-leash area your dog may run free, as long as it comes when called. Call your dog to you when children,
cyclists or other dogs approach, and pick up after it here too.</p>

<h2>Nature areas and the breeding season</h2>
<p>In many woods and nature areas dogs must be on a leash, often with separate off-leash zones. During the breeding season,
roughly from mid-March to mid-July, stricter rules apply in many places to protect birds that nest on the ground. Check
the signs at the entrance or the website of the site manager, such as Staatsbosbeheer or Natuurmonumenten.</p>

<h2>On the beach</h2>
<p>On many beaches dogs are not welcome during the day in the summer season, or only on a leash; outside the season more is
often allowed. This also differs per municipality, and sometimes per beach entrance.</p>

<h2>Dog tax</h2>
<p>Many municipalities charge a dog tax, but not all of them: some have abolished it. Register your dog if your
municipality charges the tax.</p>

<h2>What to bring</h2>
<ul>
<li>A leash, even in an off-leash area: you never know when you will need it.</li>
<li>Poop bags, enough for the whole walk.</li>
<li>Water and a collapsible bowl on warm days.</li>
<li>Treats, to practise recall.</li>
<li>In the dark: a light-up collar or a small lamp, so your dog is clearly visible.</li>
</ul>

<h2>Hot weather</h2>
<p>Asphalt and paving can get so hot in the sun that your dog burns its paw pads. Put your hand on the ground for five
seconds: if it is too hot for you, it is too hot for your dog. On warm days walk early in the morning or in the evening,
and choose shade and grass.</p>

<div class="tip"><p><b>Tip:</b> with Walks in PaWow you see which dogs are out walking near you right now, so you can go
for a walk together. Your location is only shared when you start a walk yourself, rounded to roughly a city block, and it
disappears on its own after an hour.</p></div>

<p class="disclaimer">This article gives general information. The rules differ per municipality and per nature area; check
what applies to you on the website of your municipality or the site manager.</p>
"""

WALKS_RU = """
<p class="intro">Где собаке можно бегать без поводка, а где нельзя? В Нидерландах это в основном решает ваш
муниципалитет. Вот правила, с которыми вы столкнётесь на практике.</p>

<h2>У каждого муниципалитета свои правила</h2>
<p>Муниципалитеты прописывают правила для собак в местном регламенте (Algemene Plaatselijke Verordening, APV), часто с
картой зон для выгула. Частое правило: в жилой застройке собака должна быть на поводке, кроме специально отведённых зон
без поводка. Поищите на сайте своего муниципалитета «honden» или «hondenkaart», чтобы узнать, что действует у вас.</p>

<h2>Обязанность убирать</h2>
<p>В большинстве муниципалитетов нужно убирать за собакой, а часто и носить с собой пакет для уборки. За нарушение можно
получить штраф.</p>

<h2>Зоны без поводка</h2>
<p>В зоне без поводка собака может свободно бегать, если она идёт на зов. Подзывайте собаку, когда приближаются дети,
велосипедисты или другие собаки, и убирайте за ней и здесь.</p>

<h2>Природные зоны и сезон гнездования</h2>
<p>Во многих лесах и природных зонах собаки должны быть на поводке, нередко с отдельными зонами для свободного выгула. В
сезон гнездования, примерно с середины марта до середины июля, во многих местах действуют более строгие правила, чтобы
защитить птиц, которые гнездятся на земле. Смотрите таблички у входа или сайт управляющей организации, например
Staatsbosbeheer или Natuurmonumenten.</p>

<h2>На пляже</h2>
<p>На многих пляжах летом днём собакам нельзя или можно только на поводке; вне сезона обычно разрешено больше. Это тоже
зависит от муниципалитета, а иногда и от конкретного входа на пляж.</p>

<h2>Налог на собаку</h2>
<p>Во многих муниципалитетах есть налог на собаку, но не во всех: часть его отменила. Если в вашем муниципалитете он
есть, зарегистрируйте собаку.</p>

<h2>Что взять с собой</h2>
<ul>
<li>Поводок, даже в зоне без поводка: никогда не знаешь, когда он понадобится.</li>
<li>Пакеты для уборки, с запасом на всю прогулку.</li>
<li>Воду и складную миску в жаркие дни.</li>
<li>Лакомства, чтобы тренировать подзыв.</li>
<li>В темноте: светящийся ошейник или фонарик, чтобы собаку было хорошо видно.</li>
</ul>

<h2>Жара</h2>
<p>Асфальт и плитка на солнце могут нагреться так, что собака обожжёт подушечки лап. Положите ладонь на землю на пять
секунд: если вам горячо, то и собаке тоже. В жаркие дни гуляйте рано утром или вечером и выбирайте тень и траву.</p>

<div class="tip"><p><b>Совет:</b> в разделе «Прогулки» в PaWow видно, какие собаки гуляют рядом с вами прямо сейчас, и
можно пойти гулять вместе. Ваше место показывается, только когда вы сами начинаете прогулку, округлённым примерно до
квартала, и через час исчезает само.</p></div>

<p class="disclaimer">Статья носит общий характер. Правила зависят от муниципалитета и природной зоны; что действует у
вас, смотрите на сайте муниципалитета или управляющей организации.</p>
"""


GUIDES = [
    {
        "emoji": "🐶", "minutes": 6,
        "slug": {"nl": "puppy-in-huis", "en": "puppy-at-home", "ru": "puppy-at-home"},
        "title": {"nl": "Een pup in huis: de checklist voor de eerste weken",
                  "en": "A puppy at home: the checklist for the first weeks",
                  "ru": "Щенок дома: чек-лист на первые недели"},
        "excerpt": {"nl": "Welke spullen heb je nodig voordat je pup komt, en wat regel je in de eerste weken? Van bench "
                          "tot chipregistratie.",
                    "en": "What to get before your puppy arrives and what to arrange in the first weeks, from crate to "
                          "microchip registration.",
                    "ru": "Что купить до приезда щенка и что оформить в первые недели: от клетки-домика до регистрации "
                          "чипа."},
        "body": {"nl": PUPPY_NL, "en": PUPPY_EN, "ru": PUPPY_RU},
    },
    {
        "emoji": "🧳", "minutes": 5,
        "slug": {"nl": "op-reis-met-huisdier", "en": "travelling-in-the-eu", "ru": "travelling-in-the-eu"},
        "title": {"nl": "Op reis met je hond of kat binnen de EU",
                  "en": "Travelling with your dog or cat in the EU",
                  "ru": "Поездка с собакой или кошкой по ЕС"},
        "excerpt": {"nl": "Chip, rabiësvaccinatie en dierenpaspoort: wat je nodig hebt, hoe lang van tevoren je begint en "
                          "welke landen extra eisen stellen.",
                    "en": "Microchip, rabies vaccination and pet passport: what you need, how early to start and which "
                          "countries ask for more.",
                    "ru": "Чип, прививка от бешенства и ветпаспорт: что нужно, за сколько начинать и какие страны "
                          "требуют больше."},
        "body": {"nl": TRAVEL_NL, "en": TRAVEL_EN, "ru": TRAVEL_RU},
    },
    {
        "emoji": "🦮", "minutes": 4,
        "slug": {"nl": "uitlaten-regels", "en": "dog-walking-rules", "ru": "dog-walking-rules"},
        "title": {"nl": "Uitlaten in Nederland: aanlijnen, opruimen en losloopgebieden",
                  "en": "Walking your dog in the Netherlands: leash rules, clean-up and off-leash areas",
                  "ru": "Прогулки с собакой в Нидерландах: поводок, уборка и зоны без поводка"},
        "excerpt": {"nl": "Waar mag je hond los en waar niet? Dat verschilt per gemeente. De belangrijkste regels, plus "
                          "tips voor warme dagen en donkere avonden.",
                    "en": "Where can your dog run free? Rules differ per municipality. The key ones, plus tips for hot "
                          "days and dark evenings.",
                    "ru": "Где собаке можно без поводка? Правила зависят от муниципалитета. Главное из них и советы для "
                          "жары и тёмных вечеров."},
        "body": {"nl": WALKS_NL, "en": WALKS_EN, "ru": WALKS_RU},
    },
]
