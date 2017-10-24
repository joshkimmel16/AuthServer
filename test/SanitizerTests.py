from sys import path
import os
path.append(os.pardir + "\\server\\bin")
from Sanitizer import Sanitizer, SanitizerException

#constructor
s = Sanitizer()

#/register/application
s.Evaluate("register_application", {"name": "Test Application"}) #valid
s.Evaluate("register_application", {"name": "Test Application", "algorithm": "HS256"}) #valid
try:
    s.Evaluate("register_application", {}) #invalid - missing name
    raise Exception("register_application missing name test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_application", {"name": 12323}) #invalid - bad name type
    raise Exception("register_application invalid name type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_application", {"name": ";DELETE FROM applications;"}) #invalid - bad name value
    raise Exception("register_application invalid name value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_application", {"name": "Test Application", "algorithm": 456}) #invalid - bad algorithm type
    raise Exception("register_application invalid algorithm type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_application", {"name": "Test Application", "algorithm": "blah"}) #invalid - bad algorithm value
    raise Exception("register_application invalid algorithm value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/update/application
s.Evaluate("update_application", {"name": "Test Application"}) #valid
s.Evaluate("update_application", {"name": "Test Application", "algorithm": "HS256"}) #valid
s.Evaluate("update_application", {"algorithm": "HS256"}) #valid
s.Evaluate("update_application", {}) #valid
try:
    s.Evaluate("update_application", {"name": 12323}) #invalid - bad name type
    raise Exception("update_application invalid name type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_application", {"name": ";DELETE FROM applications;"}) #invalid - bad name value
    raise Exception("update_application invalid name value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_application", {"name": "Test Application", "algorithm": 456}) #invalid - bad algorithm type
    raise Exception("update_application invalid algorithm type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_application", {"name": "Test Application", "algorithm": "blah"}) #invalid - bad algorithm value
    raise Exception("update_application invalid algorithm value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/unregister/application
s.Evaluate("unregister_application", {"id": 123}) #valid
try:
    s.Evaluate("unregister_application", {}) #invalid - missing id
    raise Exception("unregister_application missing id test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("unregister_application", {"id": "blah"}) #invalid - bad id type
    raise Exception("unregister_application invalid id type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("unregister_application", {"id": 0}) #invalid - bad id value
    raise Exception("unregister_application invalid id value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/register/user
s.Evaluate("register_user", {"name": "test.user", "password": "aA1!@#$%^&*()", "metadata": {"key": "value"}}) #valid
s.Evaluate("register_user", {"name": "test.user", "password": "aA1!@#$%^&*()"}) #valid
try:
    s.Evaluate("register_user", {"password": "aA1!@#$%^&*()", "metadata": {"key": "value"}}) #invalid - missing name
    raise Exception("register_user missing name test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": 3243, "password": "aA1!@#$%^&*()", "metadata": {"key": "value"}}) #invalid - bad name type
    raise Exception("register_user invalid name type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": ";DELETE FROM applications;", "password": "aA1!@#$%^&*()", "metadata": {"key": "value"}}) #invalid - bad name value
    raise Exception("register_user invalid name value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": "test.user", "metadata": {"key": "value"}}) #invalid - missing password
    raise Exception("register_user missing password test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": "test.user", "password": 23424, "metadata": {"key": "value"}}) #invalid - bad password type
    raise Exception("register_user invalid password type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": "test.user", "password": ";DELETE FROM applications;", "metadata": {"key": "value"}}) #invalid - bad password value
    raise Exception("register_user invalid password value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("register_user", {"name": "test.user", "password": ";DELETE FROM applications;", "metadata": 32432}) #invalid - bad metadata type
    raise Exception("register_user invalid metadata type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e

#/retrieve/user
s.Evaluate("retrieve_user", {"metadata": {"key": "value"}}) #valid
try:
    s.Evaluate("retrieve_user", {}) #invalid - missing metadata
    raise Exception("retrieve_user missing metadata test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("retrieve_user", {"metadata": 32432}) #invalid - bad metadata type
    raise Exception("retrieve_user invalid metadata type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/update/username
s.Evaluate("update_username", {"name": "test.user"}) #valid
try:
    s.Evaluate("update_username", {}) #invalid - missing name
    raise Exception("update_username missing name test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_username", {"name": 3243}) #invalid - bad name type
    raise Exception("update_username invalid name type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_username", {"name": ";DELETE FROM applications;"}) #invalid - bad name value
    raise Exception("update_username invalid name value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/update/password
s.Evaluate("update_password", {"password": "aA1!@#$%^&*()"}) #valid
try:
    s.Evaluate("update_password", {}) #invalid - missing password
    raise Exception("update_password missing password test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_password", {"password": 23424}) #invalid - bad password type
    raise Exception("update_password invalid password type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_password", {"password": ";DELETE FROM applications;"}) #invalid - bad password value
    raise Exception("update_password invalid password value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/update/metadata
s.Evaluate("update_metadata", {"metadata": {"key": "value"}}) #valid
try:
    s.Evaluate("update_metadata", {}) #invalid - missing metadata
    raise Exception("update_metadata missing metadata test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("update_metadata", {"metadata": 32432}) #invalid - bad metadata type
    raise Exception("update_metadata invalid metadata type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e

#/unregister/user
s.Evaluate("unregister_user", {"id": 123}) #valid
try:
    s.Evaluate("unregister_user", {}) #invalid - missing id
    raise Exception("unregister_user missing id test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("unregister_user", {"id": "blah"}) #invalid - bad id type
    raise Exception("unregister_user invalid id type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("unregister_user", {"id": 0}) #invalid - bad id value
    raise Exception("unregister_user invalid id value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e