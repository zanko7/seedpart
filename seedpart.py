#!/usr/bin/python
import seedpart
from seedpart.bip39xor import bip39shard
import random
import tkinter
from   tkinter import ttk, Frame, Label, Button, WORD, END, StringVar, OptionMenu
from   tkinter import messagebox, Message, Menu, Toplevel
from tkinter.scrolledtext import ScrolledText

GUI_VER = 'SeedPart GUI v0.2'

class MainWin(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        Frame.pack(self, expand=1, fill='both')
        self.root = master

        for col in range(0, 6):
            self.columnconfigure(col, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)

        alg_tb       = Label(self, text='Sharding Algorithm')
        self.algtype = StringVar(self, 'BIP39xor')
        algs         = {'BIP39xor', 'PlainTextXOR'}
        alg_om       = OptionMenu(self, self.algtype, *algs, command=self.algtype_changed)
        self.algtype = 'BIP39xor'
        clear_btn    = Button(self, text='Clear', command=self.clear)

        self.seed_lb = Label(self, text='Seed Phrase')
        self.seed_tb = ScrolledText(self, wrap=WORD, height=5, width=75)
        shard1_lb    = Label(self, text='Shard 1')
        shard2_lb    = Label(self, text='Shard 2')
        shard3_lb    = Label(self, text='Shard 3')
        shard1_tb    = ScrolledText(self, wrap=WORD, height=12, width=25)
        shard2_tb    = ScrolledText(self, wrap=WORD, height=12, width=25)
        shard3_tb    = ScrolledText(self, wrap=WORD, height=12, width=25)
        
        split_btn    = Button(self, text='\nSplit\n', command=self.split)
        join_btn     = Button(self, text='\nJoin\n',  command=self.join)
        
        alg_tb.grid(      row=0, column=0, sticky='w')
        alg_om.grid(      row=0, column=1, columnspan=4, sticky='ew')
        clear_btn.grid(   row=0, column=5, sticky='ew')
        self.seed_lb.grid(row=1, column=0, columnspan=6)
        self.seed_tb.grid(row=2, column=0, columnspan=6, sticky='nsew')
        split_btn.grid(   row=3, column=0, columnspan=3, sticky='ew')
        join_btn.grid(    row=3, column=3, columnspan=3, sticky='ew')

        shard1_lb.grid(   row=4, column=0, columnspan=2)
        shard2_lb.grid(   row=4, column=2, columnspan=2)
        shard3_lb.grid(   row=4, column=4, columnspan=2)
        shard1_tb.grid(   row=5, column=0, columnspan=2, sticky='nsew')
        shard2_tb.grid(   row=5, column=2, columnspan=2, sticky='nsew')
        shard3_tb.grid(   row=5, column=4, columnspan=2, sticky='nsew')

        self.shard_tb = [ shard1_tb, shard2_tb, shard3_tb ]
        
        self.seed_lb.bind('<Button-1>', self.shard_popup)
        shard1_lb.bind(   '<Button-1>', self.shard_popup)
        shard2_lb.bind(   '<Button-1>', self.shard_popup)
        shard3_lb.bind(   '<Button-1>', self.shard_popup)

    def algtype_changed(self, var):
        if var == 'BIP39xor':
            self.seed_lb['text'] = 'Seed Phrase'
        elif var == 'PlainTextXOR':
            self.seed_lb['text'] = 'Plain Text'
        self.algtype = var

    def clear(self):
        self.rewrite_text(self.seed_tb, '')
        for i in range(0, 3):
            self.rewrite_text(self.shard_tb[i], '')

    def rewrite_text(self, textbox, val):
        if val == None:
            val = ''
        textbox.delete('1.0', END)
        textbox.insert('1.0', val)

    def shard_popup(self, e):
        if (self.algtype != 'BIP39xor'):
            return

        shard_text = None
        lb = e.widget['text']
        part = ''
        if lb == 'Shard 1':
            shard_text = self.shard_tb[0].get('1.0', END+'-1c')
            part = 'SHARD 1'
        elif lb == 'Shard 2':
            shard_text = self.shard_tb[1].get('1.0', END+'-1c')
            part = 'SHARD 2'
        elif lb == 'Shard 3':
            shard_text = self.shard_tb[2].get('1.0', END+'-1c')
            part = 'SHARD 3'
        elif lb == 'Seed Phrase':
            shard_text = self.seed_tb.get('1.0', END+'-1c')
            part = 'SEED'
        else:
            return

        sp = seedpart.BIP39xor() 
        words = shard_text.split()

        try:
            shard = bip39shard(words) 
        except Exception as e:
            messagebox.showerror('SeedPart Shard Info', str(e))
            return

        s  = '          %s\n' % part
        s += '---------------------------\n'
        s += 'Number   Word         Index\n'
        s += '---------------------------\n'
        for i in range(0, len(shard.words)):
            s += '{:>6}   {:12} {:>5}\n'.format(i+1, shard.words[i].word, shard.words[i].num)
        popup = Message(Toplevel(master=self.root), text=s)
        popup.config(font=('Courier', 12))
        popup.pack()

    def split(self):
        key = self.seed_tb.get('1.0', END+'-1c')

        if self.algtype == 'BIP39xor':
            sp = seedpart.BIP39xor()
        elif self.algtype == 'PlainTextXOR':
            sp = seedpart.plaintextxor()
        else:
            return

        try:
            sp.split(key)
        except Exception as e:
            messagebox.showerror('SeedPart Split', str(e))

        for i in range(0, 3):
            if self.algtype == 'BIP39xor':
                val = sp.shard[i].get_words()
            elif self.algtype == 'PlainTextXOR':
                val = sp._intarr_to_hexstr(sp.shard[i])
            self.rewrite_text(self.shard_tb[i], val)

    def join(self):
        if self.algtype == 'BIP39xor':
            sp = seedpart.BIP39xor()
        elif self.algtype == 'PlainTextXOR':
            sp = seedpart.plaintextxor()
        else:
            return

        shards = [ self.shard_tb[0].get('1.0', END+'-1c'),
                   self.shard_tb[1].get('1.0', END+'-1c'),
                   self.shard_tb[2].get('1.0', END+'-1c')  ]
        for i in range(0, 3):
            if shards[i] == '':
                shards[i] = None

        try:
            sp.join(shards)
        except Exception as e:
            messagebox.showerror('SeedPart Join', str(e))
            return

        print(sp)

        if self.algtype == 'BIP39xor':          val = sp.seed
        elif self.algtype == 'PlainTextXOR':    val = sp.key
        self.rewrite_text(self.seed_tb, val)

    def menu_about(self):
        s = 'SeedPart\nhttps://github.com/MJL85/seedpart\n\n%s\n' % GUI_VER
        for v in seedpart.__version__:
            s += '%s\n' % v
        messagebox.showinfo('SeedPart', s)

def main():
    r = tkinter.Tk()
    r.title('SeedPart')
    win = MainWin(r)
    menubar = Menu(r)
    menubar.add_command(label='About', command=win.menu_about)
    r.config(menu=menubar)
    
    # start window
    r.mainloop()


main()
