from rest_framework.response import Response
from rest_framework.views import APIView
from .qq_sdk import OAuthQQ
from .models import QQUser
from utils.jwt_token import generate
from utils import tjws
from . import constants
from .serializers import QQBindSerializer
from carts.utils import merge_cookie_to_redis


class QQurlView(APIView):
    def get(self, request):
        # 接收登录后的地址
        state = request.query_params.get('next')
        # 创建工具类对象
        oauthqq = OAuthQQ(state=state)
        # 获取授权地址
        url = oauthqq.get_qq_login_url()
        # 响应
        return Response({
            'login_url': url
        })


class QQLoginView(APIView):
    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        # 根据code获取token
        oauthqq = OAuthQQ()
        token = oauthqq.get_access_token(code)

        # 根据token获取openid
        openid = oauthqq.get_openid(token)

        # 查询openid是否存在
        try:
            qquser = QQUser.objects.get(openid=openid)
        except:
            # 如果不存在，则通知客户端转到绑定页面
            # 将openid加密进行输出
            data = tjws.dumps({'openid': openid}, constants.BIND_TOKEN_EXPIRES)
            # 响应
            return Response({
                'access_token': data
            })
        else:
            # 如果存在则登录成功
            # 状态保持
            response = Response({
                'user_id': qquser.user.id,
                'username': qquser.user.username,
                'token': generate(qquser.user)
            })
            # 合并
            response = merge_cookie_to_redis(request, qquser.user.id, response)
            # 响应
            return response

    def post(self, request):
        # 接收
        serializer = QQBindSerializer(data=request.data)
        # 验证
        if not serializer.is_valid():
            return Response({'message': serializer.errors})
        # 绑定：在qquser表中创建一条数据
        qquser = serializer.save()
        # 响应：绑定完成，登录成功，状态保持
        response = Response({
            'user_id': qquser.user.id,
            'username': qquser.user.username,
            'token': generate(qquser.user)
        })
        # 合并
        response = merge_cookie_to_redis(request, qquser.user.id, response)
        # 响应
        return response
