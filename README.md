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
```text

| Branch                      | Purpose                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `main`                      | Final, stable branch. Protected. Only updated after all features are merged and tested.                      |
| `develop`                   | Integration branch. All feature branches are merged here first. App is tested end-to-end here before `main`. |
| `feature/preprocessing`     | Work for Preprocessing team (data cleaning, tokenization).                                                   |
| `feature/emotion-detection` | Work for Emotion team (train emotion model, prediction logic).                                               |
| `feature/intent-detection`  | Work for Intent team (train intent model, prediction logic).                                                 |
| `feature/response-engine`   | Work for Response + Context team (templates, response logic, conversation state).                            |
| `feature/app-integration`   | Work for App/Utils/Testing team (glue everything, run tests, main app).                                      |


```

