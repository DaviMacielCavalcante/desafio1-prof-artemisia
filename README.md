# **ETL Beginner Challenge**  

![License Used](https://img.shields.io/github/license/DaviMacielCavalcante/desafio_etl_begginer)
![Python](https://img.shields.io/badge/Python-3.12.4-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)  

## **Description:**  
This project was developed as part of an ETL challenge for beginners. The goal is to extract, transform, and load data from a CSV file into a local database. PostgreSQL was used in this project.  

## **Features:**  
- Data extraction from a CSV file  
- Data transformation with cleaning and standardization  
- Data loading into a relational database (PostgreSQL)  
- Full CRUD functionality via API with FastAPI  

## **Installation:**  

1. Clone this repository:  
   ```bash
   git clone https://github.com/DaviMacielCavalcante/desafio_etl_begginer.git
   cd desafio_etl_begginer

2. Install the dependencies from requirements.txt
   ```bash
   pip install -r requirements.txt
3. Install PostgreSQL on your machine.
4. Create a .env file with the following variables
```
DATABASE_PORT = port your database is using
DATABASE_NAME = name of your database
DATABASE_USERNAME = user with access to the database
DATABASE_PASSWORD = user's password
DATABASE_URL = your database's address
```
5. Run the script responsible for creating the database schema in PostgreSQL:
   ```bash
   python criacao_tabelas.py
6. Run the script responsible for the ETL pipeline
   ```bash
   python main.py
7. Watch the cool side of the Force in action::

<div align="center"> <img src="https://www.icegif.com/wp-content/uploads/2022/09/icegif-1012.gif" alt="darth_vader_local_nevando" width="500"/></div>

## How to Contribute:
Contributions are welcome! Please follow these guidelines:

- Fork the project.
- Create a branch for the feature you want to implement (git checkout -b my-new-feature).
- Commit your changes with meaningful messages (git commit -m 'Add new feature').
- Push to the created branch (git push origin my-new-feature).
- Open a pull request for review.

## License:
This project is licensed under the MIT License - see the LICENSE.md file for more details.

## Contact:
If you have any questions or issues, feel free to contact:

## 📧 Email: 
davicc@outlook.com.br

## Sith Lords Responsible for the Project:
- Darth Davi ⚔️😡
## Mentor Who Proposed the Challenge:
- Prof. Artemisia Weyl

👩‍💻 Mentor’s GitHub: https://github.com/arteweyl

*Through victory, my chains are broken. <br>
The Force shall free me.*
