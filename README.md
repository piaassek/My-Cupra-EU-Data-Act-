# My Cupra & VW Group (EU Data Act) - Home Assistant Integration

[![HACS Default](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/default)
[![GitHub Release](https://img.shields.io/github/v/release/WulfgarW/homeassistant-pycupra?style=flat-square)](https://github.com/WulfgarW/homeassistant-pycupra/releases)
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

### Sensory (`sensor`)
| Entity ID | Nazwa | Jednostka / Klasa |
|---|---|---|
| `sensor.<car>_battery_level` | Battery level | `%` (`battery`) |
| `sensor.<car>_electric_range` | Electric range | `km` (`distance`) |
| `sensor.<car>_odometer` | Odometer | `km` (`distance`) |
| `sensor.<car>_target_soc` | Target SoC | `%` (`battery`) |
| `sensor.<car>_charging_remaining_time` | Charging remaining time | `min` (`duration`) |
| `sensor.<car>_hv_battery_temperature_max` | HV Battery temperature max | `°C` (`temperature`) |
| `sensor.<car>_hv_battery_temperature_min` | HV Battery temperature min | `°C` (`temperature`) |
| `sensor.<car>_target_climatisation_temperature` | Target climatisation temperature | `°C` (`temperature`) |
| `sensor.<car>_climatisation_status` | Climatisation status | Tekst |
| `sensor.<car>_window_heating` | Window heating | Tekst |
| `sensor.<car>_plug_connection_state` | Plug connection state | Tekst |
| `sensor.<car>_plug_lock_state` | Plug lock state | Tekst |
| `sensor.<car>_inspection_due_in` | Inspection due in | `d` (`duration`) |
| `sensor.<car>_last_short_length` | Last short length | `km` |
| `sensor.<car>_last_short_duration` | Last short duration | `min` |
| `sensor.<car>_short_term_consumption` | Short term electric consumption | `kWh/100km` |
| `sensor.<car>_last_long_length` | Last long length | `km` |
| `sensor.<car>_last_long_duration` | Last long duration | `min` |
| `sensor.<car>_long_term_consumption` | Long term electric consumption | `kWh/100km` |
| `sensor.<car>_parking_latitude` | Parking latitude | `°` |
| `sensor.<car>_parking_longitude` | Parking longitude | `°` |
| `sensor.<car>_last_update` | Last Update | `timestamp` |

### Sensory binarne (`binary_sensor`)
| Entity ID | Nazwa | Typ urządzenia |
|---|---|---|
| `binary_sensor.<car>_is_parked` | Is Parked | Binarny |
| `binary_sensor.<car>_is_online` | Is Online | `connectivity` |
| `binary_sensor.<car>_locked` | Locked | `lock` |
| `binary_sensor.<car>_mirror_heating_enabled` | Mirror Heating Enabled | Binarny |
| `binary_sensor.<car>_trunk` | Trunk | `door` |
| `binary_sensor.<car>_hood` | Hood | `opening` |
| `binary_sensor.<car>_window_front_left` | Window Front Left | `window` |
| `binary_sensor.<car>_window_front_right` | Window Front Right | `window` |
| `binary_sensor.<car>_window_rear_left` | Window Rear Left | `window` |
| `binary_sensor.<car>_window_rear_right` | Window Rear Right | `window` |
| `binary_sensor.<car>_cable_connected` | Cable Connected | `plug` |

### Lokalizacja i Przyciski
| Entity ID | Platforma | Opis |
|---|---|---|
| `device_tracker.<car>` | `device_tracker` | Pozycja GPS pojazdu na mapie HA |
| `button.<car>_force_update` | `button` | Przycisk natychmiastowego wymuszenia aktualizacji danych |

---

## 📥 Instalacja

### Opcja 1: Przez HACS (Zalecana)
1. Otwórz **HACS** w Home Assistant.
2. Kliknij trzy kropki w prawym górnym rogu i wybierz **Niestandardowe repozytoria** (*Custom repositories*).
3. Wklej adres URL tego repozytorium GitHub.
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

## 🔒 Prywatność i Bezpieczeństwo

- Dane logowania są wykorzystywane wyłącznie do bezpośredniej autoryzacji w oficjalnym portalu VW Group EU Data Act.
- Żadne dane, tokeny ani telemetria pojazdu nie są przesyłane na serwery zewnętrzne poza oficjalną chmurą producenta pojazdu.
- Wszystkie pliki sesji są przechowywane lokalnie w folderze danych Twojej instancji Home Assistant.

---

## 📄 Licencja

Projekt udostępniany na licencji [MIT](LICENSE).
