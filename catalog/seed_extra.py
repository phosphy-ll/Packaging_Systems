"""Seed editable translations and producer references from supplied company materials."""
from .models import Page, PageTranslation, Partner, Product, ProductTranslation, ProductSpecification

PARTNERS = [
    "SIPA", "Videosystems", "Matrix", "Meccanica Italiana",
    "Stirling Cryogenics", "Makro Labelling", "MBF", "GEA", "PE Labellers",
    "TORQ Packaging", "Sidel", "BIEFFE", "SIAD Macchine Impianti",
    "Tecnocom", "Atlas Copco", "Unimac-Gherri", "ATLANTA",
]
# Original company page is Russian; these translations are editable from /admin/.
# Values below are provided as initial working translations, subject to client proofreading.
PAGE_TRANSLATIONS = {
"home": {
"en": ("Home", "Packaging Systems has supplied Kazakhstan and the Eurasian market with Italian filling and packaging equipment since 2014.", "We supply complete new and used filling and packaging lines, and individual machines that have undergone inspection and overhaul with warranty.\n\nExperienced European specialists can perform commissioning work.\n\nWe also supply spare parts from Europe, arranging delivery, customs clearance, installation and maintenance."),
"kk": ("Басты бет", "Packaging Systems 2014 жылдан бері Қазақстан және Еуразия нарығына итальяндық құю және орау жабдықтарын жеткізеді.", "Жаңа және қолданылған құю және орау желілерін, сондай-ақ тексеруден өткен жеке жабдықтарды кепілдікпен ұсынамыз.\n\nЕуропалық мамандар іске қосу-реттеу жұмыстарын орындайды.\n\nЕуропадан қосалқы бөлшектерді жеткізу, кедендік рәсімдеу, орнату және техникалық қызмет көрсету бойынша қолдау көрсетеміз."),
"it": ("Home", "Dal 2014 Packaging Systems propone attrezzature italiane per l'imbottigliamento e il confezionamento in Kazakistan e nel mercato eurasiatico.", "Forniamo linee complete nuove e usate, oltre a singole macchine revisionate con garanzia.\n\nSpecialisti europei qualificati si occupano dell'avviamento degli impianti.\n\nForniamo inoltre ricambi dall'Europa, con servizi di consegna, sdoganamento, installazione e manutenzione."),
},
"filling-lines": {
"en": ("Filling lines of various capacities", "Complete filling lines for beverages and other food liquids.", "We supply filling lines for a variety of liquids and capacities, suitable for glass, aluminum cans and PET containers.\n\nWe offer complete systems from leading Italian manufacturers.\n\nSIPA is an international manufacturer of high-speed filling lines, blowing machines and preform production equipment. The company also produces molds for preform machinery."),
"kk": ("Әртүрлі өнімділіктегі құю желілері", "Сусындар мен тағамдық сұйықтықтарға арналған толық құю желілері.", "Шыныға, алюминий банкасына және ПЭТ ыдысына арналған әртүрлі өнімділіктегі құю желілерін жеткіземіз.\n\nЖетекші итальяндық өндірушілердің толық желілерін ұсынамыз.\n\nSIPA жоғары жылдамдықты құю желілерін, үрлеу машиналарын және преформа өндіру жабдықтарын шығарады, сонымен қатар қалыптар дайындайды."),
"it": ("Linee di imbottigliamento di varie capacità", "Linee complete per bevande e altri liquidi alimentari.", "Forniamo linee di imbottigliamento di varie capacità per vetro, lattine di alluminio e PET.\n\nProponiamo linee complete di importanti produttori italiani.\n\nSIPA realizza linee ad alta velocità, soffiatrici e macchinari per la produzione di preforme, nonché stampi per le preforme."),
},
"equipment-units": {
"en": ("Machines and units for filling lines", "Individual machines for building and modernizing production lines.", "Available equipment includes linear and rotary blow-molding machines (3,000–50,000 bottles/hour); rinsing, filling and capping monoblocks; labeling machines; shrink-wrapping machines; case erectors; depalletizers and palletizers; line control and synchronization systems; conveyors; and vision, X-ray and machine-vision quality-control systems."),
"kk": ("Құю желілеріне арналған жабдықтар", "Өндіріс желілерін жинақтау және жаңғыртуға арналған жеке машиналар.", "Біз 3 000–50 000 бөтелке/сағ үрлеу машиналарын, шаю-құю-жабу моноблоктарын, затбелгі жапсыру, термоорау және қорап құрастыру машиналарын, паллетизаторларды, басқару және синхрондау жүйелерін, конвейерлерді, бейне, рентген және машиналық көру негізіндегі сапа бақылау жүйелерін ұсынамыз."),
"it": ("Macchine e componenti per linee di imbottigliamento", "Macchine singole per realizzare e ammodernare linee di produzione.", "Offriamo soffiatrici lineari e rotative (3.000–50.000 bottiglie/ora), monoblocchi di risciacquo, riempimento e tappatura, etichettatrici, termoretraibili, formatrici di cartoni, depalettizzatori, palettizzatori, sistemi di controllo e sincronizzazione, nastri trasportatori e sistemi qualità con video, raggi X e visione artificiale."),
},
"water-treatment": {
"en": ("Water treatment systems", "Water treatment systems: specifications available on request.", "Please tell us the intended application, required capacity and water characteristics so that we can review your request."),
"kk": ("Су дайындау жүйелері", "Су дайындау жүйелері туралы ақпарат сұраныс бойынша беріледі.", "Жүйенің мақсатын, қажетті өнімділігін және судың параметрлерін көрсетіңіз. Біз сұранысыңызды қарастырамыз."),
"it": ("Sistemi di trattamento acqua", "Specifiche dei sistemi disponibili su richiesta.", "Indica la destinazione d'uso, la portata richiesta e le caratteristiche dell'acqua: valuteremo la tua richiesta."),
},
"used-lines": {
"en": ("Overhauled used lines with warranty", "Used European-made filling, processing and packaging lines.", "We offer used European filling and packaging lines that have undergone inspection and functional testing. These systems can be a cost-effective alternative to new equipment.\n\nWe provide delivery, installation and commissioning support.\n\nThe warranty period for equipment overhauled by our company can be up to 12 months.\n\nIndividual units are also available for upgrades or capacity increases.\n\nOur motto: Flexibility and knowledge."),
"kk": ("Кепілдігі бар тексерілген қолданылған желілер", "Еуропада шығарылған қолданылған құю және орау желілері.", "Тексеруден және жұмыс қабілетін сынақтан өткен еуропалық желілерді ұсынамыз. Мұндай шешім жаңа жабдыққа үнемді балама болуы мүмкін.\n\nЖеткізу, монтаждау және іске қосу қызметтерін көрсетеміз.\n\nБіздің жөндеуімізден өткен жабдыққа кепілдік мерзімі 12 айға дейін.\n\nӨнімділікті арттыру үшін жеке тораптар да жеткізіледі.\n\nҰранымыз: Flexibility and knowledge."),
"it": ("Linee usate revisionate con garanzia", "Linee europee usate di imbottigliamento e confezionamento.", "Proponiamo linee europee usate, revisionate e sottoposte a test funzionali. Possono essere un'alternativa economica alle linee nuove.\n\nOffriamo consegna, montaggio e avviamento.\n\nLa garanzia sugli impianti revisionati dalla nostra azienda può arrivare a 12 mesi.\n\nSono disponibili anche singoli gruppi per ammodernamento e aumento della capacità.\n\nIl nostro motto: Flexibility and knowledge."),
},
"spare-parts": {
"en": ("Spare parts", "Components for food filling and packaging equipment.", "We supply spare parts for European equipment including SIDEL, Atlanta, GEA, SIPA, PE Labellers, Sacmi (ACMI), SIAD, Dimac, BIEFFE, TORQ Packaging, Atlas Copco, Unimac-Gherri, Robopac and others.\n\nInfrared lamps are available for blow-molding machines by KRONES, SIDEL, SIPA, KHS and SACMI (ACMI)."),
"kk": ("Қосалқы бөлшектер", "Тамақ өнімдерін құю және орау жабдықтарына арналған бөлшектер.", "SIDEL, Atlanta, GEA, SIPA, PE Labellers, Sacmi (ACMI), SIAD, Dimac, BIEFFE, TORQ Packaging, Atlas Copco, Unimac-Gherri, Robopac және басқа еуропалық жабдықтарға бөлшектер жеткіземіз.\n\nKRONES, SIDEL, SIPA, KHS және SACMI (ACMI) үрлеу машиналарына инфрақызыл шамдар бар."),
"it": ("Ricambi", "Ricambi per macchine di imbottigliamento e confezionamento alimentare.", "Forniamo ricambi per macchine europee SIDEL, Atlanta, GEA, SIPA, PE Labellers, Sacmi (ACMI), SIAD, Dimac, BIEFFE, TORQ Packaging, Atlas Copco, Unimac-Gherri, Robopac e altre.\n\nSono disponibili lampade a infrarossi per soffiatrici KRONES, SIDEL, SIPA, KHS e SACMI (ACMI)."),
},
"service": {
"en": ("Service", "Inspection, repair, technical assistance and modernization of filling lines.", "We provide inspections, repairs and technical support for individual equipment and complete filling lines. We also design new filling plants by integrating equipment from different manufacturers. Work is carried out by specialized technical staff.\n\nWe supply and install mechanical and electronic components, spare parts and production-line units.\n\nAnnual preventive maintenance programs can improve production reliability.\n\nWe also study existing equipment to propose efficiency improvements and replacements for bottlenecks."),
"kk": ("Сервис", "Құю желілерін тексеру, жөндеу және жаңғырту.", "Жеке жабдықтар мен толық құю желілеріне техникалық қызмет көрсетеміз және жөндейміз. Әртүрлі өндірушілердің жабдықтарын біріктіре отырып, жаңа құю зауыттарын жобалаймыз. Жұмысты мамандандырылған қызметкерлер орындайды.\n\nМеханикалық және электрондық бөлшектерді жеткізіп, орнатамыз.\n\nЖыл сайынғы профилактикалық қызмет бағдарламаларын ұсынамыз.\n\nҚолданыстағы желілердің өнімділігін арттыру үшін әлсіз тораптарды ауыстыруға көмектесеміз."),
"it": ("Assistenza", "Revisione, riparazione, supporto tecnico e ammodernamento delle linee.", "Effettuiamo revisioni, riparazioni e assistenza su singole unità e linee complete. Progettiamo nuovi stabilimenti integrando macchine di produttori diversi. Il lavoro è svolto da personale tecnico specializzato.\n\nForniamo e installiamo componenti meccanici ed elettronici e ricambi.\n\nProponiamo programmi annuali di manutenzione preventiva.\n\nAnalizziamo inoltre le linee esistenti per migliorarne l'efficienza e sostituire i punti critici."),
}
}

