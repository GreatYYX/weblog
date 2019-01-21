Title: QQ双扣记牌器实现
Date: 2015-05-12 01:17:00
Tags: crack, reversing, cheater, game, QQ, 记牌器, 游戏, 棋牌
Slug: qq-card-game-recorder
Summary: 本文讨论了腾讯QQ游戏大厅新双扣角色版记牌器的设计、数据抓取的思路及方法以及最终记牌器的实现细节。
Summary_en: This post demonstrates idea of design, data scrapping, hacking, implementation of card game recorder for new version of Shuang Kou in QQ Game Hall.

# 吐槽 #

到USC刷master真可谓“玩命”读书，在学校被大神虐，在路上怕被黑哥虐，出去玩耍被款爷虐，逢年过节被秀恩爱的虐，总之就是各种不择手段花式虐狗。再加上这学期悲剧的选课，期末下来，已经基本气绝。考闭，准备打打牌找找乐子，作为杭州人，当然最爱双扣，但是当你发现双扣竟然在4月底被企鹅的程序猿改的面目全非之后，就有种气急败坏的却又无从抱怨的感觉。

也不知道怎么想的，突然很想搞一个自己的记牌器玩玩（我承认这儿转折很突兀，因为我自己也不知道为什么当时还没来得及拍脑门就决定了），最后竟然三天抛出成品（不可避免有小bug），于是决定撰文记录一下，行文就按照日子来了。

我这边测试的双扣可执行文件skrpg.exe的文件版本是2.0.107.14，MD5为1c6d85c0accf6ce1a834e947e5467412。很可能游戏更新后数据会有所不同（新版本刚出来更新会特别频繁），但是思路不变的，你需要再机械劳动一次更新所有数据。

# Day1 抓数据 #

其实第一天的时候还没决定真的做出个记牌器，就想研究下这玩意是怎么实现的（好奇心害死猫）。

记牌器实现基本是两种思路：

- 第一种是图形匹配，就是抓窗口的牌面，其实这儿做匹配还是很简单的，毕竟牌面的样子是不会变的，也不需要什么复杂的匹配算法，只要弄下来所有牌面搞个数据库，直接就可以匹配得到数据。难度在于，窗口是可以缩放的，因此牌桌大小不固定，牌的相对位置不清楚是不是按照比例算的；另外，新版双扣是所谓的角色版，添加了一些动画效果，这些效果出现的时候会覆盖一部分牌面，而且是动态的，因此这个时候抓取牌面就不是一种一成不变的情况。
- 第二种是抓数据，这种没有第一种直观，很多时候需要靠推理和碰运气去猜测数据保存在内存中的形式，当然如果数据在内存中被加密了，那就更倒霉了。但是一旦能正确抓出数据并解码，实现就非常简单，而且正确率是100%。当然抓数据不局限于内存数据，很多时候可能是网络数据，那就需要抓包啦。

我选了第二种，抓取工具是Cheat Engine，直接从内存抓取。首先初步判断下需要抓取的数据：所有玩家的当前剩余的牌数，所有玩家每次出的牌，自己的座位，发牌后自己的牌（你一定得不到别人的牌面，这些都在服务器上，如果你能得到那就直接做作弊器了）。

## 玩家剩余牌数

这是思路最简单且最好抓的一步。一个思维正常的程序猿一般都会用整数类型来记录，也就是有符号整形，因此直接抓DWORD长度数据，根据牌数量变化，不断缩小范围，依次在内存中找出4个玩家的剩余牌数位置，找到位置后用CE查找谁access/write了这些位置，这就是我们要找的地址。

```no-highlight
DOWN: 	"GameLogic.dll"+3CF20
LEFT:	"GameLogic.dll"+3CE30
UP: 	"GameLogic.dll"+3D100
RIGHT: 	"GameLogic.dll"+3D010
```

这里的的DOWN、LEFT、UP、RIGHT是我用来表示玩家的座位的，这些座位是大厅中座位的绝对位置，理解这点很重要。从拿到这些数据来看，这些位置是静态的（相对GameLogic.dll加载基址的偏移），So easy!

## 自身座位号

