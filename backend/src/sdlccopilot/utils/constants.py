
CONSTANT_USER_STORIES = [{'story_id': 'US-001', 'title': 'Secure Account Access with Multi-Factor Authentication', 'description': 'As a user, I want to secure my account with multi-factor authentication, so that my financial information is protected.', 'acceptance_criteria': ['User can enable biometric authentication (fingerprint or facial recognition).', 'User can set up and use an MPIN for authentication.', 'The application prompts for a second factor of authentication upon login.']}, {'story_id': 'US-002', 'title': 'Link Multiple Bank Accounts for UPI Transfers', 'description': 'As a user, I want to link multiple bank accounts to PayMate, so that I can easily manage and transfer funds from different accounts.', 'acceptance_criteria': ['User can add multiple bank accounts to their profile.', 'User can select a default bank account for UPI transactions.', 'User can view a list of all linked bank accounts.']}, {'story_id': 'US-003', 'title': 'Access Instant Micro-Loans', 'description': 'As a user, I want to access instant micro-loans with minimal documentation, so that I can quickly address immediate financial needs.', 'acceptance_criteria': ['User can apply for a micro-loan within the app.', 'User is informed of the loan amount, interest rate, and repayment terms.', 'User receives the loan amount in their linked bank account upon approval.']}, {'story_id': 'US-004', 'title': 'Pay Utility Bills Through the App', 'description': 'As a user, I want to pay my utility bills (electricity, water, gas, broadband) directly through the app, so that I can manage all my payments in one place.', 'acceptance_criteria': ['User can add biller accounts for various utility providers.', 'User can view outstanding bills and payment history.', 'User can pay bills using UPI.']}]

CONSTANT_REVISED_USER_STORIES =  [{'story_id': 'US-001', 'title': 'Secure Account Access with Multi-Factor Authentication', 'description': 'As a user, I want to secure my account with multi-factor authentication, so that my financial information is protected.', 'acceptance_criteria': ['User can enable biometric authentication (fingerprint or facial recognition).', 'User can set up and use an MPIN for authentication.', 'The application prompts for a second factor of authentication upon login.']}, {'story_id': 'US-002', 'title': 'Link Multiple Bank Accounts for UPI Transfers', 'description': 'As a user, I want to link multiple bank accounts to PayMate, so that I can easily manage and transfer funds from different accounts.', 'acceptance_criteria': ['User can add multiple bank accounts to their profile.', 'User can select a default bank account for UPI transactions.', 'User can view a list of all linked bank accounts.']}, {'story_id': 'US-003', 'title': 'Access Instant Micro-Loans', 'description': 'As a user, I want to access instant micro-loans with minimal documentation, so that I can quickly address immediate financial needs.', 'acceptance_criteria': ['User can apply for a micro-loan within the app.', 'User is informed of the loan amount, interest rate, and repayment terms.', 'User receives the loan amount in their linked bank account upon approval.']}, {'story_id': 'US-004', 'title': 'Pay Utility Bills Through the App', 'description': 'As a user, I want to pay my utility bills (electricity, water, gas, broadband) directly through the app, so that I can manage all my payments in one place.', 'acceptance_criteria': ['User can add biller accounts for various utility providers.', 'User can view outstanding bills and payment history.', 'User can pay bills using UPI.']}, {'story_id': 'US-005', 'title': 'Purchase Insurance Policies', 'description': 'As a user, I want to purchase insurance policies through the app, so that I can easily protect myself and my assets.', 'acceptance_criteria': ['User can browse available insurance policies (e.g., health, auto, travel).', 'User can view policy details, including coverage and premiums.', 'User can purchase a policy and make payments through the app.']}]

CONSTANT_FUNCTIONAL_DOCUMENT = """
# Functional Specification Document for Financial Management and Utility Payment App

## 1. Introduction
### Purpose
This document outlines the functional requirements for the development of a comprehensive financial management and utility payment application. The system aims to provide users with a secure, convenient, and efficient platform to manage financial transactions, utility payments, and insurance purchases.

### Project Scope
The scope of this project includes the implementation of multi-factor authentication (MFA), linking of multiple bank accounts, access to instant micro-loans, payment of utility bills, and purchase of insurance policies.

### System Overview
The application will provide a secure environment for users to manage their finances and utilities, ensuring that all transactions are conducted in a secure and user-friendly manner.

## 2. Business Context
### Project Background
The rapid adoption of digital financial services necessitates a robust platform that prioritizes security and user convenience. The project aims to address the growing demand for integrated financial and utility management tools.

### Business Needs
- Provide a secure and intuitive platform for financial transactions.
- Offer a seamless experience for utility payments.
- Ensure ease of access to financial services like micro-loans and insurance.

### Objectives
- Enhance user security through MFA.
- Streamline the management of multiple bank accounts.
- Facilitate quick access to micro-loans.
- Simplify utility and insurance bill payments.

## 3. Stakeholder Analysis
- **Primary Stakeholders:**
  - End Users
  - System Administrators
  - Financial Compliance Teams
- **Secondary Stakeholders:**
  - Insurance Providers
  - Utility Companies
  - External Financial Services

## 4. Functional Requirements
### FR-1: Multi-Factor Authentication
- **FR-1.1**: The system shall provide an option for users to enable biometric authentication (fingerprint or facial recognition).
- **FR-1.2**: The system shall enable users to set up and use an MPIN as a second factor of authentication.
- **FR-1.3**: The system shall prompt for a second factor of authentication at each login.

### FR-2: Link Multiple Bank Accounts
- **FR-2.1**: The system shall allow users to add multiple bank accounts to their profile.
- **FR-2.2**: The system shall enable users to select a default bank account for UPI transactions.
- **FR-2.3**: The system shall display a list of all linked bank accounts.

### FR-3: Instant Micro-Loans
- **FR-3.1**: The system shall allow users to apply for a micro-loan within the application.
- **FR-3.2**: The system shall inform the user of the loan amount, interest rate, and repayment terms upon application.
- **FR-3.3**: Upon loan approval, the system shall transfer the loan amount to the user's linked bank account.

### FR-4: Pay Utility Bills
- **FR-4.1**: The system shall enable users to add biller accounts for various utility providers.
- **FR-4.2**: The system shall provide users with visibility of outstanding bills and payment history.
- **FR-4.3**: The system shall support the payment of bills using UPI.

### FR-5: Purchase Insurance Policies
- **FR-5.1**: The system shall provide a catalog of available insurance policies (health, auto, travel).
- **FR-5.2**: The system shall display policy details, including coverage and premiums.
- **FR-5.3**: The system shall facilitate the purchase of insurance policies and allow payment through the app.

## 5. Use Cases / Workflows
[Insert UML Use Case Diagrams here or provide textual descriptions of workflows for each feature.]
- **Login with MFA**: User logs in with primary credentials, then provides a second factor of authentication.
- **Link Bank Accounts**: User navigates to settings, adds new bank accounts, and sets a default account.
- **Apply for Micro-Loan**: User initiates a loan application, receives approval notice, and the loan is deposited.
- **Pay Utility Bills**: User selects a bill, reviews details, and makes payment.
- **Purchase Insurance Policies**: User browses policies, selects one, and completes the purchase.

## 6. Data Requirements
- **Input Fields**: User credentials, bank account details, loan application data, bill payment details, policy selection.
- **Output Fields**: Confirmation messages, transaction receipts, policy documentation.
- **Validation Rules**: Password strength, bank account number format, transaction amounts.
- **Data Formats**: JSON for API responses, XML for document generation.

## 7. Non-Functional Requirements
- **Security**: Implement industry-standard encryption for sensitive data.
- **Performance**: Handle 1,000 concurrent users without performance degradation.
- **Scalability**: Support up to 10,000 active users with minimal downtime.
- **Usability**: Ensure the app is user-friendly across Android and iOS platforms.
- **Legal**: Comply with GDPR and local data protection regulations.

## 8. Dependencies & Assumptions
- **Assumptions**: Users will have a valid email and phone number for MFA.
- **Dependencies**: Integration with external financial and utility service providers.

## 9. Edge Cases & Exception Handling
- **MFA Failure**: If biometric authentication fails, the system should prompt for an MPIN.
- **Bank Account Errors**: If a linked bank account is invalid, the system should notify the user and prevent transactions.
- **Loan Approval Delays**: If a loan approval is pending, the system should keep the user informed of the status.
- **Payment Failures**: If a payment fails, the system should notify the user and provide a reason for the failure.

## 10. Acceptance Criteria
- **US-001**: User can successfully enable and use biometric or MPIN authentication.
- **US-002**: User can view and manage multiple bank accounts, including setting a default account and viewing transaction history.
- **US-003**: User can apply for, receive, and utilize a micro-loan.
- **US-004**: User can add and manage utility accounts, view bills, and make payments.
- **US-005**: User can browse, select, and purchase insurance policies.

## 11. Glossary & Definitions
- **MFA**: Multi-Factor Authentication, a security process in which the user provides two or more verification factors to gain access.
- **UPI**: Unified Payments Interface, a system that powers peer-to-peer payments in India.
- **MPIN**: Mobile PIN, a numeric code used as a form of authentication.
- **Biller**: An entity that provides services or products that generate bills.

## 12. Traceability Matrix
| User Story ID | Functional Requirement |
|---------------|------------------------|
| US-001        | FR-1.1, FR-1.2, FR-1.3 |
| US-002        | FR-2.1, FR-2.2, FR-2.3 |
| US-003        | FR-3.1, FR-3.2, FR-3.3 |
| US-004        | FR-4.1, FR-4.2, FR-4.3 |
| US-005        | FR-5.1, FR-5.2, FR-5.3 |

---

This document serves as a comprehensive guide for the design and development of the specified functionalities, ensuring alignment with user needs and business objectives.
"""

