import pdfkit

graphs = [
    'https://plot.ly/~MichaellAlavedraMunayco/10',
    'https://plot.ly/~MichaellAlavedraMunayco/8',
    'https://plot.ly/~MichaellAlavedraMunayco/6',
    'https://plot.ly/~MichaellAlavedraMunayco/4'
]


def report_block_template(graph_url, caption=''):
    graph_block = (''
                   '<a href="{graph_url}" target="_blank">'
                   '<img style="text-align: center;align-self: center;display: block;margin: 20px auto;height: 550px;" src="{graph_url}.png">'
                   '</a>')

    report_block = ('' +
                    graph_block +
                    '{caption}' +
                    '<br>' +
                    '<a href="{graph_url}" style="font-weight: 200;" target="_blank">Visualizar y comentar Grafico interactivo</a>' +
                    '<br>' +
                    '<hr>')

    return report_block.format(graph_url=graph_url, caption=caption)


def build_report():
    static_report = ''
    for graph_url in graphs:
        static_report += report_block_template(graph_url, caption='')
    return static_report
