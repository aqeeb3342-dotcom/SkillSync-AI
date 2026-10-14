import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="SkillSync@2026",
        database="skillsync_ai"
    )

    return connection
    
