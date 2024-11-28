class GlobalData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user_id = None
            cls._instance.exam_id = None
        return cls._instance

    # Setters and getters for user_id and exam_id
    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def set_exam_id(self, exam_id):
        self.exam_id = exam_id

    def get_exam_id(self):
        return self.exam_id

