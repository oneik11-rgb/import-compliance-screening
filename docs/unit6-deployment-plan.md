\# Unit 6 Deployment and Configuration Plan



\## Explainable Human-in-the-Loop Import Compliance Document Screening System



\## 1. Deployment Strategy



Several deployment approaches were considered for the prototype.



\### Local Development Deployment



The current system runs locally using the Flask development server. This approach is appropriate for development, debugging, testing, and demonstration, but it is not suitable for production deployment.



\### Public Cloud Deployment



The application could technically be deployed to a public cloud platform. Cloud deployment would provide scalability, centralized management, automated backups, and integration with managed services. However, a future operational customs-compliance system could process sensitive government or trade information. Any cloud deployment would therefore require organizational approval, appropriate data classification, identity and access controls, encryption, logging, and compliance with applicable government security policies.



\### On-Premise Deployment



An on-premise deployment could host the application within an authorized government-controlled infrastructure. This approach provides greater organizational control over application access, network boundaries, data storage, audit information, and integration with internal government systems.



\### Selected Approach



The preferred deployment strategy for this capstone is a \*\*containerized application deployed within an authorized internal/on-premise environment or an approved private-cloud environment\*\*.



Containerization provides a reproducible runtime containing the application code and required dependencies. The container could then be deployed consistently across development, testing, and approved production infrastructure.



The current capstone remains a prototype and is not connected to the live Jamaica Customs Agency ASYCUDA World environment. Synthetic ASYCUDA-aligned declarations are used instead.



\---



\## 2. Proposed Deployment Architecture



The proposed deployment flow is:



User Browser  

→ Secure HTTPS Connection  

→ Reverse Proxy / Web Server  

→ Containerized Flask Application  

→ Compliance Rule Engine  

→ Audit and Persistence Layer  

→ Approved Database



The application should not use the Flask development server in production.



A production web server or WSGI service would host the Flask application behind an HTTPS-enabled reverse proxy.



For the current prototype, SQLite provides local persistence. A multi-user production implementation would require evaluation of a server-based database such as PostgreSQL or another database platform approved by the organization.



\---



\## 3. Configuration Management



Configuration management contributes to deployment reliability by ensuring that application versions, dependencies, environment settings, and deployment procedures are controlled and reproducible.



The project currently uses Git and GitHub for source-code version control. Development work is performed on feature branches before being merged through the development branch and then into main.



GitHub Actions provides automated testing so that changes can be verified before integration.



Tagged versions and releases provide identifiable software milestones.



Configuration values that may differ between development and deployment environments should not be hard-coded into application source code. Environment variables should be used for deployment-specific settings.



Sensitive configuration information, including credentials or secret keys, must not be committed to the source-code repository.



\---



\## 4. System Prerequisites



\### Development Environment



\- Windows 10 or Windows 11

\- Python 3.14 or compatible supported Python version

\- Git

\- Python virtual environment

\- Web browser

\- SQLite

\- Internet access for dependency installation and GitHub operations



\### Python Dependencies



The application dependencies are recorded in:



`requirements.txt`



The current core dependencies include:



\- Flask

\- pytest

\- pytest-cov



Additional production deployment packages may be introduced when the deployment environment is finalized.



\---



\## 5. Environment Variables and Settings



A production-ready version should obtain deployment-specific settings through environment variables.



Example variables include:



`FLASK\_ENV`



Defines the application environment, such as development, testing, or production.



`SECRET\_KEY`



Provides the Flask secret key where session or authentication functionality is used.



`DATABASE\_PATH`



Defines the location of the application database.



`LOG\_LEVEL`



Defines application logging verbosity.



`APP\_HOST`



Defines the network interface on which the application listens.



`APP\_PORT`



Defines the application port.



`ASYCUDA\_MODE`



Identifies whether the application is operating with synthetic ASYCUDA-aligned data or an authorized future integration.



For the current capstone prototype:



`ASYCUDA\_MODE=synthetic`



No live ASYCUDA credentials, production declarations, or confidential government data are required or stored.



\---



\## 6. Local Installation and Setup



Clone the repository:



```text

git clone https://github.com/oneik11-rgb/import-compliance-screening.git

