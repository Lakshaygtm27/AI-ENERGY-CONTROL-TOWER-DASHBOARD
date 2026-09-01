# Streaming Data Pipeline - Quick Start Guide

## 🚀 Overview

This guide shows you how to stream data from multiple sources through Kafka and display it in real-time.

**Data Sources:**
- 🌤️ **Open-Meteo** (Free weather API - 10 Indian cities)
- 📊 **Synthetic India** (Realistic energy demand patterns - 5 regions)
- 📡 **Real-time Display** (Color-coded console output)

**Expected Data:**
- Demand, generation, renewable %, pricing
- Weather (temperature, humidity, wind speed)
- Real-time updates every 5 seconds

---

## 📋 Prerequisites

1. **Docker & Docker Compose** installed
2. **Python 3.9+** with virtual environment active
3. **Kafka running** (via Docker Compose)

---

## ⚡ Quick Start (3 Steps)

### Step 1: Start Docker Infrastructure

```bash
# Navigate to project root
cd /home/lakshay/AI-Energy-Control-Tower

# Start all services (Kafka, PostgreSQL, etc.)
docker-compose up -d

# Wait 30 seconds for services to initialize
sleep 30

# Verify services are running
docker-compose ps
```

**Expected output:**
```
NAME                           STATUS
energy-tower-zookeeper        Up (healthy)
energy-tower-kafka             Up (healthy)
energy-tower-postgres          Up (healthy)
energy-tower-kafka-ui          Up
energy-tower-adminer           Up
energy-tower-app               Up (healthy)
```

### Step 2: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installations
python -c "import kafka; import requests; print('✅ Dependencies OK')"
```

### Step 3: Start Streaming Data

```bash
# Run the master streaming script
python stream_all_data.py localhost:9092 300

# or for continuous streaming:
python stream_all_data.py localhost:9092
```

**What happens:**
1. Opens 2 producer processes (weather + energy)
2. Opens 1 display consumer process
3. Shows live data in console with colors

**Expected output:**
```
╔════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                    ║
║ 🚀 AI ENERGY CONTROL TOWER - STREAMING DATA PIPELINE 🚀                                         ║
║                                                                                                    ║
║ Streaming all data sources through Kafka in real-time                                            ║
║                                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════╝

🌤️  STARTING OPEN-METEO WEATHER PRODUCER
✅ Open-Meteo producer started (PID: 12345)

📊 STARTING SYNTHETIC INDIA ENERGY PRODUCER
✅ Synthetic producer started (PID: 12346)

📺 STARTING REAL-TIME DATA DISPLAY
✅ Display consumer started (PID: 12347)

