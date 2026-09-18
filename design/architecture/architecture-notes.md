\# System Architecture Notes



\## Project

Explainable Human-in-the-Loop Import Compliance Document Screening System



\## Architectural Goal

The system screens synthetic import documents against a limited set of publicly available compliance rules. It identifies possible compliance issues, explains why each rule was triggered, and requires a human reviewer to make the final decision.



\## High-Level Data Flow



Synthetic Import Document

&#x20;       |

&#x20;       v

Document Ingestion and Input Validation

&#x20;       |

&#x20;       v

Field Extraction Module

&#x20;       |

&#x20;       v

Rule Engine

&#x20;       |

&#x20;       v

Explanation Generator

&#x20;       |

&#x20;       v

Reviewer Interface

&#x20;       |

&#x20;       v

Human Reviewer Decision

&#x20;       |

&#x20;       v

Audit Log



Supporting components:

\- Authentication and Role-Based Authorization

\- Rule Configuration Store

\- SQLite Database



\## Main Components



\### 1. Document Ingestion and Input Validation

Receives synthetic import documents and checks whether required input is present and structurally valid before further processing.



\### 2. Field Extraction Module

Uses pattern matching and regular expressions to extract selected fields such as product category, declared value, HS code, and required document fields.



\### 3. Rule Engine

Compares extracted values against stored compliance rules and determines whether a rule has been triggered.



\### 4. Explanation Generator

Produces a deterministic explanation showing the rule identifier, extracted value, and reason the rule was triggered.



\### 5. Reviewer Interface

Displays document information, flags, and explanations. The reviewer must record an explicit decision for each flagged item.



\### 6. Authentication and Authorization

Authenticates users and applies role-based permissions. Reviewers can evaluate flags, while administrators can modify rule configurations.



\### 7. Audit Logging

Records rule triggers, reviewer decisions, administrative rule changes, authenticated user identity, and timestamps.



\### 8. Data Storage

SQLite stores rules, document records, extracted values, flags, reviewer actions, and audit records.



\## Architectural Principle



The system is decision support rather than automated enforcement. A document cannot receive a final compliance determination solely from the rule engine. Final authority remains with the human reviewer.

