# TerapIA

Bot de Telegram que procesa consultas médicas mediante audio, genera resúmenes estructurados y gestiona historiales clínicos utilizando inteligencia artificial.

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado en módulos principales:

- **Core**: Contiene la lógica principal del bot, el agente de IA, procesamiento de audio, plantillas y utilidades
- **Integrations**: Módulos de conexión con servicios externos (Telegram y base de datos)
- **Observability**: Herramientas para monitoreo, evaluación y optimización del sistema
- **Audios**: Directorio donde se almacenan temporalmente los archivos de audio recibidos

## 🔄 Flujo de Funcionamiento

### Procesamiento de Consultas Médicas por Audio

Cuando un usuario envía un audio:

1. El sistema verifica si el usuario está registrado en la base de datos. Si no existe, crea un nuevo registro automáticamente.
2. El audio se descarga y se almacena temporalmente en el sistema.
3. El audio se transcribe a texto utilizando un modelo de reconocimiento de voz.
4. La transcripción se guarda en el historial clínico del paciente y se almacena como la última consulta procesada.
5. Se construye un contexto con los datos del paciente y la transcripción de la consulta.
6. El agente de IA procesa esta información y genera un resumen estructurado que incluye:
   - Motivo de consulta
   - Indicaciones médicas
   - Pautas de alarma
7. El resumen se envía al usuario y se ofrece la opción de enviarlo al médico tratante.

### Procesamiento de Mensajes de Texto

Cuando un usuario envía un mensaje de texto:

1. Se verifica la identidad del usuario de la misma manera que en el flujo de audio.
2. Se construye un contexto que incluye:
   - La última consulta médica procesada (si existe)
   - Los datos del paciente
   - El mensaje actual
   - El historial reciente de la conversación
3. El agente responde de forma contextual, manteniendo la conversación natural sin repetir información ya proporcionada.
4. Se actualiza el historial de conversación para mantener el contexto en futuras interacciones.

## 🧩 Componentes Principales

### Módulo Principal

Gestiona la comunicación con Telegram y coordina todos los procesos. Maneja dos tipos de eventos: mensajes de audio y mensajes de texto. Mantiene en memoria el historial de conversaciones recientes y las últimas transcripciones procesadas para cada usuario.

### Agente de Inteligencia Artificial

Sistema de IA que procesa las consultas médicas y genera respuestas estructuradas. Utiliza un modelo de lenguaje avanzado y tiene acceso a herramientas especializadas que le permiten:

- Programar recordatorios médicos personalizados
- Actualizar información del paciente
- Enviar mensajes por Telegram
- Enviar informes médicos por email
- Consultar códigos de clasificación médica

El agente opera con instrucciones específicas para evitar procesamiento innecesario y mantener un flujo de conversación natural.

### Procesador de Audio

Convierte los archivos de audio recibidos en texto mediante reconocimiento de voz. Utiliza un modelo especializado en transcripción médica para garantizar precisión en términos técnicos.

### Gestión de Base de Datos

Módulo responsable de almacenar y recuperar información de pacientes:

- **Información del usuario**: Datos personales básicos (nombre, apellido, edad)
- **Historial clínico**: Registro completo de todas las consultas médicas con sus fechas
- **Última transcripción**: Referencia rápida a la consulta más reciente

### Utilidades de Usuario

Sistema que verifica si un usuario está registrado en el sistema y crea nuevos registros automáticamente cuando un usuario interactúa por primera vez con el bot.

### Herramientas del Agente

Conjunto de capacidades que el agente puede utilizar para realizar acciones:

- **Envío de emails**: Permite enviar informes médicos estructurados al médico tratante
- **Mensajería**: Envía mensajes directos por Telegram
- **Recordatorios**: Programa notificaciones automáticas para el paciente
- **Actualización de datos**: Modifica información del paciente en la base de datos
- **Consulta de códigos médicos**: Obtiene códigos de clasificación internacional de enfermedades

## 🔌 Integraciones

### Telegram

Plataforma de mensajería donde opera el bot. El sistema se conecta mediante un cliente asíncrono que permite recibir mensajes en tiempo real y responder a los usuarios.

### Base de Datos

Sistema de almacenamiento persistente que guarda toda la información de los pacientes, incluyendo sus historiales clínicos completos. Utiliza una estructura que permite almacenar múltiples consultas por paciente con sus respectivas fechas.

### Servicios de IA

Proveedor de modelos de inteligencia artificial que se utilizan para:
- Procesar y entender las consultas médicas
- Generar respuestas estructuradas
- Transcribir audio a texto

### Sistema de Observabilidad

Plataforma que permite monitorear el funcionamiento del agente, almacenar las interacciones y optimizar el rendimiento del sistema mediante análisis de datos.

### Servicio de Email

Sistema externo que permite enviar emails estructurados a médicos tratantes con la información de las consultas procesadas.

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **Cliente de Telegram**: Biblioteca para comunicación asíncrona con Telegram
- **Framework de Agentes**: Sistema para crear agentes de IA con capacidades de herramientas
- **API de IA**: Servicios de modelos de lenguaje y transcripción de voz
- **Base de Datos**: Sistema de almacenamiento de datos relacional
- **Observabilidad**: Herramientas para monitoreo y análisis
- **Servicios de Email**: Plataformas para envío de correos electrónicos

## 📊 Gestión de Estado

El sistema maneja información en dos niveles:

1. **Memoria Temporal**: Almacena datos que se necesitan durante la sesión activa, como el historial reciente de conversación y las últimas transcripciones procesadas. Esta información se mantiene solo mientras el sistema está en ejecución.

2. **Persistencia Permanente**: Almacena en la base de datos toda la información que debe perdurar, incluyendo los datos del paciente, el historial clínico completo y las transcripciones de todas las consultas.

## 🔄 Lógica del Agente

El agente de IA opera de manera inteligente según el contexto:

- **Modo Consulta Médica**: Se activa cuando se recibe un audio nuevo. Valida la información del paciente, procesa la consulta y genera un resumen médico estructurado. Ofrece enviar el informe al médico tratante.

- **Modo Conversación**: Se activa cuando se recibe un mensaje de texto. Responde de forma natural y contextual, utilizando la información de consultas previas cuando es relevante, pero sin repetir resúmenes ya proporcionados.

El sistema está diseñado para evitar procesamiento redundante y mantener conversaciones fluidas, activándose solo cuando hay nueva información que procesar o cuando el usuario solicita algo específico.
