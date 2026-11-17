# Packaging Systems: GitHub + Netlify (без постоянной БД)

Статический корпоративный сайт генерируется из текущего Django-проекта **во время сборки**. На Netlify работают готовые HTML/CSS/JavaScript и фотографии. Публичной Django-админки, сервера и SQL-базы нет.

**Адрес тестовой версии:** https://aesthetic-zabaione-9d9d34.netlify.app/

## 1. Фотографии оборудования и логотипы

В исходном ZIP `Packaging_Systems_assets.zip` находится 15 фотографий Bertolaso и 17 логотипов. Фотографий на тестовом сайте сейчас нет только потому, что ZIP не был добавлен в GitHub.

**Единственное обязательное действие для фото:**
1. Скачай `Packaging_Systems_assets.zip` из чата ChatGPT.
2. Открой https://github.com/phosphy-ll/Packaging_Systems.
3. На главной странице репозитория нажми **Add file → Upload files**.
4. Перетащи ZIP **в корень репозитория рядом с `manage.py`**. Не распаковывай.
5. Нажми **Commit changes** в ветку `main`. Netlify автоматически начнёт новую сборку.
6. В Netlify → **Deploys** дождись **Published**, затем обнови страницу через Ctrl + Shift + R.

Сборка находит архив как `Packaging_Systems_assets.zip` или `content/assets/Packaging_Systems_assets.zip`, проверяет изображения и загружает их в публичное `media/`. На сайте фотографии Bertolaso автоматически листаются каждые 5 секунд и раскрываются при нажатии. Старые фотографии сохраняются; другие товары можно добавлять с PNG/JPG/WebP.

Если загрузка ZIP не происходит, проверь, что он в `main`, а не внутри другой папки, и что Netlify успешно выполнил новый Deploy.

## 2. Подключить заявки к info@packaging.kz через Netlify Forms

**Formspree и SMTP не нужны.** Отправку и хранение заявок обеспечивает Netlify Forms. Пароль корпоративного почтового ящика не вводится ни в сайт, ни в GitHub.

1. Открой Netlify → проект `aesthetic-zabaione-9d9d34` → **Forms**.
2. Найди **Form detection** и нажми **Enable form detection**, если она отключена.
3. После нового деплоя (например, после загрузки ZIP) появится форма `packaging-inquiry`.
4. Открой **Forms → Submission notifications → Add notification → Email notification**.
5. Укажи получателя `info@packaging.kz` и сохрани настройку.
6. Netlify отправит письмо подтверждения на этот адрес. **Владелец почтового ящика должен открыть письмо и нажать Confirm**. До подтверждения уведомления не доставляются.
7. Открой публичную страницу контактов, отправь тестовую заявку.
8. Проверь, что заявка появилась в **Forms → packaging-inquiry → Verified submissions**, а письмо пришло на `info@packaging.kz` (или в папку «Спам»).

Важно: с ноября 2026 Netlify допускает уведомления на внешние адреса после подтверждения адреса. Если форма не появилась, убедись, что детекция включена, выполни новый Deploy и проверь журнал сборки. Если письма не приходят, но заявка видна в Netlify Forms, проверь уведомления и подтверждение адреса.

Собираемые поля: имя, email, телефон (необязательно), компания (необязательно), тема, сообщение, выбранное оборудование и согласие. Данные сохраняются в Netlify Forms, не в GitHub. Перед приёмом персональных данных реальных клиентов согласуй правила хранения и передачи этих данных с учётом законодательства Казахстана.

## 3. Домен packaging.kz в PS.kz

Пока тестовая версия не проверена и не настроена почта, **не меняй DNS**: старый сайт должен оставаться рабочим.

После успешной проверки:
1. Netlify → **Domain management → Add a domain** → `packaging.kz`.
2. Выбери внешнее DNS-управление (**External DNS**), поскольку домен зарегистрирован в PS.kz. Не нужно менять name-серверы `ns1.ps.kz`, `ns2.ps.kz`, `ns3.ps.kz`.
3. Открой **Pending DNS verification** и скопируй именно те значения DNS-записей, которые показаны в твоём проекте Netlify.
4. PS.kz → Домены → `packaging.kz` → **Управление DNS → DNS-зона**. Замени только конфликтующие веб-записи для `@` и `www` (A/ALIAS и CNAME), как требует Netlify.
5. **Не удаляй MX и TXT SPF/DKIM/DMARC**, не перенаправляй чужие поддомены, не меняй NS: иначе может перестать работать корпоративная почта.
6. Подожди обновления DNS и выпуска HTTPS-сертификата, проверь `https://packaging.kz` и `https://www.packaging.kz`.

Если Netlify показывает `75.2.60.5` для `@` и `aesthetic-zabaione-9d9d34.netlify.app` для `www`, используй эти значения. **Приоритет у значений в Domain management твоего проекта.**

## 4. Добавление товаров и PNG через GitHub

Каталог: `content/catalog.json`. Изображения новых товаров: `content/images/` (PNG, JPG, JPEG, WebP). Документы: `content/documents/` (PDF).

В объекте нового товара укажи:
- `slug`, `title`, `category`, `status` (`draft` или `published`);
- состояние, наличие, цену, валюту, производителя, модель, полное описание;
- `translations` для `kk` и `en`;
- `specifications` со значениями `name/value`, `name_kk/value_kk`, `name_en/value_en`;
- `images: ["content/images/line-front.png", "content/images/line-side.png"]`.

Изменения в `main` автоматически разворачиваются на Netlify. Изображения отображаются без обрезки, переключаются каждые 5 секунд, при нажатии можно просмотреть полный размер. Для помощи в заполнении можешь присылать фото и описание в ChatGPT.

**Не загружай** `.env`, пароли, личные данные или список клиентов в публичный GitHub.

## 5. Безопасность

- Включи 2FA/passkey в **GitHub**, **Netlify** и **PS.kz**.
- В GitHub → Settings → Rules → Rulesets защити `main` и используй pull requests с зелёными тестами.
- Публичный Netlify-сайт не содержит Django Admin, базу данных, SMTP-секреты и пароль почты.
- Netlify Forms имеет встроенную защиту от спама; форма использует скрытое honeypot-поле. Следи за спамом и лимитами в Usage & billing.
- Пользуйся HTTPS, береги доступ к домену и почте, делай резервные копии ZIP и каталога.
- Перед запуском подтвердите политику обработки персональных данных (включая использование Netlify как стороннего провайдера).

## Локальная сборка

```powershell
git pull origin main
.\.venv\Scripts\python.exe scripts/build_static.py
.\.venv\Scripts\python.exe scripts/check_static.py
cd _site
py -m http.server 8008
```

Открой http://localhost:8008/ru/; форма Netlify Forms отправляет заявки только на реально размещённом Netlify-сайте.

Официальная документация:
- https://docs.netlify.com/manage/forms/setup/
- https://docs.netlify.com/manage/forms/notifications/
- https://docs.netlify.com/manage/domains/configure-domains/configure-external-dns/