PRODUCT_TRANSLATIONS = {
"en": ("Bertolaso 40.40.6 filling line", "Used filling line for non-carbonated liquids. Reported capacities differ; please confirm specifications.", "Used filling line for non-carbonated liquids, including spirits. The supplied presentation describes a nominal line capacity of 8,000 bottles/hour, while the Bertolaso 40.40.6 triblock is specified at 10,000 bottles/hour. This discrepancy must be confirmed.\n\nEquipment list: Bertolaso 40.40.6 rinsing/filling/capping triblock (2006); PE Universal-Master labeler with 16 stations (2004, up to 12,000 bottles/hour); APSOL case erector and case packer (2015); partition insertion station; Atlas Copco low-pressure compressor (8.5 bar, 750 l receiver); PROCONV-CHAIN bottle conveyors; electrical control and distribution cabinets; cap feeding mechanism; DRYER 3 bottle dryer; cables and connecting materials; technical documentation in Russian; light inspection panel.\n\nAccording to the presentation, the line was dismantled, packed and ready for shipment, and reported to be operational. The closing machine accommodates aluminum screw caps and Guala caps. The presentation states EUR 110,000, VAT 0%, EXW Incoterms 2020, Kazakhstan. Availability, condition, price and delivery terms must be reconfirmed before purchase."),
"kk": ("Bertolaso 40.40.6 құю желісі", "Газдалмаған сұйықтықтарға арналған қолданылған желі. Өнімділік көрсеткіштерін нақтылау қажет.", "Газдалмаған сұйықтықтарға, оның ішінде спиртті өнімдерге арналған қолданылған желі. Презентацияда жалпы желі өнімділігі 8 000 бөтелке/сағ, ал Bertolaso 40.40.6 триблогының өнімділігі 10 000 бөтелке/сағ деп көрсетілген. Бұл айырмашылықты нақтылау керек.\n\nЖабдық құрамы: Bertolaso 40.40.6 шаю-құю-жабу триблогы (2006); 16 позициялы PE Universal-Master затбелгі жапсыру машинасы (2004, 12 000 бөтелке/сағ дейін); APSOL қорап құрастыру және салу машиналары (2015); бөлгіштер салу орны; Atlas Copco компрессоры (8,5 бар, 750 л); PROCONV-CHAIN конвейерлері; басқару шкафтар; қақпақ беру жүйесі; DRYER 3 кептіргіші; кабельдер; орыс тіліндегі құжаттама; жарық бақылау панелі.\n\nПрезентацияда желінің бөлшектеліп, оралғаны және жөнелтуге дайын екені, жұмыс істейтіні көрсетілген. Жабу жүйесі алюминий бұрандалы және Guala қақпақтарына сай. Құжаттағы баға 110 000 EUR, ҚҚС 0%, EXW Incoterms 2020, Қазақстан. Сатып алудан бұрын бағасы мен шарттарын қайта тексеру қажет."),
"it": ("Linea di imbottigliamento Bertolaso 40.40.6", "Linea usata per liquidi non gassati. La capacità dichiarata richiede verifica.", "Linea usata per liquidi non gassati, inclusi alcolici. La presentazione riporta una capacità della linea di 8.000 bottiglie/ora, mentre per il triblocco Bertolaso 40.40.6 indica 10.000 bottiglie/ora. Il dato va verificato.\n\nComposizione: triblocco di risciacquo/riempimento/tappatura Bertolaso 40.40.6 (2006); etichettatrice PE Universal-Master a 16 stazioni (2004, fino a 12.000 bottiglie/ora); formatrice e incartonatrice APSOL (2015); stazione di inserimento divisori; compressore Atlas Copco (8,5 bar, serbatoio 750 l); trasportatori PROCONV-CHAIN; quadri elettrici; alimentazione tappi; asciugatrice DRYER 3; materiali di collegamento; documentazione tecnica in russo; pannello di ispezione luminoso.\n\nSecondo la presentazione, la linea è smontata, imballata e pronta alla spedizione, in condizioni operative. La tappatura supporta capsule a vite in alluminio e Guala. La presentazione indica 110.000 EUR, IVA 0%, EXW Incoterms 2020, Kazakistan. Verificare disponibilità, prezzo e condizioni aggiornate."),
}


