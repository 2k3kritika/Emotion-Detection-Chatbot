<!--
================================
FILE: README.md
================================
PURPOSE:
Primary documentation for the project.

TASKS FOR THIS FILE:
1. Explain project purpose.
2. Document folder structure.
3. Provide setup and run instructions.
4. Describe model workflow.

EXPECTED OUTPUT:
- Clear understanding for new developers.
- Smooth onboarding.

CONNECTED TO:
- Entire project

INTEGRATION NOTES:
- Update README when structure or flow changes.
- This is the first thing evaluators read.

OWNER:
Documentation Team

DO NOT:
- Leave outdated instructions
- Assume reader knows the code
================================
-->


# Emotion-Aware Chatbot 🤖

An intelligent, context-aware chatbot that understands **what users say** (intent) and **how they feel** (emotion), then responds accordingly like a well-adjusted piece of software.

No guesswork. No hard-coded replies pretending to be smart.

---

## 📌 Project Overview

The **Emotion-Aware Chatbot** is designed to simulate emotionally intelligent conversations by combining:

- **Emotion detection** (how the user feels)
- **Intent detection** (what the user wants)
- **Context management** (what has already happened)

Instead of replying blindly, the chatbot adapts its responses based on both **emotional state** and **conversational history**.

This project was **collaboratively built by a 10-member team** using a **modular architecture**, allowing parallel development, clean integration, and future scalability without chaos.

---

## 🎯 What This Chatbot Does

The chatbot performs the following tasks in sequence:

- Analyzes user input text
- Detects **emotion** (angry, sad, happy, neutral)
- Detects **intent** (greeting, help, complaint, etc.)
- Maintains conversation context across turns
- Selects an emotionally appropriate response
- Replies in a human-aware manner

No emotions are harmed during runtime.

---

## 🧠 Core Features

### 🔹 Text Preprocessing
- Lowercasing
- Noise removal
- Tokenization
- Vectorization

### 🔹 Emotion Classification
- Machine Learning based emotion prediction
- Multi-class classification
- Trained on emotion-labeled datasets

### 🔹 Intent Classification
- ML-based intent detection
- Supports extensible intent categories
- Uses labeled intent examples

### 🔹 Context Management
- Maintains conversational state
- Stores previous intents and emotions
- Prevents repetitive or tone-deaf responses

### 🔹 Response Engine
- Combines intent + emotion + context
- Chooses best-fit responses
- Easily extendable response logic

### 🔹 Modular Architecture
- Each component is isolated
- Easy to debug, test, and replace
- Designed for team-based development

---

## 🗂️ Folder Structure

```text
emotion_chatbot/
│
├── data/                       # Raw and processed datasets
│   ├── raw/                    # Original datasets
│   └── processed/              # Cleaned and vectorized data
│
├── models/                     # Trained ML models
│   ├── emotion_model.pkl       # Saved emotion classification model
│   └── intent_model.pkl        # Saved intent classification model
│
├── src/                        # Source code
│   ├── preprocessing/          # Text cleaning and tokenization
│   ├── emotion_detection/      # Emotion prediction logic
│   ├── intent_detection/       # Intent prediction logic
│   ├── context_manager/        # Conversation state handling
│   ├── response_engine/        # Response selection logic
│   ├── utils/                  # Helper utilities
│   └── app.py                  # Main application entry point
│
├── tests/                      # Unit and integration tests
│   ├── test_emotion.py         # Tests for emotion prediction
│   ├── test_intent.py          # Tests for intent prediction
│   └── test_response.py        # Tests for response selection
│
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore rules
```

---

## 🔄 System Workflow

1. User enters a message
2. Text is preprocessed
3. Emotion is predicted
4. Intent is predicted
5. Conversation context is updated
6. Best response is selected
7. Chatbot replies

No magic. Just logic. And models.

---

## 📊 Architecture & Data Flow (ASCII Diagram)

                    +----------------------+
                    |      User Input      |
                    +----------+-----------+
                               |
                               v
                    +------------------------------+
                    |     Text Preprocessing       |
                    |  - cleaning                  |
                    |  - tokenization              |
                    +----------+-------------------+
                               |
                               v
                    +----------------------+    +----------------------+
                    |    Emotion Model     |    |     Intent Model     |
                    |    (prediction)      |    |    (prediction)      |
                    +----------+-----------+    +----------+-----------+
                               |                           |
                               +-----------+---------------+
                                           |
                                           v
                    +--------------------------------------------+
                    |              Context Manager               |
                    |  - conversation history                    |
                    |  - previous states                         |
                    +-------------------+------------------------+
                                        |
                                        v
                    +--------------------------------------------+
                    |              Response Engine               |
                    |  - emotion-aware logic                     |
                    |  - intent-based responses                  |
                    +-------------------+------------------------+
                                        |
                                        v
                    +--------------------------------------------+
                    |               Chatbot Reply                |
                    +--------------------------------------------+
                    

---
## 🧪 Testing

Unit tests are written for:

- Emotion prediction accuracy
- Intent prediction accuracy
- Response selection logic
- Context handling

---
## Branch Definition


