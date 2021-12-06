Title: 40%客制化机械键盘“普朗克”打造手记
Date: 2021-12-06 15:18:00
Tags: keyboard
Slug: planck-40-keyboard
Summary: 最近入手了垂涎已久的普朗克键盘套件，本文记录了从前期选择，到组装配置，以及日常使用的心得。
Summary_en: This article details the first impression of Planck keyboard assembling and usage.

# 开篇

机械键盘大概从我本科后期开始一度成为外社区的热点，到如今十余年下来，行业不断洗牌：昔日的行业大佬Cherry近乎跌下神坛，国产的客制化键盘无论散件、套件、成品质量和创新程度都已经开始引领新一轮风潮。机械键盘的可玩性从外壳、轴体、键帽，到按键排列、布局等等几乎渗透每个角落。我个人也从最初使用的ANSI 108键全键盘，到后来的87键游戏，再到61键日常干活，一路感受了从薄膜到青红茶轴的手感变迁（暂缺长时间使用静电容的感受）。

但我一直对于小于60%的键盘持有不实用的观点：由于按键太少，除了字母以外的所有功能几乎都要通过组合键实现，实在是有些过于繁琐。直到看到普朗克Planck键盘通过两颗空格边的功能键lower和raise来调动被传统打空格浪费掉的大拇指，才发现40%键盘还是具有一定实用性的。本文使用这只还未被我使用灵活的普朗克键盘完成，当然我目前对于小于40%的键盘依然持有非常不实用的观点，60%和80%依然是我认为普适性和平衡性最好的键盘种类，而40%小键盘适合尝鲜或者想非常极致的提高输入效率的人群。

![keyboard-sizes]({{ SITEURL }}/statics/planck-40-keyboard/keyboard-sizes.png "Keyboard sizes: 40%, 60%, 80%, 100% from the inside to the outside resp. (from psu.edu)")

# 普朗克键盘

## 背景

Planck键盘具有两个比较显著的特征：1）40%键盘 2）Ortholinear的按键布局。下面展开说说这两点。

100%键盘通过去掉大部分人不常用的数字键区成为了80%键盘，再去掉方向键和功能键（包括F1-F12）则进一步成为了60%键盘。其中的60%键盘又通过加回方向键和部分功能键细分出了64和68键盘。而近期键盘圈比较热门的70%键盘则又加回了更多的功能键和旋钮（encoder）。

40%键盘的布局把一排数字键也进行了阉割，因此整个键盘只有4排，其中3排字母1排空格和modifiers。显而易见的是，数字键和大部分符号将无法通过直接输入完成而需要组合键的参与。但通过牺牲按键直接性所带来的优势就是更加科学的手指移动：手指停止的位置在从下向上数的第3排，主体活动范围在第2-4排，这样每个除了大拇指以外的手指的移动范围基本在上下一行的范围内，减少手指的移动理论上可以提高字符输入的效率和准确性。当然对于打字时候手指运动不科学甚至是一指残的朋友，此类键盘的使用效率会异常的低下。

传统键盘布局中的大空格带来的另一个问题是大拇指的极度浪费。作为最强壮的手指之一，它们的命运大部分时候是在比他们更大的空格上歇着，这显然有些浪费资源了。普朗克中的Grid和MIT布局，都是通过在空格两边分别放入两个Fn键来解决问题：左边的lower和右边的raise分别对应两只大拇指，通过大拇指的按压，激活新的按键层，从而自然而然的实现组合输入。整个键盘的按键只有1u一种、或者1u和2u两种宽度。

![plank-3-layouts]({{ SITEURL }}/statics/planck-40-keyboard/planck-3-layouts.png "Planck layouts (screenshot from Youtube)")

![plank-mit-layout]({{ SITEURL }}/statics/planck-40-keyboard/planck-mit-layout.png "Planck MIT layout (from OLKB)")