CONSTANT_REVISED_FUNCTIONAL_DOCUMENT = """
### Functional Specification Document for Financial Management and Utility Payment App (Revised)

## 1. Introduction
### Purpose
This document outlines the functional requirements for the development of a comprehensive financial management and utility payment application. The system aims to provide users with a secure, convenient, and efficient platform to manage financial transactions, utility payments, insurance purchases, and book flight tickets.

### Project Scope
The scope of this project includes the implementation of multi-factor authentication (MFA), linking of multiple bank accounts, access to instant micro-loans, payment of utility bills, purchase of insurance policies, and booking of flight tickets.

### System Overview
The application will provide a secure environment for users to manage their finances, utilities, and travel, ensuring that all transactions and bookings are conducted in a secure and user-friendly manner.

## 2. Business Context
### Project Background
The rapid adoption of digital financial services and travel booking necessitates a robust platform that prioritizes security, user convenience, and integration with external services. The project aims to address the growing demand for integrated financial, utility, and travel management tools.

### Business Needs
- Provide a secure and intuitive platform for financial transactions and travel bookings.
- Offer a seamless experience for utility and travel payments.
- Ensure ease of access to financial services like micro-loans, insurance, and flight tickets.

### Objectives
- Enhance user security through MFA.
- Streamline the management of multiple bank accounts.
- Facilitate quick access to micro-loans, insurance, and flight tickets.
- Simplify utility and insurance bill payments.

## 3. Stakeholder Analysis
- **Primary Stakeholders:**
  - End Users
  - System Administrators
  - Financial Compliance Teams
- **Secondary Stakeholders:**
  - Insurance Providers
  - Utility Companies
  - External Financial and Travel Service Providers

## 4. Functional Requirements
### FR-1: Multi-Factor Authentication
- **FR-1.1**: The system shall provide an option for users to enable biometric authentication (fingerprint or facial recognition).
- **FR-1.2**: The system shall enable users to set up and use an MPIN as a second factor of authentication.
- **FR-1.3**: The system shall prompt for a second factor of authentication at each login.

### FR-2: Link Multiple Bank Accounts
- **FR-2.1**: The system shall allow users to add multiple bank accounts to their profile.
- **FR-2.2**: The system shall enable users to select a default bank account for UPI transactions.
- **FR-2.3**: The system shall display a list of all linked bank accounts.

### FR-3: Instant Micro-Loans
- **FR-3.1**: The system shall allow users to apply for a micro-loan within the application.
- **FR-3.2**: The system shall inform the user of the loan amount, interest rate, and repayment terms upon application.
- **FR-3.3**: Upon loan approval, the system shall transfer the loan amount to the user's linked bank account.

### FR-4: Pay Utility Bills
- **FR-4.1**: The system shall enable users to add biller accounts for various utility providers.
- **FR-4.2**: The system shall provide users with visibility of outstanding bills and payment history.
- **FR-4.3**: The system shall support the payment of bills using UPI.

### FR-5: Purchase Insurance Policies
- **FR-5.1**: The system shall provide a catalog of available insurance policies (health, auto, travel).
- **FR-5.2**: The system shall display policy details, including coverage and premiums.
- **FR-5.3**: The system shall facilitate the purchase of insurance policies and allow payment through the app.

### FR-6: Book Flight Tickets
- **FR-6.1**: The system shall enable users to book flight tickets from an external travel booking site (e.g., BookMyTrip.com).
- **FR-6.2**: The system shall provide users with flight options, dates, and pricing.
- **FR-6.3**: The system shall allow users to make payments for booked flights within the application.

## 5. Use Cases / Workflows
- **Login with MFA**: User logs in with primary credentials, then provides a second factor of authentication.
- **Link Bank Accounts**: User navigates to settings, adds new bank accounts, and sets a default account.
- **Apply for Micro-Loan**: User initiates a loan application, receives approval notice, and the loan is deposited.
- **Pay Utility Bills**: User selects a bill, reviews details, and makes payment.
- **Purchase Insurance Policies**: User browses policies, selects one, and completes the purchase.
- **Book Flight Tickets**: User selects a flight, reviews details, and completes the transaction through the app.

## 6. Data Requirements
- **Input Fields**: User credentials, bank account details, loan application data, bill payment details, policy selection, travel booking details.
- **Output Fields**: Confirmation messages, transaction receipts, policy documentation, booking confirmations.
- **Validation Rules**: Password strength, bank account number format, transaction amounts, travel booking credentials.
- **Data Formats**: JSON for API responses, PDF for policy and booking documentation.

## 7. Non-Functional Requirements (NFRs)
- **Security**: Implement industry-standard encryption for sensitive data.
- **Performance**: Handle 1,000 concurrent users without performance degradation.
- **Scalability**: Support up to 10,000 active users with minimal downtime.
- **Usability**: Ensure the app is user-friendly across Android and iOS platforms.
- **Legal**: Comply with GDPR and local data protection regulations.

## 8. Dependencies & Assumptions
- **Assumptions**: Users will have a valid email and phone number for MFA.
- **Dependencies**: Integration with external financial, utility, and travel service providers.

## 9. Edge Cases & Exception Handling
- **MFA Failure**: If biometric authentication fails, the system should prompt for an MPIN.
- **Bank Account Errors**: If a linked bank account is invalid, the system should notify the user and prevent transactions.
- **Loan Approval Delays**: If a loan approval is pending, the system should keep the user informed of the status.
- **Payment Failures**: If a payment fails, the system should notify the user and provide the reason for the failure.
- **Flight Booking Issues**: If a booking fails due to an external service outage, the system should notify the user and log the issue for support.

## 10. Acceptance Criteria
- **US-001**: User can successfully enable and use biometric or MPIN authentication.
- **US-002**: User can view and manage multiple bank accounts, including setting a default account and viewing transaction history.
- **US-003**: User can apply for, receive, and utilize a micro-loan.
- **US-004**: User can add and manage utility accounts, view bills, and make payments.
- **US-005**: User can browse, select, and purchase insurance policies.
- **US-006**: User can book and manage flight tickets through an integrated booking platform.

## 11. Glossary & Definitions
- **MFA**: Multi-Factor Authentication, a security process in which the user provides two or more verification factors to gain access.
- **UPI**: Unified Payments Interface, a system that powers peer-to-peer payments in India.
- **MPIN**: Mobile PIN, a numeric code used as a form of authentication.
- **Biller**: An entity that provides services or products that generate bills.
- **Travel Booking Platform**: An external service provider that facilitates flight ticket bookings.

## 12. Traceability Matrix
| User Story ID | Functional Requirement |
|---------------|------------------------|
| US-001        | FR-1.1, FR-1.2, FR-1.3 |
| US-002        | FR-2.1, FR-2.2, FR-2.3 |
| US-003        | FR-3.1, FR-3.2, FR-3.3 |
| US-004        | FR-4.1, FR-4.2, FR-4.3 |
| US-005        | FR-5.1, FR-5.2, FR-5.3 |
| US-006        | FR-6.1, FR-6.2, FR-6.3 |

---

This document serves as a comprehensive guide for the design and development of the specified functionalities, ensuring alignment with user needs and business objectives. It includes the revised feature for booking flight tickets from an external site, enabling a more integrated and seamless user experience.
"""

