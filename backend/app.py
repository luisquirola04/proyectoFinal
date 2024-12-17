from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    #TODO
    
    app.config.from_object('config.config.Config')
    
    
    with app.app_context():
        
        # import routes
        from routes.route_chat import url_chatbot
     
        # add routes
        app.register_blueprint(url_chatbot)
            
    return app