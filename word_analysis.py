import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
import re
import os
all_chi_list1 = []
for filepath in os.listdir("./TD"):
    with open(f"./TD/{filepath}", "r") as file:
        text = file.readlines()
        text = list(enumerate(text))

    i = 0
    chi_list = []
    for line in text:
        chi_stat = ""
        if line[1].startswith("*CHI") and not line[1].endswith(".\n"):
            chi_stat = f"{line[1]}{text[i+1][1]}"
        elif line[1].startswith("*CHI") and line[1].endswith(".\n"):
            chi_stat = f"{line[1]}"
        i += 1
        if chi_stat != "":
            chi_stat = chi_stat
            chi_stat_list = chi_stat[6:-2].strip().split(" ")
            chi_list.append(chi_stat_list)
    # chi_list

    for words in chi_list:
        for word in words:
            if "\n\t" in word:
                for i in word.split("\n\t"):
                    words.append(i)
                words.remove(word)

    for words in chi_list:
        for word in words:
            if "[" in word and "]" in word:
                if word not in ["[//]", "[/]"]:
                    words.remove(word)

    for words in chi_list:
        for word in words:
            if "(" in word or ")" in word:
                if word not in ["(.)", "(..)", "(..)>"]:
                    words.remove(word)
                    word = word.replace("(", "")
                    word = word.replace(")", "")
                    words.append(word)

    for words in chi_list:
        for word in words:
            if word.startswith("&") or word.startswith("+"):
                words.remove(word)

    all_chi_list1.append([filepath, chi_list])

try:
    os.mkdir("./TD_cleaned")
except FileExistsError:
    pass
for item in all_chi_list1:
    filename = f"{item[0][::-1][4:][::-1]}_cleaned.txt"
    filepath = f"./TD_cleaned/{filename}"
    cleaned_text = ""
    for words in item[1]:
        for word in words:
            cleaned_text += word+" "
        cleaned_text += "\n"
    with open(filepath, "w") as file:
        file.write(cleaned_text)
TD_stat = dict()
for filen in os.listdir("./TD_cleaned"):
    with open(f"./TD_cleaned/{filen}", 'r') as file:
        fresh_text = ""
        keep_word = ['I', 'A', "\n", 'a', 'of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so',
                     'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am']
        for line in file.readlines():
            line = line.replace(">", "")
            line = line.replace("<", "")
            for word in line.split(" "):
                if len(word) < 3:
                    if word not in keep_word:
                        line = line.replace(word, "")
            fresh_text += line
        # print(fresh_text)
        spc = 0
        mpc = 0
        lpc = 0
        wc = 0
        list_a = []
        list_b1 = []
        list_b2 = []
        list_b3 = []
        list_b = []
        wlc = []
        for line in fresh_text.split("\n"):
            # print(line)
            non_words = ["(.)", "(..)", "(...)", "[/]", "[//]"]
            wl = []
            for word in line.split(" "):
                if word not in non_words:
                    wl.append(word)
            wlc.append(len(wl))
            items = line.strip().split(" ")
            word_count = len(items)-(items.count("(.)")+items.count("(..)") +
                                     items.count("(...)")+items.count("[/]")+items.count("[//]"))
            if word_count < 0:
                word_count = 0
            list_a.append(word_count)
            slash_count = items.count("[/]")+items.count("[//]")
            short_pause_count = items.count("(.)")
            list_b1.append(short_pause_count)
            medium_pause_count = items.count("(..)")
            list_b2.append(medium_pause_count)
            long_pause_count = items.count("(...)")
            list_b3.append(long_pause_count)
            total_pause_count = short_pause_count+medium_pause_count+long_pause_count
            list_b.append(total_pause_count)
        wc = sum(list_a)
        spc = sum(list_b1)
        mpc = sum(list_b2)
        lpc = sum(list_b3)
        tpc = sum(list_b)
    filename = filen[::-1][12:][::-1]
    TD_stat[f"{filename}"] = [["word_in_each_statment", wlc], ['word_count', wc], ["short_pause_count", spc], [
        "medium_pause_count", mpc], ["long_pause_count", lpc], ["total_pause_count", tpc]]

fig, axs = plt.subplots(3, 1, figsize=(18, 25))
plot_count = 0
cols = ["r", "g", "#f50c62"]
for key in TD_stat.keys():
    if key in ["TD1", "TD5", "TD9"]:
        axs[plot_count].plot(TD_stat[key][0][1], f"{cols[plot_count]}")
        axs[plot_count].set_title(
            f"Word in each statement in {key}.txt", fontsize=18)
        axs[plot_count].legend([f"{key}.txt"])
        axs[plot_count].set_xlabel("Statement no", fontsize=14)
        axs[plot_count].set_ylabel("Number of words", fontsize=14)
        plot_count += 1
plt.subplots_adjust(left=0.2,
                    bottom=0.1,
                    right=1.1,
                    top=0.8,
                    wspace=0.4,
                    hspace=0.4)
plt.show()

labels = [key for key in TD_stat.keys()]
vals = [TD_stat[key][1][1] for key in labels]
plt.figure(figsize=(15, 10))
plt.bar(labels, vals)
plt.xlabel("File Number", fontsize=14)
plt.ylabel("Total Number of Words", fontsize=14)
plt.title("Total Word in Each File", fontsize=18)
plt.grid()
plt.show()
pauses_each_TD = []
for key in TD_stat.keys():
    pauses = []
    pauses.append(TD_stat[key][2][1])
    pauses.append(TD_stat[key][3][1])
    pauses.append(TD_stat[key][4][1])
    pauses_each_TD.append(pauses)
pauses_combined_TD = [TD_stat[key][5][1] for key in TD_stat.keys()]
tsp = sum([x[0] for x in pauses_each_TD])
tmp = sum([x[1] for x in pauses_each_TD])
tlp = sum([x[2] for x in pauses_each_TD])
pie_data = [tsp, tmp, tlp]
label = ["short pause", "medium pause", "long pause"]
plt.figure(figsize=(15, 10))
plt.pie(pie_data, labels=label, explode=[0.1, 0, 0], autopct="%1.1f")
plt.title("Total pauses in files", fontsize=16)
plt.show()