这是一个比较奇葩但必须解决的问题。还是假设企鹅的程序猿是不脑残的，那座位号应该是设计成连续排布的，可能是0-3，也可能是1-4（当然如果是个标准程序猿应该选前者，除非他是base为1的VB党），座位号的排列可能是顺时针，也可能是逆时针，当然还有可能跳着排列（这个可能性很小）。于是排列组合一下，每种情况起始位置可能有4种，算上顺时针逆时针就是有4x2=8种，所以0-3和1-4在连续排布情况下有16种可能性。在云计算的年代，16是个多么渺小的数据，直接brutal force，每种测试一次就行。测试方法就是选取16种中的一种，假设当前这个case成立，那这个座位应该是X，进入下一个座位，应该是Y，这样依次测试，如果每次抓出来的数据都符合判断，就是这个case了。

```no-highlight
  2
1   3
  0
```

最后得到的结果是上面这种情况，0是DOWN，1是LEFT，2是UP，3是RIGHT，这些位置依然是大厅中的绝对位置。这里要提一句，找座位的时候可能会找到一个地址，每次都自增1，当时我还以为是这个，后来发现换了超过4个座位后它的数据依然在增长，测试后发现它是用来记录玩家在这桌入座了几次，不知企鹅程序猿设计这个数据有什么用……

我天真的以为座位号确定了，那座位号在内存中的位置也就确定了。但是当我点进去看access的地址处的反汇编的时候：

```x86asm
02D30214 - 8B 4D F4  - mov ecx,[ebp-0C]
02D30217 - 8B 55 F8  - mov edx,[ebp-08]
02D3021A - 89 14 88   - mov [eax+ecx*4],edx <<
02D3021D - 6A 01 - push 01
02D3021F - 66 8B 45 F4  - mov ax,[ebp-0C]
```

很遗憾，这玩意地址不是固定的，因此需要找它的指针，很可能还要找它指针的指针，甚至更多层。当我找了两层之后，发现依然是变化的地址。无奈调出IDA完整的看了下这段反汇编，发现竟然是基于ebp的传入参数，因此是不固定的。此时突然想到CE有个自动找指针的功能，于是请出这个牛X的大杀器，瞬间1个G的指针数据就算出来了（这凭人手来找得找到什么时候），发现竟然有5层左右的指针调用，还都是不同基址的，筛选下2-3层的调用，找到一个相对可以接受的偏移：`[[["GameLogic.dll"+3DCB4]+88]+4]`，而且基址和前面算玩家剩余牌数的一致，Perfect!

## 牌面数据

牌面数据的推断简直就是拼脑洞。初步想一下牌面可能涉及到数据是花色和点数，虽然花色在双扣中是没有意义的，但是对于游戏的显示来说，花色是必须要的，因为花色是牌属性的一部分。当你想到这儿的时候你会发现，牌的存储很可能是一个自定义的数据类型，而这个类型的格式是不知道的，自定义格式中每个字段长度也是不知道的，双扣有两副牌，因此包含大小王在内有等于或超过两张以上的重复牌，每次出牌数量是不确定的，因此也不知道此时内存中牌有几张，这一组牌用什么方式被表示。我凭借自认为碉堡的智商在脑洞大开的情况下猜测了几次，发现这个捷径走不了，老老实实开IDA看反汇编去……

首先判断牌面的数据处理应该也是在GameLogic.dll中，直接分析这个模块文件，当然一般情况下不可能从头看反汇编，这样的搜索效率太低了。查看一下模块的导出表，没有有价值的函数入口，于是从字符串找突破口。字符串中出现诸如`CCardsGameLogic::OnGameStart\n`样子的函数名，点进去发现是回调函数，还有类似`RefreshCardsInHand\n`的debug用的字符串，不过这些位置的上下文都没有提供有价值的信息。又尝试了一些方式都没有很好的突破口，但是作为一个懒人，怎么能向从头刷代码那么low的方式低头呢？于是准备继续开脑洞……

猜测一下特征数据。每副牌54张，双扣一共2副牌108张，4个人打，每个人就是27张。初始化的时候应该会每个人发27张牌，那时候应该会有个循环分配这27张牌。于是直接在IDA中找立即数27，发现一处有价值的代码：

