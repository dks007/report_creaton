from django.apps import AppConfig

class MainConfig (AppConfig):
    name='success_tool'

    def ready(self):
        from success_tool import scheduler
        #print(f'Inside start scheduler class')
        scheduler.start()

    
