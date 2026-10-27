# VideoClipper Web Client (Reconstructed)

Reverse engineered & reconstructed source code of [video-clipper.online](https://video-clipper.online) using **REA (Reverse Engineer Anything)**.

An online video trimming, cutting, and GIF-making web application featuring real-time Server-Sent Events (SSE) progress tracking, local client fingerprinting, and dynamic credit quota calculation.

---

## 📁 Repository Structure

```
.
├── index.html              # Main Video Clipper landing page
├── gif.html                # GIF Maker tool page
├── supported-sites.html    # Supported video platforms guide
├── faq.html                # Frequently Asked Questions accordion
├── contact.html            # Contact page
├── privacy.html            # Privacy policy
├── terms.html              # Terms of service
├── css/
│   └── styles.css          # Full responsive stylesheet
├── js/
│   ├── video-clipper.js    # Core video clipping engine (SSE, credit checks, form handler)
│   ├── gif.js              # GIF maker engine (dimension, FPS, loop, speed controls)
│   ├── main.js             # Navigation, mobile menu, affiliate rotations, Swiper
│   ├── faq.js              # INP-optimized FAQ accordion handler
│   └── site-notice.js      # Migration banner handler
├── images/
│   ├── icon-*.png          # Favicons and web app icons
│   └── preview.jpg         # OpenGraph preview card image
├── mock_server.py          # Local Python test server with mock API & SSE streaming
└── README.md
```

---

## ⚡ Tech Stack & Architecture

- **Frontend**: Vanilla ES6+ (Factory pattern, RAF batching), CSS3 Flexbox/Grid, Swiper.js v11, FontAwesome 6.4.
- **Backend Communication**: REST JSON APIs + Server-Sent Events (SSE) streaming for realtime job progress.
- **Server Architecture**: Go (Golang) microservice behind Caddy reverse proxy wrapping `yt-dlp` and `ffmpeg`.

---

## 🔌 API Endpoints Contract

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/credits` | Returns available credits and reset timestamp for `X-Client-FP` header. |
| `POST` | `/api/submit` | Submits video URL, start/end time, and quality. Returns `{"processId": "..."}`. |
| `POST` | `/api/gif/submit` | Submits video URL, start/end time, width, FPS, loops, and speed for GIF creation. |
| `GET` | `/api/progress/{processId}` | Persistent SSE connection streaming progress (`progress`, `complete`, `error`). |
| `GET` | `/api/cancel/{processId}` | Cancels active processing job. |

### Credit Calculation Formulas

**Video Trimming**:
$$\text{Cost} = \text{Rate}[\text{quality}] \times \frac{\text{duration in seconds}}{60}$$
- `480p`: 0.25 credits/min
- `720p`: 0.50 credits/min
- `1080p`: 1.00 credits/min
- `1440p`: 2.00 credits/min

**GIF Creation**:
$$\text{Cost} = \text{BaseCredit}[\text{width}] \times \frac{\text{duration}}{10} \times \text{Multiplier}[\text{FPS}] \times \text{Multiplier}[\text{speed}]$$
- Base width: 320px (`0.5`), 480px (`1.0`), 720px (`1.5`)
- FPS: 10 (`0.75`), 15 (`1.0`), 20 (`1.5`)
- Speed: 0.5x (`2.0`), 1.0x (`1.0`), 1.5x (`0.75`), 2.0x (`0.5`)

---

## 🚀 Running Locally

You can test the full user flow (including real-time progress simulation and download) using the bundled mock server:

```bash
# Run the mock server (Python 3 standard library only, no pip dependencies needed)
python3 mock_server.py
```

Then open your browser at:
```
http://localhost:8080
```

---

## 📄 License & Disclaimer

This project is a reverse-engineered reconstruction for educational, analytical, and interoperability purposes. Original intellectual property belongs to VideoClipper / Mohamed Hesham.