```x86asm
.text:10020D8C ; int __stdcall sub_10020D8C(COleControl *)
.text:10020D8C sub_10020D8C    proc near               ; CODE XREF: sub_10007D2E+97p
.text:10020D8C                                         ; sub_100081D9+151p ...
.text:10020D8C
.text:10020D8C var_10          = dword ptr -10h
.text:10020D8C var_C           = dword ptr -0Ch
.text:10020D8C var_8           = dword ptr -8
.text:10020D8C var_4           = dword ptr -4
.text:10020D8C arg_0           = dword ptr  8
.text:10020D8C
.text:10020D8C                 push    ebp
.text:10020D8D                 mov     ebp, esp
.text:10020D8F                 sub     esp, 10h
.text:10020D92                 mov     [ebp+var_10], ecx
.text:10020D95                 mov     ecx, [ebp+arg_0]
.text:10020D98                 call    sub_10034BF0
.text:10020D9D                 mov     [ebp+var_8], eax
.text:10020DA0                 mov     [ebp+var_4], 0
.text:10020DA7                 jmp     short loc_10020DB2
.text:10020DA9 ; ---------------------------------------------------------------------------
.text:10020DA9
.text:10020DA9 loc_10020DA9:                           ; CODE XREF: sub_10020D8C+68j
.text:10020DA9                 mov     eax, [ebp+var_4]
.text:10020DAC                 add     eax, 1
.text:10020DAF                 mov     [ebp+var_4], eax
.text:10020DB2
.text:10020DB2 loc_10020DB2:                           ; CODE XREF: sub_10020D8C+1Bj
.text:10020DB2                 mov     ecx, [ebp+arg_0] ; this
.text:10020DB5                 call    ?GetClientSite@COleControl@@QAEPAUIOleClientSite@@XZ ; COleControl::GetClientSite(void)
.text:10020DBA                 cmp     [ebp+var_4], eax
.text:10020DBD                 jge     short loc_10020DF6
.text:10020DBF                 cmp     [ebp+var_4], 1Bh
.text:10020DC3                 jg      short loc_10020DF6
.text:10020DC5                 mov     ecx, [ebp+var_4]
.text:10020DC8                 mov     edx, [ebp+var_8]
.text:10020DCB                 movsx   eax, byte ptr [edx+ecx*4+1]
.text:10020DD0                 push    eax
.text:10020DD1                 mov     ecx, [ebp+var_10]
.text:10020DD4                 call    sub_10020DFE
.text:10020DD9                 mov     [ebp+var_C], eax
.text:10020DDC                 mov     ecx, [ebp+var_4]
.text:10020DDF                 mov     edx, [ebp+var_8]
.text:10020DE2                 mov     al, byte ptr [ebp+var_C]
.text:10020DE5                 mov     [edx+ecx*4+3], al
.text:10020DE9                 mov     ecx, [ebp+var_4]
.text:10020DEC                 mov     edx, [ebp+var_8]
.text:10020DEF                 mov     byte ptr [edx+ecx*4+2], 0
.text:10020DF4                 jmp     short loc_10020DA9
.text:10020DF6 ; ---------------------------------------------------------------------------
.text:10020DF6
.text:10020DF6 loc_10020DF6:                           ; CODE XREF: sub_10020D8C+31j
.text:10020DF6                                         ; sub_10020D8C+37j
.text:10020DF6                 xor     eax, eax
.text:10020DF8                 mov     esp, ebp
.text:10020DFA                 pop     ebp
.text:10020DFB                 retn    4
.text:10020DFB sub_10020D8C    endp
```

F5到C语言后关键部分是这样的：

```cpp
...
for ( i = 0; i < COleControl::GetClientSite(a1) && i <= 27; ++i )
{
    *(_BYTE *)(v2 + 4 * i + 3) = sub_10020DFE(*(_BYTE *)(v2 + 4 * i + 1));
    *(_BYTE *)(v2 + 4 * i + 2) = 0;
}
...
```

可以看出这类似于一个数组操作，而数组每个元素中至少有4个byte长度的值（可以看成是一个自定义数据类型），分别是：第0个不清楚，第3个是第1个经过运算的结果，第2个恒为0。点进去看表示第3个和第1个元素之间的函数`sub_10020DFE`：