CONSTANT_TECHNICAL_DOCUMENT = """
# Technical Design Document for Financial Management and Utility Payment App

## 1. Introduction & Purpose
This document outlines the technical design for the development of a comprehensive financial management and utility payment application. The purpose is to provide a structured technical design that can guide the engineering and architecture teams through the Software Development Lifecycle (SDLC). The intended audience includes software developers, system architects, and quality assurance engineers.

### Scope
The scope includes the implementation of multi-factor authentication (MFA), linking of multiple bank accounts, access to instant micro-loans, payment of utility bills, purchase of insurance policies, and booking of flight tickets.

## 2. Architecture Overview
### High-Level Architecture
- **Frontend:** Web and mobile applications using React and React Native.
- **Backend:** Node.js with Express for APIs and server-side logic.
- **Database:** PostgreSQL for transactional data and MongoDB for unstructured data.
- **Authentication & Authorization:** OAuth2.0 and JWT (JSON Web Tokens).
- **Cloud Services:** AWS, including Lambda, API Gateway, DynamoDB, and S3.

### Low-Level Architecture
- **Services:**
  - **User Service:** Handles user authentication, MFA, and user profile management.
  - **Banking Service:** Manages bank account linking, transfers, and payments.
  - **Loan Service:** Facilitates loan applications, approval processes, and disbursement.
  - **Utility Service:** Manages utility bill payments.
  - **Insurance Service:** Manages insurance policy purchases and renewals.
  - **Travel Service:** Integrates with external travel booking platforms for flight ticket bookings.

### Diagrams
[Insert High-Level Architecture Diagram]
[Insert Low-Level Architecture Diagram]

## 3. Modules & Components Design
### User Service Module
- **User Profile Management:** Handles CRUD operations for user profiles.
- **Authentication Service:** Manages user authentication and MFA using biometrics and MPIN.
- **Audit Logging:** Tracks user activities for compliance and security.

### Banking Service Module
- **Bank Account Management:** Manages the linking and un-linking of bank accounts.
- **Payment Service:** Handles UPI transactions and utility payments.
- **Transaction Logging:** Logs financial transactions for audit and reconciliation.

### Loan Service Module
- **Loan Application:** Facilitates the application process for micro-loans.
- **Loan Disbursement:** Handles loan approval and disbursement processes.
- **Repayment Management:** Manages loan repayment schedules and reminders.

### Utility Service Module
- **Biller Management:** Manages biller accounts for utilities.
- **Payment Processing:** Facilitates the payment process for utility bills.
- **Billing History:** Maintains a history of utility bill payments.

### Insurance Service Module
- **Policy Management:** Manages user insurance policies.
- **Policy Purchase:** Facilitates the purchase and payment of insurance policies.
- **Policy Renewal:** Manages the renewal process for insurance policies.

### Travel Service Module
- **Travel Booking Integration:** Integrates with external travel booking platforms.
- **Payment Processing:** Manages payments for travel bookings.
- **Booking History:** Maintains a history of travel bookings and payments.

## 4. Data Model & Schema Design
### User Table
- `user_id` (UUID)
- `email` (string)
- `password_hash` (string)
- `mfa_enabled` (boolean)
- `mfa_type` (string: biometric, mpin)
- `created_at` (datetime)
- `updated_at` (datetime)

### Bank Account Table
- `account_id` (UUID)
- `user_id` (UUID)
- `bank_name` (string)
- `account_number` (string)
- `default_account` (boolean)
- `created_at` (datetime)
- `updated_at` (datetime)

### Utility Bill Table
- `bill_id` (UUID)
- `user_id` (UUID)
- `biller_name` (string)
- `amount` (float)
- `due_date` (datetime)
- `status` (string: unpaid, paid, overdue)
- `created_at` (datetime)
- `updated_at` (datetime)

### Insurance Policy Table
- `policy_id` (UUID)
- `user_id` (UUID)
- `policy_name` (string)
- `coverage` (string)
- `premium` (float)
- `start_date` (datetime)
- `end_date` (datetime)
- `status` (string: active, expired, revoked)
- `created_at` (datetime)
- `updated_at` (datetime)

### Travel Booking Table
- `booking_id` (UUID)
- `user_id` (UUID)
- `flight_details` (JSON)
- `booking_date` (datetime)
- `status` (string: booked, canceled, pending)
- `created_at` (datetime)
- `updated_at` (datetime)

## 5. API Design
### User Service
- **POST /api/v1/user/register**: Registers a new user.
- **POST /api/v1/user/login**: Authenticates a user and returns a JWT.
- **POST /api/v1/user/mfa**: Enables MFA for a user.

### Banking Service
- **POST /api/v1/bank-account/link**: Links a new bank account to a user.
- **POST /api/v1/transaction/make-payment**: Makes a payment (utility or UPI).

### Loan Service
- **POST /api/v1/loan/apply**: Applies for a micro-loan.
- **GET /api/v1/loan/status**: Retrieves the status of a loan application.

### Utility Service
- **POST /api/v1/utility/add-biller**: Adds a new utility biller.
- **POST /api/v1/utility/make-payment**: Makes a utility payment.

### Insurance Service
- **POST /api/v1/insurance/purchase**: Purchases an insurance policy.
- **GET /api/v1/insurance/my-policies**: Retrieves the user's insurance policies.

### Travel Service
- **POST /api/v1/travel/book**: Books a flight ticket.
- **GET /api/v1/travel/my-bookings**: Retrieves the user's travel bookings.

## 6. Sequence & Activity Diagrams
[Insert UML Sequence Diagram: User Login with MFA]
[Insert UML Activity Diagram: Bank Account Linking Workflow]
[Insert UML Activity Diagram: Loan Application and Disbursement Workflow]
[Insert UML Activity Diagram: Utility Bill Payment Workflow]
[Insert UML Activity Diagram: Insurance Policy Purchase Workflow]
[Insert UML Activity Diagram: Travel Booking Workflow]

## 7. Security Design
### Authentication
- JWT for session management.
- OAuth2.0 for secure API access.

### Authorization
- Role-based access control (RBAC) for different user roles.

### Encryption
- TLS for data in transit.
- AES-256 for data at rest.

### Compliance
- GDPR compliance for data privacy.
- PCI-DSS for financial transaction security.

## 8. Performance & Scalability
### Load Expectations
- Concurrency: Up to 1,000 concurrent users.
- Throughput: Up to 10,000 transactions per minute.

### Scalability Strategies
- Auto-scaling for backend services using AWS ECS.
- Load balancing with AWS ELB.

### Performance Benchmarks
- Response Time: < 300ms for API requests.
- Uptime: 99.99% availability.

## 9. Error Handling & Logging
### Error Handling
- HTTP status codes for API responses.
- Custom error messages for user feedback.

### Logging
- Application logs using AWS CloudWatch.
- Error logging with AWS Lambda.

## 10. Deployment & Environment Details
### CI/CD Pipeline
- Jenkins CI/CD pipeline for automated testing and deployment.
- Docker for containerization and deployment.

### Environment Configurations
- Development, Staging, Production environments.
- Infrastructure as Code (IaC) using Terraform for AWS resources.

### Cloud Infrastructure
- AWS VPC for network isolation.
- AWS S3 for static assets.
- AWS RDS for relational database services.

## 11. Assumptions & Technical Dependencies
### Assumptions
- Users have valid email and phone numbers for MFA.
- Bank accounts are valid and meet regulatory requirements.

### Technical Dependencies
- External travel booking platforms for flight booking.
- External insurance providers for policy purchases.

## 12. Risks & Mitigation Strategies
### Risks
- **Integration Risks:** External service outages.
- **Performance Risks:** High load during peak times.
- **Security Risks:** Data breaches and unauthorized access.

### Mitigation Strategies
- **Integration Risks:** Implement fallback services and failover mechanisms.
- **Performance Risks:** Monitor and scale resources using AWS Auto Scaling.
- **Security Risks:** Regular security audits and penetration testing.

## 13. Appendix
### References
- AWS Lambda Documentation
- OAuth2.0 Specification
- GDPR Compliance Guidelines

### Supplementary Notes
- Additional notes on implementation details and design choices will be added as needed.

--- 

This document serves as a comprehensive guide for the technical design of the specified functionalities, ensuring alignment with user needs and business objectives. It includes detailed designs, API specifications, and security measures to ensure a robust and scalable solution.
"""