| Branch                      | Purpose                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `main`                      | Final, stable branch. Protected. Only updated after all features are merged and tested.                      |
| `develop`                   | Integration branch. All feature branches are merged here first. App is tested end-to-end here before `main`. |
| `feature/preprocessing`     | Work for Preprocessing team (data cleaning, tokenization).                                                   |
| `feature/emotion-detection` | Work for Emotion team (train emotion model, prediction logic).                                               |
| `feature/intent-detection`  | Work for Intent team (train intent model, prediction logic).                                                 |
| `feature/response-engine`   | Work for Response + Context team (templates, response logic, conversation state).                            |
| `feature/app-integration`   | Work for App/Utils/Testing team (glue everything, run tests, main app).                                      |

---

## Branches Clear Workflow

                     ┌───────────────┐
                     │     main      │  ← Protected, stable branch
                     └──────┬────────┘
                            │
                            │ merge after testing
                            ▼
                     ┌───────────────┐
                     │   develop     │  ← Integration branch
                     └──────┬────────┘
                            │
                            |
                            ▼                    
    ┌────────────────────────────────────────────────┐
    │            feature/preprocessing               │
    │            feature/emotion-detection           │ 
    │            feature/intent-detection            │ 
    │            feature/response-engine             │ 
    │            feature/app-integration             │
    └────────────────────────────────────────────────┘
                            │                 
                            ▼                  
                       Team pushes         
                    Pull Request → develop         

       After all feature branches tested will be merged into develop:
                            │
                            ▼
                     ┌───────────────┐
                     │     main      │  ← Merge develop into main
                     └───────────────┘

---
## ✅ Key points
 
1. main branch – final stable code, protected. Only updated after all features pass tests.

2. develop branch – integration branch. All feature branches merge here first to test together.

2. Feature branches – one per team:

    - feature/preprocessing → Team 1

    - feature/emotion-detection → Team 2

    - feature/intent-detection → Team 3

    - feature/response-engine → Team 4

    - feature/app-integration → Team 5

Pull Requests – each team pushes their feature branch as a PR to develop.

Final merge – after integration testing, develop merges into main.
---

---
## 📁 Team-folder ownership

| Team   | Branch                    | Folder Ownership                                                           | Who pushes |
| ------ | ------------------------- | -------------------------------------------------------------------------- | ---------- |
| Team 1 | feature/preprocessing     | `data/`, `src/preprocessing/`                                              | Team lead  |
| Team 2 | feature/emotion-detection | `src/emotion_detection/`, `models/emotion_classifier.pkl`                  | Team lead  |
| Team 3 | feature/intent-detection  | `src/intent_detection/`, `models/intent_classifier.pkl` & `vectorizer.pkl` | Team lead  |
| Team 4 | feature/response-engine   | `src/response_engine/`, `src/context_manager/`                             | Team lead  |
| Team 5 | feature/app-integration   | `src/app.py`, `src/utils/`, `tests/`, `requirements.txt`, `README.md`      | Team lead  |

---

## 📁 Every team AIM

NOTE: Everyone else in the team works locally / via Live Share, but the lead is the only one who pushes to the branch.

### **👩‍💻 Team 1: Data & Preprocessing Team**
**Folders they own**

```
data/
src/preprocessing/
```

**People**

* 1 Data Lead (pushes to GitHub)
* 1 Data Support (pair programming, cleaning, testing)

**Responsibilities**

* Prepare `emotions_dataset.csv` and `intents.json`
* Clean text data
* Generate `cleaned_text.csv`
* Encode labels → `labels_encoded.pkl`
* Ensure preprocessing functions are reusable by models

They stop working once:

* Text cleaning + tokenization is stable
* Other teams can import preprocessing without crying

---

### **🤖 Team 2: Emotion Detection Team**

**Folders they own**

```
src/emotion_detection/
models/emotion_classifier.pkl
```

**People**

* 1 Model Lead (pushes)
* 1 Model Support

**Responsibilities**

* Train emotion classification model
* Save trained model properly
* Implement emotion prediction logic
* Output standardized emotion labels: `angry`, `sad`, `happy`, `neutral`

They must NOT touch:

* App logic
* Intent logic
* Response wording

If their output is wrong, the chatbot feels emotionally illiterate. Social crime.

---

### **💬 Team 3: Intent Detection Team**

**Folders they own**

```
src/intent_detection/
models/intent_classifier.pkl
models/vectorizer.pkl
```

**People**

* 1 Intent Lead (pushes)
* 1 Intent Support

**Responsibilities**

* Train intent classifier
* Handle intent prediction
* Ensure vectorizer consistency
* Map user input → intent reliably

They coordinate with:

* Preprocessing team (for text input)
* Response team (intent names must match)

---

### **🗣️ Team 4: Response & Context Team**

**Folders they own**

```
src/response_engine/
src/context_manager/
```

**People**

* 1 Logic Lead (pushes)
* 1 Logic Support

**Responsibilities**

* Write emotion-aware response templates
* Build response selection logic
* Maintain conversation state
* Prevent robotic or tone-deaf replies

This team makes the chatbot feel human instead of a FAQ page.

---

### **🛠️ Team 5: App, Utils & Testing Team**

**Folders they own**

```
src/app.py
src/utils/
tests/
requirements.txt
README.md
.gitignore
```

**People**

* 1 Integration Lead (pushes)
* 1 QA / Support

**Responsibilities**

* Glue everything together
* Ensure clean imports
* Write and run tests
* Handle logging
* Make sure the app actually runs end-to-end

This team catches everyone else’s mistakes. They will be tired. Be kind.

---