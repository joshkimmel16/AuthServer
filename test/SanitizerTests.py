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
    
#/statics/create
s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "key": "testKey", "value": "testValue"}) #valid
try:
    s.Evaluate("create_asset", {"component": "testComponent", "key": "testKey", "value": "testValue"}) #invalid - missing page
    raise Exception("create_asset missing page test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": 1234, "component": "testComponent", "key": "testKey", "value": "testValue"}) #invalid - bad page type
    raise Exception("create_asset invalid page type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": ";DELETE FROM users;", "component": "testComponent", "key": "testKey", "value": "testValue"}) #invalid - bad page value
    raise Exception("create_asset invalid page value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "key": "testKey", "value": "testValue"}) #invalid - missing component
    raise Exception("create_asset missing component test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": 1234, "key": "testKey", "value": "testValue"}) #invalid - bad component type
    raise Exception("create_asset invalid component type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": ";DELETE FROM users;", "key": "testKey", "value": "testValue"}) #invalid - bad component value
    raise Exception("create_asset invalid component value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "value": "testValue"}) #invalid - missing asset_key
    raise Exception("create_asset missing asset_key test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "key": 1234, "value": "testValue"}) #invalid - bad asset_key type
    raise Exception("create_asset invalid asset_key type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "key": ";DELETE FROM users;", "value": "testValue"}) #invalid - bad asset_key value
    raise Exception("create_asset invalid asset_key value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "key": "testKey"}) #invalid - missing asset_value
    raise Exception("create_asset missing asset_value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("create_asset", {"page": "testPage", "component": "testComponent", "key": "testKey", "value": 1234}) #invalid - bad asset_value type
    raise Exception("create_asset invalid asset_value type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/statics/get
s.Evaluate("get_assets", {"page": "testPage"}) #valid
try:
    s.Evaluate("get_assets", {}) #invalid - missing page
    raise Exception("get_assets missing page test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("get_assets", {"page": 1234}) #invalid - bad page type
    raise Exception("get_assets invalid page type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("get_assets", {"page": ";DELETE FROM users;"}) #invalid - bad page value
    raise Exception("get_assets invalid page value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/authorize/user
s.Evaluate("authorize_user", {"username": "test.user", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"})
try:
    s.Evaluate("authorize_user", {"app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - missing username
    raise Exception("authorize_user missing username test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": 12345, "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad username type
    raise Exception("authorize_user invalid username type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": ";DELETE FROM users;", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad username value
    raise Exception("authorize_user invalid username value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "test.user", "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - missing app_id
    raise Exception("authorize_user missing app_id test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "test.user", "app_id": "skjfksjn", "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad app_id type
    raise Exception("authorize_user invalid app_id type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "josh.kimmel", "app_id": -56, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad app_id value
    raise Exception("authorize_user invalid app_id value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "test.user", "app_id": 1}) #invalid - missing redirect_url
    raise Exception("authorize_user missing redirect_url test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "test.user", "app_id": 1, "redirect_url": 1234}) #invalid - bad redirect_url type
    raise Exception("authorize_user invalid redirect_url type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_user", {"username": "test.user", "app_id": 1, "redirect_url": ";DELETE FROM users;"}) #invalid - bad redirect_url value
    raise Exception("authorize_user invalid redirect_url value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
    
#/authorize/password
s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"})
try:
    s.Evaluate("authorize_password", {"password": "testing", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - missing user_id
    raise Exception("authorize_password missing user_id test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": "jkfdkjsn", "password": "testing", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad user_id type
    raise Exception("authorize_password invalid user_id type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 0, "password": "testing", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad user_id value
    raise Exception("authorize_password invalid username value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - missing app_id
    raise Exception("authorize_password missing app_id test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": "skjfksjn", "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad app_id type
    raise Exception("authorize_password invalid app_id type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": -56, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad app_id value
    raise Exception("authorize_password invalid app_id value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": 1}) #invalid - missing redirect_url
    raise Exception("authorize_password missing redirect_url test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": 1, "redirect_url": 1234}) #invalid - bad redirect_url type
    raise Exception("authorize_password invalid redirect_url type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": "testing", "app_id": 1, "redirect_url": ";DELETE FROM users;"}) #invalid - bad redirect_url value
    raise Exception("authorize_password invalid redirect_url value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - missing password
    raise Exception("authorize_password missing password test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": 1234, "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad password type
    raise Exception("authorize_password invalid password type test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e
try:
    s.Evaluate("authorize_password", {"user_id": 1, "password": ";DELETE FROM users;", "app_id": 1, "redirect_url": "http://v-lsg-lfstest.laserfiche.com"}) #invalid - bad password value
    raise Exception("authorize_password invalid password value test failed!")
except SanitizerException as e:
    pass
except Exception as e:
    raise e