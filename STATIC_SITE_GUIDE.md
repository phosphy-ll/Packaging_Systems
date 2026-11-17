# Packaging Systems: запуск сайта через GitHub + Netlify

**Актуальная архитектура:** GitHub хранит код, товары и фотографии; Netlify автоматически собирает и публикует статический сайт. Django применяется только во время сборки. На публичном сервере нет Django Admin, Python, SQLite/PostgreSQL или SMTP-паролей.

Почему не GitHub Pages: GitHub запрещает использовать его как бесплатный хостинг коммерческих сайтов, предназначенных для продаж. Netlify Free разрешает коммерческие проекты. Цены/лимиты проверяйте в панели Netlify: бесплатный тариф в 2026 году ограничивается кредитами.

В GitHub не нужно вручную копировать готовые страницы: Netlify запускает `scripts/build_static.py` при изменении `main`.

## 1. Подключение корпоративной почты (Formspree)

1. Открой https://formspree.io/ и создай аккаунт.
2. Добавь форму **Packaging Systems — inquiries** с получателем `info@packaging.kz`.
3. Получи и открой письмо с подтверждением получателя на этом корпоративном ящике. Без доступа к почте подтвердить доставку невозможно.
4. В Formspree открой форму → Integration и скопируй **ID формы** из адреса вида `https://formspree.io/f/XXXXXXXX`.
5. В Netlify открой проект → Project configuration → Environment variables → Add variable. Укажи `FORMSPREE_FORM_ID` = `XXXXXXXX` (только ID, без `/f/`, без адреса почты).
6. Запусти в Netlify **Deploys → Trigger deploy → Deploy project**, чтобы форма подключилась.
7. Отправь тестовую заявку со страницы контактов и убедись, что уведомление дошло в `info@packaging.kz`. Проверь папку «Спам».
8. После запуска на основном домене включи в Formspree антиспам и Restrict to Domain = `packaging.kz`. Пока тестируешь на домене `*.netlify.app`, не ограничивай форму только `packaging.kz`, иначе тестовые отправки не пройдут.

В браузере хранится только публичный ID формы. Пароль корпоративной почты или SMTP не передаются на сайт. Formspree - сторонний обработчик данных посетителей, поэтому до включения приёма реальных обращений нужно проверить актуальную политику обработки персональных данных и условия провайдера. Бесплатный тариф может иметь ограничения на количество заявок.

Если ID ещё не настроен, кнопка «Отправить запрос» отключена; посетитель увидит адрес `info@packaging.kz` и сможет написать напрямую. Так заявки не теряются незаметно.

## 2. Развёртывание сайта в Netlify

1. Перейди на https://app.netlify.com/, зарегистрируйся через **GitHub**.
2. Выбери **Add new project → Import an existing project → GitHub**.
3. Разреши Netlify доступ к репозиторию `phosphy-ll/Packaging_Systems` и выбери его.
4. Branch to deploy: **main**. Файл `netlify.toml` уже содержит сборку и публикацию; проверь параметры:
   - Build command: `python -m pip install -r requirements.txt && python scripts/build_static.py --output _site && python scripts/check_static.py --output _site`
   - Publish directory: `_site`
   - Python version: `3.12`
5. Добавь переменную окружения `FORMSPREE_FORM_ID` (если ID формы уже есть). Не добавляй `.env` в GitHub или Netlify.
6. Нажми **Deploy project**. Netlify выдаст тестовый адрес вроде `https://your-project.netlify.app/`.
7. Открой этот адрес и проверь RU/KZ/EN, каталог, поиск, карточки, изображения, адаптивность, Formspree и страницу политики.

После того как GitHub и Netlify соединены, каждый коммит в `main` автоматически собирает новую версию. Никакой локальный Python-сервер для работающего сайта не нужен.

Netlify предоставляет TLS/HTTPS для `*.netlify.app` и пользовательских доменов. Сайт настроен на безопасные заголовки (CSP, запрет фреймов, ограниченные права браузера). Проверь актуальные лимиты бесплатного тарифного плана и его кредиты в панели.

## 3. Загрузить фотографии из прежней версии

В `Packaging_Systems_assets.zip` уже собраны **15 фотографий Bertolaso и 17 логотипов производителей**. Сейчас этот ZIP ещё не лежит в GitHub. Его необходимо один раз загрузить, чтобы фотографии не исчезли при переносе с локального Django.

Самый простой способ: GitHub → репозиторий → **Add file → Upload files** → перетащи `Packaging_Systems_assets.zip` в корень репозитория → Commit changes.

Или на компьютере из папки проекта:

```powershell
git pull origin main
git add Packaging_Systems_assets.zip
git commit -m "assets: add original product and partner photos"
git push origin main
```

Если ZIP не в папке проекта, скопируй его туда. После коммита Netlify автоматически пересоберёт сайт и импортирует 15 фото и логотипы; при отсутствии архива показывает текстовые названия производителей и заглушки товара. Файлы из ZIP в сборке проверяются по формату и размеру.

## 4. Проверка до переключения packaging.kz

