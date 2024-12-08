# 📈 Pelusa BackEnd AlarmHugger - Public

## 🗂️ Table of Contents
1. [General Overview](#-1-general-overview)  
2. [Key Features](#-2-key-features)  
3. [Technologies Used](#-3-technologies-used)  
4. [Directory Structure](#-4-directory-structure)  
5. [API Structure](#-5-api-structure)  
6. [Development Cycle](#-6-development-cycle)  
7. [Installation & Setup](#-7-installation--setup)  
8. [Usage](#-8-usage)  
9. [Testing](#-9-testing)  
10. [Contributing](#-10-contributing)  
11. [License](#-11-license)
12. [Contact](#12-contact)

---

## 🧭 1. General Overview

**Project Name:** Pelusa BackEnd AlarmHugger - Public

**Description:**  
The **Pelusa BackEnd AlarmHugger** is a backend service responsible for handling and managing alarms triggered by **TradingView**. The service processes alarms and stores them in a **SiteGround-hosted database**. It is built using **FastAPI** and offers a **modular architecture** with support for:  
- IP whitelisting for security  
- Logging with **Loguru**  
- Exception handling for stable performance  

The AlarmHugger receives webhook requests, processes the incoming alarm, and stores the data in the database for later use by other services. It also supports retrieving alarms via API, filtering, and querying for the latest entries.

---

## 🚀 2. Key Features

- **Webhook Handling**: Processes incoming alarms from TradingView via a webhook.  
- **Database Storage**: Stores alarms in the **SiteGround database** for persistence.  
- **IP Filtering**: Uses IP whitelisting and blocking to ensure only allowed IPs can interact with the system.  
- **Error Handling**: Provides structured error handling to return meaningful HTTP responses.  
- **Logging**: Uses **Loguru** for logging requests, responses, and system events.  
- **CRUD Operations**: Provides endpoints to create, retrieve, and filter alarms.  
- **Health Checks**: Provides an endpoint for server health checks to verify system status.  

---

## 🛠️ 3. Technologies Used

**Core Technologies**
- **Language**: Python 3+  
- **Framework**: FastAPI  
- **Web Server**: Uvicorn (development) + Gunicorn (production)  
- **Database**: MySQL (hosted on SiteGround)  
- **ORM**: SQLAlchemy  
- **Security**: IP filtering, exception handling, and SSL certificates  

**Libraries & Tools**
- **SQLAlchemy**: ORM for defining and interacting with the alarms database.  
- **Loguru**: Advanced logging for tracking requests, responses, and errors.  
- **Pydantic**: Data validation and serialization for API request/response models.  
- **Uvicorn**: ASGI server for development.  
- **Gunicorn**: WSGI server for production deployment.  

---

## 📂 4. Directory Structure
```bash
Pelusa-BackEnd-AlarmHugger/ 
├── pytest.ini 
├── requirements.txt 
├── run.py 
├── app/ 
│ ├── alarms/ 
│ │ ├── init.py 
│ │ ├── models.py 
│ │ ├── repositories.py 
│ │ ├── routes.py 
│ │ ├── schemas.py 
│ │ └── utils.py 
│ ├── config.py 
│ ├── main.py 
│ ├── server/ 
│ │ ├── init.py 
│ │ ├── middlewares.py 
│ │ └── routes.py 
│ ├── siteground/ 
│ │ ├── init.py 
│ │ ├── base.py 
│ │ └── database.py 
│ └── utils/ 
│ ├── init.py 
│ ├── ip_check.py 
│ ├── server_status.py 
│ └── services.py 
├── Docs/ 
├── logs/ 
└── tests/
```

**Key Folders**
- **alarms/**: Handles the core logic for alarm processing, including parsing, saving, and querying alarms.  
- **server/**: Contains middlewares and routes for server health checks, IP filtering, and logging.  
- **siteground/**: Database connection logic and models for the **SiteGround-hosted database**.  
- **utils/**: Utility functions for IP checks, server status, and services.  

---

## 📡 5. API Structure

**Main Endpoints**

| **Endpoint**         | **Method** | **Description**                      |
|---------------------|------------|--------------------------------------|
| `/alarms/webhook`    | **POST**   | Receives and processes alarms from TradingView |
| `/server/status-server` | **GET** | Returns server and database health status |

---

## 📐 6. Development Cycle

**Building Cycle**
1. **Requirements Specification**: Define the alarms' models, API routes, and endpoints.  
2. **Logic Design**: Design controllers, routes, and services for processing alarms.  
3. **Data Design**: Create SQLAlchemy models and Pydantic schemas for request validation.  
4. **Implementation**: Write controller, route, and service logic.  
5. **Testing**: Write unit tests and integration tests using **Pytest**.  

**Consolidate Cycle**
1. **Documentation**: Use OpenAPI docs for documenting all endpoints.  
2. **Code Review & Refactoring**: Review and optimize code for performance and security.  
3. **Integration & Deployment**: Deploy to **AWS EC2** with connection to SiteGround databases.  

---

## ⚙️ 7. Installation & Setup

**Clone the Repository**
```bash
git clone https://github.com/username/backend-alarmhugger.git
cd backend-alarmhugger
```
**Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**Environment Variables**
Create a .env file with the following keys:
```bash
DATABASE_URL_DESARROLLO_ALARMAS=your_database_url
API_KEY=your_api_key
```
**Run the Server**
```bash
uvicorn app.main:app --reload
```

---

## 🚀 8. Usage
- **API Docs**: Available at /docs for a Swagger-based interface.
- **Server Health Check**: Call /server/status-server to check server and database health.

---

## 🧪 9. Testing
**Run Tests**
```bash
pytest tests/
```

**Key Areas to Test**

- **Controllers**: Verify request validation, route logic, and response handling.
- **Services**: Test service logic for transformations, validations, and side effects.
- **Models**: Ensure that the SQLAlchemy models work as intended for CRUD operations.

---

## 🤝 10. Contributing
**How to Contribute**

1. Fork the repository.
2. Create a new branch:
```bash
git checkout -b feature-name
```
3. Commit changes using Conventional Commits:
```bash
git commit -m "feat(alarms): add webhook for alarm processing"
```
4. Push changes to the branch:
```bash
git push origin feature-name
```
5. Open a pull request.

**Commit Guidelines**
We follow the Conventional Commits standard:
```bash
<type>(<scope>): <description>
```

**Examples**
- feat(alarms): add webhook for alarm processing
- fix(server): handle 500 errors in health check

---

## 📜 11. License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 💬 **12. Contact**

If you have any questions, issues, or feedback, feel free to contact **Gabriel** through:

- **GitHub Issues**: Open an issue in this repository.
- **Email**: [gabriel.astudillo.roca@gmail.com](mailto:your-email@example.com)