CONSTANT_REVISED_TECHNICAL_DOCUMENT = """
# Technical Design Document for Financial Management and Utility Payment App

## 1. Introduction & Purpose
This document outlines the technical design for a comprehensive financial management and utility payment application, with the added functionality to book flight tickets from Goibibo.com. The purpose is to provide a structured technical design that guides the engineering and architecture teams through the Software Development Lifecycle (SDLC). The document is intended for software developers, system architects, and quality assurance engineers.

### Scope
The scope includes the implementation of multi-factor authentication (MFA), linking of multiple bank accounts, access to instant micro-loans, payment of utility bills, purchase of insurance policies, and booking of flight tickets. The document covers design, data models, APIs, security, performance, and deployment strategies.

## 2. Architecture Overview

### High-Level Architecture
- **Frontend:** Web and mobile applications using React and React Native.
- **Backend:** Node.js with Express for APIs and server-side logic.
- **Database:** PostgreSQL for transactional data and MongoDB for unstructured data.
- **Authentication & Authorization:** OAuth2.0 and JWT (JSON Web Tokens).
- **Cloud Services:** AWS, including Lambda, API Gateway, DynamoDB, and S3.

### Low-Level Architecture
- **Services:**
  - **User Service:** Handles user authentication, MFA, and user profile management.
  - **Banking Service:** Manages bank account linking, transfers, and payments.
  - **Loan Service:** Facilitates loan applications, approval processes, and disbursement.
  - **Utility Service:** Manages utility bill payments.
  - **Insurance Service:** Manages insurance policy purchases and renewals.
  - **Travel Service:** Integrates with Goibibo.com for flight ticket bookings.
  - **Payment Service:** Manages payment processes for all transactions.

### Diagrams
[Insert High-Level Architecture Diagram]
[Insert Low-Level Architecture Diagram]

## 3. Modules & Components Design

### User Service Module
- **User Profile Management:** Handles CRUD operations for user profiles.
- **Authentication Service:** Manages user authentication and MFA using biometrics and MPIN.
- **Audit Logging:** Tracks user activities for compliance and security.

### Banking Service Module
- **Bank Account Management:** Manages the linking and un-linking of bank accounts.
- **Payment Service:** Handles UPI transactions and utility payments.
- **Transaction Logging:** Logs financial transactions for audit and reconciliation.

### Loan Service Module
- **Loan Application:** Facilitates the application process for micro-loans.
- **Loan Disbursement:** Handles loan approval and disbursement processes.
- **Repayment Management:** Manages loan repayment schedules and reminders.

### Utility Service Module
- **Biller Management:** Manages biller accounts for utilities.
- **Payment Processing:** Facilitates the payment process for utility bills.
- **Billing History:** Maintains a history of utility bill payments.

### Insurance Service Module
- **Policy Management:** Manages user insurance policies.
- **Policy Purchase:** Facilitates the purchase and payment of insurance policies.
- **Policy Renewal:** Manages the renewal process for insurance policies.

### Travel Service Module
- **Travel Booking Integration:** Integrates with Goibibo.com for flight booking.
- **Payment Processing:** Manages payments for travel bookings.
- **Booking History:** Maintains a history of travel bookings and payments.

## 4. Data Model & Schema Design

### User Table
- `user_id` (UUID)
- `email` (string)
- `password_hash` (string)
- `mfa_enabled` (boolean)
- `mfa_type` (string: biometric, mpin)
- `created_at` (datetime)
- `updated_at` (datetime)

### Bank Account Table
- `account_id` (UUID)
- `user_id` (UUID)
- `bank_name` (string)
- `account_number` (string)
- `default_account` (boolean)
- `created_at` (datetime)
- `updated_at` (datetime)

### Utility Bill Table
- `bill_id` (UUID)
- `user_id` (UUID)
- `biller_name` (string)
- `amount` (float)
- `due_date` (datetime)
- `status` (string: unpaid, paid, overdue)
- `created_at` (datetime)
- `updated_at` (datetime)

### Insurance Policy Table
- `policy_id` (UUID)
- `user_id` (UUID)
- `policy_name` (string)
- `coverage` (string)
- `premium` (float)
- `start_date` (datetime)
- `end_date` (datetime)
- `status` (string: active, expired, revoked)
- `created_at` (datetime)
- `updated_at` (datetime)

### Travel Booking Table
- `booking_id` (UUID)
- `user_id` (UUID)
- `flight_details` (JSON)
- `booking_date` (datetime)
- `status` (string: booked, canceled, pending)
- `created_at` (datetime)
- `updated_at` (datetime)

## 5. API Design

### User Service
- **POST /api/v1/user/register**: Registers a new user.
- **POST /api/v1/user/login**: Authenticates a user and returns a JWT.
- **POST /api/v1/user/mfa**: Enables MFA for a user.

### Banking Service
- **POST /api/v1/bank-account/link**: Links a new bank account to a user.
- **POST /api/v1/transaction/make-payment**: Makes a payment (utility or UPI).

### Loan Service
- **POST /api/v1/loan/apply**: Applies for a micro-loan.
- **GET /api/v1/loan/status**: Retrieves the status of a loan application.

### Utility Service
- **POST /api/v1/utility/add-biller**: Adds a new utility biller.
- **POST /api/v1/utility/make-payment**: Makes a utility payment.

### Insurance Service
- **POST /api/v1/insurance/purchase**: Purchases an insurance policy.
- **GET /api/v1/insurance/my-policies**: Retrieves the user's insurance policies.

### Travel Service
- **POST /api/v1/travel/book**: Books a flight ticket from Goibibo.com.
- **GET /api/v1/travel/my-bookings**: Retrieves the user's travel bookings.

## 6. Sequence & Activity Diagrams
[Insert UML Sequence Diagram: User Login with MFA]
[Insert UML Activity Diagram: Bank Account Linking Workflow]
[Insert UML Activity Diagram: Loan Application and Disbursement Workflow]
[Insert UML Activity Diagram: Utility Bill Payment Workflow]
[Insert UML Activity Diagram: Insurance Policy Purchase Workflow]
[Insert UML Activity Diagram: Travel Booking Workflow]

## 7. Security Design

### Authentication
- JWT for session management.
- OAuth2.0 for secure API access.

### Authorization
- Role-based access control (RBAC) for different user roles.

### Encryption
- TLS for data in transit.
- AES-256 for data at rest.

### Compliance
- GDPR compliance for data privacy.
- PCI-DSS for financial transaction security.

## 8. Performance & Scalability

### Load Expectations
- Concurrency: Up to 1,000 concurrent users.
- Throughput: Up to 10,000 transactions per minute.

### Scalability Strategies
- Auto-scaling for backend services using AWS Auto Scaling.
- Load balancing with AWS Elastic Load Balancer (ELB).

### Performance Benchmarks
- Response Time: < 300ms for API requests.
- Uptime: 99.99% availability.

## 9. Error Handling & Logging

### Error Handling
- HTTP status codes for API responses.
- Custom error messages for user feedback.

### Logging
- Application logs using AWS CloudWatch.
- Error logging with AWS Lambda.

## 10. Deployment & Environment Details

### CI/CD Pipeline
- Jenkins CI/CD pipeline for automated testing and deployment.
- Docker for containerization and deployment.

### Environment Configurations
- Development, Staging, Production environments.
- Infrastructure as Code (IaC) using Terraform for AWS resources.

### Cloud Infrastructure
- AWS VPC for network isolation.
- AWS S3 for static assets.
- AWS RDS for relational database services.

## 11. Assumptions & Dependencies

### Assumptions
- Users have valid email and phone numbers for MFA.
- Bank accounts are valid and meet regulatory requirements.
- Goibibo.com API is stable and reliable for travel bookings.

### Technical Dependencies
- External travel booking platforms for flight booking.
- External insurance providers for policy purchases.

## 12. Risks & Mitigation Strategies

### Risks
- **Integration Risks:** External service outages.
- **Performance Risks:** High load during peak times.
- **Security Risks:** Data breaches and unauthorized access.

### Mitigation Strategies
- **Integration Risks:** Implement fallback services and failover mechanisms.
- **Performance Risks:** Monitor and scale resources using AWS Auto Scaling.
- **Security Risks:** Regular security audits and penetration testing.

## 13. Appendix

### References
- AWS Lambda Documentation
- OAuth2.0 Specification
- GDPR Compliance Guidelines

### Supplementary Notes
- Additional notes on implementation details and design choices will be added as needed.

---

This document provides a comprehensive technical design for the financial management and utility payment application, including the capability to book flight tickets from Goibibo.com. It covers all the necessary components, APIs, security, and performance aspects to ensure a robust and scalable solution.

"""

CONSTANT_FRONTEND_CODE = """ 
Let me help you implement the frontend for these user stories. We'll create a modern, user-friendly interface using React, TypeScript, and Tailwind CSS.

<boltArtifact id="paymate-frontend" title="PayMate Frontend Implementation">
<boltAction type="shell">npm install @headlessui/react react-router-dom</boltAction>

<boltAction type="file" filePath="src/types/index.ts">export interface BankAccount {
  id: string;
  bankName: string;
  accountNumber: string;
  isDefault: boolean;
}

export interface Bill {
  id: string;
  provider: string;
  amount: number;
  dueDate: string;
  status: 'pending' | 'paid'
}

export interface InsurancePolicy {
  id: string;
  type: 'health' | 'auto' | 'travel';
  name: string;
  coverage: number;
  premium: number;
}

export interface LoanOffer {
  id: string;
  amount: number;
  interestRate: number;
  termMonths: number;
}</boltAction>

<boltAction type="file" filePath="src/components/Layout.tsx">import { Fragment } from 'react';
import { Disclosure } from '@headlessui/react';
import { Menu } from 'lucide-react';
import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  const navigation = [
    { name: 'Dashboard', href: '/' },
    { name: 'Bank Accounts', href: '/accounts' },
    { name: 'Bills', href: '/bills' },
    { name: 'Loans', href: '/loans' },
    { name: 'Insurance', href: '/insurance' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Disclosure as="nav" className="bg-white shadow-sm">
        {({ open }) => (
          <>
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex h-16 justify-between">
                <div className="flex">
                  <div className="flex flex-shrink-0 items-center">
                    <span className="text-xl font-bold text-indigo-600">PayMate</span>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    {navigation.map((item) => (
                      <Link
                        key={item.name}
                        to={item.href}
                        className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
                      >
                        {item.name}
                      </Link>
                    ))}
                  </div>
                </div>
                <div className="-mr-2 flex items-center sm:hidden">
                  <Disclosure.Button className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500">
                    <Menu className="h-6 w-6" />
                  </Disclosure.Button>
                </div>
              </div>
            </div>

            <Disclosure.Panel className="sm:hidden">
              <div className="space-y-1 pb-3 pt-2">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="block py-2 pl-3 pr-4 text-base font-medium text-gray-700"
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}</boltAction>

<boltAction type="file" filePath="src/App.tsx">import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import BankAccounts from './pages/BankAccounts';
import Bills from './pages/Bills';
import Loans from './pages/Loans';
import Insurance from './pages/Insurance';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="accounts" element={<BankAccounts />} />
          <Route path="bills" element={<Bills />} />
          <Route path="loans" element={<Loans />} />
          <Route path="insurance" element={<Insurance />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;</boltAction>

<boltAction type="file" filePath="src/pages/Dashboard.tsx">import { Shield, Wallet, Receipt, Building2 } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Welcome to PayMate</h1>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <DashboardCard
          icon={<Shield className="h-6 w-6" />}
          title="Security"
          description="Multi-factor authentication enabled"
        />
        <DashboardCard
          icon={<Wallet className="h-6 w-6" />}
          title="Bank Accounts"
          description="3 accounts linked"
        />
        <DashboardCard
          icon={<Receipt className="h-6 w-6" />}
          title="Bills"
          description="2 pending payments"
        />
        <DashboardCard
          icon={<Building2 className="h-6 w-6" />}
          title="Insurance"
          description="View available policies"
        />
      </div>
    </div>
  );
}

function DashboardCard({ icon, title, description }: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="bg-indigo-500 rounded-md p-3 text-white">
              {icon}
            </div>
          </div>
          <div className="ml-5">
            <h3 className="text-lg font-medium text-gray-900">{title}</h3>
            <p className="text-sm text-gray-500">{description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}</boltAction>

<boltAction type="file" filePath="src/pages/BankAccounts.tsx">import { useState } from 'react';
import type { BankAccount } from '../types';

export default function BankAccounts() {
  const [accounts] = useState<BankAccount[]>([
    { id: '1', bankName: 'Example Bank', accountNumber: '****1234', isDefault: true },
    { id: '2', bankName: 'Other Bank', accountNumber: '****5678', isDefault: false },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">Linked Bank Accounts</h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Add Account
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {accounts.map((account) => (
            <li key={account.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="text-sm font-medium text-indigo-600">{account.bankName}</div>
                    {account.isDefault && (
                      <span className="ml-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        Default
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-500">{account.accountNumber}</div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}</boltAction>

<boltAction type="shell">npx vite --port 5173</boltAction>
</boltArtifact>

I've set up the initial structure with routing and implemented the Dashboard and Bank Accounts pages. The other pages (Bills, Loans, Insurance) would follow a similar pattern. Let me know if you'd like to see those implementations as well.
"""

