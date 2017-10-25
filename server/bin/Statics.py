from Helpers import Helpers
from DataLayer import PostGres
from Errors import Error

h = Helpers()

#class defining methods to interact with static data
class Statics:
    
    #constructor that captures info for DB connections
    def __init__ (self, config):
        self.authConfig = config["data"]["statics"]
        self.data_layer = PostGres()
        
    #create an asset
    def create_asset (self, page, component, asset_key, asset_value):
        try:
            self.data_layer.Connect(self.authConfig["server"], self.authConfig["db"], self.authConfig["user"], self.authConfig["password"])
            res = self.data_layer.ExecuteFunction('create_asset', ['string', 'string', 'string', 'string'], [page, component, asset_key, asset_value])
            self.data_layer.Disconnect()
            return "Asset Created!"
        except Exception as e:
            raise StaticsException("Could not create the asset!", "create_asset", e)
            
    #retrieve all assets for a given page
    def get_assets (self, page):
        def list_reduce (item):
            return item[0]
        
        try:
            self.data_layer.Connect(self.authConfig["server"], self.authConfig["db"], self.authConfig["user"], self.authConfig["password"])
            res = self.data_layer.ExecuteFunction('get_assets', ["string"], [page])
            self.data_layer.Disconnect()
            return h.list_map(res, list_reduce)
        except Exception as e:
            raise StaticsException("Could not get the assets for the given page!", "get_assets", e)
            
#custom Statics errors
class StaticsException (Error):
    pass
        
    