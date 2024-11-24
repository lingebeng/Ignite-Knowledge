from django.db import models


class CodeForces(models.Model):
    """
    CodeForces(标题，内容，类别，样例输入，样例输出，备注，示例代码，测试输入，测试输出)
    """
    title = models.CharField(max_length=40)

    content = models.TextField()
    algorithm_type = models.CharField(max_length=40)

    example_input = models.TextField()
    example_output = models.TextField()
    test_input = models.TextField()
    test_output = models.TextField()

    remarks = models.TextField()
    code = models.TextField()



