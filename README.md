Here is the English translation of your README.md. I have maintained the professional structure and formatting while ensuring the tone remains engaging.

---

# 🦕 The 80s Guy's Toolbox | AI.Fun

> **"AI Micro-Apps to Save Your Sanity"** — This is a minimalist, fun application navigation hub built on Streamlit, featuring a collection of practical yet "unconventional" AI and data visualization widgets.

## ✨ Core Features

* **Neal.fun Style Interaction**: Adopts a minimalist design philosophy, offering fluid card hover animations and intuitive icon navigation.
* **Globalization Support (I18n)**: Built-in comprehensive Chinese-English bilingual system supporting real-time, seamless switching.
* **Lightweight Traffic Analytics**: Implements local persistence based on SQLite to track daily PV (Page Views) and UV (Unique Visitors).
* **Tipping System 2.0**: A meticulously customized "Buy the Old Guy a Coffee" module, supporting preset/custom amounts, multi-platform payment switching, and dynamic calculation.
* **Dialog-Level Interaction**: Utilizes `st.dialog` to implement WeChat Official Account subscription and tipping features without interrupting the main page experience.
* **Deep CSS Customization**: Extensive modifications to Streamlit's native styles, removing redundant headers/footers to create a clean, single-page application.

## 🛠️ Technical Architecture

The core logic of this site consists of the following modules:

| Module | Implementation | Description |
| --- | --- | --- |
| **Persistence Layer** | SQLite3 | Stores daily traffic snapshots and unique visitor IDs. |
| **Frontend Style** | HTML/CSS Injection | Customizes Streamlit container layouts and card animations. |
| **State Management** | `st.session_state` | Manages language preferences, visitor IDs, and donation values across components. |
| **Multi-language** | Nested Dictionary | Manages static text resources. |

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-fun-toolbox.git
cd ai-fun-toolbox

```

### 2. Install Dependencies

```bash
pip install streamlit

```

### 3. Configure Assets

Ensure the following image files exist in the project root directory to guarantee the UI displays correctly:

* `qrcode_for_gh.jpg` (WeChat Official Account QR Code)
* `wechat_pay.jpg` (WeChat Pay QR Code)
* `ali_pay.jpg` (Alipay QR Code)

### 4. Launch Application

```bash
streamlit run app.py

```

## 📊 Traffic Statistics Model

The program identifies uniqueness via the visitor's `uuid`. The counting process is as follows:

1. **PV (Page Views)**: Updates the daily `pv_count` every time the page loads, provided `has_counted` has not been triggered for that session.
2. **UV (Unique Visitors)**:
* **New Visitor**: Inserts the `visitor_id` and their first visit date.
* **Returning Visitor**: Updates the `last_visit_date` field to ensure accurate daily UV calculation.



## 🪴 Developer's Note

The works collected here may not exactly be "productivity tools," but they represent the interesting possibilities of the AI era.

---

## ☕ Support the Author

If you enjoy these little gadgets, feel free to use the in-app tipping feature to buy the author a coffee and support the "80s Old Guy" in creating more content.

**License**: MIT

**Author**: 80后老登 (The 80s Guy)