Ortholinear的布局是一个对习惯比较突破的尝试。我小时候一直认为我们使用的staggered键盘布局是因为人体工学的考量，殊不知其实是因为打字机时代按键轴问题造成的习惯的延续。横平竖直的ortholinear反而成了异类，其实手指应该会是更加适合这个布局（当然有曲度的版本应该会更加ergonomic一些）。题外话是我们平时用的键盘的按键位置基本都是Qwerty的，据传也不是因为它的分布有助于加快打字，仅仅是因为打字机年代为了不卡壳需要用这个方案限制输入的速度，更加科学的符合输入频率分布的是Dvorak等这些。当然一切都是向固有习惯的妥协，毕竟大部分产品的受众面是大多数的普通人。

![printing-machine]({{ SITEURL }}/statics/planck-40-keyboard/printing-machine.jpeg "Planck MIT layout (from BBC News)")

![qwerty-vs-dvorak]({{ SITEURL }}/statics/planck-40-keyboard/qwerty-vs-dvorak.jpeg "Qwerty vs Dvorak (from Ars Technica)")

## 选型和组装

在购买前我看了某宝上的普朗克方案(和其他40%键盘)，相较于60%等玩的人非常的少。考虑到社区活跃性和QMK的开源固件，最后还是偏向于Jack Humbert的Maxdrop和OLKB的合作款Planck rev6。该款Planck空格处支持Grid、MIT、双空格等多种布局，其中双空格是我预想中的布局（后面会说原因）。为了QMK牺牲了蓝牙，希望无线多模的小伙伴还是选择闭源的方案吧。

到货后的简单开箱：包含PCB、金属定位版、铝外壳、卫星轴（stabilizer）、type C线、螺丝和锁紧工具，最后还有没什么卵用的说明书。需要自己准备轴体和键帽。其中PCB上，支持（非光学）轴体热插拔，使用的凯华Kailh的轴坐，这样就不用焊接了。底面贴片的LED（underglow），但无轴间LED，RGB光污染爱好者绕道吧，虽然Jack在板子上留了二极管的孔。外壳上有两种高度，我买的high-pro，即高外壳，只露出键帽，还有mid-pro的中外壳，会露出定位版和轴，成为所谓的悬浮式键盘。

![my-planck-open-box]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-open-box.png "Planck open box")

轴我主要用了国内今年特别火的猛男专用TTC金粉和TTC月白，前者覆盖字母区，后者和TTC金茶一起覆盖其他区域。这样做的原因是我本身喜欢触发压力较低的线性轴体的打字手感，但手放在空格和modifier上的时候怕因为金粉压力克数太低引发误触，因此用段落轴来区分手感同时防止误触。最左下角我一般不会去按，成为Fn键用于调用控制键盘本身和多媒体的层，使用高特的紫轴来区分手感。传统热插拔的最大好处是轴体多可玩性强，光学热插拔现阶段暂时还是丰富性太差，而且使用轴座后的插拔寿命理论上好于轴套。

![my-planck-switch-installation]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-switch-installation.png "Planck switch installation")

键帽目前暂时使用了廉价的ABS无刻透明键帽，希望通过强制盲打用于快速适应键盘，手感众所周知的平庸。后期可能会自己做键帽或者换PBT材质的SA/DSA键帽。

![my-planck-finish]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-finish.png "My Planck")

声音角度来说没有damper感觉还是差了点什么，后期考虑买点eva发泡塑料填充一下空腔。

## 键位设计和使用感受

理想很美好，现实很骨感。首先Planck默认刷的MIT布局，而我组的双空格方案，因此没法直接使用。只能用QMK Configurator先大致撸了基本层，编译并使用QMK Tool刷入固件，这样算是基本可以用起来了。然后再不断根据习惯修改各层按键。

我这只键盘设计的操作逻辑，只考虑Mac上办公和开发的使用。由于键少，游戏使用基本是不可能的。可编程键盘的一个重要概念就是分层（layer）,每层的每个键都可以完全自定义，层则通过不同按键或者组合键的不同的状态激活。

