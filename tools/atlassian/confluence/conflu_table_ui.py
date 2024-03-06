import tkinter as tk
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import unicodedata


class Scraper:
    def __init__(self):
        print('start')
        self.config_path = 'config'
        self.now = datetime.date.today()
        self.auth_flag = 0
        self.root = tk.Tk()
        self.root.title(u"Confluence table extractor")
        ww = '500'
        wh = '300'
        self.root.geometry(ww + "x" + wh)
        self.w = tk.Frame(self.root, height=wh, width=ww)
        self.button = tk.Button(self.w, text="Extract table", fg="blue", command=self.create_data_tb_csv)
        self.spaceCheck = 0
        self.titleCheck = 0
        self.fileCheck = 0
        self.auth()
        self.create_ui()

    def auth(self):
        try:
            with open(self.config_path, "r") as f:
                res = re.split(r'\s', f.read())
                print(res)
                self.username = res[0]
                print(self.username)
                self.password = res[2]
                print(self.password)
                self.auth_flag = 1
                self.initext = 'Fill in blanks and click button to extract'
        except FileNotFoundError:
            self.button.config(state="disabled")
            self.auth_flag = 0
            self.initext = 'First of all, you have to set intra account'
            print('no config file yet')

    def get_url(self):
        print('URL')
        space = self.Space_Entry.get()
        title = self.Title_Entry.get()
        content_url = f"https://confluence.rakuten-it.com/confluence/rest/api/content?spaceKey={space}&title={title}&expand=body.storage"
        return content_url

    ############  Get the confluence data via confluence api
    def get_confluence_content(self):
        print('conflu')
        content_url = self.get_url()
        print(content_url)
        response = requests.get(content_url, auth=HTTPBasicAuth(self.username, self.password))
        print(response)
        print(response.status_code)
        if response.status_code != 200:
            print('access error')
            self.strVar.set('User name or password is wrong')
            self.button.config(state="disabled")
            return False
        return response.json()["results"]

    ###########   Create the table data from confluence to csv
    def create_data_tb_csv(self):
        print('create')
        confluence_content = self.get_confluence_content()
        if not confluence_content:
            self.strVar.set('Failed to get content - please check Space and Title')
            return False

        html_data = confluence_content[0]["body"]["storage"]["value"]

        ###########  Get the table from the html body
        table_data = [[cell.text for cell in row("td")] for row in BeautifulSoup(html_data, "lxml")("tr")]
        table_list = []

        table_header = [[cell.text for cell in row("th")] for row in BeautifulSoup(html_data, "lxml")("tr")]
        table_header_list = []
        encode_type = 'utf-8' if (self.v.get() == 1) else 'SHIFT - JIS'

        ########### Ignore the empty list from the list
        for data in table_data:
            if len(data) != 0:
                if (encode_type == 'SHIFT - JIS'):
                    for i, str in enumerate(data):
                        data[i] = unicodedata.normalize("NFKC", str)
                table_list.append(data)

        ########### Ignore the empty list from the list
        for data in table_header:
            if len(data) != 0:
                if (encode_type == 'SHIFT - JIS'):
                    for i, str in enumerate(data):
                        data[i] = unicodedata.normalize("NFKC", str)
                table_header_list.append(data)

        ########## Convert the result into csv and create a file
        df = pd.DataFrame(table_list)
        df.columns = table_header_list[0]
        file_path = self.File_Entry.get() + '.csv'
        print(encode_type)
        print('--------------------------------------------------')
        df.to_csv(file_path, index=None, encoding=encode_type)
        self.strVar.set('Done!')

    def userSet(self):
        print('userset')
        user = self.user_Entry.get()
        pw = self.pw_Entry.get()
        with open(self.config_path, "w") as f:
            f.write(user + ' /@/ ' + pw)
        self.auth()
        self.configTK.destroy()

    def main_value_change(self, sv):
        a = sv.get()
        repatter = re.compile("\s")

        if sv == self.Space_Entry:
            if (repatter.match(a) or a == ''):
                self.spaceCheck = 0
            else:
                self.spaceCheck = 1

        if sv == self.Title_Entry:
            if (repatter.match(a) or a == ''):
                self.titleCheck = 0
            else:
                self.titleCheck = 1

        if sv == self.File_Entry:
            if (repatter.match(a) or a == ''):
                self.fileCheck = 0
            else:
                self.fileCheck = 1

        if (self.spaceCheck == 1 & self.titleCheck == 1 & self.fileCheck == 1 & self.auth_flag == 1):
            self.button.config(state="normal")
            print('enabled')
        else:
            self.button.config(state="disabled")

    def config_value_change(self, sv):
        a = sv.get()
        repatter = re.compile("\s")

        if sv == self.user_Entry:
            if (repatter.match(a) or a == ''):
                self.usrCheck = 0
            else:
                self.usrCheck = 1
        if sv == self.pw_Entry:
            if (repatter.match(a) or a == ''):
                self.pwCheck = 0
            else:
                self.pwCheck = 1

        if (self.usrCheck == 1 & self.pwCheck == 1):
            self.saveButton.config(state="normal")
            print('enabled')
        else:
            self.saveButton.config(state="disabled")
        print(a)

    def generateConfigWindow(self):
        self.usrCheck = 0
        self.pwCheck = 0
        print('config')
        self.configTK = tk.Tk()
        self.configTK.title(u"Intra account setting")
        ww = '400'
        wh = '150'
        self.configTK.geometry(ww + "x" + wh)
        w = tk.Frame(self.configTK, height=wh, width=ww)
        w.pack()

        self.userSV = tk.StringVar()
        self.pwSV = tk.StringVar()
        self.user_Entry = tk.Entry(w, textvariable=self.userSV)
        self.pw_Entry = tk.Entry(w, textvariable=self.pwSV)
        self.saveButton = tk.Button(w, text="save", fg="blue", command=self.userSet)

        self.userSV.trace("w", self.config_value_change(self.userSV))
        self.pwSV.trace("w", self.config_value_change(self.pwSV))

        self.user_label = tk.Label(w, text=u'user name').pack()
        self.entry_bind(self.user_Entry, self.config_value_change)
        self.user_Entry.pack()

        self.pw_label = tk.Label(w, text=u'password').pack()
        self.entry_bind(self.pw_Entry, self.config_value_change)
        self.pw_Entry.pack()

        self.saveButton.pack()
        self.saveButton.config(state="disabled")

        self.configTK.mainloop()

    def entry_bind(self, e, f):
        e.bind('<Key>', (lambda _: f(e)))
        e.bind('<Return>', (lambda _: f(e)))
        e.bind('<FocusOut>', (lambda _: f(e)))

    def create_ui(self):
        print('UI')
        self.w.pack()

        tk.Label(self.w, text=u'exapmle URL: https://confluence.rakuten-it.com/confluence/display/RPM/Tab201904').pack()
        tk.Label(self.w, text=u'with above URL -> Space: RPM, Title: Tab201904').pack()

        self.SpaceSV = tk.StringVar()
        self.TitleSV = tk.StringVar()
        self.FileSV = tk.StringVar()
        self.Space_Entry = tk.Entry(self.w, textvariable=self.SpaceSV)
        self.File_Entry = tk.Entry(self.w, textvariable=self.FileSV)
        self.Title_Entry = tk.Entry(self.w, textvariable=self.TitleSV)

        self.Space_label = tk.Label(self.w, text=u'Space').pack()
        self.SpaceSV.trace("w", self.main_value_change(self.SpaceSV))
        self.entry_bind(self.Space_Entry, self.main_value_change)
        self.Space_Entry.pack()

        self.Title_label = tk.Label(self.w, text=u'Title').pack()
        self.TitleSV.trace("w", self.main_value_change(self.TitleSV))
        self.entry_bind(self.Title_Entry, self.main_value_change)
        self.Title_Entry.pack()

        self.File_label = tk.Label(self.w, text=u'Export file name').pack()
        self.FileSV.trace("w", self.main_value_change(self.FileSV))
        self.entry_bind(self.File_Entry, self.main_value_change)
        self.File_Entry.pack()

        self.v = tk.IntVar()

        tk.Radiobutton(self.w, text="utf-8", variable=self.v, value=1).pack()
        tk.Radiobutton(self.w, text="Shift-JIS (JP, default)", variable=self.v, value=2).pack()

        self.button.pack()
        self.ConfigButton = tk.Button(self.w, text="Intra account setting", fg="green",
                                      command=self.generateConfigWindow).pack()

        self.strVar = tk.StringVar()
        self.strVar.set(self.initext)
        self.status_label = tk.Label(self.w, textvariable=self.strVar)
        self.status_label.pack()

        if self.auth_flag == 0:
            self.button.config(state="disabled")
        self.root.mainloop()


def main():
    Scraper()


if __name__ == '__main__':
    main()