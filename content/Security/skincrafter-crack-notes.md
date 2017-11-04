Title: SkinCrafter破解笔记
Date: 2014-11-09 23:46:00
Tags: SkinCrafter, crack, reversing, 皮肤, 破解, 逆向
Slug: skincrafter-crack-notes
Summary: 记录了著名VC及.NET皮肤库SkinCrafter(3.8.0 for VS2010)的破解过程，包括license初始化函数破解，弹出框去除以及DEMO文字去除的具体方法及技巧。
Summary_en: This article records the cracking process of a famous skin library of VC and .NET SkinCrafter (3.8.0 for VS2010), includes the method of cracking of initialization function of license, removing the popup window and the sign of 'Demo'.

# 开篇废话 #

最近的一个Win下的小项目，图形界面需求简单，就直接上MFC。完成后某人觉得界面不够和谐，于是得折腾下界面。貌似目前VC++界的UI主流是MS自家DirectUI思想下的一些UI库，可惜本人的哲学“懒”字当头，再学一套UI的用法实在是要了亲命，直接放弃。记得本科期间用过一个Skin++的皮肤库，加载后可以直接换肤，可惜那玩意皮肤太少、没有皮肤编辑器而且貌似已经停止维护，因此作罢。后google到同为皮肤库的SkinCrafter，并下了3.4.4的破解版，可惜在VS2010下整合后MessageBox的按钮底色在Win7下无法匹配皮肤设置（官网查阅后发现是bug，新版已解决），遂换到3.8.0。该版本的VS2012有相关破解版，但VS2010没有，于是自己上手破解（正所谓学会破解，用D版软件都有底气了），花了差不多快2小时最终成功，并记录成本文。

# Dll版工作流程 #

对于VC/MFC程序，SkinCrafter有Dll/ActiveX两个版本，我个人喜欢使用Dll版（两个版本的破解方法其实是一样的）。下面介绍Dll版本官方的使用方法：

1. 首先需要引入CSCSkin.h和CSCSkin.cpp文件，并将dll及皮肤文件.skf放在目录下。
2. 实例化CSCSkin对象m_skin，并在App的InitInstance()中执行Init()、LoadSkinFromFile()及ApplySkin()三个函数。

对比ActiveX版本，可以发现少执行好几个函数，其实这些函数在Init()方法中都完成了，所以真正的工作流程是：

1. 定义了Dll导出表中所有的函数指针。
2. 通过LoadLibrary()加载Dll，并执行InitLicenKeys()和InitDecoration()。
3. LoadSkinFromFile()加载皮肤。
4. ApplySkin()应用皮肤。

# InitLicenKeys函数破解 #

这个函数用于写入注册信息，对于DEMO版，该函数的4个参数是定死的。其实不破解这个函数也无所谓，反正写在程序里面，但是真要破解也很简单。

由于是简单的固定字符串匹配，因此可以直接替换Dll中的字符串。当然还可以采用爆破的方法，这样无论输入什么都行。

查找四个参数中任意一个字符串，我这儿用DEMOSKINCRAFTERLICENCE（比较有代表性），定位到程序。发现有两个处strcmp()比较字符串并作出比较和跳转，因此直接nop掉跳转即可。

