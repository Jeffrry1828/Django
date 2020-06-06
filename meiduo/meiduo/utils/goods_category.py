from collections import OrderedDict

from django.conf import settings

from goods.models import GoodsCategory, GoodsChannel


def get_goods_category():
    '''
    {
        组编号（同频道）:{
            一级分类channels：[]
            二级分类sub_cats：[]
        }
    }
    如：
    {
        1:{
            channels:[
                {手机},{相机},{数码}
            ],
            sub_cats:[二级分类]
        },
        2:{
            channels:[
                {电脑},{办公},{家用电器}
            ],
            sub_cats:[二级分类]
        },
        ....
    }
    '''
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        # channel.group_id===>组编号
        # channel.category====>一级分类
        # channel.url=========>一级分类的链接
        if channel.group_id not in categories:
            categories[channel.group_id] = {'channels': [], 'sub_cats': []}
        # 添加一级分类
        categories[channel.group_id]['channels'].append({
            'id': channel.id,
            'name': channel.category.name,
            'url': channel.url
        })
        # 添加二级分类
        sub_cats = channel.category.goodscategory_set.all()
        # 添加三级分类
        for sub in sub_cats:
            sub.sub_cats = sub.goodscategory_set.all()
            categories[channel.group_id]['sub_cats'].append(sub)
    # print(categories)

    return categories
