# TerapIA: Intelligent Post-Consultation Follow-up

TerapIA is an AI-powered medical agent designed to bridge the gap between clinical consultations and patient recovery. By processing medical instructions via voice and text, it generates structured clinical summaries, manages patient history, and ensures treatment adherence through proactive monitoring.

## 🌟 Key Features

- **Voice-to-Clinical Insights:** Transcribes medical audios using specialized models to generate structured summaries (Reasoning, Instructions, Warning Signs).

- **Context-Aware Follow-up:** Maintains long-term memory of patient history and recent interactions to provide personalized support without redundancy.

- **Proactive Care Agent:** An autonomous agent capable of scheduling reminders, updating patient records, and detecting clinical "red flags".

- **Professional Integration:** Seamlessly exports structured medical reports to healthcare professionals via email.

- **Observability-Driven:** Integrated tracing and evaluation to ensure the highest quality of medical responses.

## 🏗️ System Architecture

The project follows a modular, scalable architecture:

- **Core Engine:** Orchestrates the AI agent logic, audio processing pipelines, and prompt engineering.

- **Integrations:** Asynchronous connectors for Telegram (Telethon) and Persistent Storage (Supabase/PostgreSQL).

- **Observability Stack:** Real-time monitoring and evaluation via Opik to track agent traces and response quality.

- **Data Layer:** Dual-level management combining transient session memory with permanent clinical record persistence.

## 🔄 How It Works

1. **Medical Audio Processing**

   - **Identity Verification:** Automatic patient registration or retrieval from the database.

   - **Medical Transcription:** Audio is processed by a high-precision speech-to-text model specialized in technical medical jargon.

   - **Structured Analysis:** The AI agent analyzes the transcript to extract:
     - **Clinical Summary:** Key points of the consultation.
     - **Instructions & Treatment:** Clear, actionable steps for the patient.
     - **Warning Signs:** Specific symptoms that require immediate medical attention.

   - **Closing the Loop:** The patient receives the summary and can opt to send a formal report to their doctor.

2. **Conversational Support**

   - The agent utilizes the latest medical transcript and conversation history as context.

   - It provides natural language answers to patient doubts regarding their specific treatment.

   - Updates patient data or schedules reminders in real-time as the conversation evolves.

## 🧩 Agentic Capabilities (Tool Use)

The agent is equipped with a specialized toolkit to perform autonomous actions:

- **Reminders:** Schedules automatic notifications for medication or appointments.

- **Reporting:** Generates and dispatches professional clinical emails.

- **Data Management:** Updates patient clinical records directly in the database.

- **Clinical Coding:** Accesses international disease classification codes for accurate reporting.

## 🛠️ Tech Stack

- **Language:** Python (Asynchronous).

- **AI Orchestration:** OpenAI SDK & Agentic Frameworks.

- **Communication:** Telethon (Telegram API).

- **Database:** Supabase / PostgreSQL.

- **Observability:** Opik (Comet).

- **Email:** Professional SMTP services.

## 🚀 Future Roadmap: "Compliance-First"

To transition from a prototype to a certified Medical Device, TerapIA is moving toward:

- **HIPAA Compliance:** Implementing medical-grade security protocols and access audits.

- **Bunker Infrastructure:** Migration to Microsoft Azure OpenAI Service for private environments and Business Associate Agreement (BAA) support.

- **Native App:** Transitioning to a dedicated mobile application for total data sovereignty and biometric security.
