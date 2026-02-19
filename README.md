# 🧬 PharmaGuard - Pharmacogenomic Risk Prediction System

AI-powered precision medicine platform that analyzes patient genomic VCF data to predict drug-specific pharmacogenomic risks and generate explainable clinical recommendations.

---

## 🚀 Live Demo

🌐 App: **Add Render Link Here**

🎥 LinkedIn Demo Video: **Add LinkedIn Video Link Here**

---

## 🏗 Architecture Overview

PharmaGuard follows a modular clinical decision pipeline:

```
VCF Upload
   ↓
Variant Extraction
   ↓
Genotype → Phenotype Mapping
   ↓
Drug Risk Detection Engine
   ↓
Recommendation Engine (CPIC-aligned)
   ↓
LLM Explanation Layer
   ↓
Structured JSON + UI Dashboard
```

### Key Layers

* **Data ingestion** — VCF parsing
* **Inference layer** — genotype → phenotype
* **Decision layer** — drug risk classification
* **Explainability layer** — LLM clinical reasoning
* **Presentation layer** — dashboard + JSON export

---

## 🛠 Tech Stack

### Backend

* Python
* Flask

### AI / Explainability

* Gemini API
* OpenAI API (fallback)

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Data

* VCF (Variant Call Format)

### Deployment

* Render

---

## 📦 Installation Instructions

### 1. Clone repository

```bash
git clone <repo-url>
cd pharmaguard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create environment file

Create `.env`:

```
GEMINI_API_KEY=
OPENAI_API_KEY=
SECRET_KEY=
```

### 4. Run locally

```bash
python app.py
```

Open:

```
http://localhost:5000
```

---

## 🔌 API Documentation

### POST `/analyze`

Analyzes uploaded VCF and drug input.

**Request**

* Multipart form

  * vcf_file
  * drug_name

**Response**
Returns structured JSON:

```json
{
  "patient_id": "",
  "drug": "",
  "risk_assessment": {},
  "pharmacogenomic_profile": {},
  "clinical_recommendation": {},
  "llm_generated_explanation": {},
  "quality_metrics": {}
}
```

---

## ▶️ Usage Examples

### Example Workflow

1. Upload VCF file
2. Select drug
3. Run analysis
4. View:

   * Risk label
   * Phenotype
   * Recommendation
   * AI reasoning
5. Export JSON

---

### Example Clinical Scenario

**Input**

* CYP2C19 poor metabolizer
* Drug: Clopidogrel

**Output**

* Risk: Ineffective
* Recommendation: Alternative antiplatelet therapy
* Explanation: Mechanistic reasoning via LLM

---

## 📸 Interface Preview

Add screenshots here:

```
docs/images/input.png
docs/images/dashboard.png
docs/images/ai_panel.png
```

---

## 🧠 Explainable AI Approach

* Prediction is rule-based
* Explanation uses LLM with structured clinical context
* Ensures transparency and reproducibility

---

## 👥 Team Members

Bhanu Prakash

Sree Harshini

---

