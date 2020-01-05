# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, PasswordField
from collections import OrderedDict


class A:
    a = 1
    b = 2
    c = 3


class B(A):
    a = 4


a_test = B()
print(dir(a_test))

a = [attr for attr in dir(a_test) if not callable(getattr(a_test, attr)) and not attr.startswith("__")]
print(a)


a_dict = OrderedDict({'a': 1, 'b': 2, 'c': 3})
for x in a_dict.items():
    print(x)

a_dict['a'] = 4
for x in a_dict.items():
    print(x)



# class FormA(FlaskForm):
#     """Registration form."""
#
#     email = StringField(
#         'E-mail',
#         render_kw={"placeholder": 'Enterprise mailbox'}
#     )
#
#     given_name = StringField(
#         'Given Name',
#     )
#
#     sur_name = StringField(
#         'Sur Name',
#     )
#     ...
#
#
# class FormB(FormA):
#
#     email = StringField(
#         'E-mail',
#         render_kw={"placeholder": 'Enterprise mailbox',
#                    "readonly": True}
#     )
#
#
# b_test = FormB()
# print(dir(b_test))

from itertools import chain

# a = [1,2,3,4]
#
# b = [5,6,7,8]

a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]

for a, b in chain(a, b):
    print(a, b)
