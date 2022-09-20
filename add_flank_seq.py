from os import listdir, getcwd, system
from os.path import join, isfile
 
from Bio import SeqIO
from Bio.Seq import Seq


def main():
    system('cls')
    while True:
        mypath, file = get_path_file('fasta')
        if file is None:
            return None
        
        file_name, dot, ext = file.rpartition('.')
        output_file = file_name + '_flanked.' + ext
        
        flank_5, flank_3 = get_flanks()
        
        with open(join(mypath, file), "r") as input_handle, open(join(mypath, output_file), "w") as output_handle:
            for record in SeqIO.parse(input_handle, "fasta"):
                record.seq = Seq(f'{flank_5}{str(record.seq)}{flank_3}')
                SeqIO.write(record, output_handle, "fasta-2line")

        print(f'\nOutput file saved as:\t{output_file}')

        if not next_file():
            break
        system('cls')
        

def next_file():
    while True:
        cont = input('Process next file? (Y/N): ').lower()
        if 'y' in cont:
            return True
        elif 'n' in cont:
            return False
        else:
            print('---< Input not recognized. Try again >---').center(80)

def get_flanks():
    flank_5 = input("5' flank sequence: ")
    flank_3 = input("3' flank sequence: ")
    return flank_5, flank_3

def get_path_file(ext: str):
    mypath = getcwd()
    fasta_list = scan_files(mypath, ext)
    file = choose_file(fasta_list, ext)
    if file is None:
        return mypath, None

    return mypath, file

def choose_file(file_list: list, ext: str):
    print('/ Select file \\'.center(80, '_'), '\n', sep='')
    
    fasta_dict = {str(i): file for i, file in enumerate(file_list, 1)}    
    for i, file in fasta_dict.items():
        print(f'{i.rjust(2)})', file.replace(f'.{ext}', ''), sep=" ")
        
    print('\n', 'Q - Quit')
    print(''.center(80, '_'), '\n', sep='')
    
    while True:
        file_i = input('File number: ').lower()
        if file_i in fasta_dict:
            break
        elif file_i == 'q':
            return None
        else:
            print('---< Wrong input. Try again >---'.center(80))

    system('cls')
    
    return fasta_dict[file_i]

def scan_files(path, ext):
    list_files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(ext)]
    return list_files


if __name__ == "__main__":
    main()