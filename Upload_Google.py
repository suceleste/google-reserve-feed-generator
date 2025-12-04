
import os
import time
import shutil
import json
import paramiko 
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTION_DIR = os.path.join(BASE_DIR, "action")
ENTITY_DIR = os.path.join(BASE_DIR, "entity")
SERVICE_DIR = os.path.join(BASE_DIR, "service")

SFTP_HOST = "partnerupload.google.com"
SFTP_PORT = 19321
SFTP_USER = "user-sftp"
SFTP_KEY_PATH = os.path.join(BASE_DIR, "id_rsa")

FEEDS = [
    {
        "folder": ACTION_DIR,
        "file_desc": "reservewithgoogle.action.v2",
        "file_prefix": "action_"
    },
    {
        "folder": ENTITY_DIR,
        "file_desc": "reservewithgoogle.entity",
        "file_prefix": "entity_"
    },
    {
        "folder": SERVICE_DIR,
        "file_desc": "glam.service.v0",
        "file_prefix": "service_"
    }
]

LOG_FILE = os.path.join(BASE_DIR, "activity.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def SFTP_Transfer(files, folder):
    print("\nConnexion SFTP...")
    logging.info("Connexion SFTP OK")

    try :
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SFTP_HOST, port=SFTP_PORT, username=SFTP_USER, key_filename=SFTP_KEY_PATH)
        
        sftp = ssh.open_sftp()

        for file in files :
            try :

                file_path = os.path.join(folder, file)
                sftp.put(file_path, f"/{file}")

                print(f"Fichier Transferé : {file}")
                logging.info(f'Fichier Transféré : {file}')

            except Exception as e :
                print(f'Erreur : Transfer Fichier [{e}]')
                logging.info(f"Erreur : Transfer Fichier [{e}]")

        ssh.close()
        sftp.close()

    except Exception as e :
        print(f'Erreur : Connexion SFTP [{e}]')
        logging.info(f"Erreur : Connexion SFTP [{e}]")


def Generate_Upload_File() :
    print("Démarrage...")
    logging.info("--- Démarrage Script ---")

    current_timestamp = int(time.time())
    

    for feed in FEEDS : 

        index = 0
        files_to_upload = []
        files = [f for f in os.listdir(feed["folder"]) if f.startswith(feed["file_prefix"])]

        print(f"Dossier Chargé : {files}")

        if not files :
            logging.error("Erreur : Dossier Vide")

        for file in files : 

            index += 1 

            data_filename =  f"{feed["file_prefix"]}{current_timestamp}_{index:03d}.json"
            data_path = os.path.join(feed["folder"], data_filename)

            shutil.copy(f"{feed["folder"]}\\{file}", data_path)
            files_to_upload.append(data_filename)
            os.remove(f"{feed["folder"]}\\{file}")
            print(f"Rename file : {file} to {data_filename}")

        desc_filename_before = [f for f in os.listdir(feed["folder"]) if f.startswith(feed["file_desc"])][0]
        os.remove(f"{feed["folder"]}\\{desc_filename_before}")

        desc_filename = f"{feed["file_desc"]}-{current_timestamp}.filesetdesc.json"
        desc_path = os.path.join(f"{feed["folder"]}", desc_filename)

        desc_content = {
            "generation_timestamp": current_timestamp,
            "name": feed["file_desc"],
            "data_file": files_to_upload
        }

        with open(desc_path, "w", encoding="utf-8") as f:
            json.dump(desc_content, f, indent=2)

        files_to_upload.append(desc_filename)

        print(f"Rename file : {desc_filename_before} to {desc_filename}")

        SFTP_Transfer(files_to_upload, feed["folder"])

if __name__ == '__main__' :
    Generate_Upload_File()