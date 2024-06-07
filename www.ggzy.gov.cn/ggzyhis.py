import datetime
import time
import random
import re
import base64
import json
import requests
import feapder
from feapder import Item
from lxml import etree
import tools

now = time.time()
timeArray = time.localtime(now)
nowtime = time.strftime("%Y-%m-%d", timeArray)


class AirSpiderJygk(feapder.AirSpider):
    '''
                       函数入口
                        :return:
               '''

    def start_requests(self):
        provinces = [{'value': '110000', 'province': '北京',
                      'area': [{'value': '110000', 'city': '省本级'}, {'value': '110101', 'city': '东城区'},
                               {'value': '110102', 'city': '西城区'}, {'value': '110105', 'city': '朝阳区'},
                               {'value': '110106', 'city': '丰台区'}, {'value': '110107', 'city': '石景山区'},
                               {'value': '110108', 'city': '海淀区'}, {'value': '110109', 'city': '门头沟区'},
                               {'value': '110111', 'city': '房山区'}, {'value': '110112', 'city': '通州区'},
                               {'value': '110113', 'city': '顺义区'}, {'value': '110114', 'city': '昌平区'},
                               {'value': '110115', 'city': '大兴区'}, {'value': '110116', 'city': '怀柔区'},
                               {'value': '110117', 'city': '平谷区'}, {'value': '110118', 'city': '密云区'},
                               {'value': '110119', 'city': '延庆区'}]},
                     {'value': '120000', 'province': '天津',
                      'area': [{'value': '120000', 'city': '省本级'}, {'value': '120101', 'city': '和平区'},
                               {'value': '120102', 'city': '河东区'}, {'value': '120103', 'city': '河西区'},
                               {'value': '120104', 'city': '南开区'}, {'value': '120105', 'city': '河北区'},
                               {'value': '120106', 'city': '红桥区'}, {'value': '120110', 'city': '东丽区'},
                               {'value': '120111', 'city': '西青区'}, {'value': '120112', 'city': '津南区'},
                               {'value': '120113', 'city': '北辰区'}, {'value': '120114', 'city': '武清区'},
                               {'value': '120115', 'city': '宝坻区'}, {'value': '120116', 'city': '滨海新区'},
                               {'value': '120117', 'city': '宁河区'}, {'value': '120118', 'city': '静海区'},
                               {'value': '120119', 'city': '蓟州区'}]},
                     {'value': '130000', 'province': '河北',
                      'area': [{'value': '130000', 'city': '省本级'}, {'value': '130100', 'city': '石家庄市'},
                               {'value': '130200', 'city': '唐山市'}, {'value': '130300', 'city': '秦皇岛市'},
                               {'value': '130400', 'city': '邯郸市'}, {'value': '130500', 'city': '邢台市'},
                               {'value': '130600', 'city': '保定市'}, {'value': '130700', 'city': '张家口市'},
                               {'value': '130800', 'city': '承德市'}, {'value': '130900', 'city': '沧州市'},
                               {'value': '131000', 'city': '廊坊市'}, {'value': '131100', 'city': '衡水市'}]},
                     {'value': '140000', 'province': '山西',
                      'area': [{'value': '140000', 'city': '省本级'}, {'value': '140100', 'city': '太原市'},
                               {'value': '140200', 'city': '大同市'}, {'value': '140300', 'city': '阳泉市'},
                               {'value': '140400', 'city': '长治市'}, {'value': '140500', 'city': '晋城市'},
                               {'value': '140600', 'city': '朔州市'}, {'value': '140700', 'city': '晋中市'},
                               {'value': '140800', 'city': '运城市'}, {'value': '140900', 'city': '忻州市'},
                               {'value': '141000', 'city': '临汾市'}, {'value': '141100', 'city': '吕梁市'}]},
                     {'value': '150000', 'province': '内蒙古',
                      'area': [{'value': '150000', 'city': '省本级'}, {'value': '150100', 'city': '呼和浩特市'},
                               {'value': '150200', 'city': '包头市'}, {'value': '150300', 'city': '乌海市'},
                               {'value': '150400', 'city': '赤峰市'}, {'value': '150500', 'city': '通辽市'},
                               {'value': '150600', 'city': '鄂尔多斯市'}, {'value': '150700', 'city': '呼伦贝尔市'},
                               {'value': '150800', 'city': '巴彦淖尔市'}, {'value': '150900', 'city': '乌兰察布市'},
                               {'value': '152200', 'city': '兴安盟'}, {'value': '152500', 'city': '锡林郭勒盟'},
                               {'value': '152900', 'city': '阿拉善盟'}]},
                     {'value': '210000', 'province': '辽宁',
                      'area': [{'value': '210000', 'city': '省本级'}, {'value': '210100', 'city': '沈阳市'},
                               {'value': '210200', 'city': '大连市'}, {'value': '210300', 'city': '鞍山市'},
                               {'value': '210400', 'city': '抚顺市'}, {'value': '210500', 'city': '本溪市'},
                               {'value': '210600', 'city': '丹东市'}, {'value': '210700', 'city': '锦州市'},
                               {'value': '210800', 'city': '营口市'}, {'value': '210900', 'city': '阜新市'},
                               {'value': '211000', 'city': '辽阳市'}, {'value': '211100', 'city': '盘锦市'},
                               {'value': '211200', 'city': '铁岭市'}, {'value': '211300', 'city': '朝阳市'},
                               {'value': '211400', 'city': '葫芦岛市'}]},
                     {'value': '220000', 'province': '吉林',
                      'area': [{'value': '220000', 'city': '省本级'}, {'value': '220100', 'city': '长春市'},
                               {'value': '220200', 'city': '吉林市'}, {'value': '220300', 'city': '四平市'},
                               {'value': '220400', 'city': '辽源市'}, {'value': '220500', 'city': '通化市'},
                               {'value': '220600', 'city': '白山市'}, {'value': '220700', 'city': '松原市'},
                               {'value': '220800', 'city': '白城市'}, {'value': '222400', 'city': '延边朝鲜族自治州'}]},
                     {'value': '230000', 'province': '黑龙江',
                      'area': [{'value': '230000', 'city': '省本级'}, {'value': '230100', 'city': '哈尔滨市'},
                               {'value': '230200', 'city': '齐齐哈尔市'}, {'value': '230300', 'city': '鸡西市'},
                               {'value': '230400', 'city': '鹤岗市'}, {'value': '230500', 'city': '双鸭山市'},
                               {'value': '230600', 'city': '大庆市'}, {'value': '230700', 'city': '伊春市'},
                               {'value': '230800', 'city': '佳木斯市'}, {'value': '230900', 'city': '七台河市'},
                               {'value': '231000', 'city': '牡丹江市'}, {'value': '231100', 'city': '黑河市'},
                               {'value': '231200', 'city': '绥化市'}, {'value': '232700', 'city': '大兴安岭地区'}]},
                     {'value': '310000', 'province': '上海',
                      'area': [{'value': '310000', 'city': '省本级'}, {'value': '310101', 'city': '黄浦区'},
                               {'value': '310104', 'city': '徐汇区'}, {'value': '310105', 'city': '长宁区'},
                               {'value': '310106', 'city': '静安区'}, {'value': '310107', 'city': '普陀区'},
                               {'value': '310109', 'city': '虹口区'}, {'value': '310110', 'city': '杨浦区'},
                               {'value': '310112', 'city': '闵行区'}, {'value': '310113', 'city': '宝山区'},
                               {'value': '310114', 'city': '嘉定区'}, {'value': '310115', 'city': '浦东新区'},
                               {'value': '310116', 'city': '金山区'}, {'value': '310117', 'city': '松江区'},
                               {'value': '310118', 'city': '青浦区'}, {'value': '310120', 'city': '奉贤区'},
                               {'value': '310151', 'city': '崇明区'}]},
                     {'value': '320000', 'province': '江苏',
                      'area': [{'value': '320000', 'city': '省本级'}, {'value': '320100', 'city': '南京市'},
                               {'value': '320200', 'city': '无锡市'}, {'value': '320300', 'city': '徐州市'},
                               {'value': '320400', 'city': '常州市'}, {'value': '320500', 'city': '苏州市'},
                               {'value': '320600', 'city': '南通市'}, {'value': '320700', 'city': '连云港市'},
                               {'value': '320800', 'city': '淮安市'}, {'value': '320900', 'city': '盐城市'},
                               {'value': '321000', 'city': '扬州市'}, {'value': '321100', 'city': '镇江市'},
                               {'value': '321200', 'city': '泰州市'}, {'value': '321300', 'city': '宿迁市'}]},
                     {'value': '330000', 'province': '浙江',
                      'area': [{'value': '330000', 'city': '省本级'}, {'value': '330100', 'city': '杭州市'},
                               {'value': '330200', 'city': '宁波市'}, {'value': '330300', 'city': '温州市'},
                               {'value': '330400', 'city': '嘉兴市'}, {'value': '330500', 'city': '湖州市'},
                               {'value': '330600', 'city': '绍兴市'}, {'value': '330700', 'city': '金华市'},
                               {'value': '330800', 'city': '衢州市'}, {'value': '330900', 'city': '舟山市'},
                               {'value': '331000', 'city': '台州市'}, {'value': '331100', 'city': '丽水市'}]},
                     {'value': '340000', 'province': '安徽',
                      'area': [{'value': '340000', 'city': '省本级'}, {'value': '340100', 'city': '合肥市'},
                               {'value': '340200', 'city': '芜湖市'}, {'value': '340300', 'city': '蚌埠市'},
                               {'value': '340400', 'city': '淮南市'}, {'value': '340500', 'city': '马鞍山市'},
                               {'value': '340600', 'city': '淮北市'}, {'value': '340700', 'city': '铜陵市'},
                               {'value': '340800', 'city': '安庆市'}, {'value': '341000', 'city': '黄山市'},
                               {'value': '341100', 'city': '滁州市'}, {'value': '341200', 'city': '阜阳市'},
                               {'value': '341300', 'city': '宿州市'}, {'value': '341500', 'city': '六安市'},
                               {'value': '341600', 'city': '亳州市'}, {'value': '341700', 'city': '池州市'},
                               {'value': '341800', 'city': '宣城市'}]},
                     {'value': '350000', 'province': '福建',
                      'area': [{'value': '350000', 'city': '省本级'}, {'value': '350100', 'city': '福州市'},
                               {'value': '350200', 'city': '厦门市'}, {'value': '350300', 'city': '莆田市'},
                               {'value': '350400', 'city': '三明市'}, {'value': '350500', 'city': '泉州市'},
                               {'value': '350600', 'city': '漳州市'}, {'value': '350700', 'city': '南平市'},
                               {'value': '350800', 'city': '龙岩市'}, {'value': '350900', 'city': '宁德市'}]},
                     {'value': '360000', 'province': '江西',
                      'area': [{'value': '360000', 'city': '省本级'}, {'value': '360100', 'city': '南昌市'},
                               {'value': '360200', 'city': '景德镇市'}, {'value': '360300', 'city': '萍乡市'},
                               {'value': '360400', 'city': '九江市'}, {'value': '360500', 'city': '新余市'},
                               {'value': '360600', 'city': '鹰潭市'}, {'value': '360700', 'city': '赣州市'},
                               {'value': '360800', 'city': '吉安市'}, {'value': '360900', 'city': '宜春市'},
                               {'value': '361000', 'city': '抚州市'}, {'value': '361100', 'city': '上饶市'}]},
                     {'value': '370000', 'province': '山东',
                      'area': [{'value': '370000', 'city': '省本级'}, {'value': '370100', 'city': '济南市'},
                               {'value': '370200', 'city': '青岛市'}, {'value': '370300', 'city': '淄博市'},
                               {'value': '370400', 'city': '枣庄市'}, {'value': '370500', 'city': '东营市'},
                               {'value': '370600', 'city': '烟台市'}, {'value': '370700', 'city': '潍坊市'},
                               {'value': '370800', 'city': '济宁市'}, {'value': '370900', 'city': '泰安市'},
                               {'value': '371000', 'city': '威海市'}, {'value': '371100', 'city': '日照市'},
                               {'value': '371300', 'city': '临沂市'}, {'value': '371400', 'city': '德州市'},
                               {'value': '371500', 'city': '聊城市'}, {'value': '371600', 'city': '滨州市'},
                               {'value': '371700', 'city': '菏泽市'}]},
                     {'value': '410000', 'province': '河南',
                      'area': [{'value': '410000', 'city': '省本级'}, {'value': '410100', 'city': '郑州市'},
                               {'value': '410200', 'city': '开封市'}, {'value': '410300', 'city': '洛阳市'},
                               {'value': '410400', 'city': '平顶山市'}, {'value': '410500', 'city': '安阳市'},
                               {'value': '410600', 'city': '鹤壁市'}, {'value': '410700', 'city': '新乡市'},
                               {'value': '410800', 'city': '焦作市'}, {'value': '410900', 'city': '濮阳市'},
                               {'value': '411000', 'city': '许昌市'}, {'value': '411100', 'city': '漯河市'},
                               {'value': '411200', 'city': '三门峡市'}, {'value': '411300', 'city': '南阳市'},
                               {'value': '411400', 'city': '商丘市'}, {'value': '411500', 'city': '信阳市'},
                               {'value': '411600', 'city': '周口市'}, {'value': '411700', 'city': '驻马店市'},
                               {'value': '419001', 'city': '济源市'}]},
                     {'value': '420000', 'province': '湖北',
                      'area': [{'value': '420000', 'city': '省本级'}, {'value': '420100', 'city': '武汉市'},
                               {'value': '420200', 'city': '黄石市'}, {'value': '420300', 'city': '十堰市'},
                               {'value': '420500', 'city': '宜昌市'}, {'value': '420600', 'city': '襄阳市'},
                               {'value': '420700', 'city': '鄂州市'}, {'value': '420800', 'city': '荆门市'},
                               {'value': '420900', 'city': '孝感市'}, {'value': '421000', 'city': '荆州市'},
                               {'value': '421100', 'city': '黄冈市'}, {'value': '421200', 'city': '咸宁市'},
                               {'value': '421300', 'city': '随州市'}, {'value': '422800', 'city': '恩施土家族苗族自治州'},
                               {'value': '429004', 'city': '仙桃市'}, {'value': '429005', 'city': '潜江市'},
                               {'value': '429006', 'city': '天门市'}, {'value': '429021', 'city': '神农架林区'}]},
                     {'value': '430000', 'province': '湖南',
                      'area': [{'value': '430000', 'city': '省本级'}, {'value': '430100', 'city': '长沙市'},
                               {'value': '430200', 'city': '株洲市'}, {'value': '430300', 'city': '湘潭市'},
                               {'value': '430400', 'city': '衡阳市'}, {'value': '430500', 'city': '邵阳市'},
                               {'value': '430600', 'city': '岳阳市'}, {'value': '430700', 'city': '常德市'},
                               {'value': '430800', 'city': '张家界市'}, {'value': '430900', 'city': '益阳市'},
                               {'value': '431000', 'city': '郴州市'}, {'value': '431100', 'city': '永州市'},
                               {'value': '431200', 'city': '怀化市'}, {'value': '431300', 'city': '娄底市'},
                               {'value': '433100', 'city': '湘西土家族苗族自治州'}]},
                     {'value': '440000', 'province': '广东',
                      'area': [{'value': '440000', 'city': '省本级'}, {'value': '440100', 'city': '广州市'},
                               {'value': '440200', 'city': '韶关市'}, {'value': '440300', 'city': '深圳市'},
                               {'value': '440400', 'city': '珠海市'}, {'value': '440500', 'city': '汕头市'},
                               {'value': '440600', 'city': '佛山市'}, {'value': '440700', 'city': '江门市'},
                               {'value': '440800', 'city': '湛江市'}, {'value': '440900', 'city': '茂名市'},
                               {'value': '441200', 'city': '肇庆市'}, {'value': '441300', 'city': '惠州市'},
                               {'value': '441400', 'city': '梅州市'}, {'value': '441500', 'city': '汕尾市'},
                               {'value': '441600', 'city': '河源市'}, {'value': '441700', 'city': '阳江市'},
                               {'value': '441800', 'city': '清远市'}, {'value': '441900', 'city': '东莞市'},
                               {'value': '442000', 'city': '中山市'}, {'value': '445100', 'city': '潮州市'},
                               {'value': '445200', 'city': '揭阳市'}, {'value': '445300', 'city': '云浮市'}]},
                     {'value': '450000', 'province': '广西',
                      'area': [{'value': '450000', 'city': '省本级'}, {'value': '450100', 'city': '南宁市'},
                               {'value': '450200', 'city': '柳州市'}, {'value': '450300', 'city': '桂林市'},
                               {'value': '450400', 'city': '梧州市'}, {'value': '450500', 'city': '北海市'},
                               {'value': '450600', 'city': '防城港市'}, {'value': '450700', 'city': '钦州市'},
                               {'value': '450800', 'city': '贵港市'}, {'value': '450900', 'city': '玉林市'},
                               {'value': '451000', 'city': '百色市'}, {'value': '451100', 'city': '贺州市'},
                               {'value': '451200', 'city': '河池市'}, {'value': '451300', 'city': '来宾市'},
                               {'value': '451400', 'city': '崇左市'}]},
                     {'value': '460000', 'province': '海南',
                      'area': [{'value': '460000', 'city': '省本级'}, {'value': '460100', 'city': '海口市'},
                               {'value': '460200', 'city': '三亚市'}, {'value': '460300', 'city': '三沙市'},
                               {'value': '469001', 'city': '五指山市'}, {'value': '469002', 'city': '琼海市'},
                               {'value': '469003', 'city': '儋州市'}, {'value': '469005', 'city': '文昌市'},
                               {'value': '469006', 'city': '万宁市'}, {'value': '469007', 'city': '东方市'},
                               {'value': '469021', 'city': '定安县'}, {'value': '469022', 'city': '屯昌县'},
                               {'value': '469023', 'city': '澄迈县'}, {'value': '469024', 'city': '临高县'},
                               {'value': '469025', 'city': '白沙黎族自治县'}, {'value': '469026', 'city': '昌江黎族自治县'},
                               {'value': '469027', 'city': '乐东黎族自治县'}, {'value': '469028', 'city': '陵水黎族自治县'},
                               {'value': '469029', 'city': '保亭黎族苗族自治县'}, {'value': '469030', 'city': '琼中黎族苗族自治县'}]},
                     {'value': '500000', 'province': '重庆',
                      'area': [{'value': '500000', 'city': '省本级'}, {'value': '500101', 'city': '万州区'},
                               {'value': '500102', 'city': '涪陵区'}, {'value': '500103', 'city': '渝中区'},
                               {'value': '500104', 'city': '大渡口区'}, {'value': '500105', 'city': '江北区'},
                               {'value': '500106', 'city': '沙坪坝区'}, {'value': '500107', 'city': '九龙坡区'},
                               {'value': '500108', 'city': '南岸区'}, {'value': '500109', 'city': '北碚区'},
                               {'value': '500110', 'city': '綦江区'}, {'value': '500111', 'city': '大足区'},
                               {'value': '500112', 'city': '渝北区'}, {'value': '500113', 'city': '巴南区'},
                               {'value': '500114', 'city': '黔江区'}, {'value': '500115', 'city': '长寿区'},
                               {'value': '500116', 'city': '江津区'}, {'value': '500117', 'city': '合川区'},
                               {'value': '500118', 'city': '永川区'}, {'value': '500119', 'city': '南川区'},
                               {'value': '500120', 'city': '璧山区'}, {'value': '500151', 'city': '铜梁区'},
                               {'value': '500152', 'city': '潼南区'}, {'value': '500153', 'city': '荣昌区'},
                               {'value': '500154', 'city': '开州区'}, {'value': '500155', 'city': '梁平区'},
                               {'value': '500156', 'city': '武隆区'}, {'value': '500229', 'city': '城口县'},
                               {'value': '500230', 'city': '丰都县'}, {'value': '500231', 'city': '垫江县'},
                               {'value': '500233', 'city': '忠县'}, {'value': '500235', 'city': '云阳县'},
                               {'value': '500236', 'city': '奉节县'}, {'value': '500237', 'city': '巫山县'},
                               {'value': '500238', 'city': '巫溪县'}, {'value': '500240', 'city': '石柱土家族自治县'},
                               {'value': '500241', 'city': '秀山土家族苗族自治县'}, {'value': '500242', 'city': '酉阳土家族苗族自治县'},
                               {'value': '500243', 'city': '彭水苗族土家族自治县'}]},
                     {'value': '510000', 'province': '四川',
                      'area': [{'value': '510000', 'city': '省本级'}, {'value': '510100', 'city': '成都市'},
                               {'value': '510300', 'city': '自贡市'}, {'value': '510400', 'city': '攀枝花市'},
                               {'value': '510500', 'city': '泸州市'}, {'value': '510600', 'city': '德阳市'},
                               {'value': '510700', 'city': '绵阳市'}, {'value': '510800', 'city': '广元市'},
                               {'value': '510900', 'city': '遂宁市'}, {'value': '511000', 'city': '内江市'},
                               {'value': '511100', 'city': '乐山市'}, {'value': '511300', 'city': '南充市'},
                               {'value': '511400', 'city': '眉山市'}, {'value': '511500', 'city': '宜宾市'},
                               {'value': '511600', 'city': '广安市'}, {'value': '511700', 'city': '达州市'},
                               {'value': '511800', 'city': '雅安市'}, {'value': '511900', 'city': '巴中市'},
                               {'value': '512000', 'city': '资阳市'}, {'value': '513200', 'city': '阿坝藏族羌族自治州'},
                               {'value': '513300', 'city': '甘孜藏族自治州'}, {'value': '513400', 'city': '凉山彝族自治州'}]},
                     {'value': '520000', 'province': '贵州',
                      'area': [{'value': '520000', 'city': '省本级'}, {'value': '520100', 'city': '贵阳市'},
                               {'value': '520200', 'city': '六盘水市'}, {'value': '520300', 'city': '遵义市'},
                               {'value': '520400', 'city': '安顺市'}, {'value': '520500', 'city': '毕节市'},
                               {'value': '520600', 'city': '铜仁市'}, {'value': '522300', 'city': '黔西南布依族苗族自治州'},
                               {'value': '522600', 'city': '黔东南苗族侗族自治州'}, {'value': '522700', 'city': '黔南布依族苗族自治州'}]},
                     {'value': '530000', 'province': '云南',
                      'area': [{'value': '530000', 'city': '省本级'}, {'value': '530100', 'city': '昆明市'},
                               {'value': '530300', 'city': '曲靖市'}, {'value': '530400', 'city': '玉溪市'},
                               {'value': '530500', 'city': '保山市'}, {'value': '530600', 'city': '昭通市'},
                               {'value': '530700', 'city': '丽江市'}, {'value': '530800', 'city': '普洱市'},
                               {'value': '530900', 'city': '临沧市'}, {'value': '532300', 'city': '楚雄彝族自治州'},
                               {'value': '532500', 'city': '红河哈尼族彝族自治州'}, {'value': '532600', 'city': '文山壮族苗族自治州'},
                               {'value': '532800', 'city': '西双版纳傣族自治州'}, {'value': '532900', 'city': '大理白族自治州'},
                               {'value': '533100', 'city': '德宏傣族景颇族自治州'}, {'value': '533300', 'city': '怒江傈僳族自治州'},
                               {'value': '533400', 'city': '迪庆藏族自治州'}]},
                     {'value': '540000', 'province': '西藏',
                      'area': [{'value': '610000', 'city': '省本级'}, {'value': '610100', 'city': '西安市'},
                               {'value': '610200', 'city': '铜川市'}, {'value': '610300', 'city': '宝鸡市'},
                               {'value': '610400', 'city': '咸阳市'}, {'value': '610500', 'city': '渭南市'},
                               {'value': '610600', 'city': '延安市'}, {'value': '610700', 'city': '汉中市'},
                               {'value': '610800', 'city': '榆林市'}, {'value': '610900', 'city': '安康市'},
                               {'value': '611000', 'city': '商洛市'}]},
                     {'value': '610000', 'province': '陕西',
                      'area': [{'value': '610000', 'city': '省本级'}, {'value': '610100', 'city': '西安市'},
                               {'value': '610200', 'city': '铜川市'}, {'value': '610300', 'city': '宝鸡市'},
                               {'value': '610400', 'city': '咸阳市'}, {'value': '610500', 'city': '渭南市'},
                               {'value': '610600', 'city': '延安市'}, {'value': '610700', 'city': '汉中市'},
                               {'value': '610800', 'city': '榆林市'}, {'value': '610900', 'city': '安康市'},
                               {'value': '611000', 'city': '商洛市'}]},
                     {'value': '620000', 'province': '甘肃',
                      'area': [{'value': '620000', 'city': '省本级'}, {'value': '620100', 'city': '兰州市'},
                               {'value': '620200', 'city': '嘉峪关市'}, {'value': '620300', 'city': '金昌市'},
                               {'value': '620400', 'city': '白银市'}, {'value': '620500', 'city': '天水市'},
                               {'value': '620600', 'city': '武威市'}, {'value': '620700', 'city': '张掖市'},
                               {'value': '620800', 'city': '平凉市'}, {'value': '620900', 'city': '酒泉市'},
                               {'value': '621000', 'city': '庆阳市'}, {'value': '621100', 'city': '定西市'},
                               {'value': '621200', 'city': '陇南市'}, {'value': '622900', 'city': '临夏回族自治州'},
                               {'value': '623000', 'city': '甘南藏族自治州'}]},
                     {'value': '630000', 'province': '青海',
                      'area': [{'value': '630000', 'city': '省本级'}, {'value': '630100', 'city': '西宁市'},
                               {'value': '630200', 'city': '海东市'}, {'value': '632200', 'city': '海北藏族自治州'},
                               {'value': '632300', 'city': '黄南藏族自治州'}, {'value': '632500', 'city': '海南藏族自治州'},
                               {'value': '632600', 'city': '果洛藏族自治州'}, {'value': '632700', 'city': '玉树藏族自治州'},
                               {'value': '632800', 'city': '海西蒙古族藏族自治州'}]},
                     {'value': '640000', 'province': '宁夏',
                      'area': [{'value': '640000', 'city': '省本级'}, {'value': '640100', 'city': '银川市'},
                               {'value': '640200', 'city': '石嘴山市'}, {'value': '640300', 'city': '吴忠市'},
                               {'value': '640400', 'city': '固原市'}, {'value': '640500', 'city': '中卫市'}]},
                     {'value': '650000', 'province': '新疆',
                      'area': [{'value': '650000', 'city': '省本级'}, {'value': '650100', 'city': '乌鲁木齐市'},
                               {'value': '650200', 'city': '克拉玛依市'}, {'value': '652100', 'city': '吐鲁番市'},
                               {'value': '652200', 'city': '哈密市'}, {'value': '652300', 'city': '昌吉回族自治州'},
                               {'value': '652700', 'city': '博尔塔拉蒙古自治州'}, {'value': '652800', 'city': '巴音郭楞蒙古自治州'},
                               {'value': '652900', 'city': '阿克苏地区'}, {'value': '653000', 'city': '克孜勒苏柯尔克孜自治州'},
                               {'value': '653100', 'city': '喀什地区'}, {'value': '653200', 'city': '和田地区'},
                               {'value': '654000', 'city': '伊犁哈萨克自治州'}, {'value': '654200', 'city': '塔城地区'},
                               {'value': '654300', 'city': '阿勒泰地区'}, {'value': '659001', 'city': '石河子市'},
                               {'value': '659002', 'city': '阿拉尔市'}, {'value': '659003', 'city': '图木舒克市'},
                               {'value': '659004', 'city': '五家渠市'}]},
                     {'value': '660000', 'province': '兵团', 'area': [{'value': '0', 'city': '兵团'}]}]
        ywlx = [{"业务类型": "工程建设", "value": "01"},
                {"业务类型": "政府采购", "value": "02"},
                {"业务类型": "土地使用权", "value": "03"},
                {"业务类型": "矿业权", "value": "04"},
                {"业务类型": "国有产权", "value": "05"},
                {"业务类型": "碳排放权", "value": "21"},
                {"业务类型": "林权", "value": "25"},
                {"业务类型": "其他", "value": "90"}, ]

        for pro in provinces:  # 遍历省份城市
            provalue = pro["value"]
            province = pro["province"]
            areas = pro["area"]
            for area in areas:
                area_value = area["value"]
                area_name = area["city"]
                for yw in ywlx:  # 遍历业务类型
                    for page in range(1, 2000):
                        info = {}
                        ywvalue = yw["value"]
                        ywname = yw["业务类型"]
                        info["province"] = province
                        info["provalue"] = provalue
                        info["area_name"] = area_name
                        info["area_value"] = area_value
                        info["ywname"] = ywname
                        info["ywvalue"] = ywvalue
                        url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
                        data = {
                            "TIMEBEGIN_SHOW": "2023-02-24",
                            "TIMEEND_SHOW": "2023-03-05",
                            "TIMEBEGIN": "2023-02-24",
                            "TIMEEND": "2023-03-05",
                            "SOURCE_TYPE": "1",
                            "DEAL_TIME": "06",
                            "DEAL_CLASSIFY": ywvalue,
                            "DEAL_STAGE": ywvalue + '00',
                            "DEAL_PROVINCE": provalue,
                            "DEAL_CITY": area_value,
                            "DEAL_PLATFORM": "0",
                            "BID_PLATFORM": "0",
                            "DEAL_TRADE": "0",
                            "isShowAll": "1",
                            "PAGENUMBER": page,
                            "FINDTXT": ""
                        }
                        yield feapder.Request(url, data=data, verify=False, method="POST", cs=info, count=1,
                                              request_sync=True)

    def download_midware(self, request):
        '''
                          下载中间件
                            :return:
                   '''
        request.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://deal.ggzy.gov.cn",
            "Referer": "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        return request

    def parse(self, request, response):
        '''
                            解析页面
                            :return:
                   '''
        cs = request.cs
        json_data = json.loads(response.text.strip())["data"]
        count = request.count
        for data in json_data:
            info = {}
            info["block"] = "交易公开"
            info["collet_area"] = cs["ywname"]
            info["collet_area2"] = data["stageShow"]
            info["plate"] = "招标信息"
            if info["collet_area"] == '工程建设':
                if info["collet_area2"] == "招标/资审公告":
                    info["pulic_type"] = "招标公告"
                if info["collet_area2"] == "开标记录":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "交易结果公示":
                    info["pulic_type"] = "中标公告"
                if info["collet_area2"] == "招标/资审文件澄清":
                    info["pulic_type"] = "其他公告"
            if info["collet_area"] == '政府采购':
                if info["collet_area2"] == "采购/资审公告":
                    info["pulic_type"] = "招标公告"
                if info["collet_area2"] == "中标公告":
                    info["pulic_type"] = "中标公告"
                if info["collet_area2"] == "采购合同":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "更正事项":
                    info["pulic_type"] = "其他公告"
            if info["collet_area"] == '土地使用权':
                if info["collet_area2"] == "出让公示":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "成交宗地":
                    info["pulic_type"] = "其他公告"
            if info["collet_area"] == '矿业权':
                if info["collet_area2"] == "出让公告":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "出让结果":
                    info["pulic_type"] = "中标公告"
                if info["collet_area2"] == "公开信息":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "登记公告信息":
                    info["pulic_type"] = "其他公告"
            if info["collet_area"] == '国有产权':
                if info["collet_area2"] == "挂牌披露":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "交易结果":
                    info["pulic_type"] = "其他公告"
            if info["collet_area"] == '碳排放权':
                if info["collet_area2"] == "出售公告":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "结果公示":
                    info["pulic_type"] = "中标公告"
            if info["collet_area"] == '林权':
                if info["collet_area2"] == "信息披露":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "成交公告":
                    info["pulic_type"] = "中标公告"
            if info["collet_area"] == '其他':
                if info["collet_area2"] == "交易公告":
                    info["pulic_type"] = "其他公告"
                if info["collet_area2"] == "成交公示":
                    info["pulic_type"] = "中标公告"

            info["province"] = cs["province"]
            info["city"] = cs["area_name"]
            info["field"] = data["tradeShow"]
            info["create_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info["title"] = data["title"]
            info["file_link"] = data["url"].replace('/a/', '/b/')
            info["public_time"] = data["timeShow"]

            yield feapder.Request(info["file_link"], callback=self.down_file1,
                                  meta=info, request_sync=True)
        # 翻页
        ttlpage = json.loads(response.text.strip())["ttlpage"]
        if count < int(ttlpage) + 1:
            count += 1
            url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
            data = {
                "TIMEBEGIN_SHOW": nowtime,
                "TIMEEND_SHOW": nowtime,
                "TIMEBEGIN": nowtime,
                "TIMEEND": nowtime,
                "SOURCE_TYPE": "1",
                "DEAL_TIME": "06",
                "DEAL_CLASSIFY": cs["ywvalue"],
                "DEAL_STAGE": cs["ywvalue"] + '00',
                "DEAL_PROVINCE": cs["provalue"],
                "DEAL_CITY": cs["area_value"],
                "DEAL_PLATFORM": "0",
                "BID_PLATFORM": "0",
                "DEAL_TRADE": "0",
                "isShowAll": "1",
                "PAGENUMBER": str(count),
                "FINDTXT": ""
            }
            yield feapder.Request(url, data=data, verify=False, method="POST", cs=cs, count=count, request_sync=True)

    def down_file1(self, request, response):
        '''
                   解析公告
                    :return:
           '''
        info = request.meta
        html = response.text
        res = etree.HTML(html)

        trs = res.xpath('//div[@class="detail_content"]//text()')
        info["public_text"] = "".join(trs)
        info["html"] = html
        html_text = ""
        if html:
            html_text = tools.filterHtmlTag(html)
        amount = re.search("合同估算价.*?元", html_text)
        contact_person = re.search("联系人：.*?[\u4e00-\u9fa5]+", html_text)
        contact_information = re.search("电*话：.*?[0-9a-zA-Z\-]+", html_text)
        if amount:
            amount = amount[0].split("：")[-1]
        if contact_person:
            contact_person = contact_person[0].split("：")[-1]
        if contact_information:
            contact_information = contact_information[0].split("：")[-1]
        # 提交投标文件截止时间
        # <re.Match object; span=(1534, 1550), match='开标时间：2023年03月27日'>
        bidopening_time = re.search("开标时间：.*?\d{4}-\d{1,2}-\d{1,2}", html_text)
        if bidopening_time:
            bidopening_time = bidopening_time[0].replace("开标时间：", "")
        if not bidopening_time:
            # 开标时间和地点
            bidopening_time = re.search("开标时间和地点.*?\d{4}年\d{1,2}月\d{1,2}日", html_text)
            if bidopening_time:
                bidopening_time = re.search("\d{4}年\d{1,2}月\d{1,2}日", bidopening_time[0])
                bidopening_time = bidopening_time[0] if bidopening_time else None
        item = Item()
        item.table_name = "bidding_information"
        item.bulletin_type = info.get("block", "")
        item.notice_nature = info.get("pulic_type", "")
        # province
        item.city = info.get("province", "") if info.get("city", "") == "省本级" else info.get("city", "")
        item.release_time = info.get("public_time", "")
        # item.tender_deadline = i.get("bidClosingTime")
        item.title = info.get("title", "")
        # item.attachment = info.get("file_link", "")
        item.industry_classification = info.get("field", "")
        item.announcement_content = info.get("html", "")
        item.link = info.get("file_link", "")
        item.amount = amount.replace(" ", "") if amount else None
        item.contact_person = contact_person.replace(" ", "") if contact_person else None
        item.contact_information = contact_information.replace(" ", "") if contact_information else None
        item.bidopening_time = bidopening_time.replace(" ", "") if bidopening_time else None
        # print(item)
        yield item


if __name__ == "__main__":
    AirSpiderJygk(thread_count=1).start()
