# My Cupra & VW Group (EU Data Act) - Home Assistant Integration

[![HACS Default](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/piaassek/My-Cupra-EU-Data-Act-?style=flat-square)](https://github.com/piaassek/My-Cupra-EU-Data-Act-/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dedykowana integracja dla **Home Assistant** obsługująca pojazdy **Cupra** (np. Cupra Born, Formentor, Leon) oraz grupy **Volkswagen** (VW, Skoda, Seat, Audi) za pośrednictwem oficjalnych serwerów **EU Data Act (EUDA)**.

Integracja pobiera telemetrię bezpośrednio z portalu EU Data Act grupy VW, eliminując zawodne i często blokowane stare API Cariad / OLA.

---

## ⚠️ Wymagania wstępne: Konfiguracja portalu EU Data Act (Prerequisites)

Zanim dodasz integrację do Home Assistant, **musisz jednorazowo skonfigurować żądanie danych w oficjalnym portalu VW Group EU Data Act**:

### 1. Logowanie do portalu EU Data Act
1. Otwórz w przeglądarce portal: **[https://eu-data-act.drivesomethinggreater.com/](https://eu-data-act.drivesomethinggreater.com/)**
2. Kliknij zielony przycisk **"Log in"**.
3. Wybierz swoją markę (np. **SEAT** – dotyczy również użytkowników marki **Cupra**, lub Volkswagen, Skoda, Audi) i kliknij **"Login"**, a następnie **"Continue"**.
4. Zaloguj się danymi swojego konta **My Cupra / Cupra ID** (lub odpowiednio VW ID / Skoda ID / SEAT ID).

### 2. Zezwolenie na dostęp i konfiguracja żądania danych
1. Po pomyślnym logowaniu nastąpi przekierowanie z powrotem do portalu EU Data Act z listą Twoich połączonych aut.
2. Kliknij **"Vehicle details"** przy swoim pojeździe.
3. Jeśli pojawi się monit, zezwól aplikacji **"My Data Portal"** na dostęp do danych pojazdu (*Data Sharing Consent*).
4. Przejdź do sekcji **"Get customised data"** i kliknij przycisk **"Request customised data"**.
5. Skonfiguruj nowe żądanie danych:
   - **Data clusters**: Wybierz **wszystkie klastry danych** (*All data clusters*).
   - **Interval**: Wybierz **15 minut** (*15 minutes*).
   - **Duration / Time limit**: Wybierz czas **nieograniczony** (*Unlimited / No end date*).
   - **Name**: Nazwij żądanie dowolnie (np. `All data 15mins`).
6. Zatwierdź żądanie i wyloguj się.

### 3. Oczekiwanie na wygenerowanie pierwszych plików danych
- Wygenerowanie pierwszych paczek danych przez serwery producenta zajmuje od kilku godzin do maksymalnie 24h.
- Po pewnym czasie zaloguj się ponownie na portal i wejdź w **"Vehicle details"** – gdy zobaczysz listę gotowych plików ZIP do pobrania, możesz przystąpić do konfiguracji integracji w Home Assistant.

---

## ✨ Kluczowe funkcje

- 🚀 **100% bezpośrednia komunikacja z EU Data Act (EUDA)** – stabilny dostęp do danych bez zależności od starego API OLA.
- 🔋 **Pełna telemetria baterii HV**:
  - Poziom naładowania baterii (SoC: %)
  - Zasięg elektryczny (km)
  - Docelowy limit ładowania (Target SoC: %)
  - Szacowany czas do zakończenia ładowania
  - **Maksymalna i minimalna temperatura ogniw baterii trakcyjnej (°C)** (dane dostępne w Cupra Born)
  - Stan podłączenia wtyczki i blokady gniazda ładowarki
- 🚗 **Przebieg i stan auta**:
  - Całkowity licznik przebiegu (Odometer)
  - Dni do najbliższego przeglądu/inspekcji
  - Stan zaparkowania i łączności online
  - Zamek centralny (Locked / Unlocked)
  - Dokładny timestamp ostatniej paczki telemetrii
- ❄️ **Klimatyzacja i ogrzewanie**:
  - Zadana temperatura klimatyzacji
  - Status klimatyzacji postojowej (OFF/HEATING/COOLING)
  - Podgrzewanie szyb (przód / tył)
  - Ogrzewanie lusterek zewnętrznych
- 🚪 **Drzwi, szyby i pokrywy**:
  - Stan pokrywy bagażnika i przedniej maski
  - Stan wszystkich 4 szyb (lewy/prawy przód, lewy/prawy tył)
- 📍 **Lokalizacja GPS (`device_tracker`)**:
  - Śledzenie pozycji zaparkowanego auta na mapie HA oraz strefy dom/praca
- 📊 **Statystyki podróży**:
  - Dystans, czas oraz średnie zużycie energii (krótko- i długoterminowe)
- 🔘 **Przycisk wymuszenia aktualizacji (`button`)**:
  - Możliwość natychmiastowego pobrania najświeższej paczki danych

---

## 📋 Lista udostępnianych encji (34 encje)

Wszystkie sensory posiadają ujednolicone prefiksy tematyczne, dzięki czemu na listach alfabetycznych w Home Assistant powiązane dane (np. dotyczące baterii, drzwi czy trasy) grupują się automatycznie obok siebie:

### 🔋 Bateria i Ładowanie
| Entity ID | Nazwa w HA | Jednostka / Klasa |
|---|---|---|
| `sensor.<car>_battery_level` | Bateria: Poziom naładowania | `%` (`battery`) |
| `sensor.<car>_electric_range` | Bateria: Zasięg | `km` (`distance`) |
| `sensor.<car>_target_soc` | Bateria: Docelowy limit ładowania | `%` (`battery`) |
| `sensor.<car>_charging_remaining_time` | Bateria: Czas do pełnego naładowania | `min` (`duration`) |
| `sensor.<car>_hv_battery_temperature_max` | Bateria HV: Maksymalna temperatura | `°C` (`temperature`) |
| `sensor.<car>_hv_battery_temperature_min` | Bateria HV: Minimalna temperatura | `°C` (`temperature`) |
| `binary_sensor.<car>_cable_connected` | Ładowanie: Kabel podłączony | `plug` |
| `sensor.<car>_plug_connection_state` | Ładowanie: Stan wtyczki | Tekst |
| `sensor.<car>_plug_lock_state` | Ładowanie: Blokada wtyczki | Tekst |

### 🚪 Drzwi, Okna i Zamki
| Entity ID | Nazwa w HA | Typ urządzenia |
|---|---|---|
| `binary_sensor.<car>_locked` | Drzwi: Zamek centralny | `lock` |
| `binary_sensor.<car>_trunk` | Drzwi: Bagażnik | `door` |
| `binary_sensor.<car>_hood` | Drzwi: Przednia maska | `opening` |
| `binary_sensor.<car>_window_front_left` | Okna: Szyba lewy przód | `window` |
| `binary_sensor.<car>_window_front_right` | Okna: Szyba prawy przód | `window` |
| `binary_sensor.<car>_window_rear_left` | Okna: Szyba lewy tył | `window` |
| `binary_sensor.<car>_window_rear_right` | Okna: Szyba prawy tył | `window` |

### ❄️ Klimatyzacja i Ogrzewanie
| Entity ID | Nazwa w HA | Jednostka / Typ |
|---|---|---|
| `sensor.<car>_climatisation_status` | Klimatyzacja: Status | Tekst |
| `sensor.<car>_target_climatisation_temperature` | Klimatyzacja: Zadana temperatura | `°C` (`temperature`) |
| `sensor.<car>_window_heating` | Klimatyzacja: Ogrzewanie szyb | Tekst |
| `binary_sensor.<car>_mirror_heating_enabled` | Klimatyzacja: Ogrzewanie lusterek | Binarny |

### 🚗 Status Pojazdu i Lokalizacja
| Entity ID | Nazwa w HA | Typ / Klasa |
|---|---|---|
| `sensor.<car>_odometer` | Status: Przebieg całkowity | `km` (`distance`) |
| `binary_sensor.<car>_is_parked` | Status: Zaparkowany | Binarny |
| `binary_sensor.<car>_is_online` | Status: Połączenie online | `connectivity` |
| `sensor.<car>_inspection_due_in` | Status: Dni do przeglądu | `d` (`duration`) |
| `sensor.<car>_last_update` | Status: Ostatnia aktualizacja | `timestamp` |
| `button.<car>_force_update` | Status: Wymuś aktualizację danych | `button` |
| `device_tracker.<car>` | Lokalizacja: Pozycja pojazdu | `device_tracker` |
| `sensor.<car>_parking_latitude` | Lokalizacja: Szerokość geograficzna | `°` |
| `sensor.<car>_parking_longitude` | Lokalizacja: Długość geograficzna | `°` |

### 📊 Statystyki Trasy
| Entity ID | Nazwa w HA | Jednostka |
|---|---|---|
| `sensor.<car>_last_short_length` | Trasa krótka: Dystans | `km` |
| `sensor.<car>_last_short_duration` | Trasa krótka: Czas trwania | `min` |
| `sensor.<car>_short_term_consumption` | Trasa krótka: Średnie zużycie energii | `kWh/100km` |
| `sensor.<car>_last_long_length` | Trasa długa: Dystans | `km` |
| `sensor.<car>_last_long_duration` | Trasa długa: Czas trwania | `min` |
| `sensor.<car>_long_term_consumption` | Trasa długa: Średnie zużycie energii | `kWh/100km` |

---

## 📥 Instalacja

### Opcja 1: Przez HACS (Zalecana)
1. Otwórz **HACS** w Home Assistant.
2. Kliknij trzy kropki w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (*Custom repositories*).
3. Wklej adres URL repozytorium: `https://github.com/piaassek/My-Cupra-EU-Data-Act-`
4. Wybierz typ: **Integracja** (*Integration*).
5. Kliknij **Dodaj**, a następnie znajdź **My Cupra (EU Data Act)** i kliknij **Pobierz**.
6. Zrestartuj Home Assistant.

### Opcja 2: Ręczna instalacja
1. Pobierz zawartość katalogu `custom_components/cupra_eu_data_act` z tego repozytorium.
2. Skopiuj folder `cupra_eu_data_act` do katalogu `/config/custom_components/` na swoim serwerze Home Assistant.
3. Zrestartuj Home Assistant.

---

## ⚙️ Konfiguracja

1. W Home Assistant przejdź do: **Ustawienia** ➔ **Urządzenia oraz usługi** ➔ **Integracje**.
2. Kliknij **+ Dodaj integrację** i wyszukaj **My Cupra (EU Data Act)**.
3. Wybierz markę (np. **cupra** lub **volkswagen**) oraz wprowadź swój e-mail i hasło do konta Cupra/VW.
4. Integracja automatycznie wykryje Twoje auto i utworzy wszystkie sensory oraz urządzenie.

---

---

## 🎨 Przykładowy widok Pulpitu (Lovelace Dashboard)

Możesz wkleić poniższy kod karty `entities` / `grid` bezpośrednio do swojego pulpitu w Home Assistant, aby uzyskać przejrzyste, pogrupowane kafelki z danymi pojazdu:

```yaml
type: vertical-stack
cards:
  - type: glance
    title: 🚗 Stan pojazdu
    entities:
      - entity: binary_sensor.cupra_<vin>_locked
      - entity: binary_sensor.cupra_<vin>_is_parked
      - entity: binary_sensor.cupra_<vin>_is_online
      - entity: sensor.cupra_<vin>_odometer

  - type: entities
    title: 🔋 Bateria i Ładowanie
    entities:
      - entity: sensor.cupra_<vin>_battery_level
      - entity: sensor.cupra_<vin>_electric_range
      - entity: sensor.cupra_<vin>_target_soc
      - entity: sensor.cupra_<vin>_charging_remaining_time
      - entity: sensor.cupra_<vin>_hv_battery_temperature_max
      - entity: sensor.cupra_<vin>_hv_battery_temperature_min
      - entity: binary_sensor.cupra_<vin>_cable_connected
      - entity: sensor.cupra_<vin>_plug_connection_state

  - type: entities
    title: 🚪 Drzwi i Okna
    entities:
      - entity: binary_sensor.cupra_<vin>_trunk
      - entity: binary_sensor.cupra_<vin>_hood
      - entity: binary_sensor.cupra_<vin>_window_front_left
      - entity: binary_sensor.cupra_<vin>_window_front_right
      - entity: binary_sensor.cupra_<vin>_window_rear_left
      - entity: binary_sensor.cupra_<vin>_window_rear_right

  - type: entities
    title: ❄️ Klimatyzacja i Ogrzewanie
    entities:
      - entity: sensor.cupra_<vin>_climatisation_status
      - entity: sensor.cupra_<vin>_target_climatisation_temperature
      - entity: sensor.cupra_<vin>_window_heating
      - entity: binary_sensor.cupra_<vin>_mirror_heating_enabled

  - type: entities
    title: 📊 Statystyki Trasy
    entities:
      - entity: sensor.cupra_<vin>_last_short_length
      - entity: sensor.cupra_<vin>_last_short_duration
      - entity: sensor.cupra_<vin>_short_term_consumption
      - entity: sensor.cupra_<vin>_last_long_length
      - entity: sensor.cupra_<vin>_last_long_duration
      - entity: sensor.cupra_<vin>_long_term_consumption
```

---

## 🔄 Historia wydań (Releases / Changelog)

### [1.0.6] - 2026-08-19
- 🔄 **Pełne odtwarzanie historii na starcie**: Naprawiono problem, w którym po restarcie Home Assistant pojedyncza nowa paczka telemetryczna z nocy (zawierająca tylko dane baterii/uśpienia) nadpisywała stan pamięci i powodowała status `nieznany` / `0.00 km` dla drzwi, szyb, zasięgu i lokalizacji. Teraz historia z `processed/` jest zawsze wczytywana jako baza przed nałożeniem nowych aktualizacji.
- 🎯 **Poprawka wartości brakujących**: Pola brakujące w danej paczce zwracają `None` zamiast fałszywych zer, a tracker GPS ignoruje współrzędne `(0.0, 0.0)`.

### [1.0.5] - 2026-08-19
- 🏷️ **Grupowanie tematyczne encji**: Wszystkie nazwy sensorów w języku polskim i angielskim otrzymały logiczne prefiksy tematyczne (`Bateria: ...`, `Drzwi: ...`, `Okna: ...`, `Klimatyzacja: ...`, `Ładowanie: ...`, `Status: ...`, `Trasa: ...`, `Lokalizacja: ...`), dzięki czemu na listach alfabetycznych w Home Assistant powiązane encje wyświetlają się zawsze razem.

### [1.0.4] - 2026-08-18
- 🇵🇱 **Wymuszenie polskich nazw encji**: Usunięto nadpisujące nazwy statyczne (`_attr_name`), dzięki czemu Home Assistant automatycznie tłumaczy wszystkie nazwy sensorów, sensorów binarnych, przycisków i trackera GPS na język polski (zgodnie z językiem interfejsu HA).

### [1.0.3] - 2026-08-18
- 🐛 **Poprawka sensorów binarnych**: Usunięto błąd `AttributeError: 'EUDABinarySensor' object has no attribute '_sensor_def'` blokujący ładowanie encji otwarcia drzwi, okien, zamka i stanu ładowania.
- 🇵🇱 **Pełna lokalizacja**: Dodano kompletne polskie (`pl.json`) oraz angielskie (`en.json`) nazwy dla wszystkich 34 encji.
- 🏷️ **Zmiana domeny integracji**: Oficjalna domena komponentu została ujednolicona na `cupra_eu_data_act`.
- 🛠️ **Poprawka Config Flow & Options Flow**: Usunięto błąd 500 (`Internal Server Error`) przy przeładowywaniu i opcjach integracji w nowszych wersjach Home Assistant (2024+ / 2025+).

### [1.0.2] - 2026-08-18
- 📦 Aktualizacja struktury repozytorium pod kątem HACS (`cupra_eu_data_act`).

### [1.0.1] - 2026-08-18
- 🚗 Wstępna obsługa modeli Cupra Born, Formentor, Leon oraz platformy MEB.

### [1.0.0] - 2026-08-18
- 🎉 Pierwsze oficjalne wydanie z obsługą protokołu EU Data Act (EUDA).

---

## 🔒 Prywatność i Bezpieczeństwo

- Dane logowania są wykorzystywane wyłącznie do bezpośredniej autoryzacji w oficjalnym portalu VW Group EU Data Act.
- Żadne dane, tokeny ani telemetria pojazdu nie są przesyłane na serwery zewnętrzne poza oficjalną chmurą producenta pojazdu.
- Wszystkie pliki sesji są przechowywane lokalnie w folderze danych Twojej instancji Home Assistant.

---

## 📄 Licencja

Projekt udostępniany na licencji [MIT](LICENSE).
