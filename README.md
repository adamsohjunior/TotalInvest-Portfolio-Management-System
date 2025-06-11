# TotalInvest-Portfolio-Management-System
**NTU College of Computing and Data Science**

This repository contains the implementation of a SQL-based database application for **SC2207: Introduction to Databases** at Nanyang Technological University (AY2024/2025 Semester 2). The application simulates a backend database system for **TotalWealth**, a digital investment platform.

---

## Overview

TotalWealth is a licensed digital investment company that provides a mobile app acting as a digital financial advisor to help people manage their wealth. The mobile app is the client-facing tool for their proprietary investment management system called TotalInvest. Our team are assigned to build the database for TotalInvest to capture all the data necessary for the operations of the mobile app and TotalInvest. This project covers the lifecycle stages of database design and implementation, including:

- Entity-Relationship (ER) Modeling
- Normalized Relational Schema Design
- SQL DDL Implementation
- Query Writing and Testing
- Data Population for Demonstration
- Analysis with Advanced SQL Queries

---

## 📋 Project Tasks

| Task | Description |
|------|-------------|
| 1 | **ER Diagram Creation**<br>Designed the initial conceptual model based on the business requirements from TotalWealth's investment platform. |
| 2 | **ER Diagram Finalization**<br>Refined and validated the conceptual model based on supervisor feedback, ensuring accurate use of relationships, weak entities, and constraints. |
| 3 | **Relational Schema Design & Normalization**<br>Translated the ER diagram into relational schema, identified functional dependencies, and ensured all relations were in 3NF or higher. |
| 4 | **SQL Schema Implementation & Data Population**<br>Created SQL tables using DDL with appropriate primary/foreign key constraints and inserted realistic data. We simulated stock market transactions including asset purchases, top-ups, withdrawals, and rebalancing to support query testing. |
| 5 | **SQL Query Development & Testing**<br>Wrote and executed complex SQL queries to fulfill analytical requirements (e.g., investor performance, behavioral patterns), and captured output results for final demonstration. |

---

## Queries
1. Find investors who are making on average a loss across all their portfolios in 2024.
2. Find investors who are seeing an annualized return of more than 10% from their portfolios in 2024.
3. Find the monthly average unrealized gain/loss of portfolios for each month in 2024.
4. What is the top three most popular first financial goals for investors in 2024?
5. Find investors who consistently top up their investment at the beginning of every month (dollar-cost averaging) in 2024 for at least one of their portfolios.
6. Find the most popular financial goals for investors working in the same company and whose age is between 30 to 40 years old.
7. Are male investors in their 20s making more money from their investments than their female counterparts in 2024?
