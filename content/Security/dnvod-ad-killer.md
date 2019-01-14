Title: 多瑙视频广告移除思路及实现
Date: 2018-02-11 11:06:00
Tags: bypass, mitm, hacking
Slug: dnvod-ad-killer
Summary: 本文主要阐述了多瑙视频网站(dnvod.tv)广告移除的思路及可行实现。
Summary_en: The article mainly discussed how to remove the ads on dnvod.tv and how to make an implementation.

## Update: 2019-01-13

多瑙最近更新了广告投放的实现，此文已经失效，请移步到[新文章](dnvod-ad-killer-v2.html)。之前的代码可通过tag `v1`来索取。

# 小白通道

首先代码仓库和使用方法送上：[https://github.com/GreatYYX/dnvod-ad-killer/tree/v1](https://github.com/GreatYYX/dnvod-ad-killer/tree/v1)。然后不用往下看了。

# 背景铺垫

17年在美帝工作后，就再没来写过blog，一年一更的“好习惯”也被打破了。其实过去这一年多时间里自己在安全方面基本没有hands-on的动作，除了去某哥onsite前那晚上成功zuo si把手机上一个游戏给破解了然后华丽的gg，主要在研究以流量伪装手段绕过GFW的方法和binary文件准确恢复函数图谱的可能性，不过目前这两者都只停留在思路阶段（Sigh～菜的抠脚）。

这次萌发动力写个文章主要是被多瑙的bling bling的广告闪瞎了可又掏不起银子充会员，而单纯的AdBlock / AdBlock Plus以及Chrome Extension里的[dnvod-ad-remover](https://github.com/AugustusZ/Dnvod-Ad-Remover)都已经失效，于是乎只能寡人亲自操刀了。

# 思路概述

## 前人走过的路

本着先做好功课再下手的一贯作风，去网上找了圈现有的思路。

由于HTML5的普及，大多数视频网站已经抛弃了Flash播放器（比如激进的Youtube和一些不可描述的网站），而鉴于特殊国情，国内大多数采用HTML5和Flash两者并用的局面。HTML5本身作为开放的web标准，所有东西都是暴露在用户面前的，正所谓前端无秘密。因此之前的思路基本属于：屏蔽掉Flash播放器，转而强制使用HTML5播放器从而实施后续的移除。只不过目前dnvod已经强制要求使用Flash了，也不知道为何会采用这种逆时代进程的做法而不是换一种投放广告的思路。

还有一则思路采用修改host表的方法，将几个ad来源的domain进行屏蔽。不过此方法最大的问题在于，相关的资源直接就出现了无法访问的情况，而现在最基本的判断是不是有AdBlock类插件的方案就是判断相应的资源能否下载成功（相比binary判断自身是否处于被调试状态要简单太多了）。所以一旦使用该方法，网页上就会告诉你，我和AdBlock你只能选一个。

## 长江后浪

前人的思路已经死在了沙滩上，因此只能另辟蹊径。

其实主要是破解两个问题：1.移除视频前70s的广告和等待时间 2.移除那些闪闪发光的小广告。

### 移除视频前等待

对于第一点，本身网站界面加载的也只有基本的框架，评论、集数、广告均由js创建而来。而加载后最显而易见的就是视频播放区的这段dom：

```html
<object ...>
	...
	<param name="movie" value="/_player/954684356/ckplayer.swf">
	<param name="flashvars" value="f=rtmp://s1-r1.dnvod.tv/kvod/mp4:lxj-hpfd-01-021E92666.mp4&amp;loaded=loadedHandler&amp;s=0&amp;b=0&amp;c=0&amp;a=&amp;i=//static.dnvod.tv/images/logo-group.jpg&amp;l=http://static.dnvod.tv/upload/video/201802081401510175878s.jpg|...&amp;r=http://public.dnvod.tv/c/c?position%3db%26i%3d376%26r%3d4|...&amp;t=10|10|10|10|10|10|10..." width="100%" height="100%" name="ckplayer_a1" id="ckplayer_a1" align="middle" type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer">
	<embed ...>
</object>
```

这段html比较长，重点部分主要是一个`object`标签里面的两个`param`及一个`embed`。从这儿的第一个`param`可以看出采用了一个叫做ckplayer的播放器，我查了下是个国人开发的通用的网页视频播放器。第二个`param`是真正干活的地方了，利用`flashvar`把网页参数传入播放器中。凭空猜测，`f`是具体的视频地址，`l`是左边广告，`r`是右边广告，`t`是每个广告时间，每组广告图片采用`|`分割。于是上神器burp修改request的payload，不过竟然没有成功。这个思路是最最直接最最简单的，理论上来说应该是可行的，不过可能我当时实验时候有失误，于是阴差阳错的放弃了这个方法（后面会阐述这反而成了优势）。

之后就从js上下手，过了一遍加载的js。有一个混淆了js特别值得注意，`playerselection-1.2.7.90.js`。过一下反混淆器，代码的大致架子基本能还原出来（相比binary下反汇编的作业环境，js的这个的可读性还真不错）。快速scan一遍代码，感觉`settimeout`最可能作为突破点，毕竟倒计时在js里面最直观的做法就是用这个函数。一个个过下去发现有个的值被设置成`70000`，这不会就是70秒（70000ms）的广告吧？不好意思，对。

```javascript
function loadedHandler() {
    ...
    } else {
        if (!_vp['noads']) {
            setTimeout(function() {
                var _0xf706x34 = CKobject['getObjectById'](_vp['ckid']);
                if (_0xf706x34 && _0xf706x34['frontAdUnload']) {
                    _0xf706x34['frontAdUnload']()
                }
            }, 70000) // <---- HERE!!!!! OMG F*** IT
        }
    };
    ...
}

```

随手在burp里把response body（注意这次不是改request是改response）改成10000，画面依然显示70s广告，不过到60s的时候就自动结束了。于是再接再厉，改成5000（此时记得`header`中的`content-length`也需要修改，否则malformat的包会被Chrome丢弃）。尝试把这个数字再改小就存在了没有了倒计时可广告仍然存在的问题，于是又定位了其他几个`settimeout`：

```
function CheckPlay(_0xf706x8c, _0xf706x8d) {
    ...
        $('.playtimer')['text'](('' + _0xf706x8c)['toHHMMSS']());
        setTimeout(function() {
            CheckPlay(--_0xf706x8c)
        }, 1000)
    }
}

function PlayAds(_0xf706xf, _0xf706x5, _0xf706x6) {
    var _0xf706xae = _0xf706xf['split']('|');
    var _0xf706xaf = _0xf706x5['split']('|');
    var _0xf706xb0 = _0xf706x6['split']('|');
    var _0xf706xb1 = 0;
    for (var _0xf706x3 = 0; _0xf706x3 < _0xf706xae['length']; _0xf706x3++) {
        if (_0xf706xae[_0xf706x3]['indexOf']('swf') > 0) {
            _0xf706xae['splice'](_0xf706x3, 1);
            _0xf706xaf['splice'](_0xf706x3, 1);
            _0xf706xb0['splice'](_0xf706x3, 1);
            _0xf706x3--
        } else {
            _0xf706xb1 += parseInt(_0xf706xb0[_0xf706x3])
        }
    };
    callAdd(_0xf706xae, _0xf706xaf, _0xf706xb0);
    var _0xf706xb2 = _0xf706xb1;
    var _0xf706xb3 = setInterval(function() {
        var _0xf706xb4 = $('.second');
        _0xf706xb4['text'](_0xf706xb2--)
    }, 980);
    setTimeout(function() {
        $('.ads-control')['remove']();
        var _0xf706xb4 = $('.second');
        clearInterval(_0xf706xb3);
        _0xf706xb4['text']('');
        if (CKobject) {
            CKobject['getObjectById'](_vp['ckid'])['videoPlay']()
        }
    }, _0xf706xb1 * _0xf706xb1 * 1020)
}

function EmbedFlash(_0xf706x24, _0xf706x2b, _0xf706x2a, _0xf706x4f) {
    var _0xf706x50 = _0xf706x2b;
    if (!_vp['playlistM'] || !_vp['playlistM']['length']) {
        if (_0xf706x4f && _0xf706x4f['wa'] && _0xf706x4f['timeout'] > 0) {
        	...
            setTimeout(_vp.TirggerPending, _0xf706x4f['timeout'] * 1000)
        }
    }
    ...
}
```

其中最关键的应该就是`PlayAds`这个函数了，基本就是读取广告然后丢到Flash中，这里的`settimeout`用于时间到了之后把广告的div移调。另外`CheckPlay`是用来检测状态改变的(相当于刷新器)，因此需要把值改的要比较小，否则就会出现上面的值改小了却不生效的情况。

### 移除广告

有时候灵光一闪真的很重要，还记得当年比CTF睡觉时候突然有思路爬起来增援刷夜的老曾和潘神的情况。判断AdBlock这类插件是否存在的原理上面已经说了，就是只要设定一个timeout，过了timeout之后看这个资源有没有下载成功即可。因此直接屏蔽资源肯定是不行的，思路就变成了伪造一个正常的资源。之后就想到CSS1/2标准不完善的时候一个hack div的技巧，于是构造了一个1px x 1px的透明gif图片，直接替换掉所有广告图片，这样对于检测程序来说，依然认为ad下载成功，而事实上什么都看不到喽。

# 自动化去广告

这里没有采用开发一个Chrome Extension的方案，原因主要是Chrome团队是很激进的（褒义词），为了推动web标准进步和增强浏览器安全问题费尽了心思，比如这儿修改response body本身会或者将会受到Chrome API的限制。于是直接就用炉火纯青的中间人攻击(mitm)解决这个问题，网上随便找了个[HTTP Proxy](https://github.com/abhinavsingh/proxy.py)，code写的不错，全是Python原生库。之后主要修改下处理response body的环节：

```
 def _process_response(self, data):
        # parse incoming response packet
        # only for non-https requests
        if not self.request.method == b"CONNECT":
            self.response.parse(data)

        # print self.request.host_, self.request.url_
        if self.request.host_ and self.request.host_.endswith('dnvod.tv'):
            # ads
            one_px_gif_data = 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
            if self.request.url_ and self.request.url_.startswith('/upload/video'):
                if os.path.splitext(self.request.url_)[-1] in ('.jpg', '.gif'):
                    data = base64.b64decode(one_px_gif_data)

            # count down
            if self.request.url_ and self.request.url_ == '/js/2016/playerselection-1.2.7.90.js':
                with open('dn_replace.js', 'r') as f:
                    data = f.read()

        # queue data for client
        self.client.queue(data)
```

我这儿对于修改好的js直接存在文件里了，所以读取后替换。对于1px的transparent gif，实在没必要专门创建个文件然后浪费一次io，于是直接base64了这个图片的byte。

之后浏览器代理挂好，对于`*.dnvod.tv`的流量转向这个代理即可。

## Update: 2018-02-25

据网友Orooz反应，程序在Windows下不可用，测试后发现原本使用的HTTP Proxy在Windows下无法正常工作，遂使用[proxy2](https://github.com/inaz2/proxy2)替换之。原理完全一样，直接贴修改的代码。


```
def response_handler(self, req, req_body, res, res_body):
        url = urlparse.urlparse(req.path)
        url_domain = url.netloc
        url_path = url.path

        if url_domain and url_domain.endswith('dnvod.tv'):
            # ads
            one_px_gif_data = 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
            if url_path and url_path.startswith('/upload/video'):
                if os.path.splitext(url_path)[-1] in ('.jpg', '.gif'):
                    res_body = base64.b64decode(one_px_gif_data)

            # count down
            if url_path and url_path == '/js/2016/playerselection-1.2.7.90.js':
                with open('dn_replace.js', 'r') as f:
                    res_body = f.read()

            return res_body
```


意外收获是该Proxy支持HTTPS的mitm。


# 后续

其实从防御方来说，修改Flash Player本身可以明显增加破解门槛，在Flash内部强制限定广告时间，广告资源本身甚至可以固化到Flash的内置资源列表中，这样不会产生单独的下载流量。但是缺点也显而易见，每次广告更新都要完整更新这个播放器，维护成本不可小觑。另外对于空白图片，也可以在前端检测一下（比如图片byte是否固定，图片大小如何，不过这类检测脚本也可以被中间人替换了或者被重新构造的资源绕过）。

从攻击方来说，后续需要的基本增强就是对于https时候mitm，不过这个就是一个库两个证书的问题。另外就是对于规则的修订问题了。进一步说，如果防御方真修改了Flash Player，那就decompile这个播放器然后替换之...

攻防本身就是个矛盾体，只要平衡其实就好。毕竟Amazon和Walmart还天天互爬数据并互相屏蔽对方的爬虫呢。

一开始没有选择修改request是个阴差阳错，但是这个反而成为了后续的优势。因为修改的request payload可以被服务器鉴别，而response已经返回到了本地，主动权完全在我方，因此可以被任意修改而服务器并不知道中间人的存在。而没有写成Chrome Extension也是为了突破Chrome API目前以及将来的种种限制。这两点都为后续可能存在的更强的反广告策略提供了保障。

懒癌最后扯一句：只要多瑙不更新，伦家是不会主动更新的嘤嘤嘤。
