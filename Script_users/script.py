import os
import random
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()



class DatabaseHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Conected to the database")
        except psycopg2.Error as e:
            print(f"Unable to connect to the database. Error: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")
        else:
            print("Your database already Disconnected")

    def execute_query(self, query, params=None, return_last_inserted_id=False):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()

            if return_last_inserted_id:
                self.cursor.execute("SELECT lastval();")
                last_inserted_id = self.cursor.fetchone()[0]
                return last_inserted_id

            print("Query executed succssfully")
        except psycopg2.Error as e:
            print(f"Error executing query. {e}")
            self.connection.rollback()

    def fetchall_all_rows(self, query, params=None, chunk_size=1000):
        try:
            self.cursor.execute(query, params)
            rows = []
            while True:
                chunk = self.cursor.fetchmany(chunk_size)
                if not chunk:
                    break
                rows.extend(chunk)
            return rows
        except psycopg2.Error as e:
            print(f"Error fetching rows. {e}")
            return None


class GetData:
    def __init__(self):
        self.file_path = None
        self.folder_path = None

    def read_file(self):
        try:
            with open(self.file_path, 'r') as f:
                connect = f.read()
                return connect
        except FileNotFoundError:
            print(f"File not found at path: {self.file_path}")
        except PermissionError as permission_error:
            print(f"Error: Permission issue - {permission_error}")
        except OSError as os_error:
            print(f"Error: OS-related error - {os_error}")
        except Exception as e:
            print(f"Error: An unexpected exception occurred - {e}")

    def read_folder(self):
        try:
            files = os.listdir(self.folder_path)
            return files
        except FileNotFoundError as file_not_found_error:
            print(f"Error: Folder not found {file_not_found_error}")
        except PermissionError as permission_error:
            print(f"Error: Permission issue - {permission_error}")
        except OSError as os_error:
            print(f"Error: OS-related error - {os_error}")
        except Exception as e:
            print(f"Error: An unexpected exception occurred - {e}")


class RegexHandler:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.username = None
        self.email = None
        self.date_list = None
        self.password = os.getenv('SECRET_KEY')

        self.data_range = None
        self.image_list = None
        self.image_folder = None
        self.text_list = None
        self.used_text = []
        self.used_images = []

    def get_data_from_users_file(self):
        try:
            if self.date_list:
                user_data = self.date_list.split(' ')
                if user_data:
                    self.first_name = user_data[2]
                    self.last_name = user_data[5]
                    self.username = user_data[7]
                    self.email = user_data[9]
                else:
                    print("Cannot split your data")
            else:
                print("Date list does not exist")
        except IndexError as index_error:
            print(f"Error: Index error occurred - {index_error}")
        except Exception as e:
            print(f"Error: An unexpected exception occurred - {e}")

    def get_random_image(self):
        try:
            if self.image_list:
                image = f'{self.image_folder}/'+random.choice(self.image_list)
                return image
            else:
                print("Image list does not exist")
        except Exception as e:
            print(f"Error: An unexpected exception occurred - {e}")

    def get_random_text(self):
        try:
            if self.text_list:
                text = random.choice(self.text_list)
                while text in self.used_text:
                    text = random.choice(self.text_list)
                self.used_text.append(text)
                return text
            else:
                print("Text list does not exist")
        except IndexError as index_error:
            print(f"Error: Index error occurred - {index_error}")
        except Exception as e:
            print(f"Error: An unexpected exception occurred - {e}")


def read_data_files(data_connect):
    data_connect.file_path = "data/Users.txt"
    file_user_content = data_connect.read_file().split('\n')

    data_connect.folder_path = "../media/profile_images"
    folder_avatar_content = data_connect.read_folder()

    data_connect.file_path = "data/Users bio.txt"
    file_bio_content = data_connect.read_file().split('.')

    data_connect.folder_path = "../media/posts_images"
    folder_post_image_content = data_connect.read_folder()

    data_connect.file_path = "data/Post/Post_comment.txt"
    file_comments_content = data_connect.read_file().split('!')

    data_connect.file_path = "data/Post/Post_tag.txt"
    file_tags_content = data_connect.read_file().split()

    return (file_user_content, folder_avatar_content, file_bio_content,
            folder_post_image_content, file_comments_content, file_tags_content)


def insert_user_data(db, developing, file_user_content, folder_avatar_content, file_bio_content,
                     folder_post_image_content, file_comments_content, file_tags_content):

    for content in file_user_content:
        developing.date_list = content
        developing.get_data_from_users_file()

        developing.image_list = folder_avatar_content
        developing.image_folder = 'profile_images'
        avatar = developing.get_random_image()

        developing.text_list = file_bio_content
        bio = developing.get_random_text()

        developing.image_list = folder_post_image_content
        developing.image_folder = "posts_images"
        post_image = developing.get_random_image()

        developing.text_list = file_comments_content
        comment = developing.get_random_text()

        developing.text_list = file_tags_content
        tag = developing.get_random_text()

        first_name = developing.first_name
        last_name = developing.last_name
        username = developing.username
        email = developing.email
        password = developing.password
        is_staff = False
        is_active = True
        is_superuser = False
        current_date = datetime.now()

        user_id = db.execute_query("INSERT INTO auth_user (first_name, last_name, password, username, email, is_staff, is_active, is_superuser, date_joined) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                                   (first_name, last_name, password, username, email, is_staff, is_active, is_superuser, current_date),
                                   return_last_inserted_id=True)

        if user_id is not None:
            profile_id = db.execute_query("INSERT INTO users_profile (avatar, bio, user_id) VALUES (%s, %s, %s) RETURNING id;",
                                          (avatar, bio, user_id),
                                          return_last_inserted_id=True)

            post_id = db.execute_query("INSERT INTO posts_posts (comments, user_id, date) VALUES (%s, %s, %s) RETURNING id;",
                                       (comment, profile_id, current_date),
                                       return_last_inserted_id=True)

            if post_image is not None and tag is not None:
                image_id = db.execute_query("INSERT INTO posts_images(image) VALUES (%s) RETURNING id;",
                                            (post_image,),
                                            return_last_inserted_id=True)
                tag_id = db.execute_query("INSERT INTO posts_tags(tags) VALUES (%s) RETURNING id;",
                                          (tag,),
                                          return_last_inserted_id=True)

                db.execute_query("INSERT INTO posts_posts_images(posts_id, images_id) VALUES (%s, %s);", (post_id, image_id))
                db.execute_query("INSERT INTO posts_posts_tags(posts_id, tags_id) VALUES (%s, %s);", (post_id, tag_id))


def main():
    data_connect = GetData()

    (file_user_content, folder_avatar_content, file_bio_content,
     folder_post_image_content, file_comments_content, file_tags_content) = read_data_files(data_connect)

    db = DatabaseHandler(dbname='backend',
                         user='postgres',
                         password='2002182000',
                         host='backend.c92aeqekkolm.eu-north-1.rds.amazonaws.com',
                         port='5432')
    db.connect()

    developing = RegexHandler()

    insert_user_data(db, developing, file_user_content, folder_avatar_content, file_bio_content,
                     folder_post_image_content, file_comments_content, file_tags_content)

    db.disconnect()


if __name__ == '__main__':
    main()