```x86asm
...
10005A49  |> \85C0          test eax,eax
10005A4B  |.  75 48         jnz XSkinCraf.10005A95                   ;  第一次跳转判断
10005A4D  |.  8B45 14       mov eax,[arg.4]
10005A50  |.  B9 8C420610   mov ecx,SkinCraf.1006428C                ;  DEMOSKINCRAFTERLICENCE
...
10005A7A  |>  85C0          test eax,eax
10005A7C  |.  75 17         jnz XSkinCraf.10005A95                   ;  第二次跳转判断
10005A7E  |.  5E            pop esi
10005A7F  |.  B8 01000000   mov eax,0x1
10005A84  |.  5B            pop ebx
10005A85  |.  8B4D FC       mov ecx,[local.1]
10005A88  |.  33CD          xor ecx,ebp
10005A8A  |.  E8 E91E0500   call SkinCraf.10057978
10005A8F  |.  8BE5          mov esp,ebp
10005A91  |.  5D            pop ebp
10005A92  |.  C2 1000       retn 0x10
10005A95  |>  6A 00         push 0x0                                 ; /Style = MB_OK|MB_APPLMODAL
10005A97  |.  68 80420610   push SkinCraf.10064280                   ; |SkinCrafter
10005A9C  |.  68 D8410610   push SkinCraf.100641D8                   ; |You are using DEMO version of SkinCrafter. InitLicenKeys function parameters should be: SKINCRAFTER, SKINCRAFTER.COM, support@skincrafter.com, DEMOSKINCRAFTERLICENCE
10005AA1  |.  6A 00         push 0x0                                 ; |hOwner = NULL
10005AA3  |.  FF15 4C350610 call dword ptr ds:[<&USER32.MessageBoxA>>; \MessageBoxA
...
```

# 去除弹出框 #

最明显的莫过于这个弹出框，程序启动后就会出现。该弹出框无边框可拖动，而且强制置顶（TOP_MOST），因此想到SetWindowPos()及SetWindowLong()两个函数，仔细查找后均无果。后来又查找了CreateWindow()、CreateRectRgn()及CreateRectRgnIndirect()也没有很好的下手位置。就在找函数这条思路没有突破口的时候，看到弹出窗口上有一条可以点击的网址，因此直接查字符串找这个网址，然后跳转到程序处。

找到程序处之后翻看上下文，无非就在load一些资源，突然看到ShowWindow()函数。

```x86asm
10002F40  /$  55            push ebp
10002F41  |.  8BEC          mov ebp,esp
...
10002F87  |.  68 F3000000   push 0xF3
10002F8C  |.  6A 02         push 0x2
10002F8E  |.  68 F3000000   push 0xF3
10002F93  |.  E8 D6410500   call <jmp.&mfc100.#AfxFindResourceHandle_1900>
10002F98  |.  50            push eax                                             ; |hInst
10002F99  |.  FF15 70350610 call dword ptr ds:[<&USER32.LoadBitmapW>]            ; \LoadBitmapW
10002F9F  |.  50            push eax
10002FA0  |.  B9 CC450710   mov ecx,SkinCraf.100745CC
10002FA5  |.  E8 BE410500   call <jmp.&mfc100.#CGdiObject::Attach_2184>
10002FAA  |.  A1 D0450710   mov eax,dword ptr ds:[0x100745D0]
10002FAF  |.  A3 D85F0710   mov dword ptr ds:[0x10075FD8],eax
10002FB4  |.  391D DC5F0710 cmp dword ptr ds:[0x10075FDC],ebx
10002FBA  |.  0F85 7C020000 jnz SkinCraf.1000323C
...
10003143  |.  A1 E05F0710   mov eax,dword ptr ds:[0x10075FE0]
10003148  |.  6A 01         push 0x1
1000314A  |.  51            push ecx
1000314B  |.  8BCC          mov ecx,esp
1000314D  |.  8965 DC       mov [local.9],esp
10003150  |.  68 843D0610   push SkinCraf.10063D84                               ;  http://www.skincrafter.com/order.html
10003155  |.  C780 84000000>mov dword ptr ds:[eax+0x84],0x497D
1000315F  |.  FF15 A4390610 call dword ptr ds:[<&mfc100.#ATL::CStringT<char,StrT>;  mfc100.#ATL::CStringT<char,StrTraitMFC_DLL<char,ATL::ChTraitsCRT<char> > >::CStringT<char,StrTraitMFC_DLL<char,ATL::ChTraitsCRT<char> > >_310
10003165  |.  8B0D E05F0710 mov ecx,dword ptr ds:[0x10075FE0]
...
1000323C  |>  8B0D DC5F0710 mov ecx,dword ptr ds:[0x10075FDC]
10003242  |.  6A 05         push 0x5
10003244  |.  E8 35410500   call <jmp.&mfc100.#CWnd::ShowWindow_12962>
...
```

