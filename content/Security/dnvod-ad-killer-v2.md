Title: 多瑙视频广告移除思路及实现（v2）
Date: 2019-01-13 19:18:00
Tags: bypass, mitm, hacking
Slug: dnvod-ad-killer-v2
Summary: 本文主要阐述了多瑙视频网站(dnvod.tv)广告移除的思路及可行实现。此篇取代之前那篇文章，解决了多瑙近期更新后的问题。
Summary_en: The article mainly discussed how to remove the ads on dnvod.tv and how to make an implementation. This is the replacement of previous post: it solves the issue after dnvod.tv's latest update.

# 前言

18年年底比较忙，一直没再去多瑙看过视频。今年开年回来后发现之前的实现已经失效，因此重新撰文。

新的代码仓库地址不变：[https://github.com/GreatYYX/dnvod-ad-killer](https://github.com/GreatYYX/dnvod-ad-killer)。

考虑到多瑙之后可能的连续更新，这里提出一个约定：每个重大升级会对应一个major版本号（比如这次的`v2`），并可能会写相对应的文章，文章的标题和URL也会带有这个major版本号。minor的更新版本号会直接采用当天的日期，比如`v2.20190113`（如果一天更新多次则会再加入一个后缀，如`v2.20190113.2`），思路将直接更新在其major的文章中。之前的老版本命名为`v1`。

# 上手

多瑙总算拿掉了之前诟病的Flash而采用纯HTML播放器了（之前的文章吐槽过，电脑端禁止了H5的播放器），顺应时代潮流才能繁衍生息。而且广告也不是在一开始就出现，而是播放一段时间后才出现，并会有5s倒计时和20s广告（不过这个广告的时间计算方法很有问题或者是故意的，一旦快进了间隔很短的时间就要看广告，貌似如果要播n段广告的话，会在剩下的时间中插入所有没有播放的广告）。视频采用MP2T流协议分片下载，另外只加载了常规的html、js、css还有图片等。值得一提的是，（几乎）所有http请求都已经是https了，总算跟上了“时代进程”（当然我觉得主要是如果没SSL/TLS会直接被浏览器提示“不安全网站”的原因）。

H5的播放器理论上都通过js加载和控制。从Chrome的DevTools中可以看出这些js和加载顺序：

- DNA-3.0.0.2.js: 由html加载，UI库。
- inline.1dc40c191965336599d8.bundle.js：由html加载。
- polyfills.c30af323737f4e73902d.bundle.js：由html加载，UI库。
- scripts.a00c037d89f30e04f3e1.bundle.js：由html加载。
- main.2e8c4bc9ac78a55fed3d.bundle.js：由html加载。
- 0.a3d01277a3706629fe95.chunk.js：由inline.1dc40c191965336599d8.bundle.js加载。
- 1.ed0cb8b173b9bfffa25f.chunk.js：由inline.1dc40c191965336599d8.bundle.js加载。
- ckplayer.js：由1.ed0cb8b173b9bfffa25f.chunk.js加载，播放器。

另外需要注意的是，每次广告播放完会再下载一个名字随机的js，不过这个对于目前破解并没有干扰。

除了两个UI库和播放器之外，其他的名字都像是用户代码然后bundle和混淆了的。因此从html的DOM和js两部下手（废话）。这次考虑到所有访问流量都已经变成https，我将代理更新为了更加成熟的[mitmproxy](https://mitmproxy.org/)。

# 分析和实现

最开始尝试了一下通过DOM里面的广告的element来定位的办法，不过貌似都是Angular的`ng-xxxx`，而`xxxx`很多都在混淆了的代码里被参数化了，因此不太好定位，尝试了5分钟遂放弃-_-|||

当然促使我那么快就放弃当然不是因为我懒（反正我也不会承认的），因为更简单的思路已经萌上心头：搜索特征字符串，比如`广告`。不幸的是，js中都没有出现中文。但是大致浏览这些js后就会发现字符串都做了unicode编码，找个编码器翻一下就是`\u5e7f\u544a`。尝试grep一下所有可能的js发现基本都存在，于是加长为`后跳过广告`（`多少s`可能会是变量）后定位到`1.ed0cb8b173b9bfffa25f.chunk.js`。下面开刀这个文件。

根据`\u540e\u8df3\u8fc7\u5e7f\u544a`定位到：

```
function t() {}
return t.secondFormat = '<font class="text-red" color="#F00000">{second}s</font > \u540e\u64ad\u653e\u5e7f\u544a', ...
```

之后根据`secondFormat`发现一处关键代码：

```
this.subscriptions.push(this.publicManager.eventList.subscribe(function(e) {
    switch (t.api.intersitialHandler(e), e.event) {
        case Ye.Timer:
            t.api.showInfo(nn.secondFormat.replace("{second}", e.data.time), 0);
            break;
        case Ye.ShouldPlayAds:
            t.api.showInfo("", 0), n = t.api.getPlayMedia, i = t.api.currentTime, t.currentPlayingAds = t.loadMedia, t.currentPlayingAds.isImage ? t.api.pause() : t.api.playVideo([t.currentPlayingAds], !0), t.isPlayingAds = !0, t.skipAfter = 10;
            break;
        case Ye.ShouldBackToPlay:
            t.isBackToPlayMedia = !0, (!t.shouldSkipAds && !t.hasBought || t.isPlayingAds) && null != n && (t.currentPlayingAds = t.loadMedia = null, t.api.playVideo([n], !1), t.isPlayingAds = !1, t.shouldPlaySeoncd = i);
            break;
        case Ye.ShouldLoadAds:
            t.isBackToPlayMedia = !1, t.shouldSkipAds || t.hasBought ? (t.publicManager.stopPlay(), t.hasState || t.api.showInfo(t.needBought ? 1 == t.hasBought ? nn.alreadyBought : nn.highFormat : nn.vipskipFormat, 5)) : t.startLoadMedia(e.data);
            break;
        case Ye.SkipTimer:
            t.skipAfter = e.data.time, t.leftSecond = e.data.left;
            break;
        case Ye.ShouldCancel:
            t.caption = "", n = null, i = 0, t.loadMedia = null, t.isPlayingAds = !1
    }
})), this.pendding && (this.publicManager.invokeList(this.pendding.mediaList, this.pendding.startSecond, this.pendding.periodicSecond), this.pendding = null)
```

这段其实就是精髓了：`ShouldLoadAds`用于加载广告，`ShouldPlayAds`用于播放广告，`Timer`用于倒计时多少秒后播放广告。直接把这三个的内容砍掉，就奇迹般的没有广告等待了。

在破解过程中其实发现并尝试过修改`leftSecond`和`skipAfter`两个变量，效果并没有上面这个直接。

对于暂停之后的广告窗口，根据DOM搜索`.vg-bg`找到：

```
styles: [....vg-bg{\n            position:absolute;\n\n            max-width: 640px;\n            max-height: 360px;\n  ...]
```

加入`display:none;`即可。

攻击代码实现非常简单：对于广告图片依然采用之前的透明图片替换法，欺骗浏览器图片已经下载，不容易被脚本检测到。js文件直接替换成修改后的即可。

```
def response(self, flow: mitmproxy.http.HTTPFlow):
    """
        The full HTTP response has been read.
    """
    if flow.request.host.endswith('dnvod.tv'):
        one_px_gif_data = 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
        if flow.request.path.startswith('/upload/video'):
            if os.path.splitext(flow.request.path)[-1] in ('.jpg', '.gif'):
                flow.response.set_content(base64.b64decode(one_px_gif_data))

        if flow.request.path.endswith('1.ed0cb8b173b9bfffa25f.chunk.js'):
            with open('js/1.ed0cb8b173b9bfffa25f.chunk.de.js', 'r') as f:
                flow.response.set_text(f.read())
```

# 后记

这次过程出奇的顺利，前后也就一个小时。经过这次其实我脑海中有一个相对比较有破解门槛的保护手法，不过作为用户我是不会告诉多瑙的，除非。。。（收买我？）

最后，还是那句话：只要多瑙不更新，伦家是不会主动更新的嘤嘤嘤。