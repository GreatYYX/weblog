# YYX's Personal Website

This repository is for my personal website powered by [Pelican](https://github.com/getpelican/pelican).

Theme is based on [MinimalX](https://github.com/art1fa/minimalX) & [MinimalXY](https://github.com/petrnohejl/MinimalXY) so I named it to MinimalXYZ which is in `theme/MinimalXYZ`.

## Usage

Install Python dependencies.

    virtualenv venv
    . venv/bin/activate
    pip install pelican markdown

Clone plug-ins.

    git clone https://github.com/getpelican/pelican-plugins.git

Start local web server. Write articles in Markdown and save them to `content`.

    make devserver

Access local web site at `http://localhost:8000`, use `./develop_server.sh stop` to stop development server).

Publish to Github once done.

    make publish
    git add .
    git commit -m "update"
    git push

> `CNAME` is in `content/extra`, replace it to your domain.

> In order to upload whole project directory (then I can write article and generate it wherever I want), I use `<repo name>/docs` folder as web root, method can be found from [Github help manual](https://help.github.com/articles/configuring-a-publishing-source-for-github-pages/#publishing-your-github-pages-site-from-a-docs-folder-on-your-master-branch). If you don't have custom domain, use `<user name>.github.io/<repo name>` to access your website, or you can just publish the content in `docs` to the root of `<user name>.github.io`.