# TODO: Add the revised frontend code
CONSTANT_REVISED_FRONTEND_CODE = """
Let me help you implement the frontend for these user stories. We'll create a modern, user-friendly interface using React, TypeScript, and Tailwind CSS.

<boltArtifact id="paymate-frontend" title="PayMate Frontend Implementation">
<boltAction type="shell">npm install @headlessui/react react-router-dom</boltAction>

<boltAction type="file" filePath="src/types/index.ts">export interface BankAccount {
  id: string;
  bankName: string;
  accountNumber: string;
  isDefault: boolean;
}

export interface Bill {
  id: string;
  provider: string;
  amount: number;
  dueDate: string;
  status: 'pending' | 'paid'
}

export interface InsurancePolicy {
  id: string;
  type: 'health' | 'auto' | 'travel';
  name: string;
  coverage: number;
  premium: number;
}

export interface LoanOffer {
  id: string;
  amount: number;
  interestRate: number;
  termMonths: number;
}</boltAction>

<boltAction type="file" filePath="src/components/Layout.tsx">import { Fragment } from 'react';
import { Disclosure } from '@headlessui/react';
import { Menu } from 'lucide-react';
import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  const navigation = [
    { name: 'Dashboard', href: '/' },
    { name: 'Bank Accounts', href: '/accounts' },
    { name: 'Bills', href: '/bills' },
    { name: 'Loans', href: '/loans' },
    { name: 'Insurance', href: '/insurance' },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Disclosure as="nav" className="bg-white shadow-sm">
        {({ open }) => (
          <>
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex h-16 justify-between">
                <div className="flex">
                  <div className="flex flex-shrink-0 items-center">
                    <span className="text-xl font-bold text-indigo-600">PayMate</span>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    {navigation.map((item) => (
                      <Link
                        key={item.name}
                        to={item.href}
                        className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
                      >
                        {item.name}
                      </Link>
                    ))}
                  </div>
                </div>
                <div className="-mr-2 flex items-center sm:hidden">
                  <Disclosure.Button className="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500">
                    <Menu className="h-6 w-6" />
                  </Disclosure.Button>
                </div>
              </div>
            </div>

            <Disclosure.Panel className="sm:hidden">
              <div className="space-y-1 pb-3 pt-2">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="block py-2 pl-3 pr-4 text-base font-medium text-gray-700"
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}</boltAction>

<boltAction type="file" filePath="src/App.tsx">import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import BankAccounts from './pages/BankAccounts';
import Bills from './pages/Bills';
import Loans from './pages/Loans';
import Insurance from './pages/Insurance';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="accounts" element={<BankAccounts />} />
          <Route path="bills" element={<Bills />} />
          <Route path="loans" element={<Loans />} />
          <Route path="insurance" element={<Insurance />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;</boltAction>

<boltAction type="file" filePath="src/pages/Dashboard.tsx">import { Shield, Wallet, Receipt, Building2 } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Welcome to PayMate</h1>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <DashboardCard
          icon={<Shield className="h-6 w-6" />}
          title="Security"
          description="Multi-factor authentication enabled"
        />
        <DashboardCard
          icon={<Wallet className="h-6 w-6" />}
          title="Bank Accounts"
          description="3 accounts linked"
        />
        <DashboardCard
          icon={<Receipt className="h-6 w-6" />}
          title="Bills"
          description="2 pending payments"
        />
        <DashboardCard
          icon={<Building2 className="h-6 w-6" />}
          title="Insurance"
          description="View available policies"
        />
      </div>
    </div>
  );
}

function DashboardCard({ icon, title, description }: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="bg-indigo-500 rounded-md p-3 text-white">
              {icon}
            </div>
          </div>
          <div className="ml-5">
            <h3 className="text-lg font-medium text-gray-900">{title}</h3>
            <p className="text-sm text-gray-500">{description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}</boltAction>

<boltAction type="file" filePath="src/pages/BankAccounts.tsx">import { useState } from 'react';
import type { BankAccount } from '../types';

export default function BankAccounts() {
  const [accounts] = useState<BankAccount[]>([
    { id: '1', bankName: 'Example Bank', accountNumber: '****1234', isDefault: true },
    { id: '2', bankName: 'Other Bank', accountNumber: '****5678', isDefault: false },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">Linked Bank Accounts</h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
          Add Account
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {accounts.map((account) => (
            <li key={account.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="text-sm font-medium text-indigo-600">{account.bankName}</div>
                    {account.isDefault && (
                      <span className="ml-2 px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        Default
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-500">{account.accountNumber}</div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}</boltAction>

<boltAction type="shell">npx vite --port 5173</boltAction>
</boltArtifact>

I've set up the initial structure with routing and implemented the Dashboard and Bank Accounts pages. The other pages (Bills, Loans, Insurance) would follow a similar pattern. Let me know if you'd like to see those implementations as well.
"""

CONSTANT_BACKEND_CODE = """ 
Let's create a Node.js backend for the financial app with proper structure and security features.

<boltArtifact id="financial-app-backend" title="Financial App Backend Setup">
<boltAction type="file" filePath="package.json">
{
  "name": "financial-app-backend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "express-validator": "^7.0.1",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
</boltAction>

<boltAction type="file" filePath="src/server.js">
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.js';
import bankRoutes from './routes/bank.js';
import loanRoutes from './routes/loan.js';
import billRoutes from './routes/bill.js';
import insuranceRoutes from './routes/insurance.js';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/bank', bankRoutes);
app.use('/api/loan', loanRoutes);
app.use('/api/bill', billRoutes);
app.use('/api/insurance', insuranceRoutes);

app.listen(port, () => console.log(`Server running on port ${port}`));
</boltAction>

<boltAction type="file" filePath="src/routes/auth.js">
import express from 'express';
import { body, validationResult } from 'express-validator';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

const router = express.Router();

router.post('/mfa/enable', 
  body('userId').notEmpty(),
  body('mfaType').isIn(['biometric', 'mpin']),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    res.json({ message: 'MFA enabled successfully' });
});

router.post('/mfa/verify', 
  body('userId').notEmpty(),
  body('mfaToken').notEmpty(),
  (req, res) => {
    res.json({ message: 'MFA verification successful' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/bank.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/link', 
  body('accountNumber').notEmpty(),
  body('bankName').notEmpty(),
  (req, res) => {
    res.json({ message: 'Bank account linked successfully' });
});

router.get('/accounts', (req, res) => {
  res.json({ accounts: [] });
});

router.put('/default/:accountId', (req, res) => {
  res.json({ message: 'Default account updated' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/loan.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/apply',
  body('amount').isNumeric(),
  body('term').isNumeric(),
  (req, res) => {
    res.json({
      loanId: '123',
      status: 'PENDING',
      amount: req.body.amount,
      interest: '12%'
    });
});

router.get('/status/:loanId', (req, res) => {
  res.json({ status: 'APPROVED' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/bill.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/add-biller',
  body('billerName').notEmpty(),
  body('billerId').notEmpty(),
  (req, res) => {
    res.json({ message: 'Biller added successfully' });
});

router.get('/pending', (req, res) => {
  res.json({ bills: [] });
});

router.post('/pay',
  body('billId').notEmpty(),
  body('amount').isNumeric(),
  (req, res) => {
    res.json({ transactionId: '123', status: 'SUCCESS' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/insurance.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.get('/policies', (req, res) => {
  res.json({ policies: [] });
});

router.post('/purchase',
  body('policyId').notEmpty(),
  body('term').isNumeric(),
  (req, res) => {
    res.json({ 
      policyNumber: '123',
      status: 'ACTIVE',
      coverage: '1000000'
    });
});

export default router;
</boltAction>
<boltAction type="shell">npm install && npm run dev</boltAction>
</boltArtifact>
"""

