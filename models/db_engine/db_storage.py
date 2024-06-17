
from os import getenv
import dotenv
import logging
from datetime import datetime
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session 
from models.base_model import Base
from models.user import User
from models.blog import Blog
from models.comment import Comment
from models.archived_comment import ArchivedComment
from models.archived_user import ArchivedUser
from models.archived_blog import ArchivedBlog

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

DB_USER = getenv('DB_USERNAME')
DB_PWD = getenv('DB_PASSWORD')
HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')

CLASSES = {
    'User': User,
    'Blog': Blog,
    'Comment': Comment,
    'ArchivedComment': ArchivedComment,
    'ArchivedUser': ArchivedUser,
    'ArchivedBlog': ArchivedBlog
    }


def hash_password(pwd):
    """
    Hashes a password using bcrypt.

    Parameters:
    pwd (str): The password to hash.

    Returns:
    str: The hashed password.
    """
    if not isinstance(pwd, str):
        raise ValueError("Password must be a string")
    if not pwd:
        raise ValueError("Password cannot be empty")
    
    try:
        encoded_pwd = pwd.encode()
        hashed_pwd = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
        return hashed_pwd.decode()
    except Exception as e:
        raise ValueError(f"An error occurred while hashing the password: {e}")



class DBStorage:
    def __init__(self):
        con_strings = f'mysql+mysqlconnector://{DB_USER}:{DB_PWD}@{HOST}/{DB_NAME}'
        self.engine = create_engine(con_strings, pool_recycle=True, echo=True)
        
        Session_factory = sessionmaker(expire_on_commit=False,
                                       autoflush=False,
                                       autocommit=False,
                                       bind=self.engine)
        # the scoped_session is used mostly in web-apps for handling multiple
        # user requests
        self.Session = scoped_session(Session_factory)
        # The scoped_session decorator wraps the Session_factory to provide thread-local sessions.
        # Scoped Session: The scoped_session should be created once in the __init__ method and reused.

    # for using DBStorage as a context manager
    def __enter__(self):
        '''Enter the runtime context related to this object.'''
        self.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Exit the runtime context related to this object.

            exc_type: The type of the exception that was raised.
            This is the class of the exception (e.g., ValueError, TypeError).

            exc_val:The value of the exception. This is the instance of the exception
            that was raised.
            
            exc_tb: The traceback object, which contains the stack trace at the point
            where the exception was raised.
        '''
        try:
            if exc_val is None:
                self.session().commit()  # Commit if no exception occurred
            else:
                self.session().rollback()  # Rollback if an exception occurred
        except Exception as exc:
            logger.error(exc_type)
            logger.error(exc_tb)
            logger.error(f"Error in context manager: {exc}")
        finally:
            self.close()  # Always close the session on exiting

    def session(self):
        return self.Session
    # Session Handling: The session method should return a new session instance each time it's called.

    def add(self, obj):
        '''Adds an object to the current session.'''
        session = self.session()
        try:
            session.add(obj)
        except Exception as exc:
            logger.error('Error adding object: ', exc)

    def save(self):
        '''Commits the current session, saving changes to the database.'''
        session = self.session()
        try:
            session.commit()
        except Exception as exc:
            logger.error('Error saving to table: ', exc)
    
    def handle_user(self, user_dict: dict = None, user_id=None, edit=False, delete=False):
        session = self.session()
        with session.begin():
            # for user deletion
            try:
                if user_id and delete and not user_dict and not edit:
                    print('about to delete user')
                    user_to_delete: object = session.query(User).filter_by(id=user_id).one_or_none()
                    if user_to_delete:
                        session.delete(user_to_delete)
                        session.commit()
                        # print(f'user {user_to_delete} successfully deleted')
                        return self.to_dict(user_to_delete)
            except Exception as exc:
                logger.error(f'error deleting user {user_id}', exc)

        # for user update
        try:
            with session.begin():
                if edit and user_id and user_dict and not delete:
                    if isinstance(user_id, str):
                        if not all(hasattr(User, key) for key in user_dict.keys()):
                            print(f'User dictionary contains invalid attributes')
                            return
                        user_dict['updated_at'] = datetime.now()
                        user_to_update: int = session.query(User).filter_by(id=user_id).update(user_dict, synchronize_session='fetch')
                        if not user_to_update:
                            print(f'could not find user to update {user_dict}')
                            return
                        else:
                            session.commit()
                            # print(f'user_to_update: {user_to_update}')
                            return user_to_update
                    else:
                        logger.info('Invalid user_id type, expected a string')
                        return
        except Exception as exc:
            logger.error(f'Error updating user: {exc}')
            return

        # for adding new user
        try:
            with session.begin():
                if not edit and not delete and not user_id and user_dict:
                    if isinstance(user_dict, dict):
                        if not all(hasattr(User, key) for key in user_dict.keys()):
                            logger.info('User dictionary contains invalid attributes')
                            return
                        user_email_exists = session.query(User).filter_by(email=user_dict['email']).one_or_none()
                        username_exists = session.query(User).filter_by(username=user_dict['username']).one_or_none()
                        if user_email_exists or username_exists:
                            logger.info('username or user_email already exists')
                            return

                        hashed_pwd = hash_password(user_dict['password'])
                        user_dict['password'] = hashed_pwd
                        new_user = User(**user_dict)
                        session.add(new_user)
                        session.commit()
                        print('new_user from dbstorage: ', self.to_dict(new_user))
                        return self.to_dict(new_user)
                    else:
                        logger.info('Invalid user_dict type, expected a dictionary')
                        return
        except Exception as exc:
            logger.error(f'Error adding new user: {exc}')
            return
    
    def handle_blog(self, user_id, blog_dict: dict = None, blog_id=None, delete=False, edit=False):
        session = self.session()

        with session.begin():
            # blog deletion
            if user_id and blog_id and delete and not blog_dict and not edit:
                try:
                    if not isinstance(blog_id, int):
                        logger.info(f'blog with id {blog_id} not an integer')
                        return False
                    blog_to_delete: object = session.query(Blog).filter_by(
                        user_id=user_id,
                        id=blog_id,
                        ).one_or_none()
                    if blog_to_delete:
                        session.delete(blog_to_delete)
                        session.commit()
                        return self.to_dict(blog_to_delete)
                except Exception as exc:
                    logger.error(f'error deleting blog with id: {blog_id}: ', exc)

        with session.begin():
            # edit a blog
            if user_id and blog_dict and blog_id and edit and not delete:
                checks = [isinstance(user_id, str), isinstance(blog_dict, dict)]
                if all(checks):
                    blog_dict['updated_at'] = datetime.now()
                    try:
                        blog_to_update: int = session.query(Blog).filter_by(id=blog_id, user_id=user_id).update(blog_dict, synchronize_session='fetch')
                        # print(f'blog: {blog_to_update}')
                        session.commit()
                        return blog_to_update
                    except Exception as exc:
                        logger.error(f'error updating blog: {blog_dict}')
                        return
                else:
                    logger.info('user_id or blog_id not a string')
                    return

        with session.begin(): 
            # add new blog
            if user_id and not delete and not edit and blog_dict and not blog_id:
                if isinstance(user_id, str) and isinstance(blog_dict, dict):
                    if not all(hasattr(Blog, key) for key in blog_dict.keys()):
                        logger.info(f'{blog_dict} not an attr of blog')
                        return
                    try:
                        logger.info(f'searching for user {user_id} to add new blog')
                        user = session.query(User).filter_by(id=user_id).one_or_none()
                        if user:
                            blog_dict['user_id'] = user_id
                            new_blog = Blog(**blog_dict)
                            session.add(new_blog)
                            session.commit()
                            logger.info('added blog successfully')
                            return self.to_dict(new_blog)
                        else:
                            logger.info(f'user with id {user_id} not found')
                    except Exception as exc:
                        logger.error(f'error add new blog {exc}')
                        return
                else:
                    logger.info('user_id or blog_id not a string')
                    return
    
    def handle_comment(self, user_id, blog_id=None, comment=None, comment_id=None, delete=False, edit=False):
        session = self.session()
        # comment deletion
        if user_id and blog_id and comment_id and delete and not comment and not edit:
            try:
                with session.begin():
                    if not isinstance(blog_id, int) or not isinstance(comment_id, int):
                        logger.info(f'{blog_id} or {comment_id} not an integer')
                        return False
                    comment_to_delete: object = session.query(Comment).filter_by(
                        user_id=user_id,
                        blog_id=blog_id,
                        id=comment_id
                        ).one_or_none()
                    print('comment_to_delete: ', self.to_dict(comment_to_delete))
                    if comment_to_delete:
                        session.delete(comment_to_delete)
                        session.commit()
                        return self.to_dict(comment_to_delete)
            except Exception as exc:
                logger.error(f'error deleting comment with id: {comment_id}: ', exc)

        # for comment updating
        if edit and user_id and comment_id and blog_id and not delete:
            try:
                with session.begin():
                    comment_to_update: int = session.query(Comment).filter_by(id=comment_id, user_id=user_id, blog_id=blog_id).update(
                        {'comment': comment, 'updated_at': datetime.now()},
                        synchronize_session='fetch'
                    )
                    print(f'comment: {comment_to_update}')
                    session.commit()
                    return comment_to_update
            except Exception as exc:
                logger.error('db.handle_comment: error editing comment: ', exc)
                return

        # for comment insertion
        if not edit and not delete and user_id and comment and blog_id:
            checks = [isinstance(user_id, str), isinstance(blog_id, int)]
            if not all(checks):
                logger.info('user_id or comment not a string')
                return
            if comment.strip() == '':
                logger.info('comment can not be empty')
                return
            try:
                with session.begin():
                    new_comment = Comment(comment=comment, user_id=user_id, blog_id=blog_id)
                    session.add(new_comment)
                    session.commit()
                    return self.to_dict(new_comment)
            except Exception as exc:
                logger.error('db.handle_comment: error adding comment: ', exc)
                return
        else:
            logger.info('no user_id or comment provided')
            return
    
    def get_blogs(self, user_id, blog_id=None):
        session = self.session()

        # retrieve a single blog
        if user_id and blog_id:
            try:
                with session.begin():
                    blog = session.query(Blog).filter_by(id=blog_id, user_id=user_id).one_or_none()
                    if blog:
                        return self.to_dict(blog)
            except Exception as exc:
                logger.error(f'could not find blog with id {blog_id}')

        # retrieve all blogs associated with a user
        elif user_id and not blog_id:
            try:
                with session.begin():
                    all_blogs = session.query(Blog).filter_by(user_id=user_id).all()
                    if all_blogs:
                        return self.to_dict(list(all_blogs))
            except Exception as exc:
                logger.error(f'error finding blog with user_id :{user_id}')

    def get_user(self, user_id, blog_id=None):
        session = self.session()

        # retrieve a single blog
        if user_id and blog_id:
            try:
                with session.begin():
                    blog = session.query(Blog).filter_by(id=blog_id, user_id=user_id).one_or_none()
                    if blog:
                        return self.to_dict(blog)
            except Exception as exc:
                logger.error(f'could not find blog with id {blog_id}')

        # retrieve all blogs associated with a user
        elif user_id and not blog_id:
            try:
                with session.begin():
                    all_blogs = session.query(Blog).filter_by(user_id=user_id).all()
                    if all_blogs:
                        return self.to_dict(list(all_blogs))
            except Exception as exc:
                logger.error(f'error finding blog with user_id :{user_id}')

    def get_comment(self, user_id, blog_id=None):
        session = self.session()

        # retrieve a single blog
        if user_id and blog_id:
            try:
                with session.begin():
                    blog = session.query(Blog).filter_by(id=blog_id, user_id=user_id).one_or_none()
                    if blog:
                        return self.to_dict(blog)
            except Exception as exc:
                logger.error(f'could not find blog with id {blog_id}')

        # retrieve all blogs associated with a user
        elif user_id and not blog_id:
            try:
                with session.begin():
                    all_blogs = session.query(Blog).filter_by(user_id=user_id).all()
                    if all_blogs:
                        return self.to_dict(list(all_blogs))
            except Exception as exc:
                logger.error(f'error finding blog with user_id :{user_id}')
    
    def to_dict(self, obj):
        '''converts obj to list of dict or a dict
            params: obj
                a list of objects
                or a single object
        '''
        # if obj is a list
        if isinstance(obj, list):
            all_obj = []
            for ob in obj:
                obj_dict = ob.__dict__.copy()
                obj_dict.pop('_sa_instance_state', None)
                all_obj.append(obj_dict)
            return all_obj
        # if obj is not a list
        obj_dict = obj.__dict__.copy()
        obj_dict.pop('_sa_instance_state', None)
        if 'comments' in obj_dict.keys():
            comments_obj = [{k: v for k, v in com.__dict__.copy().items() if k != '_sa_instance_state'} for com in obj_dict.get('comments')]
        if 'blogs' in obj_dict.keys():
            blogs_obj = [{k: v for k, v in blog.__dict__.copy().items() if k != '_sa_instance_state'} for blog in obj_dict.get('blogs')]
            relationship = [obj_dict, blogs_obj, comments_obj]
            return relationship
        return obj_dict

    def close(self):
        '''Removes the current session from the scoped session registry.'''
        session = self.session()
        try:
            session.close()
        except Exception as exc:
            logger.error(f'Error closing session: {exc}')
            return
        

    def create_all_tables(self):
        try:
            # next is to use the metadata of declarative_base to create the table
            Base.metadata.create_all(self.engine)
        except Exception as exc:
            logger.error(f'Error creating Tables: {exc}')
            return

    def drop_all_tables(self):
        '''Drops all tables associated with the models '''
        try:
            Base.metadata.drop_all(self.engine)
        except Exception as exc:
            logger.error(f'Error dropping tables: {exc}')
            return
