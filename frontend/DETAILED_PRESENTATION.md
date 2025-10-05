# TerraGrow Academy – 3D Satellite Farming Experience  
### By OrbitSowers Labs – NASA Space Apps Challenge 2025, Montréal  

---

## 1. Vision

TerraGrow Academy is a 3D web experience that transforms NASA satellite data into an immersive educational game.  
Our goal is to connect space science with agricultural sustainability by showing how satellite data can guide real farming decisions about water, climate, and soil management.  
We believe precision agriculture should be **accessible, visual, and inspiring**.

---

## 2. Concept

Players explore Earth through an **interactive 3D globe**, select real regions (e.g., Cameroon, Canada, India), and view live climate data from the **NASA POWER API** — temperature, humidity, and precipitation.  
They then choose a crop (wheat, corn, rice, tomato, etc.) and make weekly decisions about irrigation and fertilization.  
Behind the scenes, the engine runs **water balance and NDVI growth models** to simulate plant health and productivity.  
At the end of 12 virtual weeks, the player receives results showing yield, sustainability, and resource efficiency.

---

## 3. Technical Structure

- **Backend**: Python + Flask  
  - REST APIs (`/api/init`, `/api/action`, `/api/harvest`)  
  - Simulation of NDVI and soil moisture  
  - Real-time climate data from NASA POWER  
- **Frontend**: React + Three.js (React Three Fiber)  
  - Animated 3D globe with orbiting satellite  
  - Realistic 3D field scene (GLB models from Sketchfab)  
  - Open-source textures (Solar System Scope, Poly Haven)  
  - HUD interface displaying NDVI, humidity, and budget  

This architecture bridges **scientific accuracy and smooth WebGL rendering**, maintaining ~60 FPS on desktop.

---

## 4. Scientific Logic

The simulation relies on simplified yet realistic equations:
\[
M_{t+1} = M_t + P + I - ET - D
\]
\[
NDVI_{t+1} = NDVI_t + f(M, N, T)
\]
where M = soil moisture, N = nitrogen, and T = temperature.  
Each weekly decision affects NDVI growth, yield, and sustainability, helping players understand the cause-and-effect relationships behind data-driven farming.

---

## 5. Long-Term Vision

TerraGrow is designed as a **global learning platform**, combining real Earth observation data, machine learning, and interactive visualization.  

Next steps include:
- AI-driven recommendations for irrigation and fertilizer  
- Mobile and AR versions for classrooms  
- Regional leaderboards and open data dashboards  
- Partnerships with NGOs and institutions (FAO, NASA Harvest)

---

## 6. Impact

TerraGrow makes the invisible visible — transforming satellite data into an experience anyone can understand.  
It helps students, farmers, and citizens grasp how NASA’s Earth observation contributes to smarter, more sustainable agriculture.  
Our mission is to **turn data into experience, and science into understanding.**

> Cultivating the future through the eyes of NASA.