# TODO: Add the revised backend code
CONSTANT_REVISED_BACKEND_CODE = """
Let's create a Node.js backend for the financial app with proper structure and security features.

<boltArtifact id="financial-app-backend" title="Financial App Backend Setup">
<boltAction type="file" filePath="package.json">
{
  "name": "financial-app-backend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "express-validator": "^7.0.1",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
</boltAction>

<boltAction type="file" filePath="src/server.js">
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.js';
import bankRoutes from './routes/bank.js';
import loanRoutes from './routes/loan.js';
import billRoutes from './routes/bill.js';
import insuranceRoutes from './routes/insurance.js';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/bank', bankRoutes);
app.use('/api/loan', loanRoutes);
app.use('/api/bill', billRoutes);
app.use('/api/insurance', insuranceRoutes);

app.listen(port, () => console.log(`Server running on port ${port}`));
</boltAction>

<boltAction type="file" filePath="src/routes/auth.js">
import express from 'express';
import { body, validationResult } from 'express-validator';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

const router = express.Router();

router.post('/mfa/enable', 
  body('userId').notEmpty(),
  body('mfaType').isIn(['biometric', 'mpin']),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    res.json({ message: 'MFA enabled successfully' });
});

router.post('/mfa/verify', 
  body('userId').notEmpty(),
  body('mfaToken').notEmpty(),
  (req, res) => {
    res.json({ message: 'MFA verification successful' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/bank.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/link', 
  body('accountNumber').notEmpty(),
  body('bankName').notEmpty(),
  (req, res) => {
    res.json({ message: 'Bank account linked successfully' });
});

router.get('/accounts', (req, res) => {
  res.json({ accounts: [] });
});

router.put('/default/:accountId', (req, res) => {
  res.json({ message: 'Default account updated' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/loan.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/apply',
  body('amount').isNumeric(),
  body('term').isNumeric(),
  (req, res) => {
    res.json({
      loanId: '123',
      status: 'PENDING',
      amount: req.body.amount,
      interest: '12%'
    });
});

router.get('/status/:loanId', (req, res) => {
  res.json({ status: 'APPROVED' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/bill.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.post('/add-biller',
  body('billerName').notEmpty(),
  body('billerId').notEmpty(),
  (req, res) => {
    res.json({ message: 'Biller added successfully' });
});

router.get('/pending', (req, res) => {
  res.json({ bills: [] });
});

router.post('/pay',
  body('billId').notEmpty(),
  body('amount').isNumeric(),
  (req, res) => {
    res.json({ transactionId: '123', status: 'SUCCESS' });
});

export default router;
</boltAction>

<boltAction type="file" filePath="src/routes/insurance.js">
import express from 'express';
import { body } from 'express-validator';

const router = express.Router();

router.get('/policies', (req, res) => {
  res.json({ policies: [] });
});

router.post('/purchase',
  body('policyId').notEmpty(),
  body('term').isNumeric(),
  (req, res) => {
    res.json({ 
      policyNumber: '123',
      status: 'ACTIVE',
      coverage: '1000000'
    });
});

export default router;
</boltAction>
<boltAction type="shell">npm install && npm run dev</boltAction>
</boltArtifact>
"""



CONSTANT_SECURITY_REVIEW = [{'sec_id': 'SR-001', 'review': "The `/mfa/verify` route in `src/routes/auth.js` lacks any actual verification logic for the `mfaToken`. It simply returns a success message regardless of the token's validity. This allows any user to bypass MFA by providing any arbitrary value as the `mfaToken`, effectively rendering the MFA implementation useless. An attacker could gain unauthorized access to user accounts by exploiting this vulnerability.", 'file_path': 'src/routes/auth.js', 'recommendation': 'Implement proper MFA token verification logic. This should involve checking the provided `mfaToken` against a stored secret or a trusted authentication service. Consider using time-based one-time passwords (TOTP) or integrating with a dedicated MFA provider. The verification process should also include measures to prevent replay attacks.', 'priority': 'high'}, {'sec_id': 'SR-002', 'review': 'The `/mfa/enable` route in `src/routes/auth.js` accepts `userId` and `mfaType` without any authentication or authorization checks. This means any user can enable MFA for any other user by simply providing their `userId`. This is a critical vulnerability that allows an attacker to force MFA on other users, potentially locking them out of their accounts or causing denial of service. Furthermore, the application does not validate if the user exists before enabling MFA.', 'file_path': 'src/routes/auth.js', 'recommendation': 'Implement authentication and authorization checks before allowing a user to enable MFA. The server should verify that the user making the request is the same user for whom MFA is being enabled. Also, validate that the user exists in the system before enabling MFA.', 'priority': 'high'}, {'sec_id': 'SR-003', 'review': "The application uses `bcryptjs` for password hashing (although the code provided doesn't show the actual hashing implementation, the `package.json` indicates its usage). However, the code lacks salt generation and proper storage of the hashed passwords. Without proper salting, rainbow table attacks become feasible. Without secure storage, the hashed passwords could be compromised if the database is breached.", 'file_path': 'package.json', 'recommendation': 'Ensure that `bcryptjs` is used correctly with randomly generated salts for each password. Store the salt along with the hashed password in the database. Use a sufficiently high number of rounds (cost factor) for the bcrypt hashing algorithm to make brute-force attacks computationally expensive. The code for password hashing and storage is missing, so this recommendation is based on the assumption that it will be implemented elsewhere.', 'priority': 'medium'}, {'sec_id': 'SR-004', 'review': "The `/loan/apply` route in `src/routes/loan.js` returns a hardcoded interest rate of '12%'. This is a security issue because it exposes a fixed value that should be dynamically calculated based on various factors such as credit score, loan amount, and market conditions. An attacker could potentially exploit this by manipulating the loan application process to always receive the fixed interest rate, regardless of their actual risk profile. This could lead to financial losses for the application.", 'file_path': 'src/routes/loan.js', 'recommendation': 'Implement a dynamic interest rate calculation based on relevant factors. Store the interest rate calculation logic on the server-side and ensure that it cannot be manipulated by the client. The interest rate should be determined based on factors such as credit score, loan amount, and market conditions.', 'priority': 'medium'}, {'sec_id': 'SR-005', 'review': 'The application uses `express-validator` for input validation, but the validation rules are basic and only check for the presence of certain fields. There is no validation of the *content* of the fields. For example, the `accountNumber` in `src/routes/bank.js` is only checked for being non-empty, but not for its format or length. This could lead to invalid data being stored in the database or unexpected application behavior. An attacker could potentially exploit this by providing malformed input that bypasses the validation checks.', 'file_path': 'src/routes/bank.js', 'recommendation': 'Implement more comprehensive input validation using `express-validator`. Define specific validation rules for each field based on its expected format and content. For example, the `accountNumber` should be validated for its length and format (e.g., using regular expressions). The `amount` field should be validated to ensure it is a positive number within a reasonable range.', 'priority': 'low'}, {'sec_id': 'SR-006', 'review': 'The `/accounts` route in `src/routes/bank.js` returns an empty array of accounts. This might be acceptable during initial development, but in a production environment, it should either return actual account data or a proper error message indicating that no accounts are available. Returning an empty array without any context could be confusing for the user and could potentially mask underlying issues with the data retrieval process.', 'file_path': 'src/routes/bank.js', 'recommendation': 'Implement proper account data retrieval logic or return a meaningful error message if no accounts are found. If no accounts are found, return a 404 status code with a message indicating that no accounts are available. If there is an error retrieving the accounts, return a 500 status code with an appropriate error message.', 'priority': 'low'}]

# TODO: Add the revised Backend code
CONSTANT_REVISED_BACKEND_CODE = "print('Hello World')"



