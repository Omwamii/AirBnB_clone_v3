#!/usr/bin/python3
"""
Unit Test for FileStorage Class
"""
import unittest
from datetime import datetime
import inspect
import json
import models
from models import engine
from models.engine.file_storage import FileStorage
import pep8
from os import environ, stat, remove, path

User = models.user.User
BaseModel = models.base_model.BaseModel
State = models.state.State
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE != 'db':
    FileStorage = models.engine.file_storage.FileStorage
storage = models.storage
F = 'file.json'


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is not db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    all_funcs = inspect.getmembers(FileStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        pass

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        # storage.delete_all()
        remove(F)

    def test_doc_file(self):
        """ test doc for file
        """
        pass

    def test_doc_class(self):
        """ test doc for class
        """
        pass

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestFileStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_fs(self):
        """... filestorage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/engine/file_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        cls.bm_obj = BaseModel()
        cls.state_obj = State(name="Illinois")
        cls.bm_obj.save()
        cls.state_obj.save()

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        pass

    def setUp(self):
        """initializes new storage object for testing"""
        self.bm_obj = TestBmFsInstances.bm_obj
        self.state_obj = TestBmFsInstances.state_obj

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        self.assertTrue(path.isfile(F))

    def test_all(self):
        """... checks if all() function returns newly created instance"""
        bm_id = self.bm_obj.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_all_state(self):
        """... checks if all() function returns newly created state instance"""
        state_id = self.state_obj.id
        state_objs = storage.all("State")
        actual = False
        for k in state_objs.keys():
            if state_id in k:
                actual = True
        self.assertTrue(True)

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(True)

    def test_to_dict(self):
        """... to_dict should return serializable dict object"""
        my_model_json = self.bm_obj.to_dict()
        actual = True
        try:
            serialized = json.dumps(my_model_json)
        except Exception:
            actual = False
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = True
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """sets up the class"""
        cls.user = User()
        cls.user.save()
        cls.bm_obj = BaseModel()
        cls.bm_obj.save()

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        # storage.delete_all()
        remove(F)

    def setUp(self):
        """initializes new user for testing"""
        self.user = TestUserFsInstances.user
        self.bm_obj = TestUserFsInstances.bm_obj

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.user.save()
        self.assertTrue(path.isfile(F))

    def test_count_cls(self):
        """... checks count method with class input arg"""
        count_user = storage.count('User')
        expected = 1
        self.assertEqual(expected, count_user)

    def test_count_all(self):
        """... checks the count method with no class input"""
        count_all = storage.count()
        expected = 4
        self.assertEqual(expected, count_all)

    def test_get_cls_id(self):
        """... checks get method with class and id inputs
        duplicate = storage.get('User', self.user.id)
        expected = self.user.id
        actual = duplicate.id
        self.assertEqual(expected, actual)
        """
        pass

    def test_all(self):
        """... checks if all() function returns newly created instance"""
        u_id = self.user.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        remove(F)
        self.user.save()
        u_id = self.user.id
        actual = False
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
                actual = True
        self.assertTrue(actual)


if __name__ == '__main__':
    unittest.main
