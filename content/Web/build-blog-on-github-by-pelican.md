Title: 利用Pelican在Github上搭建博客
Date: 2014-08-14 16:17:00
Tags: github, pelican, bootstrap
Slug: build-blog-on-github-by-pelican
Summary: 主要介绍利用Pelican静态博客生成系统和Github Page搭建个人博客的完整方法，其中包括各个组件的下载、安装、Pelican的基本语法等内容。同时后半篇讨论了Pelican主题制作等相关问题。
Summary_en: Tutorial about how to build personal blog with static blog generated system Pelican and Github Page. It focuses on downloading, installation and configuration of all components and the basic grammar of Pelican. It also discusses some relevant problems includes theme customization.

# 写在前面 #
一直知道Github有Page功能，但是从来没想到把它用来做Blog。那天突然发现静态博客系统Jekyll，让我这种用惯Wordpress的人顿感欣喜，简单、轻量、纯粹的博客才是那个真正的博客。静态博客有着自己的优势，比如速度快，安全性高，同时Github的免费空间足够大(300M)，还提供CDN，甚至可以绑定域名。这比免费动态主机、自己买个虚拟空间或VPS架个动态CMS都要来的划算。最最重要的是，Github本身是分布式机制的，这样你的文章完全就是在本地写(妈妈再也不用担心断网了)，之后sync到服务器即可，相当于多重备份+Git强大的版本管理。不过Jekyll基于Ruby，个人对于Ruby只有耳闻没有尝试，因此只能作罢(当然也放弃了Octopress之类基于Jekyll的)，于此同时google到了基于Python的静态博客系统Pelican，因此开始折腾。一周后自制主题的Blog总算竣工，因此决定撰文以方便后人。

OK，在正式开始之前还要说几点：

1. 虽然静态博客系统有很多优势，但是也有很多缺陷。当然大部分缺陷可以用一些小hint来弥补，这对于优势来说还是可以接受的，当然你需要既然决然的去折腾。
1. 网上Jekyll系+Github建博客的文章很多，Pelican也不算特别少，因此本文力求写出一些不一样的、有营养的东西。
1. Pelican升级时候配置文件做了较大变化(虽然我认为对于接口或配置的不严谨设置与改动是不可取的)，不排除其他工具或环境的版本升级时候的变化。如不幸碰到，请自行查阅相关工具或环境的手册，RTFM :D。 
1. 成文仓促，水平有限，望不吝赐教。
 
So, let's start...
# 基础准备 #
## 系统环境 ##
由于平时办公环境还是以Win7为主，因此还是决定将环境搭建在Windows下。Linux下搭建环境比Windows更加简单，网上也有相关文章，请自行检索。
## 套件选择 ##
必装：

- Python3 (2 or 3你自己纠结去)
- pip和setuptool(为了方便package的安装)
- Pelican3
- Markdown（个人觉得Markdown语法简洁优美，Pelican3还支持其他语法）
- make工具（GNU的make，win下的nmake不行）
- Git工具集（当然还要去Github上搞个账号）

可选（主要这里比较折腾）：

- Bootstrap3 (Twitter出品的快速网站搭建框架)
- Disqus (可以选择国内的社会化评论系统，比如多说)
- Google Analytics (可以选择其他网站分析服务商，比如CNZZ)
- MarkdownPad2 (可视化的Markdown写作软件，还有很多可以选择的，甚至是在线的)
- 一些基于JQuery的插件
- 一堆其他什么的……

