# Packaging Systems: запуск без сервера и БД

Этот файл относится к **статической версии** проекта. Django в репозитории используется только во время сборки HTML через GitHub Actions. На GitHub Pages нет работающих Python, админки, БД или SMTP-паролей.

## Что уже готово

- Сборка страниц на русском, казахском и английском из действующего оформления Django.
- Все публичные разделы, карточка Bertolaso, фото, галерея, переключатель языков.
- Фильтрация каталога и поиск на JavaScript в браузере.
- Контактная форма с Formspree; без настроенного Formspree кнопка отправки отключена.
- Фотографии PNG, JPEG, WebP хранятся в GitHub (файлы размером до 20 МБ).
- Автопубликация после правок в main **после включения Pages**.

## Шаг 1. Создать форму для info@packaging.kz

1. Зайти на https://formspree.io/ и зарегистрироваться (или войти).
2. Создать форму **Packaging Systems — inquiries**.
3. Указать адрес получателя `info@packaging.kz` и подтвердить его через письмо, полученное в корпоративном ящике.
4. В разделе Form / Integration скопировать адрес вида `https://formspree.io/f/XXXXXXXX` или только ID `XXXXXXXX`.
5. На GitHub зайти в репозиторий → Settings → Secrets and variables → Actions → Variables → New repository variable.
6. Имя переменной **FORMSPREE_FORM_ID**, значение — только ID после `/f/` (не email, не полный URL и не пароль).
7. В панели Formspree проверить уведомления на `info@packaging.kz`, включить антиспам и, после настройки домена, ограничить допустимые домены.
8. Отправить тестовый запрос с опубликованного сайта и убедиться, что письмо дошло (проверь папку «Спам»).

ID формы публичный по своей природе, поэтому это именно **Actions Variable**, а не пароль/секрет. Данные посетителей будут обрабатываться Formspree: до запуска необходимо согласовать политику персональных данных, включая зарубежную обработку и хранение данных.

**Важно:** без доступа к ящику `info@packaging.kz` невозможно подтвердить получателя, поэтому эту часть выполняет владелец корпоративной почты. Не отправляй пароль в чат и не добавляй его в репозиторий.

## Шаг 2. Загрузить архив с фотографиями

В имеющемся ZIP `Packaging_Systems_assets.zip` собраны 15 фотографий Bertolaso и 17 логотипов производителей, использованных в текущем сайте.