def upgrade_seed():
    for order, name in enumerate(PARTNERS):
        Partner.objects.get_or_create(name=name, defaults={"sort_order":order})

    for slug, translations in PAGE_TRANSLATIONS.items():
        page=Page.objects.filter(slug=slug).first()
        if not page:
            continue
        for language,(title,lead,body) in translations.items():
            PageTranslation.objects.get_or_create(page=page,language=language,defaults={
                "title":title,"lead":lead,"body":body,
            })

    product=Product.objects.filter(title="Линия розлива Bertolaso 40.40.6").first()
    if product:
        if product.status == Product.Status.DRAFT:
            product.status = Product.Status.PUBLISHED
            product.availability = Product.Availability.AVAILABLE
            product.featured = True
            product.summary = (
                "Линия для спокойных жидкостей, включая ликероводочную продукцию. "
                "Производительность: 8 000 бут/час по описанию линии, 10 000 бут/час "
                "для триблока Bertolaso. Данные требуют уточнения."
            )
            product.description = (
                "Комплектная линия розлива спокойных жидкостей (в том числе ликероводочной продукции).\n\n"
                "В презентации заявлена производительность линии 8 000 бутылок в час. "
                "При этом триблок Bertolaso 40.40.6 указан с производительностью "
                "10 000 бутылок в час, а этикетировочная машина PE - 12 000 бутылок в час. "
                "Данные об общей производительности необходимо уточнить.\n\n"
                "СОСТАВ ЛИНИИ:\n"
                "1. Триблок ополаскивания, розлива и укупорки Bertolaso 40.40.6 (2006 г.), 1 шт.\n"
                "2. Этикетировочная машина PE Универсал-Мастер, 16 столиков (2004 г.), 1 шт.\n"
                "3. Машина формирования картонных коробок APSOL (2015 г.), 1 шт.\n"
                "4. Машина-укладчик бутылок в короба APSOL (2015 г.), 1 шт.\n"
                "5. Станция ручной укладки перегородок для бутылок в коробках, 1 шт.\n"
                "6. Компрессор низкого давления Atlas Copco, 8,5 бар, ресивер 750 л, 1 шт.\n"
                "7. Конвейерная система для бутылок со смазкой PROCONV-CHAIN, 1 комплект.\n"
                "8. Электрический шкаф управления конвейерами, 1 шт.\n"
                "9. Шкаф распределения электропитания, 1 шт.\n"
                "10. Механизм распределения и подачи пробок, датчики, распределительная коробка, "
                "шесть укупорочных головок, 1 комплект.\n"
                "11. Машина обдува и сушки бутылок DRYER 3, 1 шт.\n"
                "12. Соединительные материалы: короба, кабели, ленты, 1 комплект.\n"
                "13. Техническая документация на русском языке на бумажном и электронном носителях, 1 комплект.\n"
                "14. Световой экран визуального контроля, 1 шт.\n\n"
                "ДОПОЛНИТЕЛЬНЫЕ СВЕДЕНИЯ И УСЛОВИЯ ПОСТАВКИ:\n"
                "По материалам презентации линия полностью демонтирована, упакована и готова к отправке; "
                "на момент составления предложения находилась в рабочем состоянии. "
                "Триблок может работать с алюминиевыми винтовыми крышками и крышками Guala.\n"
                "В презентации указаны цена 110 000 EUR, НДС 0% и поставка EXW Incoterms 2020, Казахстан. "
                "Перед заключением сделки требуется подтвердить актуальное наличие, техническое состояние, "
                "комплектацию, цену и условия поставки."
            )
            product.save(update_fields=[
                "status","availability","featured","summary","description","updated_at",
            ])
        for lang,(title,summary,description) in PRODUCT_TRANSLATIONS.items():
            ProductTranslation.objects.get_or_create(product=product,language=lang,defaults={
                "title":title,"summary":summary,"description":description,
            })
        ProductSpecification.objects.get_or_create(
            product=product,
            name="Общая производительность (по презентации)",
            defaults={"value":"8 000 бут/час; триблок: 10 000 бут/час (уточнить)","sort_order":0},
        )
