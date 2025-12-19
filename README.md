# 🏥 Pro-Hosp

**Pro-Hosp** es una plataforma predictiva para hospitales diseñada para **anticipar la demanda de pacientes**, optimizar recursos críticos y **reducir la saturación en salas de emergencia** mediante analítica avanzada y modelos de Machine Learning.

> ✨ *De la reacción a la anticipación.*

---

## 🚀 ¿Qué problema resuelve?

Muchos hospitales operan de forma **reactiva**:

* Esperan a que los pacientes lleguen
* Reaccionan cuando ya no hay camas
* Sobrecargan al personal en horas pico

Esto genera:

* Colapso en emergencias
* Uso ineficiente de camas y UCI
* Riesgo para la vida de los pacientes

**Pro-Hosp cambia este enfoque**, permitiendo **predecir escenarios futuros** y tomar decisiones con antelación.

---

## 🧠 ¿Qué hace Pro-Hosp?

* 📈 **Predicción de flujo de pacientes (24H)**
* 🏥 **Monitoreo de ocupación hospitalaria y UCI**
* 🛏️ **Gestión de camas y recursos críticos**
* ⚠️ **Alertas tempranas del sistema**
* 👤 **Predicciones a nivel paciente**
* 📊 **Dashboard interactivo en tiempo real**

Toda la data mostrada puede integrarse con modelos ML externos.

---

## 🖥️ Tecnologías utilizadas

### Frontend

* **Next.js (App Router)**
* **React + TypeScript**
* **TailwindCSS**
* **Chart.js** (Line & Doughnut charts)
* **Three.js / React Three Fiber** (visualización 3D)

### Backend (preparado para integración)

* API Routes de Next.js (`NextResponse`)
* Compatible con:

  * FastAPI
  * Python ML services
  * Microservicios externos

---

## 📊 Dashboard

El dashboard incluye:

* **KPIs principales**

  * Pacientes estimados hoy
  * Ocupación UCI
  * Camas disponibles

* **Gráficos**

  * Flujo de pacientes anticipado
  * Disponibilidad de recursos

* **Tabla predictiva**

  * Severidad
  * Diagnóstico
  * Estancia estimada
  * Riesgo de bloqueo

* **Sistema de alertas**

  * Picos de demanda
  * Insumos críticos
  * Estado del personal

---

## 📝 Formulario de Predicción

El sistema incluye un formulario para enviar datos estructurados como:

```json
{
  "Hospital_type": 1,
  "Hospital_city": 1,
  "Hospital_region": 1,
  "Available_Extra_Rooms_in_Hospital": 6,
  "Bed_Grade": 2.0,
  "Patient_Visitors": 1,
  "City_Code_Patient": 3,
  "Admission_Deposit": 2500,
  "Department": "radiotherapy",
  "Ward_Type": "R",
  "Ward_Facility": "A",
  "Type_of_Admission": "Urgent",
  "Illness_Severity": "Minor",
  "Age": "21-30"
}
```

Estos datos pueden enviarse a un modelo de ML para generar predicciones.

---

## 🔐 Autenticación

* Login y Register UI
* Preparado para:

  * JWT
  * OAuth
  * Autenticación hospitalaria

---

## 📦 Instalación

```bash
git clone https://github.com/Colertrash1721/ProHost.git
cd ProHost
npm install
npm run dev
```

Luego abre:

```
http://localhost:3000
```

---

## 🧩 Estructura del proyecto

```
src/
 ├─ app/
 │   ├─ page.tsx        # Landing
 │   ├─ dashboard/      # Dashboard principal
 │   ├─ auth/           # Login / Register
 │   └─ api/            # API Routes
 ├─ components/
 │   ├─ charts/
 │   ├─ forms/
 │   ├─ three/
 │   └─ ui/
 └─ hooks/
```

---

## 🧠 Filosofía

> *No se trata de reaccionar más rápido,
> sino de **no llegar tarde**.*

Pro-Hosp está pensado para **salvar tiempo, recursos y vidas**.

---

## 📄 Licencia

Proyecto en fase **demo / investigación**.
Licencia definida según despliegue final.

---

## ✨ Autor

Desarrollado con enfoque en **salud, tecnología e impacto real**.

💙 Pro-Hosp