Перед переключением DNS **обязательно** проверь:
- главная и все разделы RU/KZ/EN;
- фотографии, галерея 5 секунд и полноэкранный просмотр;
- поиск, категории, фильтры, карточки;
- отправка заявки и получение письма на info@packaging.kz;
- браузер и мобильный экран;
- текущая цена Bertolaso и две разные производительности (8 000 / 10 000 бут/час), которые взяты из старой презентации и требуют подтверждения.

До этого момента старый `packaging.kz` остаётся без изменений.

## 5. Подключить packaging.kz через PS.kz

1. В Netlify → **Domain management → Add a domain** укажи `packaging.kz` и при необходимости `www.packaging.kz`.
2. В Netlify посмотри экран **Pending DNS verification** - он показывает конкретные DNS-записи для вашего проекта.
3. Открой https://console.ps.kz → Домены → packaging.kz → Управление DNS → DNS-зона.
4. Для обычного Netlify CDN и внешнего DNS обычно нужны:
   - `A` запись для корня (`@`) → `75.2.60.5`.
   - `CNAME` для `www` → **имя твоего Netlify-проекта**, например `my-project.netlify.app` (не выдумывай значение, возьми из Netlify).
   - Если PS.kz поддерживает ALIAS/ANAME для корня, Netlify рекомендует вместо A запись на `apex-loadbalancer.netlify.com`.
5. Удалять или заменять можно только конфликтующие **веб-записи** для `@` и `www`. **Не меняй** MX, TXT (SPF/DKIM/DMARC), почтовые записи, поддомены и NS `ns1.ps.kz / ns2.ps.kz / ns3.ps.kz`, если не переносишь весь DNS осознанно.
6. Подожди обновления DNS и выпуска сертификата в Netlify. Проверь `https://packaging.kz` и `https://www.packaging.kz` без ошибок.

Обычную смену DNS делаем один раз, только после успешного теста на `*.netlify.app`. При проблеме с DNS сначала сверяй значения с инструкциями Netlify именно для твоего проекта.

## 6. Как менять товары через GitHub

Главный файл - `content/catalog.json`. Фотографии новых товаров - `content/images/`, документация PDF - `content/documents/`.

Форматы: PNG, JPG, JPEG, WebP, PDF. Изображения не обрезаются; в каталоге они автоматически перелистываются каждые 5 секунд. Для новых товаров укажи фотографии в массиве `images` в нужном порядке. На публикации доступны только товары со статусом `published`, с активной категорией и не отмеченные `sold`.

Пример новой записи **внутри массива products**:

```json
{
  "slug": "example-filling-machine",
  "title": "Машина розлива Example 1000",
  "category": "equipment-units",
  "status": "published",
  "condition": "used",
  "availability": "available",
  "featured": false,
  "manufacturer": "Example",
  "model_name": "1000",
  "price": null,
  "currency": "EUR",
  "summary": "Короткое описание.",
  "description": "Полное описание товара.\\nВторая строка.",
  "translations": {
    "kk": {"title": "Example 1000 құю машинасы", "summary": "Қысқаша сипаттама", "description": "Толық сипаттама"},
    "en": {"title": "Example 1000 filling machine", "summary": "Short overview", "description": "Full description"}
  },
  "specifications": [
    {
      "name": "Производительность", "value": "1 000 бут/час",
      "name_kk": "Өнімділік", "value_kk": "1 000 бөтелке/сағ",
      "name_en": "Capacity", "value_en": "1,000 bottles/hour"
    }
  ],
  "images": [
    "content/images/example-front.png",
    "content/images/example-side.png"
  ]
}
```

Нельзя просто вставить один JSON-объект вместо всего файла: нужно добавить его в существующий список `products` через запятую. Можешь передать мне описание и фотографии, и я внесу изменения в GitHub.

Для черновика установи `status: "draft"`; убрать товар с публикации можно удалением записи или установкой `archived`. Данные файлов в GitHub публичны, если репозиторий публичный; не загружай туда персональные данные и коммерческие секреты.

## 7. Безопасность

- Защити **GitHub, PS.kz, Netlify и Formspree** через двухфакторную аутентификацию или passkeys.
- В GitHub → Settings → Rules → Rulesets включи защиту `main`, обязательную проверку тестов и работу через pull requests.
- Публикуем только `_site` (HTML/CSS/JS/медиа), без Django Admin, БД, `.env` и ключей.
- Не загружай пароли, токены, данные клиентов в публичный GitHub.
- Настрой фильтрацию Formspree и Restrict to Domain после переноса основного домена.
- Храни резервные копии фотографий и `content/catalog.json` отдельно от GitHub.
- Проверяй объём трафика и кредитов Netlify. На бесплатном тарифе возможна приостановка при достижении лимитов.
- Проверь правовые требования к обработке контактных данных посетителей.

## Локальная проверка статической версии

```powershell
.\.venv\Scripts\python.exe scripts/build_static.py
.\.venv\Scripts\python.exe scripts/check_static.py
cd _site
py -m http.server 8008
```

Открой `http://localhost:8008/ru/`. Временная SQLite нужна лишь для генерации файлов и удаляется после сборки.

Официальные инструкции:
- https://docs.netlify.com/start/quickstarts/deploy-from-repository/
- https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/
- https://help.formspree.io/articles/building-your-form/building-an-html-form/