13:45:23 [open-meteo] 🌤️  WEATHER | Delhi        |   32.5°C | Humidity:  65% | Wind: 12.3 km/h
13:45:24 [synthetic] 📈 DEMAND | North        |     35,234 MW | Hour: 13:00
13:45:25 [synthetic] ☀️  GENERATION | South        | Solar          |      1,245 MW
13:45:26 [synthetic] 🔋 RENEWABLE | North        | Solar: 2,345 MW | Wind: 3,456 MW | Hydro:   4,567 MW
13:45:27 [synthetic] 💰 PRICE | North        |    4.25 INR/MWh | Volume:      5,432 MWh
```

---

## 🎯 Individual Producer/Consumer Startup

If you want to run producers separately:

### Run Open-Meteo Producer Only

```bash
python -m energy_kafka.producers.openmeteo_producer localhost:9092 300
```

**Output:**
```
🌤️  Fetching weather data from Open-Meteo...
✅ Weather data for Delhi: 32.5°C
✅ Weather data for Mumbai: 28.3°C
...
Weather cycle complete: 10 successful, 0 failed
```

### Run Synthetic India Producer Only

```bash
python -m energy_kafka.producers.synthetic_india_producer localhost:9092 300
```

**Output:**
```
🚀 Starting Synthetic India producer (interval: 5s)
================================================================================
Cycle 1 - 2026-09-01T13:45:23.456Z
================================================================================
📊 Cycle 1 - North: 35234.56MW @ 13:00
Generated: 35 generation + 5 renewable + 5 price messages
```

### Run Display Consumer Only

```bash
python -m energy_kafka.consumers.display_consumer --bootstrap-servers localhost:9092
```

**Displays all topics in real-time**

---

## 🌍 Data Sources Overview

### Weather Data (Open-Meteo)

Covers 10 Indian cities:

| City | Region | Coordinates |
|------|--------|------------|
| Delhi | North | 28.6139°N, 77.2090°E |
| Mumbai | West | 19.0760°N, 72.8777°E |
| Bangalore | South | 12.9716°N, 77.5946°E |
| Chennai | South | 13.0827°N, 80.2707°E |
| Kolkata | East | 22.5726°N, 88.3639°E |
| Hyderabad | South | 17.3850°N, 78.4867°E |
| Pune | West | 18.5204°N, 73.8567°E |
| Ahmedabad | West | 23.0225°N, 72.5714°E |
| Jaipur | North | 26.9124°N, 75.7873°E |
| Lucknow | North | 26.8467°N, 80.9462°E |

**Fields per message:**
- Temperature, humidity, wind speed, cloud cover
- Solar radiation, pressure, UV index
- Data source: "open-meteo"

### Energy Data (Synthetic India)

Generates realistic patterns for 5 regions:

| Region | Base Load | Peak Hour | Notes |
|--------|-----------|-----------|-------|
| North | 35,000 MW | 19:00 | High demand |
| South | 25,000 MW | 18:00 | Industrial heavy |
| East | 20,000 MW | 20:00 | Moderate |
| West | 28,000 MW | 19:00 | High demand |
| Northeast | 5,000 MW | 19:00 | Low demand |

**Simulated patterns:**
- Hourly demand variations (peaks at 18-22)
- Seasonal factors (summer/winter/monsoon)
- Weekend effects (-5% demand)
- Solar (0 at night, peaks at noon)
- Wind (variable, higher at night)
- Pricing correlates with demand

---

## 📊 Kafka Topics

All topics created automatically with these settings:

```
Topic Name                  Partitions   Retention
─────────────────────────   ──────────   ─────────
weather                     3            7 days
energy_demand              3            7 days
power_generation           3            7 days
renewable_generation       3            7 days
electricity_price          3            7 days
energy_alerts              3            7 days
forecast_results           3            7 days
```

### Topic Structure

Each message is JSON with these fields:

**Weather message:**
```json
{
  "timestamp": "2026-09-01T13:45:23.456Z",
  "location": "Delhi",
  "temperature_celsius": 32.5,
  "humidity_percent": 65,
  "wind_speed_kmh": 12.3,
  "cloud_cover_percent": 45,
  "data_source": "open-meteo"
}
```

**Demand message:**
```json
{
  "timestamp": "2026-09-01T13:45:23.456Z",
  "region": "North",
  "demand_mw": 35234.56,
  "hour_of_day": 13,
  "day_of_week": 2,
  "is_holiday": false,
  "data_source": "synthetic"
}
```

---

## 🔍 Real-Time Display Format

Console output with color coding:

```
TIME      [SOURCE]    MESSAGE
─────────────────────────────────────────────────────────
13:45:23  [open-meteo] 🌤️  WEATHER | Delhi        |   32.5°C | Humidity:  65% | Wind: 12.3 km/h
13:45:24  [synthetic]  📈 DEMAND | North        |     35,234 MW | Hour: 13:00
13:45:25  [synthetic]  ☀️  GENERATION | South        | Solar          |      1,245 MW
13:45:26  [synthetic]  🔋 RENEWABLE | North        | Solar: 2,345 MW | Wind: 3,456 MW | Hydro: 4,567 MW | Total: 23.4%
13:45:27  [synthetic]  💰 PRICE | North        |    4.25 INR/MWh | Volume:      5,432 MWh
```

**Color Key:**
- 🔵 Open-Meteo: Cyan
- 🟢 Synthetic: Green
- 🟡 ENTSO-E: Yellow
- 🟣 IEX: Magenta
- 🔷 CEA: Blue

---

## 🛑 Stopping the Pipeline

Press `Ctrl+C` to stop all services gracefully:

```
🛑 STOPPING ALL SERVICES...
Stopping process 1 (PID: 12345)...
  ✓ Process 1 stopped
Stopping process 2 (PID: 12346)...
  ✓ Process 2 stopped
Stopping process 3 (PID: 12347)...
  ✓ Process 3 stopped

✅ ALL SERVICES STOPPED
```

---

## 🔧 Troubleshooting

### Producer won't connect

```bash
# Check if Kafka is running
docker-compose ps kafka
# Should show: energy-tower-kafka  Up (healthy)

# If not healthy, restart:
docker-compose restart kafka
sleep 10
```

### Display not showing data

```bash
# Check if Kafka has data
docker-compose exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic weather \
  --from-beginning \
  --max-messages 5

# Check consumer group
docker-compose exec kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group real-time-display \
  --describe
```

### Port conflicts

If ports are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "9092:9092"  # Change first number (e.g., 9095:9092)
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

---

## 📈 Performance Metrics

Typical throughput:

| Source | Messages/min | Payload | Topics |
|--------|-------------|---------|--------|
| Weather | 10 (1/city/min) | ~800 bytes | 1 |
| Synthetic | 25 (5 regions × 5 types) | ~500 bytes | 4 |
| **Total** | **~300/min** | **~400 KB** | **5** |

Network usage: ~2.4 MB/hour

---

## 🎓 Next Steps

1. **Store in Database** (Phase 6)
   ```python
   # Consumer that writes to PostgreSQL
   python -m energy_kafka.consumers.energy_consumer
   ```

2. **Run Analytics** (Phase 7)
   ```python
   # Baseline calculation and anomaly detection
   python -m analytics.baseline_engine
   ```

3. **Forecasting** (Phase 8)
   ```python
   # ARIMA + Prophet models
   python -m analytics.forecast_engine
   ```

4. **Dashboard** (Phase 9)
   ```bash
   # Power BI or Streamlit visualization
   streamlit run dashboard/app.py
   ```

---

## 📚 Documentation

- **Docker Setup**: See [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Architecture**: See [ENTERPRISE_BUILD_PLAN.md](ENTERPRISE_BUILD_PLAN.md)
- **API Docs**: Visit http://localhost:8000/api/docs (when app is running)

---

## 💬 Questions?

Check logs:
```bash
# All producer logs
python -m energy_kafka.producers.openmeteo_producer 2>&1 | tail -20

# All consumer logs
python -m energy_kafka.consumers.display_consumer 2>&1 | tail -20

# Docker logs
docker-compose logs -f
```

---

**Happy Streaming! 🚀**

*Last Updated: September 1, 2026*
