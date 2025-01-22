import os
import random
import pathlib
import subprocess

langdata = 'app/langdata_lstm'
training_text_file = f'{langdata}/heb/heb.training_text'
unicharset = f'{langdata}/heb.unicharset'
output_directory = 'heb_hw/gt'
fonts_previous_len = 0
count = 10000
lines = []

#
# note: In my case, I run the script twice. first with 4 fonts, and second with 28 fonts.
#

#070824
fonts = ['Gveret Levin AlefAlefAlef Regular','Anka CLM Bold Expanded','Dana Yad AlefAlefAlef Condensed','Gadi Almog AlefAlefAlef Regular','Ktav Yad CLM Medium Italic']

#110824
fonts_previous_len = len(fonts)
fonts = ['Awanta DL AAA Regular','Benchmark FM Regular','EFT_Afarsek Regular','EFT_Atzmai Regular','EFT_Authentica Regular','EFT_caricature Regular','EFT_Graphologya Light','EFT_Graphologya','EFT_Kitabet','EFT_matcon','EFT_olehadash','EFT_shaashuim','EFT_sicumim','EFT_studentit','EFT_zrima','Eshkolita FM Regular','Flamingo v2 FM Regular','Jacqueline FM Regular','Obege FM Regular','PFT_Sivan Regular','Ploni ML v2 AAA Regular','Shesek FM Regular','shluk DL V2 AAA Regular','TslilaBau v2 FM Regular']



# Open the training text file with UTF-8 encoding
with open(training_text_file, 'r', encoding='utf-8') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

lines = lines[:count]

line_count = 0
for line in lines:
    file_name_stem = pathlib.Path(training_text_file).stem

    for font in range(len(fonts)):
        file_name = f'{file_name_stem}_f{str(fonts_previous_len + font)}_{line_count}'
        
        line_training_text = os.path.join(output_directory, f'{file_name}.gt.txt')
        with open(line_training_text, 'w', encoding='utf-8') as output_file:
            output_file.writelines([line])

        outputbase = f'{output_directory}/{file_name}'

        subprocess.run([
            'text2image',
            f'--font={fonts[font]}', 
            f'--text={line_training_text}',
            f'--outputbase={outputbase}',
            '--max_pages=1',
            '--strip_unrenderable_words',
            f'--unicharset_file={unicharset}'
        ])

    line_count += 1

    print (line_count, ' / ', count)