```x86asm
.text:10020DFE sub_10020DFE    proc near               ; CODE XREF: sub_10020D8C+48p
.text:10020DFE
.text:10020DFE var_8           = dword ptr -8
.text:10020DFE var_4           = dword ptr -4
.text:10020DFE arg_0           = dword ptr  8
.text:10020DFE
.text:10020DFE                 push    ebp
.text:10020DFF                 mov     ebp, esp
.text:10020E01                 sub     esp, 8
.text:10020E04                 mov     [ebp+var_8], ecx
.text:10020E07                 mov     eax, [ebp+arg_0]
.text:10020E0A                 mov     [ebp+var_4], eax
.text:10020E0D                 cmp     [ebp+arg_0], 2
.text:10020E11                 jnz     short loc_10020E1C
.text:10020E13                 mov     [ebp+var_4], 0Eh
.text:10020E1A                 jmp     short loc_10020E4B
.text:10020E1C ; ---------------------------------------------------------------------------
.text:10020E1C
.text:10020E1C loc_10020E1C:                           ; CODE XREF: sub_10020DFE+13j
.text:10020E1C                 cmp     [ebp+arg_0], 1
.text:10020E20                 jnz     short loc_10020E2B
.text:10020E22                 mov     [ebp+var_4], 0Ch
.text:10020E29                 jmp     short loc_10020E4B
.text:10020E2B ; ---------------------------------------------------------------------------
.text:10020E2B
.text:10020E2B loc_10020E2B:                           ; CODE XREF: sub_10020DFE+22j
.text:10020E2B                 cmp     [ebp+arg_0], 0Eh
.text:10020E2F                 jz      short loc_10020E37
.text:10020E31                 cmp     [ebp+arg_0], 0Fh
.text:10020E35                 jnz     short loc_10020E42
.text:10020E37
.text:10020E37 loc_10020E37:                           ; CODE XREF: sub_10020DFE+31j
.text:10020E37                 mov     ecx, [ebp+var_4]
.text:10020E3A                 add     ecx, 1
.text:10020E3D                 mov     [ebp+var_4], ecx
.text:10020E40                 jmp     short loc_10020E4B
.text:10020E42 ; ---------------------------------------------------------------------------
.text:10020E42
.text:10020E42 loc_10020E42:                           ; CODE XREF: sub_10020DFE+37j
.text:10020E42                 mov     edx, [ebp+var_4]
.text:10020E45                 sub     edx, 2
.text:10020E48                 mov     [ebp+var_4], edx
.text:10020E4B
.text:10020E4B loc_10020E4B:                           ; CODE XREF: sub_10020DFE+1Cj
.text:10020E4B                                         ; sub_10020DFE+2Bj ...
.text:10020E4B                 mov     eax, [ebp+var_4]
.text:10020E4E                 mov     esp, ebp
.text:10020E50                 pop     ebp
.text:10020E51                 retn    4
.text:10020E51 sub_10020DFE    endp
```

这段翻译过来就是：

```cpp
X = 第一个元素
Y = 第三个元素
if (X == 1)
	Y = 12
else if (X == 2)
	Y = 14
else if (X == 14 || X == 15)
	Y = X + 1
else if (X >= 3 && X <= 13)
	Y = X - 2
```

这时候果断脑补：第一个元素可能是1~15，刚好是15种牌的点数（3~10，J，Q，K，A，2，小王F，大王Z）。假设第1个元素就是点数了，那第3个元素是什么呢？根据上面的算法画出对应的表：

```no-highlight
| 3 ~ K  |  A  |  2  |  F  |  Z  |
----------------------------------
| 1 ~ 11 |  12 |  14 |  15 |  16 |
```

有理由这样推测：第3个元素是用来比较牌的点数大小的，而至于为什么A和2之间空一个数，很可能是为顺子设计的，因为顺子只能从3连到A。

在验证猜想之前还需要做一件事，就是确定牌是按照从大到小还是从小到大排列的，同时确定大小比较是根据牌的点数数值（第1个元素）还是点数大小（第3个元素）决定的。只有四种可能性，依然直接穷举测试。打开CE，设定数据长度为byte，测试牌面点数。最后得到的结论是，牌在内存中是按照点数大小从大到小排列的（最大的牌是数组的起始）。在验证内存数据的过程中，同时确定了每张牌的存储空间是4bytes，前面没法确定的第0个元素实际上是花色：

```no-highlight
  王  黑桃  红桃  梅花  方片
-----------------------------
  0    1     2     3     4
```

