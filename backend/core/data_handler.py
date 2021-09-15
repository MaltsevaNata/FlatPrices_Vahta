from models import RealEstate


class DataHandler:
    def __init__(self, data: RealEstate):
        self.data = data

    def perform_handling(self):
        pass

    def enrich_data(self):
        pass

    def send_predict_task(self):
        pass