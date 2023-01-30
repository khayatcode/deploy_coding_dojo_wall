from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the user table from our database
from flask import flash

from flask_app.models.user import User

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        
    @classmethod
    def save(cls, data):
        query = """ INSERT INTO posts ( user_id, content, created_at, updated_at ) 
        VALUES ( %(user_id)s, %(content)s, NOW() , NOW() ); """
        return connectToMySQL('user_post').query_db( query, data )
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('user_post').query_db( query, data )
    
    @staticmethod
    def validate_post_data( data ):
        is_valid = True
        if len(data['content']) == 0:
            flash("Content cannot be blank", "post")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all_posts_with_creator(cls):
        # Get all tweets, and their one associated User that created it
        query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL('user_post').query_db(query)
        all_posts = []
        for row in results:
            # Create a Tweet class instance from the information from each db row
            one_post = cls(row)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_posts_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author = User(one_posts_author_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_post.creator = author
            # Append the Tweet containing the associated User to your list of tweets
            all_posts.append(one_post)
        return all_posts


    