第0层是base层，主要负责字母输入。作为计算机专业背景和Vi党，Esc是一个非常重要的键，因此在这层保留。方向键看电影时候比较实用，因此也保留了。我自己平时Ctrl就和CapsLock替换的，此处也保留了这个设置，这样按Ctrl相关的组合键非常舒服不用委屈小手指。符号上第二第三行保留了普通键盘的布局，但置换了Enter和引号的位置，因为普通的Enter就在第三行，小手指比较适应，所以只能下移相对不常用的引号。

![my-planck-layer-0]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-layer-0.png "Layer 0")

第1层和第2层通过分别按压左右空格实现。选择双空格的原因是：1) 我并不希望大拇指停留在太小的键上（1u长度的lower和raise），这样敲击时候有区分度也保留了一定的精确度上的冗余减少误触 2) 同时硕大的空格也一直在被用到不会浪费 3) 对于空格周边键的相对位置不变。QMK的功能可以让按键在不同按压下触发不同功能。比如我使用的LT，即任何一个空格单击tap的时候是空格，完全按下之后则激活对应的层。无论第1还是2层，另外一个空格都还是空格，因此实现空格连按只需要同时按下两个空格。第1层主要是数字符号，以及和Vi使用逻辑一致的方向键们，总算充分实现了移动方向不移动手指。第2层主要是剩余的符号和F功能键。Tab放在这层的原因是做任务切换的时候（Tab+cmd）可以不用左手大拇指按住两个键（空格和cmd）。当然这个布局也会让在terminal里面快速跳跃词移动光标的时候右手大拇指需要按住两个键。另外tab不在base层也导致了terminal里自动补全时候按键的增加。此处还需要继续优化。

![my-planck-layer-1]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-layer-1.png "Layer 1")

![my-planck-layer-2]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-layer-2.png "Layer 2")

第3层通过最左下角的Fn激活，目前放了多媒体和键盘背光的操作。同时还有刷固件的Reset和调试用的Debug。

![my-planck-layer-3]({{ SITEURL }}/statics/planck-40-keyboard/my-planck-layer-3.png "Layer 3")

目前从使用上来说还没有完全适应，主要原因并不是字母区全盲打，而是ortholinear导致键位的错位以及符号区盲打输入的难度。另外，感觉在中文社区热度不高的一大原因应该就是中文输入的复杂度问题。拼音输入法需要不断选择输入的内容，因此数字区的访问频率远高于纯英文主体的内容输入。

当然无刻40%键盘最大的优势同时也是限制就是：手本身基本没有大范围移动，也必须强制双手的参与。手部的小范围移动在熟练布局后的速度应该是非常可观的。但一个手位置错误将导致完全没法输入，因为整个输入就是两个手的手感的配合。也因此手离开键盘后必须完全归位，杜绝了偷懒的可能性。

# 后记

有句话说，一个人步入中年的标志就是对周围事物失去兴趣，喜欢折腾一些没什么卵用的东西。当然键盘作为最主要的外设，每天基本都会触摸，还是非常实用的。期待使用一段时间之后能在流畅性上有比较好的突破直到正式中年时起飞上宇宙。

国内键盘圈大部分还是玩客制化键帽和外壳，快感的来源需要动辄几千几万的投入。相比之下，技术向的玩法比较倾向于去尝试更加新奇或者更加ergo的布局、更加有意思的技术以及自己手工制作的键帽或者外壳。比如[Awesome keyboard](https://github.com/BenRoe/awesome-mechanical-keyboard/blob/master/docs/README.md)就提供了相当丰富资源来完全自主的设计各种稀奇古怪键盘。估摸着我下一块键盘会试试Lily58，一次满足入坑split keyboard和玩through hole的愿望。总之，期望国产厂商在创新、制造和品控上再接再厉，也期望国内客制化圈更加开放和多元。









