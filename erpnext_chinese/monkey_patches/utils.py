from frappe import utils

#因网络问题导致获取用户图像超时，故取消此功能，详见https://gitee.com/yuzelin/erpnext-chinese-docs/issues/I3PXHV
def has_gravatar(email):
    return ''

utils.has_gravatar = has_gravatar