# 搭建环境 #
## 安装Python ##
在[https://www.python.org/downloads/](https://www.python.org/downloads/)下载Python并安装，就那么简单。安装完成后把Python的安装路径扔到环境变量Path里。
## 安装pip和setuptool ##
在[https://pip.pypa.io/en/latest/installing.html](https://pip.pypa.io/en/latest/installing.html)下载get-pip.py。打开cmd，进入get-pip.py所在目录，之后执行`python get-pip.py`，pip和setuptool都会安装好。
## 安装Pelican和Markdown ##
装好了pip就方便了，直接执行以下命令。

	pip install pelican
	pip install markdown

之后将Python目录下的script目录路径加入环境变量Path中。
## 安装Git工具 ##
下载Github for Windows [https://windows.github.com/](https://windows.github.com/) 并安装即可。
关于Git的命令，推荐一个简单的[git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)。和图形界面相比，git的shell也非常好用。
## 其他 ##
- make只需要下载下来就可以了[http://www.equation.com/servlet/equation.cmd?fa=make](http://www.equation.com/servlet/equation.cmd?fa=make)。
- 网上可能会推荐把Pelican装在虚拟环境virtalenv中，这点你自己决定。
- 可选部分的下载和安装在写到的时候再给出。

# 发表Blog的完整流程 #
Pelican创建Blog的步骤可以总结为：创建框架(包括目录结构，主题模板，配置文件)-->(创建主题)-->写文章-->生成html-->(上传Github等)。

当碰到问题时候记得查阅手册，这部分在手册[http://docs.getpelican.com/](http://docs.getpelican.com/)的getting started中。
## 创建框架 ##
所谓的框架就是一个静态Blog的生成骨架，Pelican只需要一句命令即可（先cd到要生成的目录中）：

	pelican-quickstart

运行命令后根据提示设置，会生成默认的配置文件。此时Pelican已经为我们构建了框架，结构如下:

	yourproject/
	├── content				#写好的Markdown格式的博文
	│   └── (pages)			#Markdown格式的静态界面(比如About，同WP的Page)
	├── output				#通过Pelican最终生成的html界面
	├── develop_server.sh	#Pelican服务器的脚本
	├── fabfile.py			#生成和上传等自动化操作
	├── Makefile			#make的自动化脚本
	├── pelicanconf.py		#主配置文件(测试环境)
	└── publishconf.py		#主配置文件的扩展，用于(生产环境)

## 写文章 ##
这里其实和Pelican没多大关系了。这里使用[Makedown语法](http://wowubuntu.com/markdown/)写文章，并保存为.md文件。

	Title: My super title
	Date: 2010-12-03 10:20
	Category: Python
	Tags: pelican, publishing
	Slug: my-super-post
	Author: Alexis Metaireau
	Summary: Short version for index and feeds
	
	This is the content of my super blog post. #正文内容

上面是官方给出的模板，可以看到正文内容前为文章的meta数据，你可以制定文章的标题、日期、类别、标签、路径名、作者、摘要等(这些信息部分会出现在最终生成html的meta数据中，当然这取决于主题文件是否引用这些数据)。这些里面只有Title和Date是必须的(默认配置下，Date要自己指定是不是很BT，法国人的思维真是……)。meta块之后就用Makrdown写文章啦~当然你可以和我上面说的一样搞一个Markdown的可视化编辑器，写起来很愉快。Markdown语法实现不了的直接用html的语法即可。

## Pelican重要的操作命令 ##
目录中的makefile非常重要，通过make调用makefile中的命令即可完成相关操作。

	make html 			#创建静态界面
	make regenerate 	#修改后自动创建静态界面
	make serve 			#创建服务器
	make devserver		#相当于regenerate+serve
	make publish		#生成用于发布的html

手册上还有其他一些命令，请自行发掘。

## 生成与预览 ##
文章写好了就用上面的`make html`生成文章，你需要反复不停修改和生成的话就用`make regenerate`，每次修改会自动生成新的html。之后用`make serve`开启服务器，默认`http://localhost:8000`可浏览你的Blog。

当然最后发布的请使用`make publish`，该配置更加适合用于正式发布。

## Github相关操作 ##
以上步骤后静态blog已经生成，默认在output文件夹中。下面需要把它上传到github中。所有关于github page的操作都在[http://pages.github.io](http://pages.github.io)。

先去Github注册账号，比如用户名是username，然后Create New Repository, Repository的名字必须为username.github.io（网上流传的.com的貌似已经无效了，所以看手册是多么的重要）。

创建好了之后直接点上面的绿色的set up in desktop就会打开桌面端的Git图形化操作界面。之后会让你同步一个本地的目录，这样本地的目录就和远程的关联好了。commit之后sync即可。

当然也可以用gitshell，命令也很简单。首先进入需要上传的目录，之后执行(具体命令含义可以看相关git教程)：

	git init
	git remote origin https://github.com/username/username.github.io.git
	git pull
	git add .
	git commit -m "update"
	git push origin master


大概等几分钟之后即可访问username.github.io。至此，一个完整的Pelican+Github生成静态Blog的流程已经完成。

## 一些问题和处理 ##
- 对于Python3默认的配置可能会出现问题，需要将develop_server.sh将`PY=${PY:-python2}`改为python3，makefile中如果有问题也需要修改。
- 可以将pelicanconf.py中的SITEURL改成`http://localhost:8000`，将publishconf.py中的SITEURL改为`http://username.github.io`。

# 主题制作 #
到这儿，你应该已经能顺利搭建起一个基于Pelican的Blog并在Github上发布了。下面我们探讨一下Pelican下的个性化主题制作。主题制作的官方文档[在此](http://docs.getpelican.com/en/3.4.0/themes.html)，请不断查阅与参考。另外，Pelican官方的Github上也有别人制作好的主题，你可以[点这儿](https://github.com/getpelican/pelican-themes)进去参考或者下载。
## 制作思路及组件 ##
Pelican的主题制作基于[Jinjia模板引擎](http://jinja.pocoo.org/)，看这个名字和Logo就知道是小日本的作品了，如果你曾经用过smarty（N年以前了）或者是类似的模板引擎，基本能秒速上手。利用模板引擎的优势就是视图和数据的分离，整个过程相当于你写的.md文件就是数据，通过Pelican驱动之后按照Jinjia作为模板填充数据，并输出最终html。

对于主题制作，无非就是前端的一些东西，什么html啊js啊之类的东西，我这边采用bootstrap3加上一堆插件的方法创建html，之后改写成Jinjia模板。

通过主题制作，基本可以搞明白大部分Pelican配置的含义。另外，由于这块内容本身覆盖知识面很广，这里只能按照Pelican中特有的一些规定展开，周边的前端知识只能说到一些必要的，其他方面还请读者自行补充。
## 主题结构 ##
首先创建主题目录，我准备放在yourproject/theme目录下，此时打开`pelicanconf.py`，添加如下字段：

	THEME = "theme"				#主题目录
	THEME_STATIC_DIR = 'theme'	#生成后的主题目录


手册上给出如下主题结构，这写文件可以放在yourproject/theme目录下（具体哪儿都可以通过配置文件指定）。

	├── static
	│   ├── css
	│   └── images
	└── templates
	    ├── archives.html         // 文章归档
	    ├── period_archives.html  // 按照时间排序的归档
	    ├── article.html          // 每篇文章
	    ├── author.html           // 每个作者
	    ├── authors.html          // 所有作者
	    ├── categories.html       // 所有分类
	    ├── category.html         // 每个分类
	    ├── index.html            // 主页
	    ├── page.html             // page界面（自定义的界面）
	    ├── tag.html              // 每个不同tag的界面
	    └── tags.html             // 总tag界面，可以创建tag云

看到上面的目录构造可以基本明白各个文件的作用了。static中的文件会被完整复制到生成目录中，而templates中的文件则会通过Pelican处理。

需要特别说明的是，不是所有文件都是必须的，比如我的Blog就我一个人写文章，只有一个作者，所以author和authors我就不用，你可以保留文件，之后把里面内容删除即可。当然你也可以创建文件，采用Jinjia的包含语句包含到其他界面中，这在后面会说明。

## 主题和配置 ##
待续……











