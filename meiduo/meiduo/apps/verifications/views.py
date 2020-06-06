from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework import serializers
import random
from utils.ytx_sdk.sendSMS import CCP
from . import constants
from celery_tasks.sms.tasks import send_sms_code


class SMSCodeView(APIView):
    # 发送短信验证码
    def get(self, request, mobile):
        '''
        限制60秒内只向一个手机号发送一次短信验证码
        '''
        # 获取Redis的连接：从配置中的cache处，根据名称获取连接
        redis_cli = get_redis_connection('sms_code')

        # 1.判断60秒内是不向指定手机号发过短信，如果发过，则抛异常
        if redis_cli.get('sms_flag_' + mobile):
            raise serializers.ValidationError('向此手机号发短信太频繁了')

        # 2.如果未发短信，则
        # 2.1随机生成6位数
        code = random.randint(100000, 999999)

        # 2.2保存到redis：验证码，发送的标记
        # redis_cli.setex('sms_code_'+mobile,300,code)
        # redis_cli.setex('sms_flag_'+mobile,60,1)
        # 优化：pipeline管道
        redis_pipeline = redis_cli.pipeline()
        redis_pipeline.setex('sms_code_' + mobile, constants.SMS_CODE_EXPIRES, code)
        redis_pipeline.setex('sms_flag_' + mobile, constants.SMS_FLAG_EXPIRES, 1)
        redis_pipeline.execute()

        # 2.3发短信：云通讯
        # CCP.sendTemplateSMS(mobile,code,constants.SMS_CODE_EXPIRES/60,1)
        # print(code)
        #调用celery任务，执行耗时代码
        send_sms_code.delay(mobile,code,constants.SMS_CODE_EXPIRES/60,1)

        # 3.响应
        return Response({'message': 'OK'})
