import argparse
import yaml, json
import datetime
import re
import os


parser = argparse.ArgumentParser(
        description='''Render html page''',
        epilog="""Use --help to receive help for this script""")
parser.add_argument('run', default='', help='start the exporter')
parser.add_argument('--config', type=str, default='default-config.yml', help='--config config.yaml | default: default-config.yml')
args = parser.parse_args()

with open(args.config, "r") as ymlfile:
    CONFIG = yaml.load(ymlfile, Loader=yaml.FullLoader)

x = datetime.datetime.now()

STRING=CONFIG['email']['subj']
# MARKET=os.environ.get('COMPILATION_MARKETS')
MARKET='EU'
pipeline_url='https://test.com'
html_file=CONFIG['email']['body_template']
html_file_gen="emailBody.html"

f = open(html_file, 'r')
html_template = f.read()
f.close()

html_template = html_template.replace('#STRING', STRING)
html_template = html_template.replace('#MARKET', MARKET)
html_template = html_template + "</TABLE><br><br>Please find the link for the pipeline <a href="+pipeline_url+">here</a> ."
html_template = html_template + "<br><br>NOTE: This is an auto-generated email. <br><br> Thanks, <br>" + CONFIG['email']['signature']


fg = open(html_file_gen, 'w')  
fg.write(html_template)
fg.close()

print(html_file_gen, "file created!")