可以看到，函数执行完成之后会ShowWindow()，而当参数为5的时候，就是SW_SHOW，因此可以将push的参数设置为0(SW_HIDE)或者直接把整合函数nop掉。


**2014-12-03更新：**

今天在项目上调试的时候发现又出现弹窗，使用相同的dll在皮肤测试程序上则没有出现。于是直接调试项目程序，发现还有几处ShowWindow函数。

```x86asm
10012B40  /$  55            push ebp
10012B41  |.  8BEC          mov ebp,esp
10012B43  |.  833D D45F0710>cmp dword ptr ds:[0x10075FD4],0x0
10012B4A  |.  56            push esi
10012B4B  |.  8BF1          mov esi,ecx
10012B4D  |.  75 42         jnz XSkinCraf.10012B91
10012B4F  |.  8B0D DC5F0710 mov ecx,dword ptr ds:[0x10075FDC]
10012B55  |.  6A 05         push 0x5
10012B57  |.  E8 22480400   call <jmp.&mfc100.#CWnd::ShowWindow_12962>
10012B5C  |.  8B0D DC5F0710 mov ecx,dword ptr ds:[0x10075FDC]
10012B62  |.  6A 00         push 0x0
10012B64  |.  6A 08         push 0x8
10012B66  |.  6A 00         push 0x0
10012B68  |.  E8 8B490400   call <jmp.&mfc100.#CWnd::ModifyStyle_7889>
10012B6D  |.  8B0D E05F0710 mov ecx,dword ptr ds:[0x10075FE0]
10012B73  |.  6A 05         push 0x5
10012B75  |.  E8 04480400   call <jmp.&mfc100.#CWnd::ShowWindow_12962>
10012B7A  |.  8B0D E45F0710 mov ecx,dword ptr ds:[0x10075FE4]
10012B80  |.  6A 05         push 0x5
10012B82  |.  E8 F7470400   call <jmp.&mfc100.#CWnd::ShowWindow_12962>
10012B87  |.  C705 D45F0710>mov dword ptr ds:[0x10075FD4],0x1
10012B91  |>  8B46 18       mov eax,dword ptr ds:[esi+0x18]
10012B94  |.  85C0          test eax,eax
10012B96  |.  74 74         je XSkinCraf.10012C0C
...
```

可直接在OD的Name表中找出MFC的CWnd::ShowWindow函数调用处全部下断，此处连续出现3处ShowWindow()，将第一次出现处的`push 0x5`改成`push 0x0`即可。

# 去除标题栏DEMO字样 #

本以为这步会很简单，很可惜，低估了作者的智商。直接找字符串没看到SkinCrafter Demo字样，因此怀疑很可能字符串是被加密的了。OD调试Dll会加载LoadDll.exe这个程序，并在Dll加载后允许通过接口执行Dll的导出函数，对于一般作为函数库的Dll这样调试当然没问题，每个函数都是独立的，但是对于这种函数之间有数据依赖的Dll来说，我必须先调用几个依赖的函数，这样就过于麻烦了（主要懒得输那么长的参数，还要小端码，而且每次加载都要输入……）。这里就用到一个技巧，自己写一个调用dll的exe，直接调试exe，并进入Dll的领空找需要的东西。

在OD的调试选项中，找到事件(Event)选项卡，把“中断于新模块”这项勾上，之后加载exe程序。每当exe加载一个dll的时候，就会被断下，F9继续执行，直到目标出现。当然SkinCrafterDll这个Dll是在程序中通过LoadLibrary()加载的，因此先要把程序跑起来。

断下后进入该Dll领空，并查看所有函数符号。考虑到和绘图有关，并经过几次实验，最后定位在GdiPlus库中的GdipDrawString()函数上，直接下断函数。但是查找函数引用的时候却没有结果，这是因为Dll刚开始并没有填充IAT，所以需要再继续F9，直到IAT初始化完毕。再查找引用就可以找到函数调用处了。