CONSTANT_TEST_CASES = [{'test_id': 'US001_TC001', 'description': 'Verify successful login with biometric authentication.', 'steps': ['Step 1: Enable biometric authentication in the app settings.', 'Step 2: Log out of the application.', 'Step 3: Attempt to log in using biometric authentication (fingerprint or facial recognition).', 'Step 4: Verify that the application grants access upon successful biometric authentication.'], 'status': 'draft'}, {'test_id': 'US001_TC002', 'description': 'Verify successful login with MPIN authentication.', 'steps': ['Step 1: Enable MPIN as a second factor of authentication in the app settings.', 'Step 2: Log out of the application.', 'Step 3: Attempt to log in using primary credentials.', 'Step 4: Enter the correct MPIN when prompted.', 'Step 5: Verify that the application grants access upon successful MPIN authentication.'], 'status': 'draft'}, {'test_id': 'US001_TC003', 'description': 'Verify that the system prompts for a second factor of authentication at each login.', 'steps': ['Step 1: Enable either biometric or MPIN authentication.', 'Step 2: Log out of the application.', 'Step 3: Attempt to log in using primary credentials.', 'Step 4: Verify that the system prompts for the configured second factor of authentication (biometric or MPIN).'], 'status': 'draft'}, {'test_id': 'US001_TC004', 'description': 'Verify that login fails after multiple incorrect MPIN attempts.', 'steps': ['Step 1: Enable MPIN authentication.', 'Step 2: Log out of the application.', 'Step 3: Attempt to log in using primary credentials.', 'Step 4: Enter an incorrect MPIN multiple times (e.g., 3-5 times).', 'Step 5: Verify that the application locks the account or requires a password reset after multiple failed MPIN attempts.'], 'status': 'draft'}, {'test_id': 'US001_TC005', 'description': 'Verify that biometric authentication can be disabled.', 'steps': ['Step 1: Enable biometric authentication.', 'Step 2: Navigate to the security settings.', 'Step 3: Disable biometric authentication.', 'Step 4: Log out and attempt to log in. Verify that biometric authentication is no longer an option.'], 'status': 'draft'}, {'test_id': 'US002_TC001', 'description': 'Verify that a user can successfully add multiple bank accounts.', 'steps': ["Step 1: Navigate to the 'Linked Bank Accounts' section in the app.", 'Step 2: Add a new bank account using valid bank details.', 'Step 3: Repeat step 2 to add at least two more bank accounts.', 'Step 4: Verify that all added bank accounts are displayed in the list of linked accounts.'], 'status': 'draft'}, {'test_id': 'US002_TC002', 'description': 'Verify that a user can set a default bank account for UPI transactions.', 'steps': ['Step 1: Add at least two bank accounts to the profile.', "Step 2: Navigate to the 'Linked Bank Accounts' section.", 'Step 3: Select one of the added bank accounts and set it as the default account.', 'Step 4: Verify that the selected bank account is marked as the default account in the list.'], 'status': 'draft'}, {'test_id': 'US002_TC003', 'description': 'Verify that the system displays a list of all linked bank accounts.', 'steps': ['Step 1: Add multiple bank accounts to the profile.', "Step 2: Navigate to the 'Linked Bank Accounts' section.", 'Step 3: Verify that all added bank accounts are displayed in the list, showing relevant details (e.g., account number, bank name).'], 'status': 'draft'}, {'test_id': 'US002_TC004', 'description': 'Verify that the user can remove a linked bank account.', 'steps': ['Step 1: Add at least one bank account.', "Step 2: Navigate to the 'Linked Bank Accounts' section.", "Step 3: Select a bank account and choose the 'Remove' option.", 'Step 4: Confirm the removal.', 'Step 5: Verify that the removed bank account is no longer displayed in the list.'], 'status': 'draft'}, {'test_id': 'US002_TC005', 'description': 'Verify that the system prevents adding a bank account with invalid details.', 'steps': ["Step 1: Navigate to the 'Linked Bank Accounts' section.", 'Step 2: Attempt to add a new bank account using invalid details (e.g., incorrect account number format).', 'Step 3: Verify that the system displays an error message indicating the invalid details and prevents adding the account.'], 'status': 'draft'}, {'test_id': 'US003_TC001', 'description': 'Verify that a user can successfully apply for a micro-loan.', 'steps': ["Step 1: Navigate to the 'Micro-Loan' section in the app.", 'Step 2: Initiate a loan application.', 'Step 3: Enter the required details (e.g., loan amount, purpose).', 'Step 4: Submit the application.', 'Step 5: Verify that the system displays a confirmation message indicating that the application has been submitted.'], 'status': 'draft'}, {'test_id': 'US003_TC002', 'description': 'Verify that the system informs the user of the loan amount, interest rate, and repayment terms upon application.', 'steps': ['Step 1: Apply for a micro-loan.', 'Step 2: Before submitting the application, verify that the system displays the loan amount, interest rate, and repayment terms clearly.', 'Step 3: Submit the application.'], 'status': 'draft'}, {'test_id': 'US003_TC003', 'description': "Verify that upon loan approval, the system transfers the loan amount to the user's linked bank account.", 'steps': ['Step 1: Apply for a micro-loan and ensure the application is approved (mock approval if necessary).', "Step 2: Verify that the loan amount is transferred to the user's linked bank account.", 'Step 3: Check the transaction history in the app and the linked bank account to confirm the transfer.'], 'status': 'draft'}, {'test_id': 'US003_TC004', 'description': 'Verify that the system displays an error message if the loan application is rejected.', 'steps': ['Step 1: Apply for a micro-loan and ensure the application is rejected (mock rejection if necessary).', 'Step 2: Verify that the system displays an error message indicating that the application has been rejected and provides a reason for the rejection.'], 'status': 'draft'}, {'test_id': 'US003_TC005', 'description': 'Verify that the system prevents applying for a loan if the user has an outstanding loan.', 'steps': ['Step 1: Apply for and receive a micro-loan.', 'Step 2: Before repaying the loan, attempt to apply for another micro-loan.', 'Step 3: Verify that the system displays an error message indicating that the user cannot apply for another loan while an outstanding loan exists.'], 'status': 'draft'}, {'test_id': 'US004_TC001', 'description': 'Verify that a user can add biller accounts for various utility providers.', 'steps': ["Step 1: Navigate to the 'Pay Utility Bills' section in the app.", 'Step 2: Select the option to add a new biller account.', 'Step 3: Choose a utility provider from the list.', 'Step 4: Enter the required details (e.g., account number, customer ID).', 'Step 5: Verify that the biller account is successfully added and displayed in the list of billers.'], 'status': 'draft'}, {'test_id': 'US004_TC002', 'description': 'Verify that the system provides users with visibility of outstanding bills and payment history.', 'steps': ['Step 1: Add a biller account.', "Step 2: Navigate to the 'Pay Utility Bills' section.", 'Step 3: Select the added biller account.', 'Step 4: Verify that the system displays the outstanding bill amount and due date.', 'Step 5: Verify that the system displays the payment history for the selected biller account.'], 'status': 'draft'}, {'test_id': 'US004_TC003', 'description': 'Verify that the system supports the payment of bills using UPI.', 'steps': ['Step 1: Add a biller account with an outstanding bill.', "Step 2: Navigate to the 'Pay Utility Bills' section.", 'Step 3: Select the biller account and choose the option to pay the bill.', 'Step 4: Select UPI as the payment method.', 'Step 5: Complete the UPI payment process.', "Step 6: Verify that the payment is successful and the bill status is updated to 'Paid'."], 'status': 'draft'}, {'test_id': 'US004_TC004', 'description': 'Verify that the system displays an error message if the UPI payment fails.', 'steps': ['Step 1: Add a biller account with an outstanding bill.', 'Step 2: Attempt to pay the bill using UPI, but simulate a payment failure.', 'Step 3: Verify that the system displays an error message indicating that the payment has failed and provides a reason for the failure.'], 'status': 'draft'}, {'test_id': 'US004_TC005', 'description': 'Verify that the user can delete a biller account.', 'steps': ['Step 1: Add a biller account.', "Step 2: Navigate to the 'Pay Utility Bills' section.", 'Step 3: Select the biller account and choose the option to delete it.', 'Step 4: Confirm the deletion.', 'Step 5: Verify that the biller account is no longer displayed in the list of billers.'], 'status': 'draft'}, {'test_id': 'US005_TC001', 'description': 'Verify that the system provides a catalog of available insurance policies (health, auto, travel).', 'steps': ["Step 1: Navigate to the 'Purchase Insurance Policies' section in the app.", 'Step 2: Verify that the system displays a catalog of available insurance policies, including health, auto, and travel insurance.', 'Step 3: Verify that each policy type is clearly labeled and accessible.'], 'status': 'draft'}, {'test_id': 'US005_TC002', 'description': 'Verify that the system displays policy details, including coverage and premiums.', 'steps': ["Step 1: Navigate to the 'Purchase Insurance Policies' section.", 'Step 2: Select an insurance policy from the catalog.', 'Step 3: Verify that the system displays the policy details, including coverage amount, premium amount, and policy terms.'], 'status': 'draft'}, {'test_id': 'US005_TC003', 'description': 'Verify that the system facilitates the purchase of insurance policies and allows payment through the app.', 'steps': ['Step 1: Select an insurance policy.', 'Step 2: Review the policy details and choose the option to purchase it.', 'Step 3: Complete the purchase process, including providing the required information and making the payment through the app.', 'Step 4: Verify that the purchase is successful and the system displays a confirmation message.'], 'status': 'draft'}, {'test_id': 'US005_TC004', 'description': 'Verify that the system generates and provides access to the policy documentation after purchase.', 'steps': ['Step 1: Purchase an insurance policy.', 'Step 2: Verify that the system generates the policy documentation (e.g., PDF).', 'Step 3: Verify that the user can access and download the policy documentation from the app.'], 'status': 'draft'}, {'test_id': 'US005_TC005', 'description': 'Verify that the system displays an error message if the insurance purchase fails.', 'steps': ['Step 1: Select an insurance policy and attempt to purchase it.', 'Step 2: Simulate a payment failure during the purchase process.', 'Step 3: Verify that the system displays an error message indicating that the purchase has failed and provides a reason for the failure.'], 'status': 'draft'}, {'test_id': 'US006_TC001', 'description': 'Verify that the system enables users to book flight tickets from an external travel booking site.', 'steps': ["Step 1: Navigate to the 'Book Flight Tickets' section in the app.", 'Step 2: Verify that the system redirects the user to the integrated external travel booking site (e.g., BookMyTrip.com).'], 'status': 'draft'}, {'test_id': 'US006_TC002', 'description': 'Verify that the system provides users with flight options, dates, and pricing.', 'steps': ["Step 1: Navigate to the 'Book Flight Tickets' section.", 'Step 2: Search for flights using valid criteria (e.g., departure city, destination city, dates).', 'Step 3: Verify that the system displays a list of flight options with dates and pricing information.'], 'status': 'draft'}, {'test_id': 'US006_TC003', 'description': 'Verify that the system allows users to make payments for booked flights within the application.', 'steps': ['Step 1: Search for and select a flight.', 'Step 2: Proceed to the payment page within the application.', 'Step 3: Complete the payment process.', 'Step 4: Verify that the payment is successful and the booking is confirmed.'], 'status': 'draft'}, {'test_id': 'US006_TC004', 'description': 'Verify that the system displays a booking confirmation after successful flight booking.', 'steps': ['Step 1: Book a flight and complete the payment process.', 'Step 2: Verify that the system displays a booking confirmation with details such as booking reference number, flight details, and passenger information.'], 'status': 'draft'}, {'test_id': 'US006_TC005', 'description': 'Verify that the system displays an error message if the flight booking fails due to an external service outage.', 'steps': ['Step 1: Attempt to book a flight while simulating an external service outage.', 'Step 2: Verify that the system displays an error message indicating that the booking has failed due to an external service outage and suggests trying again later.'], 'status': 'draft'}]