至此，每张牌在内存中的表示方法已经确定：`[花色][点数][0][大小]`，每个属性各占1byte，每张牌占4bytes。无论所有玩家出的牌还是玩家自己的牌，只要找到最大一张牌的花色位置和牌的数量，根据每张牌占4bytes，就可以从内存中拿出这组牌数据。下面是我找到的各种情况下最大牌的起始位置（和找座位号时候确定指针的方法一致）：

```no-highlight
玩家手里的牌： 	[["GameLogic.dll"+3DAB8]+108]
下家最后出的牌: 	[["GameLogic.dll"+3DABC]+118]
上家最后出的牌: 	[["GameLogic.dll"+3DABC]+2f8]
左家最后出的牌: 	[["GameLogic.dll"+3DABC]+28]
右家最后出的牌: 	[["GameLogic.dll"+3DABC]+208]
```

所有基址基于GameLogic.dll，而且最后出的牌第一次偏移都是0x3DABC，Good job!

# Day2 实现逻辑 #

工作量最大最烧脑的Day1过去了，Day2就轻松了很多。写代码之前当然是要确定语言啦，一般来说写外挂都用C++，毕竟要直接和Windows的API打交道。但是为了快（lan），我决定用Python……

## 获取内存数据

- 首先找到游戏的进程，通过进程的可执行文件名skrpg.exe找到相应的进程pid（当然也可以通过窗口标题借助FindWindow来拿pid）。
- 根据pid执行OpenProcess。
- 由于地址偏移是根据GameLogic.dll这个模块确定的，因此需要读取该模块的基址：利用EnumProcessModulesEx得到所有已经加载的模块的句柄（注意权限为LIST_MODULES_ALL）
- 遍历模块句柄，使用GetModuleFileNameEx来得到模块名，找到GameLogic.dll，通过GetModuleInformation得到模块信息，lpBaseOfDll即为模块载入的基址。
- 通过ReadProcessMemory获取指定位置和长度的数据。

很遗憾没有一个完整的库实现了这些API的Python封装，Pywin32也只实现了部分。所以我使用psutil库获取pid，其他都是通过ctype把Python数据转换成C的数据类型后直接调用系统API实现的（此处可以参考WinAppDbg的代码，很可惜它使用Python2.7实现，我用的是3.4，因此不能直接用这个库，需要提取和改写）。

## 主逻辑

当所有玩家剩余牌的数量为27时游戏开始，所有数量为0的时候游戏结束（测试发现当游戏结束的时候所有玩家牌会被瞬间置0）。`玩家每次出牌数量=上次手里剩下牌的数量-目前手里牌的数量`，当出牌数量不为0的时候（0是不出），则利用这个长度和最大牌的位置读取这组牌。

# Day3 界面实现 #

既然上了Python的船，图形界面就顺理成章的PyQt了，反正Qt我还是比较熟的，PyQt用法差不了多少。这里要鄙视下PyQt的文档，大部分都依赖于Qt官网，你让只会Python不会C++的怎么搞？

程序设计为双线程，一个图形线程，一个工作线程，线程间通信通过Qt特有的Signal/Slot实现。

由于每个人对于记牌器最终功能设计的不一致，所以在写图形界面的时候也会有很大的差异。我目前粗略的实现了显示玩家剩余牌数、已经出的牌以及除了自己的牌以外还剩下的牌。

这边需要特别说明一下一个不可避免的问题：玩家的座位。当玩家入座后，无论他在游戏大厅中是哪个座位，他的位置一定是显示在最下面的。我上面一直强调无论是玩家剩余的牌数还是玩家打出去的牌，都是根据大厅中的绝对位置来确定的。所以这里涉及到计算相对座位的问题，公式其实很简单：`相对座位 = (座位-玩家自己的座位) MOD 4`。

最后上一张成品图：

![record]({{ SITEURL }}/statics/qq-card-game-recorder/recorder.jpg)

# DayN 完善和后话 #

找八阿哥（bug）当然是不可缺少的重要一步，不然怎么做第八个男人（Debug Man）呢？

QQ新双扣角色版的内存数据抓取总的来说没有碰到特别大的问题，主要还是因为数据没有加密，因此可以靠猜想和CE的辅助最终找到数据。GameLogic.dll也没有加壳，所以直接就能在IDA中看反汇编，相对也降低了破解的门槛。联网游戏的破解难度就是实时性，因此很难用OD之类的工具来下断点跟踪，所以推断的能力和阅读静态反汇编的能力需要加强。