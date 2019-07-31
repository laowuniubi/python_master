from django import forms
from django import forms


class ErrorInfoForm(forms.Form):
    # 该form用于被多继承
    # 继承者可以调用这里的方法来获取表单验证的错误信息
    def get_errors(self):
        """
        返回表单验证的所有错误信息
        :return: 字典，key为表单字段的值，元素为列表，列表为错误信息的集合
        """
        errors = self.errors.get_json_data()
        new_errors = {}
        for key, message_dicts in errors.items():
            messages = []
            for message in message_dicts:
                messages.append(message['message'])
            new_errors[key] = messages
        return new_errors

    def get_first_error(self):
        """
        :return: 第一个错误信息的值，没有则返回None
        """
        errors = self.get_errors()
        for key in errors.keys():
            return errors[key][0]
        return None