CONSTANT_REVISED_TEST_CASES = [{'test_id': 'US005_TC001', 'description': 'Verify that the system provides a catalog of available insurance policies (health, auto, travel).', 'steps': ["Step 1: Navigate to the 'Purchase Insurance Policies' section in the app.", 'Step 2: Verify that the system displays a catalog of available insurance policies, including health, auto, and travel insurance.', 'Step 3: Verify that each policy type is clearly labeled and accessible.', 'Step 4: Verify that the catalog displays at least three different insurance providers for each policy type.'], 'status': 'draft'}, {'test_id': 'US005_TC002', 'description': 'Verify that the system displays policy details, including coverage, premiums, deductibles, and exclusions.', 'steps': ["Step 1: Navigate to the 'Purchase Insurance Policies' section.", 'Step 2: Select an insurance policy from the catalog.', 'Step 3: Verify that the system displays the policy details, including coverage amount, premium amount, policy terms, deductible amount, and key exclusions.', 'Step 4: Verify that the policy details are presented in a clear and understandable format.'], 'status': 'draft'}, {'test_id': 'US005_TC003', 'description': 'Verify that the system facilitates the purchase of insurance policies and allows payment through the app using various methods (UPI, Net Banking, Credit/Debit Card).', 'steps': ['Step 1: Select an insurance policy.', 'Step 2: Review the policy details and choose the option to purchase it.', 'Step 3: Complete the purchase process, including providing the required information (e.g., personal details, nominee details) and making the payment through the app using UPI.', 'Step 4: Verify that the purchase is successful and the system displays a confirmation message with the policy number and effective date.', 'Step 5: Repeat steps 3 and 4 using Net Banking as the payment method.', 'Step 6: Repeat steps 3 and 4 using Credit/Debit Card as the payment method.'], 'status': 'draft'}, {'test_id': 'US005_TC004', 'description': "Verify that the system generates and provides access to the policy documentation (PDF) immediately after purchase and sends a copy to the user's registered email address.", 'steps': ['Step 1: Purchase an insurance policy.', 'Step 2: Verify that the system generates the policy documentation (e.g., PDF).', 'Step 3: Verify that the user can access and download the policy documentation from the app.', "Step 4: Verify that a copy of the policy documentation is sent to the user's registered email address.", 'Step 5: Verify that the downloaded and emailed policy documents are identical.'], 'status': 'draft'}, {'test_id': 'US005_TC005', 'description': 'Verify that the system displays an appropriate error message if the insurance purchase fails due to insufficient balance, invalid card details, or network issues.', 'steps': ['Step 1: Select an insurance policy and attempt to purchase it.', 'Step 2: Simulate a payment failure due to insufficient balance.', 'Step 3: Verify that the system displays an error message indicating that the purchase has failed due to insufficient balance and suggests adding funds.', 'Step 4: Repeat steps 1-3, simulating a payment failure due to invalid card details.', 'Step 5: Verify that the system displays an error message indicating that the purchase has failed due to invalid card details and suggests checking the card information.', 'Step 6: Repeat steps 1-3, simulating a payment failure due to network issues.', 'Step 7: Verify that the system displays an error message indicating that the purchase has failed due to network issues and suggests trying again later.'], 'status': 'draft'}, {'test_id': 'US005_TC006', 'description': 'Verify that the system allows users to compare different insurance policies side-by-side based on key features and pricing.', 'steps': ["Step 1: Navigate to the 'Purchase Insurance Policies' section.", 'Step 2: Select two or more insurance policies to compare.', 'Step 3: Initiate the policy comparison feature.', 'Step 4: Verify that the system displays a side-by-side comparison of the selected policies, highlighting key features (e.g., coverage amount, premium, deductible) and pricing.', 'Step 5: Verify that the comparison table is easy to read and understand.'], 'status': 'draft'}, {'test_id': 'US005_TC007', 'description': 'Verify that the system provides a clear and concise explanation of insurance terms and conditions before purchase.', 'steps': ['Step 1: Select an insurance policy.', "Step 2: Before proceeding to purchase, locate the 'Terms and Conditions' section.", "Step 3: Verify that the system displays a clear and concise explanation of the policy's terms and conditions.", 'Step 4: Verify that the terms and conditions are easily accessible and understandable to a non-expert user.'], 'status': 'draft'}, {'test_id': 'US005_TC008', 'description': 'Verify that the system allows users to save a quote for an insurance policy and retrieve it later.', 'steps': ['Step 1: Select an insurance policy and configure the desired coverage options.', 'Step 2: Save the quote for the policy.', 'Step 3: Verify that the system saves the quote with a unique identifier.', 'Step 4: Navigate away from the insurance policy details.', 'Step 5: Retrieve the saved quote.', 'Step 6: Verify that the system retrieves the saved quote with all the previously configured options.'], 'status': 'draft'}]


CONSTANT_QA_TESTING_RESULTS = {'test_results': [{'test_id': 'TC001', 'description': 'Enable MFA with valid userId and mfaType', 'status': 'pass', 'actual_result': "The request to /api/auth/mfa/enable with a valid userId and mfaType ('mpin') returns a 200 status code and the message 'MFA enabled successfully'. The express-validator middleware validates the request body.", 'expected_result': "Response status 200 and message 'MFA enabled successfully'", 'failure_reason': None},
 {'test_id': 'TC002', 'description': 'Apply for a loan with valid amount and term', 'status': 'pass', 'actual_result': "The request to /api/loan/apply with a valid amount and term returns a response with loanId, status 'PENDING', and interest value. The amount is also returned in the response.", 'expected_result': "Response with loanId, status: 'PENDING', and interest value", 'failure_reason': None}, {'test_id': 'TC003', 'description': 'Link a bank account with valid details', 'status': 'pass', 'actual_result': "The request to /api/bank/link with valid accountNumber and bankName returns a 200 status code and the message 'Bank account linked successfully'.", 'expected_result': "Response status 200 and message 'Bank account linked successfully'", 'failure_reason': None}, {'test_id': 'TC004', 'description': 'Pay a bill with valid billId and amount', 'status': 'pass', 'actual_result': "The request to /api/bill/pay with a valid billId and amount returns a response with transactionId and status 'SUCCESS'.", 'expected_result': "Response with transactionId and status: 'SUCCESS'", 'failure_reason': None}, {'test_id': 'TC005', 'description': 'Purchase an insurance policy with valid policyId and term', 'status': 'pass', 'actual_result': "The request to /api/insurance/purchase with a valid policyId and term returns a response with policyNumber, status 'ACTIVE', and coverage amount.", 'expected_result': "Response with policyNumber, status: 'ACTIVE', and coverage amount", 'failure_reason': None}], 'summary': {'total_tests': 5, 'passed': 5, 'failed': 0, 'pass_percentage': 100}}

CONSTANT_DEPLOYMENT_STEPS = """
To deploy the provided backend and frontend applications, follow the steps outlined below. The frontend is built using React, TypeScript, and Tailwind CSS, while the backend is a Node.js application with Express. We\'ll deploy the backend using Docker and run it in a production environment.\n\n### Deployment Guide\n\n#### Prerequisites\n1. **Node.js** (version 14 or higher)\n2. **Docker**\n3. **A package manager like `npm`**\n4. **A cloud provider or local environment to host the application**\n\n#### Environment Setup\n\n1. **Clone the repositories for the frontend and backend.**\n\n    ```sh\n    git clone <frontend-repo-url> frontend\n    git clone <backend-repo-url> backend\n    ```\n\n2. **Install dependencies for both the frontend and backend.**\n\n    ```sh\n    cd frontend\n    npm install\n    cd ../backend\n    npm install\n    ```\n\n3. **Prepare the backend application for production.**\n\n    - Create a `.env` file in the backend root directory and add the necessary environment variables such as `PORT`, `JWT_SECRET`, `DB_URL`, etc.\n    \n    ```env\n    PORT=3000\n    JWT_SECRET=your_jwt_secret\n    # Add other environment variables as necessary\n    ```\n\n#### Build Instructions\n\n1. **Build the frontend for production.**\n\n    ```sh\n    cd frontend\n    npm run build\n    ```\n\n    This will create a `build` directory containing the production-ready files.\n\n2. **Build the Docker image for the backend.**\n\n    Add a Dockerfile in the backend directory:\n\n    ```dockerfile\n    # Dockerfile\n    FROM node:14-alpine\n\n    WORKDIR /app\n\n    COPY package*.json ./\n    RUN npm ci\n\n    COPY . .\n\n    CMD ["node", "src/server.js"]\n    ```\n\n    Build the Docker image:\n\n    ```sh\n    docker build -t paymate-backend .\n    ```\n\n#### Deployment Commands or Service Usage\n\n1. **Run the backend application using Docker.**\n\n    ```sh\n    docker run -p 3000:3000 -d --name paymate-backend paymate-backend\n    ```\n\n2. **Serve the frontend using a static file server.** If you are using a web server like Nginx or Apache, configure it to serve the `build` directory. If you are using a cloud provider, you can use its static hosting service.\n\n    Example using `http-server`:\n\n    ```sh\n    npm install -g http-server\n    cd frontend/build\n    http-server -p 8080\n    ```\n\n#### Post-Deployment Checks\n\n1. **Verify the application is running.**\n\n    - Access the frontend at `http://localhost:8080` (or the domain you\'ve set up).\n    - Access the backend APIs at `http://localhost:3000/api` (or the domain you\'ve set up).\n\n2. **Check the logs for any errors.**\n\n    For the backend, use Docker logs:\n\n    ```sh\n    docker logs paymate-backend\n    ```\n\n3. **Test the application.**\n\n    - Ensure all routes and functionalities work as expected.\n    - Check for security vulnerabilities and fix them.\n\n4. **Monitor and maintain the application.**\n\n    - Set up monitoring tools like Prometheus and Grafana for the backend.\n    - Use a CI/CD pipeline for continuous integration and deployment.\n\n### Troubleshooting Notes\n\n- **If you encounter issues with Docker, ensure Docker is running and check the Docker logs for errors.**\n- **For frontend issues, ensure you\'ve built the application correctly and that the web server is correctly serving the built files.**\n- **Ensure your backend is correctly configured with the environment variables and that the application is correctly handling them.**\n\nThis guide provides a general overview of setting up and deploying the frontend and backend applications. Adjust the steps as needed based on your specific deployment environment and requirements.


"""