В браузере: [репозиторий](https://github.com/phosphy-ll/Packaging_Systems) → Add file → Upload files → перетащи файл `Packaging_Systems_assets.zip` в корень репозитория и нажми Commit changes.

Альтернатива через PowerShell:

```powershell
copy .\Packaging_Systems_assets.zip .\content\assets\Packaging_Systems_assets.zip
git add content/assets/Packaging_Systems_assets.zip
git commit -m "assets: add existing equipment and partner photos"
git push origin main
```

Если у тебя уже есть ZIP в корне проекта, достаточно:

```powershell
git add Packaging_Systems_assets.zip
git commit -m "assets: keep equipment photos for static site"
git push origin main
```

Архив не содержит настроек доступа. Если он отсутствует, сайт соберётся, но фотографии тестовой линии и логотипы будут отображаться как заглушки или названия. Можно повторно загрузить архив позже.

## Шаг 3. Включить GitHub Pages

1. Открыть https://github.com/phosphy-ll/Packaging_Systems/settings/pages.
2. В **Build and deployment → Source** выбрать **GitHub Actions**.
3. В Settings → Secrets and variables → Actions → Variables добавить `PAGES_ENABLED` = `true`.
4. Открыть вкладку Actions → **Static site build and Pages deployment** → Run workflow → Branch `main`.
5. Дождаться успешного шага Deploy. Сайт получит тестовый адрес:
   `https://phosphy-ll.github.io/Packaging_Systems/`

Если Pages ещё не включён, workflow только собирает сайт и загружает `packaging-static-preview` как артефакт, **не** пытаясь деплоить его. При этом предыдущий сайт packaging.kz остаётся без изменений.

## Шаг 4. Проверить сайт и домен

На тестовом адресе проверь:
- меню, RU/KZ/EN, переходы и поиск по каталогу;
- 15 фотографий первого товара, отображение остальных изображений;
- адаптивность на телефоне, полноэкранную галерею;
- заявку из формы (до получения письма на info@packaging.kz);
- корректную ссылку на политику обработки персональных данных.

**Только после проверки** переходить к DNS.

### Привязка packaging.kz через PS.kz

1. В GitHub Settings → Pages, поле Custom domain → `packaging.kz` → Save.
2. Желательно заранее подтвердить владение доменом в настройках GitHub Pages пользователя, добавив TXT-запись, которую GitHub покажет (это снижает риск захвата).
3. В PS.kz → Домены → packaging.kz → Управление DNS → DNS-зона → Изменить:
   - A `@` → `185.199.108.153`
   - A `@` → `185.199.109.153`
   - A `@` → `185.199.110.153`
   - A `@` → `185.199.111.153`
   - CNAME `www` → `phosphy-ll.github.io.`
4. Удалить/заменить **только конфликтующие веб-записи** для @ и www. Существующие почтовые MX, TXT (SPF, DKIM, DMARC) и другие записи не изменять.
5. После выпуска сертификата включить **Enforce HTTPS** в Pages и протестировать `https://packaging.kz` и `https://www.packaging.kz`.

Важно: если домен уже обслуживает действующий сайт, изменение его A/CNAME-записей заменит адрес сайта. До шага 4 ничего в DNS не трогать. Для полноценной проверки можно использовать стандартный адрес GitHub Pages, не затрагивая DNS.

## Шаг 5. Как добавлять товары через GitHub

Основной файл товаров: `content/catalog.json`. Фотографии новых товаров размещаются в `content/images/`; один товар может иметь много изображений. Выбранное фото можно записать первым. Каждые 5 секунд на сайте фотографии пролистываются автоматически, по нажатию открываются в полном размере.

Образец объекта для массива `products`:

```json
{
  "slug": "example-filling-machine",
  "title": "Машина розлива Example 1000",
  "category": "equipment-units",
  "status": "published",
  "condition": "used",
  "availability": "available",
  "featured": true,
  "manufacturer": "Example",
  "model_name": "1000",
  "price": null,
  "currency": "EUR",
  "summary": "Короткое описание для каталога.",
  "description": "Полное описание без ограничений по длине.\nВторая строка.",
  "translations": {
    "kk": {
      "title": "Example 1000 құю машинасы",
      "summary": "Қысқаша сипаттама",
      "description": "Толық сипаттама"
    },
    "en": {
      "title": "Example 1000 filling machine",
      "summary": "Short overview",
      "description": "Full description"
    }
  },
  "specifications": [
    {
      "name": "Производительность",
      "value": "1 000 бут/час",
      "name_kk": "Өнімділік",
      "value_kk": "1 000 бөтелке/сағ",
      "name_en": "Capacity",
      "value_en": "1,000 bottles/hour"
    }
  ],
  "images": [
    "content/images/example-front.png",
    "content/images/example-side.png"
  ]
}
```

Эту запись нужно **добавить** в `products`, не затирая существующую запись Bertolaso. Сохранять JSON в UTF-8 без комментариев (кроме строковых полей). Поля `name_kk` и `name_en` для новых категорий пока заполняются через код; у существующих категорий переводы уже есть.

`status: "draft"` — черновик; не появляется в каталоге. `status: "published"` — публичная карточка. `availability: "sold"` — не виден посетителям. Для временного скрытия достаточно перевести в черновик.

После коммита workflow автоматически обновит сайт. Любой, у кого есть доступ на запись в этот GitHub-репозиторий, может редактировать каталог, поэтому включи двухфакторную аутентификацию и защиту ветки `main`.

### Новые фотографии и документация

Загружай файлы через GitHub → Add file → Upload files в `content/images/` (для PDF — `content/documents/`). Доступные форматы: PNG, JPG, JPEG, WebP; документы PDF. Максимум 20 МБ на файл.

Имена файлов пиши латиницей: `line-01-front.png`, `line-01-side.png`. Размеры изображений сохраняются, визуально вписываются в карточки через `object-fit:contain`. Для больших исходных фотографий рекомендуется уменьшать разрешение, чтобы страницы быстро загружались.

## Безопасность

- На публичном сайте нет Django Admin, серверных сессий, БД и SMTP-паролей.
- Защити аккаунты GitHub, PS.kz и Formspree с помощью 2FA / passkeys.
- В GitHub Settings → Branches / Rulesets включи защиту `main` с обязательными проверками; для публикации изменений используй pull requests.
- Не коммить `.env`, пароли, токены, персональные данные или списки клиентов.
- Formspree: включи фильтры спама, ограничение домена, проверь email-уведомления.
- Храни резервную копию фотографий, ZIP и JSON отдельно от GitHub; регулярные бэкапы почты/заявок также важны.
- Прежде чем включать отправку реальных персональных данных, согласуй актуальную политику обработки данных.

## Локальная проверка статической версии

```powershell
.\.venv\Scripts\python.exe scripts/build_static.py
.\.venv\Scripts\python.exe scripts/check_static.py
cd _site
py -m http.server 8008
```

Адрес: `http://localhost:8008/ru/`. Это именно статическая версия, а не `python manage.py runserver`.

Билд использует временную SQLite только в момент генерации. Она не входит в готовый сайт. Фотографии и товары берутся из репозитория, а не из локальной базы `db.sqlite3`.
