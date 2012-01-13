from jinja2 import evalcontextfilter, Markup


@evalcontextfilter
def github_link(eval_ctx, value):
    if 'file' in value:
        path = str(value['file'])
        line = str(value['line'])
        shortPath = path.replace('/mnt/hgfs/projects/contests/', '')

        github = path.replace('/mnt/hgfs/projects/contests/', 'https://github.com/99designs/contests/tree/production/')

        result = '<a href="' + github + '#L' + line + '" target="_blank">' + shortPath + ':' + line + '</a>'

        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    return ''