```x86asm
...
02E01511  |.  53            push ebx                                             ; /hIcon
02E01512  |.  FF15 0034E102 call dword ptr ds:[<&USER32.DestroyIcon>]            ; \DestroyIcon
02E01518  |>  8B9D 54FFFFFF mov ebx,[local.43]
02E0151E  |>  A1 406CE102   mov eax,dword ptr ds:[0x2E16C40]
02E01523  |.  8B15 3C6CE102 mov edx,dword ptr ds:[0x2E16C3C]
02E01529  |.  8B0D 446CE102 mov ecx,dword ptr ds:[0x2E16C44]
02E0152F  |.  8945 E0       mov [local.8],eax
02E01532  |.  66:A1 4C6CE10>mov ax,word ptr ds:[0x2E16C4C]
02E01538  |.  8955 DC       mov [local.9],edx
02E0153B  |.  8B15 486CE102 mov edx,dword ptr ds:[0x2E16C48]
02E01541  |.  66:8945 EC    mov word ptr ss:[ebp-0x14],ax
02E01545  |.  8D45 DC       lea eax,[local.9]
02E01548  |.  894D E4       mov [local.7],ecx
02E0154B  |.  8955 E8       mov [local.6],edx
02E0154E  |.  33C9          xor ecx,ecx
02E01550  |.  8D70 01       lea esi,dword ptr ds:[eax+0x1]
...
02E017E5  |.  8B8D 64FFFFFF mov ecx,[local.39]
02E017EB  |.  56            push esi
02E017EC  |.  51            push ecx
02E017ED  |.  8B8D 48FFFFFF mov ecx,[local.46]
02E017F3  |.  8D95 F8FEFFFF lea edx,[local.66]
02E017F9  |.  52            push edx
02E017FA  |.  8B95 6CFFFFFF mov edx,[local.37]
02E01800  |.  51            push ecx
02E01801  |.  6A FF         push -0x1
02E01803  |.  50            push eax
02E01804  |.  52            push edx
02E01805  |.  E8 D26D0000   call <jmp.&gdiplus.GdipDrawString>
02E0180A  |.  8B85 64FFFFFF mov eax,[local.39]
02E01810  |.  50            push eax
02E01811  |.  E8 846D0000   call <jmp.&gdiplus.GdipDeleteStringFormat>
02E01816  |.  56            push esi
02E01817  |.  E8 A66C0000   call <jmp.&gdiplus.GdipDeleteBrush>
02E0181C  |.  8B8D 48FFFFFF mov ecx,[local.46]
02E01822  |.  51            push ecx
02E01823  |.  E8 906D0000   call <jmp.&gdiplus.GdipDeleteFont>
02E01828  |.  8B95 6CFFFFFF mov edx,[local.37]
02E0182E  |.  52            push edx
02E0182F  |.  C645 FC 01    mov byte ptr ss:[ebp-0x4],0x1
02E01833  |.  E8 906C0000   call <jmp.&gdiplus.GdipDeleteGraphics>
...
```

经过跟踪，可以发现字符串在DestroyIcon()执行之后被装入，在内存中显示为：

```no-hightlight
02E16C38  80 0F E0 02 54 6C 6E 69 44 75 66 61 73 62 75 27  €?TlniDufasbu'
02E16C48  43 62 6A 68 27 00 00 00 E4 D9 E1 02 A0 2B E0 02  Cbjh'...滟???
```

因此字符串为TlniDufasbu'Cbjh'，这个字符串经过后面的算法转换成了SkinCrafter Demo，因此只要直接干掉字符串就可以，或者nop掉GdipDrawString()。我采用删掉字符串的方法，用16进制编辑器打开dll找到这个字符串并填0。

# 后记 #

从我使用的情况来看暂时没有出现其他问题，如果有破解不完全或造成错误的地方，我会在后续做出完善。另外，此次调试过程中全程在IDA中同步参考，IDA的图形视图能很好的看出程序的执行流程，当然IDA还有万恶的F5大杀器 :P