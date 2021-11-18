
def add_user_data_api(cls):

    @property
    def user_data(self):
        if self.has_object_user_data:
            return self._get_object_user_data()
        else:
            return None

    cls.user_data = user_data

    @user_data.setter
    def user_data(self, ud):
        if ud is None:
            self._clear_object_user_data()
        else:
            self._set_object_user_data(ud)
    cls.user_data = user_data

    @property
    def int_user_data(self):
        if self.has_int_user_data:
            return self._get_int_user_data()
        else:
            return None
    cls.user_data = user_data

    @int_user_data.setter
    def int_user_data(self, ud):
        if ud is None:
            self._clear_int_user_data()
        else:
            self._set_int_user_data(int(ud))
    cls.int_user_data = int_user_data
